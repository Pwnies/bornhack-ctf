#!/usr/bin/python -u

class UTM:
    _tables = {}
    linecounter = 0
    current = 'A'
    tape = ['' for x in range(5000)]
    tapepointer = 2500
    current_collatz = 24

    def __init__(self):
        max_len = 0
        collatz = self.current_collatz
        while collatz != 1:
            binlen = len(bin(collatz))#yes, this gives us two more spaces
            if binlen > max_len:
                max_len = binlen
            collatz = self.next_collatz(collatz)
        totape = bin(self.current_collatz)[2:]
        missing = max_len - len(totape)
        totape = '0'*missing + totape
        for i,c in enumerate(totape):
            self.tape[self.tapepointer+i+1] = 'C'*(1+int(c))


    def decode_line(self, line):
        def check(testee, letter, argument):
            for char in testee:
                if char not in  letter:
                    print(argument +" contains other letters then " + letter)
                    exit()

        ds = line.split('D')
        if len(ds) != 5:
            print("The following line is table is malformed")
            print(str(self.linecounter)+": "+line)
            exit()
        name = ds[1]
        check(name, 'A', 'Configuration name')
        symbol = ds[2]
        check(symbol, 'C', 'Tape Symbol')
        print_operation = ds[3][:-1]
        check(print_operation, 'C', 'Print Operation')
        motion = ds[3][-1]
        if motion not in ['R','L','N']:
            print('The direction has to be a "R", "L" or "N"')
            exit()
        goto = ds[4]
        check(goto, 'AH', 'Next Configuration Name')
        self.linecounter += 1
        return TableEntry(name, symbol, print_operation, motion, goto)


    def decode_program(self, program):
        for line in program.split(';')[1:]:
            table_entry = self.decode_line(line)
            key = (table_entry.name,table_entry.symbol)
            if key in self._tables.keys():
                print(
                    "(" + table_entry.name + "," + table_entry.symbol +
                    ") has been defined twice"
                )
                exit()
            self._tables[key] = table_entry


    def step(self):
        key = (self.current,self.tape[self.tapepointer])
        if key not in self._tables.keys():
            key = str(key[0]) + ':'+ str(key[1])
            print('D' + key + " is the next table entry, but it isn't defined")
            exit()
        current_entry = self._tables[key]
        self.tape[self.tapepointer] = current_entry.print_operation
        if current_entry.motion == 'R':
            self.tapepointer += 1
        elif current_entry.motion == 'L':
            self.tapepointer -= 1
        self.current = current_entry.goto


    def get_input(self):
        program = raw_input("Input program:\n")
        return program
    def get_input_from_file(self,name):
        f = open(name,'r')
        return f.read()
    def run(self):
        program = self.get_input()
        self.execturing(program)

    def runfromfile(self,filename):
        program = self.get_input_from_file(filename)
        self.execturing(program)

    def execturing(self, program):
        self.decode_program(program)
        done = 1337
        while done != 1:
            while self.current != 'H':
                self.step()
                #print(self.tape[2500:2550])
                #print str(self.tapepointer) + ' D'+self.current
            done = self.extract_number()
            #print("Calulated collatz number: " + str(done))
            self.current_collatz = self.next_collatz(self.current_collatz)
            if done != self.current_collatz:
                print("sorry, your machine isn't computing the correct result")
                exit()
            self.current = 'A'
        with open('flag','r') as flag:
            print(flag.read())

    def extract_number(self):
        number = ''
        tp = self.tapepointer +1
        while self.tape[tp]:
            number += str(len(self.tape[tp])-1)
            tp += 1
        return int(number,2)


    def next_collatz(self,n):
        if n % 2 == 1:
            return 3 * n +1
        else:
            return n/2


class TableEntry:
    def __init__(self, name, symbol, print_operation, motion, goto):
        self.name = name
        self.symbol = symbol
        self.print_operation = print_operation
        self.motion = motion
        self.goto = goto

if __name__ == "__main__":
#tests
    mytm = UTM()
    #mytm.runfromfile('solution')
    mytm.run()
