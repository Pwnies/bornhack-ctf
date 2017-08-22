[BITS 64]
[GLOBAL _start]
[EXTERN main]

[SECTION .start progbits alloc exec]

%define SYS_exit 60

_start:
    mov rdi, rsp
    call main
    xor rdx, rdx
    ;; int3
    jmp rax
