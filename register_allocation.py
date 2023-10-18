from z3 import *
import numpy as np

file = open("./big-dimacs/fpsol2.i.1.col", "r")

coloring = Function('coloring', IntSort(), IntSort())
k = Int('k')

o = Optimize()

i = 1
limit = 1000
for row in file:
    match row[0]:
        case 'c':
            continue
        case 'p':
            rows = row.split(' ')
            for i in range(1, int(rows[2]) + 1):
                o.add(And(coloring(i) >= 1, coloring(i) <= k))
        case 'e':
            rows = row.split(' ')
            o.add(coloring(int(rows[1])) != coloring(int(rows[2])))
    i += 1
    if i > limit:
        break

o.minimize(k)
o.check()
o.model()