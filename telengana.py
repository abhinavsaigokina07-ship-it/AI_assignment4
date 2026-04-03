

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


def solve_telangana():
    print("=" * 60)
    print("  TELANGANA 33-DISTRICT MAP COLOURING — CSP")
    print("=" * 60)

    districts = [
        'Adilabad', 'Kumurambheem Asifabad', 'Mancherial', 'Nirmal',
        'Nizamabad', 'Jagtial', 'Peddapalli', 'Rajanna Sircilla',
        'Karimnagar', 'Jayashankar Bhupalpally', 'Mulugu',
        'Bhadradri Kothagudem', 'Khammam', 'Suryapet', 'Nalgonda',
        'Yadadri Bhuvanagiri', 'Medchal Malkajgiri', 'Hyderabad',
        'Rangareddy', 'Vikarabad', 'Sangareddy', 'Medak', 'Kamareddy',
        'Siddipet', 'Jangaon', 'Mahabubabad', 'Warangal Urban',
        'Warangal Rural', 'Nagarkurnool', 'Wanaparthy', 'Gadwal',
        'Mahabubnagar', 'Narayanpet'
    ]

    adjacency = {
        'Adilabad':                    ['Kumurambheem Asifabad', 'Nirmal', 'Mancherial'],
        'Kumurambheem Asifabad':       ['Adilabad', 'Mancherial'],
        'Mancherial':                  ['Adilabad', 'Kumurambheem Asifabad', 'Nirmal', 'Jagtial', 'Peddapalli', 'Jayashankar Bhupalpally'],
        'Nirmal':                      ['Adilabad', 'Mancherial', 'Nizamabad', 'Jagtial', 'Kamareddy'],
        'Nizamabad':                   ['Nirmal', 'Kamareddy', 'Sangareddy'],
        'Jagtial':                     ['Nirmal', 'Mancherial', 'Rajanna Sircilla', 'Karimnagar', 'Peddapalli'],
        'Peddapalli':                  ['Mancherial', 'Jagtial', 'Karimnagar', 'Rajanna Sircilla', 'Jayashankar Bhupalpally'],
        'Rajanna Sircilla':            ['Jagtial', 'Peddapalli', 'Karimnagar', 'Siddipet', 'Kamareddy'],
        'Karimnagar':                  ['Jagtial', 'Peddapalli', 'Rajanna Sircilla', 'Siddipet', 'Jayashankar Bhupalpally', 'Warangal Urban'],
        'Jayashankar Bhupalpally':     ['Mancherial', 'Peddapalli', 'Karimnagar', 'Mulugu', 'Warangal Rural', 'Warangal Urban'],
        'Mulugu':                      ['Jayashankar Bhupalpally', 'Warangal Rural', 'Bhadradri Kothagudem'],
        'Bhadradri Kothagudem':        ['Mulugu', 'Warangal Rural', 'Khammam'],
        'Khammam':                     ['Bhadradri Kothagudem', 'Mahabubabad', 'Suryapet', 'Nalgonda'],
        'Suryapet':                    ['Khammam', 'Nalgonda', 'Yadadri Bhuvanagiri', 'Mahabubabad'],
        'Nalgonda':                    ['Khammam', 'Suryapet', 'Yadadri Bhuvanagiri', 'Medchal Malkajgiri', 'Rangareddy'],
        'Yadadri Bhuvanagiri':         ['Suryapet', 'Nalgonda', 'Medchal Malkajgiri', 'Jangaon', 'Mahabubabad'],
        'Medchal Malkajgiri':          ['Nalgonda', 'Yadadri Bhuvanagiri', 'Hyderabad', 'Rangareddy', 'Medak', 'Siddipet', 'Jangaon'],
        'Hyderabad':                   ['Medchal Malkajgiri', 'Rangareddy'],
        'Rangareddy':                  ['Hyderabad', 'Medchal Malkajgiri', 'Nalgonda', 'Vikarabad', 'Mahabubnagar'],
        'Vikarabad':                   ['Rangareddy', 'Mahabubnagar', 'Narayanpet', 'Sangareddy'],
        'Sangareddy':                  ['Nizamabad', 'Kamareddy', 'Medak', 'Rangareddy', 'Vikarabad'],
        'Medak':                       ['Sangareddy', 'Kamareddy', 'Siddipet', 'Medchal Malkajgiri'],
        'Kamareddy':                   ['Nizamabad', 'Nirmal', 'Rajanna Sircilla', 'Sangareddy', 'Medak'],
        'Siddipet':                    ['Kamareddy', 'Rajanna Sircilla', 'Karimnagar', 'Medak', 'Medchal Malkajgiri', 'Jangaon'],
        'Jangaon':                     ['Siddipet', 'Karimnagar', 'Warangal Urban', 'Warangal Rural', 'Yadadri Bhuvanagiri', 'Medchal Malkajgiri'],
        'Mahabubabad':                 ['Warangal Rural', 'Khammam', 'Suryapet', 'Yadadri Bhuvanagiri'],
        'Warangal Urban':              ['Karimnagar', 'Jayashankar Bhupalpally', 'Jangaon', 'Warangal Rural'],
        'Warangal Rural':              ['Jayashankar Bhupalpally', 'Mulugu', 'Bhadradri Kothagudem', 'Mahabubabad', 'Yadadri Bhuvanagiri', 'Jangaon', 'Warangal Urban'],
        'Nagarkurnool':                ['Mahabubnagar', 'Wanaparthy', 'Nalgonda'],
        'Wanaparthy':                  ['Nagarkurnool', 'Mahabubnagar', 'Gadwal'],
        'Gadwal':                      ['Wanaparthy', 'Mahabubnagar', 'Narayanpet'],
        'Mahabubnagar':                ['Rangareddy', 'Vikarabad', 'Narayanpet', 'Gadwal', 'Wanaparthy', 'Nagarkurnool'],
        'Narayanpet':                  ['Vikarabad', 'Mahabubnagar', 'Gadwal'],
    }

    colors  = ['Red', 'Green', 'Blue', 'Yellow']
    domains = {d: list(colors) for d in districts}

    def diff_colors(v1, c1, v2, c2):
        return c1 != c2

    csp    = CSP(districts, domains, adjacency, diff_colors)
    result = csp.backtrack()

    if result:
        print("\n  Solution found!\n")
        max_len = max(len(d) for d in districts)
        print(f"  {'District':<{max_len+2}} {'Color'}")
        print(f"  {'-'*(max_len+2)} {'-'*10}")
        for d in districts:
            print(f"  {d:<{max_len+2}} {result[d]}")

        violations = [(dist, nb) for dist, nbrs in adjacency.items() for nb in nbrs if result[dist] == result[nb]]
        print(f"\n  {'✓ All 33 district constraints satisfied!' if not violations else f'⚠ Violations: {violations}'}")
    else:
        print("  No solution found.")


if __name__ == '__main__':
    solve_telangana()
