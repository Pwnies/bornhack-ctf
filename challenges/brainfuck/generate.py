getchar = ","
putchar = "."
debug = "D"

# [X] -> [0]
clear = "[-]"
# [X, Y] -> [X-Y, 0]
sub = "[-<->]"
# [X, Y] -> [X+Y, 0]
add = "[-<+>]"
# [X, Y] -> [0, X]
copyup = ">" + clear + "<" + "[->+<]"
# [X] -> [X == 0]
neq_zero = copyup + ">[[-]<+>]<"
# [X, Y] -> [X == Y]
neq = sub + "<" + neq_zero

_numbers = {}
def number(n):
    if n in _numbers:
        return _numbers[n]
    q = n / 16
    r = n % 16
    return ">" + clear + "+"*q + "[-<" + "+"*16 + ">]" + "<" + "+"*r

def puts(s):
    code = ""
    s += "\n"
    for c in s:
        code += clear + number(ord(c)) + putchar
    return code + clear

def get_flag():
    with open("flag", "r") as f:
        return f.read().strip()

flag = get_flag()

code = ""
code += puts("Input flag>")

for c in flag:
    code += ">" + clear + number(ord(c)) + ">" + getchar + neq + add + "<"

code += neq_zero + ">>+<<" + "[" + puts("bad flag") + ">>-<<" + "]" + ">>" + "[" + clear + puts("good flag") + "]"
code = code.replace("[-][-]", "[-]")
code = code.replace("<>", "")
code = code.replace("><", "")
code = code.replace("+-", "")
code = code.replace("-+", "")

print code
