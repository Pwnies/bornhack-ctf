#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

unsigned char code[1 << 16];
unsigned char tape[256];
unsigned char ptr = 0;

void do_debug(){
    int i;
    printf("\n");
    printf("\n");
    for(i=0; i < 256; i++){
        if(i == ptr){
            printf("[%02x]", tape[i]);
        } else {
            printf(" %02x ", tape[i]);
        }
        if(i % 16 == 15){
            printf("\n");
        }
    }
    //exit(0);
}

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
                case 'D': do_debug(); break;
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

int main(int argc, char **argv){
    int script = open(argv[1], O_RDONLY);
    read(script, code, sizeof(code));
    close(script);

    run_brainfuck(code, 1);
}

