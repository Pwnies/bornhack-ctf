#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

unsigned char tape[256];
unsigned char ptr = 0;

unsigned char *run_brainfuck(unsigned char *code_ptr, int executing){
    unsigned char *new_code_ptr;
    while(1){
        if(executing){
            switch(*code_ptr){
                case '+': tape[ptr]++; break;
                case '-': tape[ptr]--; break;
                case '>': ptr++; break;
                case '<': ptr--; break;
                case ',': tape[ptr] = getchar(); break;
                case '.': putchar(tape[ptr]); break; 
            }
        }
        
        switch(*code_ptr++){
            case '[':
                new_code_ptr = run_brainfuck(code_ptr, executing && tape[ptr] != 0);
                code_ptr = tape[ptr] ? code_ptr - 1 : new_code_ptr;
                break;
            case ']': return code_ptr;
            case '\x00': return NULL;
        }
    }
}

#include "chal.h"

int main(int argc, char **argv){
    run_brainfuck(chal_bf, 1);
}

