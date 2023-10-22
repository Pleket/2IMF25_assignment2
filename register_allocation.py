from z3 import *
import numpy as np
import dd.autoref as bdd

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

# t = Then('simplify', 'normalize-bounds', 'solve-eqs')
# r = t(o)
# print(r)
# print(r[0])

# s = Optimize()
# s.add(r[0])
# print(s.check())
# print(s.model())
# print(r.convert_model(s.model()))

bdd = bdd.BDD()
vert = 0
first = True
u = None
file.seek(0)
for row in file:
    match row[0]:
        case 'c':
            continue
        case 'p':
            rows = row.split(' ')
            vert = int(rows[2])
            for i in range(1, vert + 1):
                for j in range(1, 6):
                    bdd.add_var(f"x_{i}_{j}")
            for j in range(1, 6):
                bdd.add_var(f"k_{j}")
            # for i in range(1, vert + 1):
            #     z = bdd.add_expr(f"(k_{5} | !x_{i}_{5}) & 
            #                     (!(!k_{5} & !k_{4}) | !x_{i}_{4}) &
            #                     (!(!k_{5} & !k_{4} & !k_{3}) | !x_{i}_{3}) &
            #                     (!(!k_{5} & !k_{4} & !k_{3} & !k_{2}) | !x_{i}_{2})")
            # if first:
            #     u = z
            #     first = False
        case 'e':
            rows = row.split(' ')
            a = int(rows[1])
            b = int(rows[2])
            z = bdd.add_expr(f"""!((x_{a}_{5} & x_{b}_{5}) | (!x_{a}_{5} & !x_{b}_{5})) |
                            !((x_{a}_{4} & x_{b}_{4}) | (!x_{a}_{4} & !x_{b}_{4})) |
                            !((x_{a}_{3} & x_{b}_{3}) | (!x_{a}_{3} & !x_{b}_{3})) |
                            !((x_{a}_{2} & x_{b}_{2}) | (!x_{a}_{2} & !x_{b}_{2})) |
                            !((x_{a}_{1} & x_{b}_{1}) | (!x_{a}_{1} & !x_{b}_{1}))""")
            if first:
                u = z
            # print(u)
            # print(u.negated)

print(bdd.count(u))