#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/sysinfo.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <stdbool.h>
#include <grp.h>
#include <sys/statvfs.h>
#include <ifaddrs.h>
#include <openssl/sha.h>
#include <signal.h>

#define SADPANDA(S, ...)                                        \
  do {                                                          \
    fprintf(stderr, S " :'(\n", ##__VA_ARGS__);                 \
    exit(EXIT_FAILURE);                                         \
  } while (0)

#define MIN(a, b) ((a) <= (b) ? (a) : (b))

char *getname(pid_t pid) {
  int fd;
  struct stat st;
  ssize_t ret;
  size_t i, numb;
  char path[64], *name;

  snprintf(path, sizeof(path), "/proc/%d/comm", pid);

  fd = open(path, O_RDONLY);
  if (-1 == fd) {
    perror("open()");
    exit(EXIT_FAILURE);
  }

  numb = 0;
  name = NULL;
  i = 0;
  for (;;) {
    if (i == numb) {
      numb += 16;
      name = realloc(name, numb);
      if (NULL == name) {
        perror("malloc()");
        exit(EXIT_FAILURE);
      }
    }

    ret = read(fd, &name[i], numb - i);
    if (-1 == ret) {
      if (EINTR == errno) {
        continue;
      }
      perror("read()");
      exit(EXIT_FAILURE);
    }
    if (0 == ret) {
      if (i && name[i - 1] == '\n') {
        name[i - 1] = 0;
      } else {
        name[i] = 0;
      }
      break;
    }
    i += ret;
  }

  close(fd);

  return name;
}

bool ismember(char *group) {
  int i, ngroups;
  gid_t *groups;
  struct group *gr;

  ngroups = getgroups(0, NULL);

  groups = malloc(ngroups * sizeof(gid_t));
  if (groups == NULL) {
    perror("malloc()");
    exit(EXIT_FAILURE);
  }

  if (-1 == getgroups(ngroups, groups)) {
    perror("getgroups()");
    exit(EXIT_FAILURE);
  }

  for (i = 0; i < ngroups; i++) {
    gr = getgrgid(groups[i]);
    if (NULL != gr) {
      if (0 == strcmp(gr->gr_name, group)) {
        return true;
      }
    }
  }
  return false;
}

unsigned long freespace(char *path) {
  struct statvfs f;

  if (-1 == statvfs(path, &f)) {
    perror("statvfs()");
    exit(EXIT_FAILURE);
  }

  return f.f_bsize * f.f_bfree;
}

unsigned int numifaces() {
  struct ifaddrs *addrs,*tmp;
  unsigned int nif = 0;

  getifaddrs(&addrs);
  tmp = addrs;

  while (tmp) {
    if (tmp->ifa_addr && tmp->ifa_addr->sa_family == AF_PACKET) {
      nif++;
    }
    tmp = tmp->ifa_next;
  }

  freeifaddrs(addrs);

  return nif;
}

bool sigd = false;
void handler(int signum) {
  sigd = true;
}

int main(int argc, char *argv[]) {
  char *name, *pname, *user;
  pid_t pid, ppid;
  bool bornhacker;
  unsigned long ncores, ram, space, ifaces;
  struct sysinfo info;
  SHA256_CTX ctx;
  unsigned char digest[20];

  signal(SIGTRAP, handler);
  kill(0, SIGTRAP);
  while (!sigd);

  if (!SHA256_Init(&ctx)) {
    fprintf(stderr, "SHA256_Init() failed\n");
    exit(EXIT_FAILURE);
  }

#define UPDATE(buf, len)                                        \
  do {                                                          \
    if (!SHA256_Update(&ctx, (unsigned char*)buf, len)) {       \
      fprintf(stderr, "SHA256_Update() failed\n");              \
      exit(EXIT_FAILURE);                                       \
    }                                                           \
  } while (0)

#define PID 1337
#ifdef DEBUG
  pid = PID;
#else
  pid = getpid();
#endif
  UPDATE(&pid, sizeof(pid));

  ppid = getppid();

  name = getname(getpid());

#define PNAME "powershell.exe"
#ifdef DEBUG
  pname = PNAME;
#else
  pname = getname(getppid());
#endif
  UPDATE(pname, strlen(pname));

#define USER "root"
#ifdef DEBUG
  user = USER;
#else
  user = getlogin();
#endif
  UPDATE(user, strlen(user));

#define BORNHACKER true
#ifdef DEBUG
  bornhacker = BORNHACKER;
#else
  bornhacker = ismember("bornhack");
#endif
  UPDATE(&bornhacker, sizeof(bornhacker));

#define NCORES 1024
#ifdef DEBUG
  ncores = NCORES;
#else
  ncores = MIN(sysconf(_SC_NPROCESSORS_ONLN), NCORES);
#endif
  UPDATE(&ncores, sizeof(ncores));

#define RAM (unsigned long)1<<40
#ifdef DEBUG
  ram = RAM;
#else
  sysinfo(&info); ram = MIN(info.totalram, RAM);
#endif
  UPDATE(&ram, sizeof(ram));

#define SPACE (unsigned long)1<<50
#ifdef DEBUG
  space = SPACE;
#else
  space = MIN(freespace("/tmp"), SPACE);
#endif
  UPDATE(&space, sizeof(space));

#define IFACES 200
#ifdef DEBUG
  ifaces = IFACES;
#else
  ifaces = MIN(numifaces(), IFACES);
#endif
  UPDATE(&ifaces, sizeof(ifaces));

  if (strcmp(pname, "powershell.exe")) {
    SADPANDA("no PowerShell^TM");
  }

  if (strcmp(user, USER)) {
    SADPANDA("i no can bez " USER "?");
  }

  if (PID != pid) {
    SADPANDA("PID is not h4x0r enough");
  }

  if (!bornhacker) {
    SADPANDA("not a bornhack'er");
  }

  if (ncores < NCORES) {
    SADPANDA("i wish i was an HPC");
  }

  if (ram < RAM) {
    SADPANDA("<1T RAM, cannot start Chrome");
  }

  if (space < SPACE) {
    SADPANDA("need more free space in /tmp");
  }

  if (ifaces < IFACES) {
    SADPANDA("too few network interfaces");
  }

  if (!SHA256_Final(digest, &ctx)) {
    fprintf(stderr, "SHA256_Final() failed\n");
    exit(EXIT_FAILURE);
  }

  printf("FLAG{%08x%08x%08x%08x%08x}\n",
         ((unsigned int*)digest)[0],
         ((unsigned int*)digest)[1],
         ((unsigned int*)digest)[2],
         ((unsigned int*)digest)[3],
         ((unsigned int*)digest)[4]
         );

  return 0;
}
