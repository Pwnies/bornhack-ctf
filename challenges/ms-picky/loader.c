#include <stdlib.h>
#include <stdbool.h>
#include <link.h>
#include <sys/mman.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>

#include "syscalls.h"
#include "xprintf.h"

#define MIN(a, b) ((a) <= (b) ? (a) : (b))
#define MAX(a, b) ((a) >= (b) ? (a) : (b))

#ifndef __builtin_memcpy
void *memcpy (void *dest, const void *src, size_t n) {
  size_t i;

  for (i = 0; i < n; i++) {
    ((unsigned char*)dest)[i] = ((unsigned char*)src)[i];
  }

  return dest;
}
#else
#define memcpy __builtin_memcpy
#endif

#ifndef __builtin_strncpy
char *strncpy (char *dest, const char *src, size_t n) {
  size_t i;

  for (i = 0; i < n - 1 && src[i]; i++) {
   dest[i] = src[i];
  }
  dest[i] = 0;

  return dest;
}
#else
#define strncpy __builtin_strncpy
#endif

typedef struct {
  unsigned long k, v;
} auxv_t;

typedef struct {
  unsigned long base, bias, entry;
  ElfW(Ehdr) *ehdr;
  ElfW(Phdr) *phdrs;
  unsigned int phnum, type;
  char interp[0x100];
} img_t;

char inner[] = {
#include "inner.enc.inc"
};

int argc;
char **argv, **envp;
auxv_t *auxv;

bool setauxv(unsigned long k, unsigned long v) {
  auxv_t *p = auxv;
  while (p->k) {
    if (k == p->k) {
      p->v = v;
      return true;
    }
    p++;
  }
  return false;
}

bool getauxv(unsigned long k, unsigned long *vp) {
  auxv_t *p = auxv;
  while (p->k) {
    if (k == p->k) {
      *vp = p->v;
      return true;
    }
    p++;
  }
  return false;
}

void load(void *elf, img_t *imgp) {
  ElfW(Ehdr) *ehdr;
  ElfW(Phdr) *phdrs;
  int i, phnum;
  unsigned long base, bias, vaddr, laddr, haddr;

  imgp->interp[0] = 0;
  printf("elf = %p\n", elf);

  ehdr = elf;
  phdrs = elf + ehdr->e_phoff;
  phnum = ehdr->e_phnum;

  laddr = ~0;
  haddr = 0;
  for (i = 0; i < phnum; i++) {
    if (PT_LOAD == phdrs[i].p_type) {
      laddr = MIN(laddr, phdrs[i].p_vaddr);
      haddr = MAX(haddr, phdrs[i].p_vaddr + phdrs[i].p_memsz);
    }
  }

  laddr &= ~0xfff;
  haddr += 0xfff;
  haddr &= ~0xfff;

  printf("map %p %#x\n", ehdr->e_type == ET_EXEC ? (void*)laddr : NULL, haddr - laddr);
  base = (unsigned long)
    mmap(ehdr->e_type == ET_EXEC ? (void*)laddr : NULL,
         haddr - laddr,
         PROT_READ | PROT_WRITE | PROT_EXEC,
         MAP_PRIVATE | MAP_ANON,
         -1, 0);

  bias = base - laddr;

  printf("base = %p, bias = %p\n", base, bias);
  haddr = base;
  for (i = 0; i < phnum; i++) {
    switch (phdrs[i].p_type) {

    case PT_LOAD:
      vaddr = bias + phdrs[i].p_vaddr;
      laddr = vaddr & ~0xfff;
      if (laddr > haddr) {
        printf("unmap %p %#x\n", haddr, laddr - haddr);
        munmap((void*)haddr, laddr - haddr);
      }
      haddr = (vaddr + phdrs[i].p_memsz + 0xfff) & ~0xfff;
      printf("memcpy %p %p %#x\n", vaddr, elf + phdrs[i].p_offset, phdrs[i].p_filesz);
      memcpy((void*)vaddr, elf + phdrs[i].p_offset, phdrs[i].p_filesz);
      break;

    case PT_INTERP:
      strncpy(imgp->interp, elf + phdrs[i].p_offset, sizeof(imgp->interp));
      break;

    }
  }

  imgp->base = base;
  imgp->bias = bias;
  imgp->ehdr = base;
  imgp->phdrs = base + ehdr->e_phoff;
  imgp->phnum = phnum;
  imgp->type = ehdr->e_type;
  imgp->entry = bias + ehdr->e_entry;
}

unsigned long main(unsigned long *stack) {
  unsigned long laddr, haddr, cc;
  unsigned int i;
  unsigned char k;
  img_t exe, interp;
  void *addr;
  int fd;
  struct stat st;

  argc = stack[0];
  argv = (char**)&stack[1];
  envp = (char**)&stack[1 + argc + 1];

  for (i = 0; envp[i]; i++);
  auxv = (auxv_t*)&envp[i + 1];

  for (i = 0, k = 0xff; i < sizeof(inner); i++) {
    inner[i] ^= k--;
  }

  load(inner, &exe);
  setauxv(AT_ENTRY, exe.entry);
  setauxv(AT_PHDR,  exe.phdrs);
  setauxv(AT_PHNUM, exe.phnum);
  cc = exe.entry;

  laddr = ((unsigned long)inner + 0xfff) & ~0xfff;
  haddr = ((unsigned long)inner + sizeof(inner)) & ~0xfff;
  munmap((void*)laddr, haddr - laddr);

  if (exe.interp[0]) {
    fd = open(exe.interp, O_RDONLY);
    fstat(fd, &st);
    addr = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);
    load(addr, &interp);
    munmap(addr, st.st_size);
    printf("INTERP\n");
    printf(" base = %p\n", interp.base);
    printf(" bias = %p\n", interp.bias);
    printf(" ehdr = %p\n", interp.ehdr);
    printf(" phdrs = %p\n", interp.phdrs);
    printf(" phnum = %p\n", interp.phnum);
    printf(" type = %p\n", interp.type);
    printf(" entry = %p\n", interp.entry);
    printf(" interp = %s\n", interp.interp);
    setauxv(AT_BASE, addr);
    cc = interp.entry;
  }

  printf("TARGET\n");
  printf(" base = %p\n", exe.base);
  printf(" bias = %p\n", exe.bias);
  printf(" ehdr = %p\n", exe.ehdr);
  printf(" phdrs = %p\n", exe.phdrs);
  printf(" phnum = %p\n", exe.phnum);
  printf(" type = %p\n", exe.type);
  printf(" entry = %p\n", exe.entry);
  printf(" interp = %s\n", exe.interp);

  return cc;
}
