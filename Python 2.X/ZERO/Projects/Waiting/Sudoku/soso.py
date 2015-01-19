import matrix

################################################################################

sdk1 = [[6, 0, 3, 0, 9, 0, 7, 0, 5],
        [0, 0, 1, 2, 0, 0, 0, 8, 0],
        [5, 0, 0, 0, 0, 0, 6, 1, 0],
        [4, 0, 8, 3, 6, 5, 0, 9, 0],
        [0, 5, 0, 0, 0, 0, 0, 3, 0],
        [0, 9, 0, 7, 4, 2, 1, 0, 8],
        [0, 6, 2, 0, 0, 0, 0, 0, 3],
        [0, 4, 0, 0, 0, 7, 8, 0, 0],
        [8, 0, 9, 0, 2, 0, 5, 0, 1]]

sdk2 = [[9, 0, 1, 0, 4, 0, 0, 0, 0],
        [7, 3, 0, 6, 0, 8, 0, 0, 0],
        [0, 5, 0, 3, 0, 0, 0, 0, 0],
        [0, 2, 0, 8, 0, 0, 3, 0, 0],
        [4, 0, 0, 5, 3, 7, 0, 0, 9],
        [0, 0, 7, 0, 0, 1, 0, 5, 0],
        [0, 0, 0, 0, 0, 2, 0, 4, 0],
        [0, 0, 0, 4, 0, 6, 0, 7, 8],
        [0, 0, 0, 0, 8, 0, 9, 0, 1]]

sdk3 = [[0, 0, 0, 2, 0, 0, 6, 8, 5],
        [0, 0, 0, 8, 0, 0, 0, 0, 9],
        [0, 2, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 6, 0, 0, 8, 0, 4, 7],
        [0, 3, 0, 0, 6, 0, 0, 5, 0],
        [2, 7, 0, 5, 0, 0, 1, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 6, 0],
        [3, 0, 0, 0, 0, 2, 0, 0, 0],
        [9, 8, 7, 0, 0, 1, 0, 0, 0]]

OPTIONS = set(range(1, 10))

################################################################################

def build_options(grid):
    options = 0
    new_grid = matrix.Matrix(9, 9)
    for y in range(9):
        for x in range(9):
            number = grid[y][x]
            if number:
                new_grid[y][x] = number
            else:
                options += 1
                new_set = OPTIONS.copy()
                scan_col(grid, y, x, new_set)
                scan_row(grid, y, x, new_set)
                scan_box(grid, y, x, new_set)
                new_grid[y][x] = new_set
    return new_grid, options

def scan_col(grid, y, x, options):
    for row in range(9):
        if row != y:
            options.discard(grid[row][x])

def scan_row(grid, y, x, options):
    for col in range(9):
        if col != x:
            options.discard(grid[y][col])

def scan_box(grid, y, x, options):
    row_base = (y / 3) * 3
    col_base = (x / 3) * 3
    for row_offset in range(3):
        row_index = row_base + row_offset
        for col_offset in range(3):
            col_index = col_base + col_offset
            if not (row_index == y and col_index == x):
                options.discard(grid[row_index][col_index])

################################################################################

def build_answers(grid):
    answers = 0
    new_grid = matrix.Matrix(9, 9)
    for y in range(9):
        for x in range(9):
            cell = grid[y][x]
            if isinstance(cell, int):
                new_grid[y][x] = cell
            elif len(cell) == 1:
                new_grid[y][x] = cell.copy().pop()
                answers += 1
            elif solve_col(grid, y, x, cell.copy(), new_grid) or \
                 solve_row(grid, y, x, cell.copy(), new_grid) or \
                 solve_box(grid, y, x, cell.copy(), new_grid):
                answers += 1
            else:
                new_grid[y][x] = 0
    return new_grid, answers

def solve_col(grid, y, x, options, new_grid):
    for row in range(9):
        if row != y:
            cell = grid[row][x]
            if isinstance(cell, set):
                options.difference_update(cell)
                if not options:
                    return False
    return solve(options, new_grid, y, x)

def solve_row(grid, y, x, options, new_grid):
    for col in range(9):
        if col != x:
            cell = grid[y][col]
            if isinstance(cell, set):
                options.difference_update(cell)
                if not options:
                    return False
    return solve(options, new_grid, y, x)

def solve_box(grid, y, x, options, new_grid):
    row_base = (y / 3) * 3
    col_base = (x / 3) * 3
    for row_offset in range(3):
        row_index = row_base + row_offset
        for col_offset in range(3):
            col_index = col_base + col_offset
            if not (row_index == y and col_index == x):
                cell = grid[row_index][col_index]
                if isinstance(cell, set):
                    options.difference_update(cell)
                    if not options:
                        return False
    return solve(options, new_grid, y, x)

def solve(options, new_grid, y, x):
    if len(options) == 1:
        new_grid[y][x] = options.pop()
        return True
    return False

################################################################################

def main(puzzle):
    op_grid, op_count = build_options(puzzle)
    an_grid, an_count = build_answers(op_grid)
    loop = 1
    while True:
        if an_count == op_count:
            print 'PASS',
            break
        if an_count == 0:
            print 'FAIL',
            break
        op_grid, op_count = build_options(an_grid)
        an_grid, an_count = build_answers(op_grid)
        loop += 1
    print '[', loop, ']'
    for row in an_grid:
        print row
    if an_count == 0:       # DEBUG
        print               # DEBUG
        for row in op_grid: # DEBUG
            print row       # DEBUG

if __name__ == '__main__':
    main(sdk3)
