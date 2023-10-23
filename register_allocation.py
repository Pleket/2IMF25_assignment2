from z3 import *
import numpy as np
import dd.autoref as bdd

file = open("./big-dimacs/less-dimacs/gcd.col", "r")

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

bdd1 = bdd.BDD()
vert = 0
first = True
u = None
file.seek(0)
expressions = []
expressions.append("(k_5 & !k_4 & k_3 & k_2 & k_1)")
for row in file:
    match row[0]:
        case 'c':
            continue
        case 'p':
            rows = row.split(' ')
            vert = int(rows[2])
            for i in range(1, vert + 1):
                for j in range(1, 6):
                    bdd1.declare(f"x_{i}_{j}")
            for j in range(1, 6):
                bdd1.declare(f"k_{j}")
            for i in range(1, vert + 1):
                expressions.append(f"""((k_{5} | !x_{i}_5) & 
                                (!(!k_5 & !k_4) | !x_{i}_4) &
                                (!(!k_5 & !k_4 & !k_3) | !x_{i}_3) &
                                (!(!k_5 & !k_4 & !k_3 & !k_2) | !x_{i}_2))""")
        case 'e':
            rows = row.split(' ')
            a = int(rows[1])
            b = int(rows[2])
            expressions.append(f"""(!((x_{a}_5 & x_{b}_5) | (!x_{a}_5 & !x_{b}_5)) |
                            !((x_{a}_4 & x_{b}_4) | (!x_{a}_4 & !x_{b}_4)) |
                            !((x_{a}_3 & x_{b}_3) | (!x_{a}_3 & !x_{b}_3)) |
                            !((x_{a}_2 & x_{b}_2) | (!x_{a}_2 & !x_{b}_2)) |
                            !((x_{a}_1 & x_{b}_1) | (!x_{a}_1 & !x_{b}_1)))""")
u = bdd1.add_expr(" & ".join(expressions))

print(bdd1.count(u))

# check_bdd = bdd.BDD()
# check_bdd.declare("x", "y")
# z1 = check_bdd.add_expr("x")
# z2 = check_bdd.add_expr("!y")
# print(check_bdd.count(z1))
# models = list(check_bdd.pick_iter(z1, ['x', 'y']))
# print(models)
# print(check_bdd.count(z2))
# models = list(check_bdd.pick_iter(z2, ['x', 'y']))
# print(models)