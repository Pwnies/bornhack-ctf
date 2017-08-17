#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>

/* #define DEBUG */

#ifdef DEBUG
#define A 1 // 13
#define B 1 // 14
#define C 3 // 29
#define D 1 // 5
#define E 1 // 3
#define X 5
#else
#define A 2824347577
#define B 3808051021
#define C 2834384563
#define D 3483568087
#define E 3475818217
#define X 670617279
#endif

uint32_t FLAG[5] = {0, 0, 0, 0, 0}, n = 0, x = X, i = 0, j = 0, t = 0;
unsigned long long steps = 0;
#define STEPS "9364283555546638214264"

/* STEP { */
int f00() {
  /* printf("f00\n"); */
  n++;
  return 1;
}

int f01() {
  /* printf("f01\n"); */
  i = A;
  return 2;
}

int f02() {
  /* printf("f02\n"); */
  FLAG[0]++;
  i--;
  return i ? 2 : 3;
}

int f03() {
  /* printf("f03\n"); */
  i = B;
  return 4;
}

int f04() {
  /* printf("f04\n"); */
  FLAG[1]++;
  i--;
  return i ? 4 : 5;
}

int f05() {
  /* printf("f05\n"); */
  i = C;
  return 6;
}

int f06() {
  /* printf("f06\n"); */
  FLAG[2]++;
  i--;
  return i ? 6 : 7;
}

int f07() {
  /* printf("f07\n"); */
  i = D;
  return 8;
}

int f08() {
  /* printf("f08\n"); */
  FLAG[3]++;
  i--;
  return i ? 8 : 9;
}

int f09() {
  /* printf("f09\n"); */
  i = E;
  return 10;
}

int f10() {
  /* printf("f10\n"); */
  FLAG[4]++;
  i--;
  return i ? 10 : 11;
}
/* } STEP */

int f11() {
  /* printf("f11\n"); */
#ifdef DEBUG
  printf(" X = %d, N = %d, STEPS = %d\n", x, n, steps);
  printf(" F0 = 0x%08x, F1 = 0x%08x, F2 = 0x%08x, F3 = 0x%08x, F4 = 0x%08x\n",
         FLAG[0], FLAG[1], FLAG[2], FLAG[3], FLAG[4]);
#endif
  return x == 1 ? 12 : 13;
}

int f12() {
  /* printf("f12\n"); */
#ifdef DEBUG
  printf(" STEPS = %lu\n", steps);
#endif
  printf("\nFLAG{%08x%08x%08x%08x%08x}\n",
    FLAG[0], FLAG[1], FLAG[2], FLAG[3], FLAG[4]);
  _exit(0);
}

int f13() {
  /* printf("f13\n"); */
  return x & 1 ? 14 : 33;
}

int f14() {
  /* printf("f14\n"); */
  x *= 3;
  return 15;
}

int f15() {
  /* printf("f15\n"); */
  x++;
  return 16;
}

/* ODD { */

/* F1 += F0 */
int f16() {
  /* printf("f16\n"); */
#ifdef DEBUG
  printf(" STEPS = %d\n", steps);
  printf(" F1 += F0 = 0x%08x + 0x%08x\n", FLAG[1], FLAG[0]);
#endif
  i = FLAG[0];
  return 17;
}

int f17() {
  /* printf("f17\n"); */
  return i-- ? 18 : 19;
}

int f18() {
  /* printf("f18\n"); */
  FLAG[1]++;
  return 17;
}

/* F2 -= F1 */
int f19() {
  /* printf("f19\n"); */
#ifdef DEBUG
  printf(" STEPS = %d\n", steps);
  printf(" F2 -= F1 = 0x%08x - 0x%08x\n", FLAG[2], FLAG[1]);
#endif
  i = FLAG[1];
  return 20;
}

int f20() {
  /* printf("f20\n"); */
  return i-- ? 21 : 22;
}

int f21() {
  /* printf("f21\n"); */
  FLAG[2]--;
  return 20;
}

/* F3 *= F2 */
int f22() {
  /* printf("f22\n"); */
#ifdef DEBUG
  printf(" STEPS = %d\n", steps);
  printf(" F3 *= F2 = 0x%08x * 0x%08x\n", FLAG[3], FLAG[2]);
#endif
  i = FLAG[2];
  return 23;
}

int f23() {
  /* printf("f23\n"); */
  t = FLAG[3];
  return 24;
}

int f24() {
  /* printf("f24\n"); */
  FLAG[3] = 0;
  return 25;
}

