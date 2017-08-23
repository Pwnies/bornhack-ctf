from itertools import product

def check_rules(sz, dim, board):
    if dim == 1:
        return set(range(1,sz*sz+1)) == set(board[(i,)] for i in range(sz*sz))

    if dim == 2:
        for i, j in product(range(sz), repeat=2):
            box = set()
            for x, y in product(range(sz), repeat=2):
                box.add(board[(sz*i + x, sz*j + y)])
            if box != set(range(1, sz*sz+1)):
                return False
        
    for i in range(dim):
        for j in range(sz*sz):
            board_slice = {}
            for p, v in board.items():
                if p[i] == j:
                    board_slice[p[:i] + p[i+1:]] = v
            if not check_rules(sz, dim-1, board_slice):
                return False

    return True

def check_sudoku(sz, solution, challenge):
    solution = from_lists(sz, 2, solution)
    challenge = from_lists(sz, 2, challenge)
    for p, v in challenge.items():
        if v != 0 and solution[p] != v:
            return False

    return check_rules(sz, 2, solution)

def from_lists(sz, dim, l):
    sudoku = {}
    for p in product(range(sz*sz), repeat=dim):
        v = l
        for i in p: v = v[i]
        assert type(v) == int
        sudoku[p] = v
    return sudoku
