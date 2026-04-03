

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables   = variables
        self.domains     = {v: list(d) for v, d in domains.items()}
        self.neighbors   = neighbors
        self.constraints = constraints

    def ac3(self, domains=None):
        if domains is None:
            domains = {v: list(d) for v, d in self.domains.items()}
        queue = [(xi, xj) for xi in self.variables for xj in self.neighbors.get(xi, [])]
        while queue:
            xi, xj = queue.pop(0)
            if self._revise(domains, xi, xj):
                if not domains[xi]:
                    return None
                for xk in self.neighbors.get(xi, []):
                    if xk != xj:
                        queue.append((xk, xi))
        return domains

    def _revise(self, domains, xi, xj):
        revised = False
        for x in domains[xi][:]:
            if not any(self.constraints(xi, x, xj, y) for y in domains[xj]):
                domains[xi].remove(x)
                revised = True
        return revised

    def backtrack(self, assignment=None, domains=None):
        if assignment is None:
            assignment = {}
        if domains is None:
            domains = self.ac3() or {v: list(d) for v, d in self.domains.items()}
        if len(assignment) == len(self.variables):
            return assignment
        var = min([v for v in self.variables if v not in assignment], key=lambda v: len(domains[v]))
        for value in sorted(domains[var], key=lambda val: sum(1 for nb in self.neighbors.get(var, []) if nb not in assignment and val in domains[nb])):
            if all(self.constraints(var, value, nb, assignment[nb]) for nb in self.neighbors.get(var, []) if nb in assignment):
                assignment[var] = value
                new_domains = {v: list(d) for v, d in domains.items()}
                new_domains[var] = [value]
                reduced = self.ac3(new_domains)
                if reduced is not None:
                    result = self.backtrack(assignment, reduced)
                    if result is not None:
                        return result
                del assignment[var]
        return None


def print_sudoku(grid):
    for r, row in enumerate(grid):
        if r % 3 == 0 and r != 0:
            print("  " + "-" * 21)
        line = "  "
        for c, val in enumerate(row):
            if c % 3 == 0 and c != 0:
                line += "| "
            line += (str(val) if val != 0 else ".") + " "
        print(line)
    print()


def solve_sudoku():
    print("=" * 55)
    print("  SUDOKU PUZZLE — CSP")
    print("=" * 55)

    # 0 = empty cell
    puzzle = [
        [5, 3, 0,  0, 7, 0,  0, 0, 0],
        [6, 0, 0,  1, 9, 5,  0, 0, 0],
        [0, 9, 8,  0, 0, 0,  0, 6, 0],

        [8, 0, 0,  0, 6, 0,  0, 0, 3],
        [4, 0, 0,  8, 0, 3,  0, 0, 1],
        [7, 0, 0,  0, 2, 0,  0, 0, 6],

        [0, 6, 0,  0, 0, 0,  2, 8, 0],
        [0, 0, 0,  4, 1, 9,  0, 0, 5],
        [0, 0, 0,  0, 8, 0,  0, 7, 9],
    ]

    print("\n  Input puzzle:")
    print_sudoku(puzzle)

    # Variables: (row, col)
    variables = [(r, c) for r in range(9) for c in range(9)]

    # Domains
    domains = {}
    for r, c in variables:
        domains[(r, c)] = [puzzle[r][c]] if puzzle[r][c] != 0 else list(range(1, 10))

    # Neighbours: same row, col, or 3×3 box
    def get_neighbors(r, c):
        nbrs = set()
        for i in range(9):
            if i != c: nbrs.add((r, i))
            if i != r: nbrs.add((i, c))
        br, bc = (r // 3) * 3, (c // 3) * 3
        for dr in range(3):
            for dc in range(3):
                nr, nc = br + dr, bc + dc
                if (nr, nc) != (r, c):
                    nbrs.add((nr, nc))
        return list(nbrs)

    neighbors = {v: get_neighbors(*v) for v in variables}

    def diff_values(v1, val1, v2, val2):
        return val1 != val2

    csp    = CSP(variables, domains, neighbors, diff_values)
    result = csp.backtrack()

    if result:
        solution = [[result[(r, c)] for c in range(9)] for r in range(9)]
        print("  Solved puzzle:")
        print_sudoku(solution)
        print("  ✓ Sudoku solved successfully!")
    else:
        print("  No solution found.")


if __name__ == '__main__':
    solve_sudoku()
