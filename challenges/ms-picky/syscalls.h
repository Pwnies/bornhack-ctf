#ifndef __SYSCALLS_H_
#define __SYSCALLS_H_

#include <sys/syscall.h>
#include <sys/stat.h>
#include <unistd.h>

#ifdef SYS_mmap2
void *mmap2(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
#define mmap mmap2
#else
void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
#endif

int mprotect(void *addr, size_t length, int prot);
int munmap(void *addr, size_t length);
void *mremap(void *oldaddr, size_t oldsize, size_t newsize, int flags, ...);
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
void exit(int status) __attribute__((noreturn));
int open(const char *pathname, int flags, ...);
int close(int fd);
int access(const char *pathname, int mode);
int fstat(int fd, struct stat *buf);

long clone(unsigned long flags, void *child_stack);

int nanosleep(const struct timespec *req, struct timespec *rem);

pid_t getpid(void);
int kill(pid_t pid, int sig);
#define raise(sig)                              \
  kill(getpid(), sig)

#endif
