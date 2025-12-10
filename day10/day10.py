import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import re
from itertools import product
import pulp
from collections import defaultdict

from util import *

data = get_data('day10/day10.txt', 'lines')

def parse_line(line, part):
    if part == 1:
        # Lijst van knoppen
        buttons_raw = re.findall(r"\(([\d,]*)\)", line)
        buttons = []
        for g in buttons_raw:
            if g.strip() == "":
                buttons.append([])
            else:
                buttons.append(list(map(int, g.split(','))))
        m = len(buttons)
        
        # Lichtpatroon (doel)
        pattern = re.search(r"\[([.#]+)\]", line)
        if pattern:
            pattern = pattern.group(1)
            b = [1 if c == '#' else 0 for c in pattern]
            n = len(b)
        else:
            raise ValueError("Geen lichtpatroon aanwezig in: " + line)
        
        # Creëer matrix n (aantal lampen) x m (aantal knoppen)
        # mat[i][j] = 1 als knop j lamp i togglet
        mat = [[0]*m for _ in range(n)]
        for j, btn in enumerate(buttons):
            for i in btn:
                mat[i][j] ^= 1

        return mat, b
    
    else:
        # Lijst van knoppen
        buttons_raw = re.findall(r"\(([\d,]*)\)", line)
        masks = []
        for g in buttons_raw:
            g = g.strip()
            if g == "":
                mask = 0
            else:
                idxs = [int(x) for x in g.split(',')]
                mask = 0
                for i in idxs:
                    mask |= (1 << i)
            masks.append(mask)
            
        # Lijst van joltage doelen
        joltage = re.search(r"\{([^}]*)\}", line)
        if not joltage:
            raise ValueError("no curly braces found")
        b = [int(s.strip()) for s in joltage.group(1).split(',')]
        n = len(b)
        
        # Comprimeer functioneel identieke masks
        mask_to_indices = defaultdict(list)
        for idx, mask in enumerate(masks):
            mask_to_indices[mask].append(idx)

        compressed = [(mask, mask_to_indices[mask]) for mask in mask_to_indices]
        return compressed, b
        
def gauss_elim_gf2(mat, b):
    # Gauss-eliminatie mod 2 op mat met augmented kolom b
    n = len(mat)
    m = len(mat[0]) if n>0 else 0
    # Augmented rijen
    M = [row[:] + [b_i] for row, b_i in zip(mat, b)]

    row = 0
    pivot_cols_in_order = []
    pivot_row_for_col = {}
    for col in range(m):
        # Zoek pivot rij met 1 in deze kolom op of onder 'row'
        sel = None
        for r in range(row, n):
            if M[r][col] == 1:
                sel = r
                break
        if sel is None:
            continue
        M[row], M[sel] = M[sel], M[row]
        pivot_cols_in_order.append(col)
        pivot_row_for_col[col] = row

        # Elimineer alle andere rijen
        for r in range(n):
            if r != row and M[r][col] == 1:
                # XOR de hele rij
                M[r] = [ (a ^ b) for a,b in zip(M[r], M[row]) ]
        row += 1
        if row == n:
            break

    # Check voor inconsistentie
    for r in range(n):
        if all(M[r][c] == 0 for c in range(m)) and M[r][m] == 1:
            return M, pivot_row_for_col, pivot_cols_in_order, False  # inconsistent

    return M, pivot_row_for_col, pivot_cols_in_order, True

def min_weight_solution(mat, b):

    n = len(mat)
    m = len(mat[0]) if n>0 else 0
    M, pivot_row_for_col, pivot_cols_in_order, consistent = gauss_elim_gf2(mat, b)
    if not consistent:
        return None

    # Bouw een specifieke oplossing x0 en een basis voor de nullruimte
    pivot_cols = pivot_cols_in_order[:]
    pivot_set = set(pivot_cols)
    free_cols = [c for c in range(m) if c not in pivot_set]
    k = len(free_cols)

    x0 = [0]*m

    # Terugsubstitutie om specifieke oplossing te vinden
    for pc in pivot_cols_in_order[::-1]:
        r = pivot_row_for_col[pc]
        rhs = M[r][m]
        s = rhs
        for c in range(pc+1, m):
            if M[r][c] and x0[c]:
                s ^= 1
        x0[pc] = s

    null_basis = []
    for f in free_cols:
        v = [0]*m
        v[f] = 1
        for pc in pivot_cols:
            r = pivot_row_for_col[pc]
            if M[r][f] == 1:
                v[pc] = 1
        null_basis.append(v)

    best = None

    for bits in product([0,1], repeat=k):
        x = x0[:]
        for bit, v in zip(bits, null_basis):
            if bit:
                x = [ (xi ^ vi) for xi, vi in zip(x, v) ]
        weight = sum(x)
        if best is None or weight < best:
            best = weight
    return best

def solve_part_1(lines):
    total = 0
    for line in lines:
        mat, b = parse_line(line, part = 1)
        res = min_weight_solution(mat, b)
        if res is None:
            raise ValueError("Machine unsolvable (inconsistent):\n" + line)
        total += res
    return total

# ============= Part 2 =============

def solve_with_pulp(compressed_masks, b):
    n = len(b)
    masks = [m for m, _ in compressed_masks]

    prob = pulp.LpProblem("joltage_min_presses", pulp.LpMinimize)
    vars_x = {}
    for mask in masks:
        affected = [i for i in range(n) if (mask >> i) & 1]
        if not affected:
            ub = 0
        else:
            ub = min(b[i] for i in affected)
        var = pulp.LpVariable(f"x_{mask:0{n}b}", lowBound=0, upBound=ub, cat="Integer")
        vars_x[mask] = var

    # per-counter constraints
    for i in range(n):
        expr = None
        for mask in masks:
            if (mask >> i) & 1:
                if expr is None:
                    expr = vars_x[mask]
                else:
                    expr += vars_x[mask]
        if expr is None:
            if b[i] != 0:
                return None
            else:
                continue
        prob += (expr == b[i])

    prob += sum(vars_x[mask] for mask in masks)

    pulp.PULP_CBC_CMD(msg = False).solve(prob)
    status = pulp.LpStatus[prob.status]
    if status in ("Optimal", "Feasible"):
        x_vals = [int(pulp.value(vars_x[mask])) for mask in masks]
        return sum(x_vals)
    else:
        return None


def min_presses_for_machine_line(line):
    compressed, b = parse_line(line, part = 2)
    # Verwijder masks die geen effect hebben
    compressed = [(mask, idxs) for mask,idxs in compressed if mask != 0]
    # ALs er geen masks over zijn, check of b allemaal 0 is
    if not compressed:
        if any(v != 0 for v in b):
            raise ValueError("Infeasible machine (no buttons affect counters but b>0):\n" + line)
        return 0

    # Roep pulp aan
    return solve_with_pulp(compressed, b)

def solve_part_2(lines):
    overall = 0
    for line in lines:
        result = min_presses_for_machine_line(line)
        if result is not None:
            overall += result
    return overall
    
print("Part 1:", solve_part_1(data))
print("Part 2:", solve_part_2(data))