from z3 import *
import random
import json
import hashlib
from itertools import product
import config

def generate_rules(sz, dim, board):
    if dim == 1:
        return [Distinct([board[(i,)] for i in range(sz*sz)])]
    rules = []
    if dim == 2:
        for i, j in product(range(sz), range(sz)):
            box = []
            for x, y in product(range(sz), range(sz)):
                box.append(board[(sz*i + x, sz*j + y)])
            rules.append(Distinct(box))
        
    for i in range(dim):
        for j in range(sz*sz):
            board_slice = {}
            for p, v in board.items():
                if p[i] == j:
                    board_slice[p[:i] + p[i+1:]] = v
            rules += generate_rules(sz, dim-1, board_slice)
    return rules

def generate_sudoku(sz):
    board = {}
    rules = []
    for i, p in enumerate(product(range(sz*sz), repeat=2)):
        board[p] = Int("x_%d" % i)
        rules.append(And(1 <= board[p], board[p] <= sz*sz))
    return board, rules + generate_rules(sz, 2, board)

def random_points(sz):
    return random.sample(list(product(range(sz*sz), repeat=2)), sz*sz)

def generate_challenge(sz):
    board, rules = generate_sudoku(sz)
    while True:
        solver = Solver()
        solver.add(rules)
        for p in random_points(sz):
            solver.add(board[p] == random.randint(1, sz*sz))
        if solver.check() == sat: 
            model = solver.model()
            solution = [[None]*sz*sz for _ in range(sz*sz)]
            for p, v in board.items():
                solution[p[0]][p[1]] = int(str(model.eval(v)))
            return solution

if __name__ == "__main__":
    for sz in config.SIZES:
        for i in range(config.POPULATION_SIZE):
            chal = generate_challenge(sz)
            print sz, i
            data = json.dumps(chal)
            shasum = hashlib.sha256(data).hexdigest()
            with open("chals/sudoku-%d-%s" % (sz, shasum), "w") as f:
                f.write(data)
