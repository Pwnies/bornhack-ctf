#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <link.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/auxv.h>

static off_t bias = 0;
static uint8_t *elf;
static size_t elf_size;
static char exe[4096];

static
__attribute__((always_inline))
void find_bias(void) {
  ElfW(Phdr) *phdrs;
  int phnum, i;

  phdrs = (ElfW(Phdr)*)getauxval(AT_PHDR);
  if (NULL == phdrs) {
    fprintf(stderr, "getauxv: no AT_PHDR\n");
    exit(EXIT_FAILURE);
  }

  phnum = (int)getauxval(AT_PHNUM);
  if (0 == phnum) {
    fprintf(stderr, "getauxv: no AT_PHNUM\n");
    exit(EXIT_FAILURE);
  }

  for (i = 0; i < phnum; i++) {
    if (PT_PHDR == phdrs[i].p_type) {
      bias = (off_t)phdrs - (off_t)phdrs[i].p_vaddr;
      break;
    }
  }
}

static
__attribute__((always_inline))
void writen(int fd, void *buf, size_t len) {
  size_t i = 0;
  ssize_t ret;
  while (i < len) {
    ret = write(fd, buf + i, len - i);
    if (-1 == ret) {
      if (EINTR == errno) {
        continue;
      }
      perror("write");
      exit(EXIT_FAILURE);
    }
    i += ret;
  }
}

static
__attribute__((always_inline))
void mmap_elf(void) {
  int fd;
  ssize_t ret;
  struct stat st;

  ret = readlink("/proc/self/exe", exe, sizeof(exe));
  if (-1 == ret) {
    perror("readlink");
    exit(EXIT_FAILURE);
  }
  exe[ret] = 0;

  fd = open(exe, O_RDONLY);
  if (-1 == fd) {
    perror("open");
    exit(EXIT_FAILURE);
  }

  ret = fstat(fd, &st);
  if (-1 == fd) {
    perror("fstat");
    exit(EXIT_FAILURE);
  }

  elf_size = (size_t)st.st_size;
  elf = mmap(NULL, elf_size, PROT_READ, MAP_PRIVATE, fd, 0);
  if (NULL == elf) {
    perror("mmap");
    exit(EXIT_FAILURE);
  }

  close(fd);
}

static
__attribute__((always_inline))
void deobfu(void *addr) {
  ElfW(Ehdr) *ehdr;
  ElfW(Shdr) *shdrs;
  ElfW(Sym) *symtab = NULL;
  int shnum, symnum, i, symsz;
  void *laddr, *haddr;

  ehdr = (ElfW(Ehdr)*)elf;
  shdrs = (void*)(ehdr->e_shoff + elf);
  shnum = ehdr->e_shnum;

  for (i = 0; i < shnum; i++) {
    if (shdrs[i].sh_type == SHT_SYMTAB) {
      symtab = (void*)(shdrs[i].sh_offset + elf);
      symnum = shdrs[i].sh_size / sizeof(ElfW(Sym));
      break;
    }
  }

  if (NULL == symtab) {
    fprintf(stderr, "no symbol table\n");
    exit(EXIT_FAILURE);
  }

  for (i = 0; i < symnum; i++) {
    if (symtab[i].st_value + bias == (unsigned long)addr) {
      symsz = symtab[i].st_size;
    }
  }

  if (0 == symsz) {
    fprintf(stderr, "could not find symbol\n");
    exit(EXIT_FAILURE);
  }

  laddr = (void*)((unsigned long)addr & ~0xfff);
  haddr = (void*)(((unsigned long)(addr + symsz - 1) & ~0xfff) + 0x1000);

  mprotect(laddr, haddr - laddr, PROT_READ | PROT_WRITE | PROT_EXEC);
  for (i = 0; i < symsz; i++) {
    ((unsigned char*)addr)[i] ^= (unsigned long)addr + i;
  }
  mprotect(laddr, haddr - laddr, PROT_READ | PROT_EXEC);
}

static
__attribute__((always_inline))
void save_elf(void) {
  ElfW(Ehdr) *ehdr;
  ElfW(Shdr) *shdrs;
  int fd, i, shnum;
  char tmp[4096], *shstrtab;
  struct stat st;
  ssize_t ret;

  strncpy(tmp, "heks-XXXXXX", sizeof(tmp));

  fd = mkstemp(tmp);
  if (-1 == fd) {
    perror("mkstemp");
    exit(EXIT_FAILURE);
  }

  ret = stat(exe, &st);
  if (-1 == fd) {
    perror("stat");
    exit(EXIT_FAILURE);
  }

  writen(fd, elf, elf_size);

  ehdr = (ElfW(Ehdr)*)elf;
  shdrs = (void*)(ehdr->e_shoff + elf);
  shnum = ehdr->e_shnum;
  shstrtab = (void*)(shdrs[ehdr->e_shstrndx].sh_offset + elf);
  for (i = 0; i < shnum; i++) {
    if (strcmp(&shstrtab[shdrs[i].sh_name], ".data") == 0) {
      lseek(fd, shdrs[i].sh_offset, SEEK_SET);
      writen(fd, (void*)(shdrs[i].sh_addr + bias), shdrs[i].sh_size);
    }
  }

  close(fd);
  munmap(elf, elf_size);

  rename(tmp, exe);
  chmod(exe, st.st_mode);
}

__attribute__((destructor))
void fini(void) {
  save_elf();
  char *argv[] = {exe, NULL};
  execv(argv[0], argv);
}

extern int (*ftbl[])();
extern int cc;

__attribute__((constructor))
void init(void) {
  find_bias();
  mmap_elf();
  deobfu(ftbl[cc]);
  deobfu(fini);
}
