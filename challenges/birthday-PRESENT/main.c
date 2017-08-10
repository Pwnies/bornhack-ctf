#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int st;
typedef unsigned char u8;

#define ROUNDS (31)

/* A SMALL PRESENTation of the cipher follows below.
 * Also long key is best key.
 */

u8 sbox[] = {
    0xC, 0x5, 0x6, 0xB,
    0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8,
    0x4, 0x7, 0x1, 0x2
};

st layer_add_key(st s, st k) {
    return s ^ k;
}

st layer_sub(st s) {
    st o = 0;
    for (size_t n = 0; n < 8; n++) {
        o >>= 4;
        o |= sbox[s & 0xf] << 28;
        s >>= 4;
    }
    return o;
}

st layer_permute(st s) {
    st o = 0;
    for (size_t i = 0; i < sizeof(o) * 8 - 1; i++) {
        st n = (8*i) % 31;
        o |= (s & 1) << n;
        s >>= 1;
    }
    o |= (s & 1) << 31;
    return o;
}

st encrypt(st s, st k[]) {
    for (size_t r = 0; r < ROUNDS; r++) {
        s = layer_add_key(s, k[r]);
        s = layer_sub(s);
        s = layer_permute(s);
    }
    s = layer_add_key(s, k[ROUNDS]);
    return s;
}

void cbc(char *ct, char* pt, st iv, st k[], size_t len) {
    memcpy(ct, (char*) &iv, sizeof(iv));
    ct += sizeof(iv);
    for (size_t n = 0; n < len / sizeof(st); n++) {
        iv ^= ((st*) pt)[n];
        iv = encrypt(iv, k);
        memcpy(ct, (char*) &iv, sizeof(iv));
        ct += sizeof(iv);
    }
}

int main(int argc, char* argv[]) {
    const size_t PT_SIZE = 1 << 20;
    const size_t CT_SIZE = PT_SIZE + sizeof(st);

    // read flag
    char *pt = malloc(PT_SIZE);
    {
        FILE* f = fopen("./flag.fmt", "r");
        size_t len = fread(pt, 1, PT_SIZE, f);
        for (size_t i = len; i + len < PT_SIZE; i += len) {
            memcpy(&pt[i], &pt[0], len);
        }
        fclose(f);
    }

    // read user input
    fgets(pt, PT_SIZE, stdin);

    // encrypt
    char *ct = malloc(CT_SIZE);
    {
        st iv = rand();
        st key[ROUNDS + 1];
        FILE* f = fopen("/dev/urandom", "r");
        size_t len = fread(key, sizeof(key), 1, f);
        if (len != 1)
            exit(-1);
        fclose(f);
        cbc(ct, pt, iv, key, PT_SIZE);
    }

    // write ciphertext
    for (size_t n = 0; n < CT_SIZE;) {
        n += fwrite(&ct[n], 1, CT_SIZE - n, stdout);
    }

    fflush(stdout);
    return 0;
}
