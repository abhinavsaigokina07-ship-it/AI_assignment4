
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


def solve_australia():
    print("=" * 55)
    print("  AUSTRALIA MAP COLOURING — CSP")
    print("=" * 55)

    states = ['WA', 'NT', 'SA', 'Queensland', 'NSW', 'V', 'T']

    adjacency = {
        'WA':         ['NT', 'SA'],
        'NT':         ['WA', 'SA', 'Queensland'],
        'SA':         ['WA', 'NT', 'Queensland', 'NSW', 'V'],
        'Queensland': ['NT', 'SA', 'NSW'],
        'NSW':        ['SA', 'Queensland', 'V'],
        'V':          ['SA', 'NSW'],
        'T':          []
    }

    colors  = ['Red', 'Green', 'Blue']
    domains = {s: list(colors) for s in states}

    def diff_colors(v1, c1, v2, c2):
        return c1 != c2

    csp    = CSP(states, domains, adjacency, diff_colors)
    result = csp.backtrack()

    if result:
        print("\n  Solution found!\n")
        print(f"  {'State':<15} {'Color'}")
        print(f"  {'-'*15} {'-'*10}")
        for state in states:
            print(f"  {state:<15} {result[state]}")

        violations = [(s, nb) for s, nbrs in adjacency.items() for nb in nbrs if result[s] == result[nb]]
        print(f"\n  {'✓ All constraints satisfied!' if not violations else f'⚠ Violations: {violations}'}")
    else:
        print("  No solution found.")


if __name__ == '__main__':
    solve_australia()
