from z3 import *
import numpy as np

file = open("./big-dimacs/fpsol2.i.1.col", "r")

coloring = Function('coloring', IntSort(), IntSort())
k = Int('k')

o = Goal()

# i = 1
# limit = 5000
for row in file:
    match row[0]:
        case 'c':
            continue
        case 'p':
            rows = row.split(' ')
            for i in range(1, int(rows[2]) + 1):
                o.add(And(coloring(i) > 0, coloring(i) < k + 1))
        case 'e':
            rows = row.split(' ')
            o.add(Or(coloring(int(rows[1])) < coloring(int(rows[2])), coloring(int(rows[1])) > coloring(int(rows[2]))))
    # i += 1
    # if i > limit:
    #     break
o.add(k == 30)

# o.minimize(k)
# print(o.check())
# print(o.model())

t = Then('simplify', 'normalize-bounds', 'solve-eqs')
r = t(o)
print(r)
print(r[0])

s = Optimize()
s.add(r[0])
print(s.check())
print(s.model())
# print(r.convert_model(s.model()))