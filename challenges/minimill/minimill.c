#include<stdint.h>
#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<unistd.h>

typedef uint16_t reg_t;

typedef struct regs {
    reg_t belt[16];
    int belt_idx;
    reg_t pc;
    reg_t sp;
} regs_t;

typedef struct cpu {
    regs_t regs;
    uint8_t memory[0x10000];
} cpu_t;

typedef reg_t (*aluop_t)(reg_t, reg_t);
typedef void (*inst_t)(cpu_t *, reg_t );

void belt_push(cpu_t *cpu, reg_t val) {
    cpu->regs.belt[++cpu->regs.belt_idx % 16] = val;
}

reg_t belt_peek(cpu_t *cpu, int off) {
    return cpu->regs.belt[(cpu->regs.belt_idx - off) & 0xf];
}

void print_debug(cpu_t *cpu){
    #define peek(off) belt_peek(cpu, off)
    int i;
    fprintf(stderr, "\n");
    fprintf(stderr, "pc: 0x%04x sp: 0x%04hx", cpu->regs.pc, cpu->regs.sp);
    for(i = 0; i < 16; i++){
        if(i % 4 == 0) fprintf(stderr, "\n");
        fprintf(stderr, "b%01x: 0x%04hx ", i, peek(i));
    }
    fprintf(stderr, "\n");
}

void mmio_write(cpu_t *cpu, reg_t addr, char *data, int size) {
    char tmp;
    if(size != 2){
        return;
    }

    switch(addr & 0xff) {
        case 2:
            write(1, data, 1);
            break;
    }
}

void mmio_read(cpu_t *cpu, reg_t addr, char *data, int size) {
    char tmp;
    if(size != 2){
        memset(data, 0x55, size);
        return;
    }

    switch(addr & 0xff){
        case 0:
            read(0, &tmp, 1);
            data[0] = tmp;
            data[1] = 0;
            break;
    }
}

void memory_write(cpu_t *cpu, reg_t addr, void *data, int size) {
    if(0xff00 <= addr) return mmio_write(cpu, addr, data, size);
    memcpy(&cpu->memory[addr], data, size);
}

void memory_read(cpu_t *cpu, reg_t addr, void *data, int size) {
    if(0xff00 <= addr) return mmio_read(cpu, addr, data, size);
    memcpy(data, &cpu->memory[addr], size);
}

#define A(inst) (((inst) >> 12) & 0xf)
#define B(inst) (((inst) >> 8) & 0xf)
#define C(inst) (((inst) >> 4) & 0xf)
#define D(inst) (((inst) >> 0) & 0xf)

void nop_instruction(cpu_t *cpu, reg_t inst){
    // nothing to see here...
}

reg_t alu_add(reg_t a, reg_t b){ return a + b; }
reg_t alu_sub(reg_t a, reg_t b){ return a - b; }
reg_t alu_xor(reg_t a, reg_t b){ return a ^ b; }
reg_t alu_or(reg_t a, reg_t b){ return a | b; }
reg_t alu_and(reg_t a, reg_t b){ return a | b; }
reg_t alu_not(reg_t a, reg_t b){ return ~a; }
reg_t alu_equ(reg_t a, reg_t b){ return a == b; }
reg_t alu_neq(reg_t a, reg_t b){ return a != b; }
reg_t alu_geq(reg_t a, reg_t b){ return a <= b; }
reg_t alu_leq(reg_t a, reg_t b){ return a >= b; }
reg_t alu_rol(reg_t a, reg_t b){ b = b & 0xf; return (a << b) | (a >> (16 - b)); }
reg_t alu_ror(reg_t a, reg_t b){ b = b & 0xf; return (a >> b) | (a << (16 - b)); }

aluop_t aluops[16] = {
    alu_add,    // 0x10xx
    alu_sub,    // 0x11xx
    alu_xor,    // 0x12xx
    alu_or,     // 0x13xx
    alu_and,    // 0x14xx
    alu_not,    // 0x15xx
    alu_equ,    // 0x16xx
    alu_neq,    // 0x17xx
    alu_geq,    // 0x18xx
    alu_leq,    // 0x19xx
    alu_rol,    // 0x1axx
    alu_ror,    // 0x1bxx
    alu_add,    // 0x1cxx
    alu_add,    // 0x1dxx
    alu_add,    // 0x1exx
    alu_add,    // 0x1fxx
};

