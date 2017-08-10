#include <stdio.h>

int main(int argc, char **argv){
    char name[100];
    setbuf(stdout, NULL);
    printf("Hello! Who are you?\n");
    gets(name);
    printf("Hi %s! Nice to meet you\n", name);
}
