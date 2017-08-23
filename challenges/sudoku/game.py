#!/usr/bin/python2.7 -u
import check
import json
import os
import random
from itertools import product
import config

def list_solutions(sz): 
    return [chal for chal in os.listdir("chals") if chal.startswith("sudoku-%d" % sz)]

def load_solution(chal):
    with open("chals/%s" % chal, "r") as f:
        return json.load(f)

def choose_solutions():
    return map(load_solution, random.sample(list_solutions(sz), config.SAMPLE_SIZE))


def random_points(sz, n):
    return random.sample(list(product(range(sz*sz), repeat=2)), n)


if __name__ == "__main__":
    print "Welcome the the sudoku solving challenge!"

    for sz in [2,3,4,5]:
        for solution in choose_solutions():
            challenge = map(list, solution)
            for p in random_points(sz, (sz*sz*sz*sz) * 3 / 4 ):
                challenge[p[0]][p[1]] = 0
            print challenge
            line = raw_input()
            solution = json.loads(line)
            if check.check_sudoku(sz, solution, challenge):
                print "OK"
            else:
                print "BAD"
                exit(0);

    with open("flag", "r") as f:
        print f.read().strip()