void alu_instruction(cpu_t *cpu, reg_t inst){
    belt_push(cpu, aluops[B(inst)](belt_peek(cpu, C(inst)), belt_peek(cpu, D(inst))));
}

void alui_instruction(cpu_t *cpu, reg_t inst){
    belt_push(cpu, aluops[B(inst)](belt_peek(cpu, C(inst)), D(inst)));
}


void mem_instruction(cpu_t *cpu, reg_t inst){
    reg_t tmp = 0;
    reg_t addr = belt_peek(cpu, C(inst));
    reg_t val  = belt_peek(cpu, D(inst));
    switch(B(inst)){
        case 2:
            addr = cpu->regs.sp + C(inst);
        case 0:
            memory_read(cpu, addr, &tmp, sizeof(reg_t));
            belt_push(cpu, tmp);
            break;
        case 3:
            addr = cpu->regs.sp + C(inst);
        case 1:
            memory_write(cpu, addr, &val, sizeof(reg_t));
            break;
        case 6:
            addr = cpu->regs.sp + C(inst);
        case 4:
            memory_read(cpu, addr, &tmp, sizeof(uint8_t));
            belt_push(cpu, tmp);
            break;
        case 7:
            addr = cpu->regs.sp + C(inst);
        case 5:
            memory_write(cpu, addr, &val, sizeof(uint8_t));
            break;
    }
}

void mux_instruction(cpu_t *cpu, reg_t inst){
    belt_push(cpu, belt_peek(cpu, belt_peek(cpu, B(inst)) ? C(inst) : D(inst)));
}

void misc_instruction(cpu_t *cpu, reg_t inst){
    reg_t new_pc;
    switch(B(inst)){
        case 0: // immh
            belt_push(cpu, inst & 0xff);
            break;
        case 1: // imml
            cpu->regs.belt[cpu->regs.belt_idx % 16] |= (inst & 0xff) << 8;
            break;
        case 2: // rel pc
            belt_push(cpu, cpu->regs.pc + (inst & 0xff));
            break;
        case 3: // rel sp
            belt_push(cpu, cpu->regs.sp + (inst & 0xff));
            break;
        case 4: // adjsp 0xnn
            belt_push(cpu, cpu->regs.sp);
            cpu->regs.sp -= (inst & 0xff);
            break;
        case 5: // setsp bx:
            cpu->regs.sp = belt_peek(cpu, inst & 0xf);
            break;
        case 6: // jmp bx
            new_pc = belt_peek(cpu, inst & 0xf);
            cpu->regs.pc = new_pc;
            break;
        case 14: // debug
            print_debug(cpu);
            break;
        case 15: // halt 0xnn
            exit(inst & 0xff);
            break;

    }
}


inst_t opcodes[16] = {
    alu_instruction,    // 0x0xxx
    alui_instruction,   // 0x1xxx
    mem_instruction,    // 0x2xxx
    mux_instruction,    // 0x3xxx
    nop_instruction,    // 0x4xxx
    nop_instruction,    // 0x5xxx
    nop_instruction,    // 0x6xxx
    nop_instruction,    // 0x7xxx
    nop_instruction,    // 0x8xxx
    nop_instruction,    // 0x9xxx
    nop_instruction,    // 0xaxxx
    nop_instruction,    // 0xbxxx
    nop_instruction,    // 0xcxxx
    nop_instruction,    // 0xdxxx
    nop_instruction,    // 0xexxx
    misc_instruction,   // 0xfxxx
};

#include "rom.h"

int main(int argc, char **argv) {
    cpu_t cpu;
    memset(&cpu, 0, sizeof(cpu));
    memset(cpu.memory, 0xff, 0x10000);
    cpu.regs.pc = 0x0000;
    cpu.regs.sp = 0xff00;
    int count = 0x100000;

    memory_write(&cpu, 0, (void *)rom_bin, rom_bin_len);

    while(count--){
        reg_t inst;
        memory_read(&cpu, cpu.regs.pc, &inst, sizeof(inst));
        cpu.regs.pc += sizeof(reg_t);
        opcodes[(inst >> 12) & 0xf](&cpu, inst);
    }

    return 0;
}