int f25() {
  /* printf("f25\n"); */
  return i-- ? 26 : 30;
}

int f26() {
  /* printf("f26\n"); */
  j = t;
  return 27;
}

int f27() {
  /* printf("f27\n"); */
  return j-- ? 28 : 29;
}

int f28() {
  /* printf("f28\n"); */
  FLAG[3]++;
  return 27;
}

int f29() {
  /* printf("f29\n"); */
  return 25;
}

/* F4 ^= F3 */
int f30() {
  /* printf("f30\n"); */
#ifdef DEBUG
  printf(" STEPS = %d\n", steps);
  printf(" F4 ^= F3 = 0x%08x ^ 0x%08x\n", FLAG[4], FLAG[3]);
#endif
  i = 32;
  return 31;
}

int f31() {
  /* printf("f31\n"); */
  return i-- ? 32 : 0;
}

int f32() {
  /* printf("f32\n"); */
  FLAG[4] ^= FLAG[3] & (1 << i);
  return 31;
}
/* } ODD */

int f33() {
  /* printf("f33\n"); */
  x >>= 1;
  return 34;
}

/* EVEN { */

/* F3 += F4 */
int f34() {
  /* printf("f34\n"); */
#ifdef DEBUG
  printf(" STEPS = %d\n", steps);
  printf(" F3 += F4 = 0x%08x + 0x%08x\n", FLAG[3], FLAG[4]);
#endif
  i = FLAG[4];
  return 35;
}

int f35() {
  /* printf("f35\n"); */
  return i-- ? 36 : 37;
}

int f36() {
  /* printf("f36\n"); */
  FLAG[3]++;
  return 35;
}

/* F2 -= F3 */
int f37() {
  /* printf("f37\n"); */
#ifdef DEBUG
  printf(" STEPS = %d\n", steps);
  printf(" F2 -= F3 = 0x%08x - 0x%08x\n", FLAG[2], FLAG[3]);
#endif
  i = FLAG[3];
  return 38;
}

int f38() {
  /* printf("f38\n"); */
  return i-- ? 39 : 40;
}

int f39() {
  /* printf("f39\n"); */
  FLAG[2]--;
  return 38;
}

/* F1 *= F2 */
int f40() {
  /* printf("f40\n"); */
#ifdef DEBUG
  printf(" STEPS = %d\n", steps);
  printf(" F1 *= F2 = 0x%08x * 0x%08x\n", FLAG[1], FLAG[2]);
#endif
  i = FLAG[2];
  return 41;
}

int f41() {
  /* printf("f41\n"); */
  t = FLAG[1];
  return 42;
}

int f42() {
  /* printf("f42\n"); */
  FLAG[1] = 0;
  return 43;
}

int f43() {
  /* printf("f43\n"); */
  return i-- ? 44 : 48;
}

int f44() {
  /* printf("f44\n"); */
  j = t;
  return 45;
}

int f45() {
  /* printf("f45\n"); */
  return j-- ? 46 : 47;
}

int f46() {
  /* printf("f46\n"); */
  FLAG[1]++;
  return 45;
}

int f47() {
  /* printf("f47\n"); */
  return 43;
}

/* F0 ^= F1 */
int f48() {
  /* printf("f48\n"); */
#ifdef DEBUG
  printf(" STEPS = %d\n", steps);
  printf(" F0 ^= F1 = 0x%08x ^ 0x%08x\n", FLAG[0], FLAG[1]);
#endif
  i = 32;
  return 49;
}

int f49() {
  /* printf("f49\n"); */
  return i-- ? 50 : 0;
}

int f50() {
  /* printf("f50\n"); */
  FLAG[0] ^= FLAG[1] & (1 << i);
  return 49;
}
/* } EVEN */

int (*ftbl[])() = {
  f00, f01, f02, f03, f04, f05, f06, f07,
  f08, f09, f10, f11, f12, f13, f14, f15,
  f16, f17, f18, f19, f20, f21, f22, f23,
  f24, f25, f26, f27, f28, f29, f30, f31,
  f32, f33, f34, f35, f36, f37, f38, f39,
  f40, f41, f42, f43, f44, f45, f46, f47,
  f48, f49, f50, /* f51, f52, f53, f54, f55, */
  /* f56, f57, f58, f59, f60, f61, f62, f63, */
};
int cc = 0;

int main(int argc, char *argv[]) {
  /* for (;;) { */
  printf("\033[G\033[KGenerating flag: %llu/"STEPS, steps);
  fflush(stdout);
  cc = ftbl[cc]();
  steps++;
  /* } */
}
