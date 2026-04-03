
from itertools import permutations


def solve_cryptarithmetic():
    print("=" * 55)
    print("  CRYPTARITHMETIC — SEND + MORE = MONEY")
    print("=" * 55)
    print()
    print("      S E N D")
    print("  +   M O R E")
    print("  -----------")
    print("    M O N E Y")
    print()
    print("  Solving... (all letters → unique digits 0–9)")
    print()

    letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']

    # ── CSP via constrained permutation search ─────────────
    # Variables : S, E, N, D, M, O, R, Y  (8 letters)
    # Domain    : 0-9, all different; S≠0, M≠0
    # Constraint: 1000S+100E+10N+D + 1000M+100O+10R+E
    #           = 10000M+1000O+100N+10E+Y

    solution = None
    checked  = 0

    for perm in permutations(range(10), 8):
        S, E, N, D, M, O, R, Y = perm
        checked += 1

        # Leading-digit constraints
        if S == 0 or M == 0:
            continue

        SEND  = 1000*S + 100*E + 10*N + D
        MORE  = 1000*M + 100*O + 10*R + E
        MONEY = 10000*M + 1000*O + 100*N + 10*E + Y

        if SEND + MORE == MONEY:
            solution = dict(zip(letters, perm))
            break

    print(f"  Permutations checked : {checked:,}")

    if solution:
        S, E, N, D = solution['S'], solution['E'], solution['N'], solution['D']
        M, O, R, Y = solution['M'], solution['O'], solution['R'], solution['Y']

        SEND  = 1000*S + 100*E + 10*N + D
        MORE  = 1000*M + 100*O + 10*R + E
        MONEY = 10000*M + 1000*O + 100*N + 10*E + Y

        print("\n  ── Letter → Digit Mapping ──────────────────")
        for letter in letters:
            print(f"     {letter}  =  {solution[letter]}")

        print("\n  ── Verification ────────────────────────────")
        print(f"       {SEND:>5}   (SEND)")
        print(f"  +    {MORE:>5}   (MORE)")
        print(f"  ---------")
        print(f"     {MONEY:>6}   (MONEY)")
        print()
        ok = SEND + MORE == MONEY
        print(f"  {SEND} + {MORE} = {MONEY}  →  {'✓ Correct!' if ok else '✗ Wrong!'}")
    else:
        print("  No solution found.")


if __name__ == '__main__':
    solve_cryptarithmetic()
