import struct
import functools

def p16(v): return struct.pack("<H", v)

def belt(s, **kwargs):
    assert s[0] in ("%", "$")
    return int(s[1], 16)

def imm(s, **kwargs):
    try:
        return int(s, 10)
    except ValueError:
        return int(s, 16)

def lbl(s, **kwargs):
    if s in kwargs["labels"]:
        return kwargs["labels"][s]
    kwargs["missing"].add(s)
    return 0

def imm_or_lbl(s, **kwargs):
    try:
        return imm(s, **kwargs)
    except ValueError:
        return lbl(s, **kwargs)

def name(s, **kwargs):
    return s.strip()

def fmt0(a,b,c,d):
    assert 0 <= a <= 15
    assert 0 <= b <= 15
    assert 0 <= c <= 15
    assert 0 <= d <= 15
    return p16((a << 12) | (b << 8) | (c << 4) | d)

def fmt1(a,b,imm):
    assert 0 <= a <= 15
    assert 0 <= b <= 15
    assert 0 <= imm <= 255
    return p16((a << 12) | (b << 8) | imm)

instructions = {}

def instruction(inst_name, *ps):
    def deco(f):
        global instructions
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*[p(a, **kwargs) for (p,a) in zip(ps, args)], **kwargs)
        instructions[inst_name] = wrapper
        return wrapper
    return deco

@instruction("#")
def comment_inst(*args, **kwargs):
    return ""

@instruction("label", name)
def label_inst(name, **kwargs):
    addr = len(kwargs["code"])
    kwargs["labels"][name] = addr
    return ""

def data_inst(*args, **kwargs):
    return "".join(chr(imm(arg)) for arg in args)

instructions["data"] = data_inst

def alu_inst(name, aluop):
    def alu(r1, r2, **kwargs):
        return fmt0(0, aluop, r1, r2)
    instruction(name, belt, belt)(alu)

def alui_inst(name, aluop):
    def alui(r1, imm, **kwargs):
        return fmt0(1, aluop, r1, imm)
    instruction(name+"i", belt, imm)(alui)

for aluop, name in enumerate(["add", "sub", "xor", "or", "and", "not", "equ", "neq", "geq", "leq", "rol", "ror"]):
    alu_inst(name, aluop);
    alui_inst(name, aluop)

@instruction("lw", belt)
def lw_inst(addr, **kwargs):
    return fmt0(2, 0, addr, 0)

@instruction("lw.sp", imm)
def lwsp_inst(off, **kwargs):
    return fmt0(2, 2, off, 0)

@instruction("lb", belt)
def lb_inst(addr, **kwargs):
    return fmt0(2, 4, addr, 0)

@instruction("lb.sp", imm)
def lbsp_inst(off, **kwargs):
    return fmt0(2, 6, off, 0)

@instruction("sw", belt, belt)
def sw_inst(addr, val, **kwargs):
    return fmt0(2, 1, addr, val)

@instruction("sw.sp", imm, belt)
def swsp_inst(off, val, **kwargs):
    return fmt0(2, 3, off, val)

@instruction("sb", belt, belt)
def sb_inst(addr, val, **kwargs):
    return fmt0(2, 5, addr, val)

@instruction("sb.sp", imm, belt)
def sbsp_inst(off, val, **kwargs):
    return fmt0(2, 7, off, val)


@instruction("mux", belt, belt, belt)
def mux_inst(r1, r2, r3, **kwargs):
    return fmt0(3, r1, r2, r3)

@instruction("const", imm_or_lbl)
def const_inst(imm, **kwargs):
    assert 0 <= imm <= 0xffff
    return fmt1(15, 0, imm & 0xff) + fmt1(15, 1, imm >> 8)

@instruction("relpc", imm)
def relpc_inst(imm, **kwargs):
    assert 0 <= imm <= 0xff
    return fmt1(15, 2, imm)

@instruction("relsp", imm)
def relsp_inst(imm, **kwargs):
    assert 0 <= imm <= 0xff
    return fmt1(15, 3, imm)

@instruction("adjsp", imm)
def adjsp_inst(imm, **kwargs):
    assert 0 <= imm <= 0xff
    return fmt1(15, 4, imm)

@instruction("setsp", belt)
def setsp_inst(reg, **kwargs):
    return fmt0(15, 5,0, reg)

@instruction("jmp", belt)
def jmp_inst(destreg, **kwargs):
    return fmt0(15, 6,0, destreg)

@instruction("debug")
def debug_inst(**kwargs):
    return fmt1(15, 14, 0)

@instruction("halt", imm)
def halt_inst(exit_code, **kwargs):
    return fmt1(15,15, exit_code)

def asm_single_pass(source, labels):
    missing = set()
    code = ""

    for line in source.split("\n"):
        line = line.strip()
        if not line: continue
        try:
            op, args = line.split(" ", 1)
        except ValueError:
            op = line
            args = ""

        op = op.strip()
        inst = instructions[op]
        args = map(str.strip, args.split(","))
        try:
            code += inst(*args, **locals())
        except Exception:
            print line
            raise

    return code, missing, labels

def asm(source):
    code, missing, labels = asm_single_pass(source, {})
    code, missing, labels = asm_single_pass(source, labels)

    if len(missing) != 0:
        print "Error, missing labels: %s" % ",".join(missing)
        exit(1)

    return code, labels

def main():
    import sys
    source = sys.argv[1]
    output = sys.argv[2]
    with open(source, "r") as f:
        source = f.read()
        code, labels = asm(source)
    print labels
    with open(output, "w") as f:
        f.write(code)

if __name__ == "__main__": main()
