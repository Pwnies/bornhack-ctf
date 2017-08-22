#ifndef __XPRINTF_H_
#define __XPRINTF_H_

#ifdef PRINTF
#include <stdarg.h>

int vsnprintf(char *str, size_t size, const char  *fmt, va_list ap);
int snprintf(char *str, size_t size, const  char  *fmt, ...);
int vprintf(const char *fmt, va_list ap);
int printf(const char *fmt, ...);
#else
#define vsnprintf(...)
#define snprintf(...)
#define vprintf(...)
#define printf(...)
#define flush(...)
#endif

#endif
