from z3 import *
import numpy as np

file = open("./big-dimacs/fpsol2.i.1.col", "r")

n = 0
m = 0
edges = []
# n_nb = np.zeros(n)
for row in file:
    match row[0]:
        case 'c':
            continue
        case 'p':
            rows = row.split(' ')
            n = int(rows[2])
            m = int(rows[3])
        case 'e':
            rows = row.split(' ')
            edges.append((int(rows[1]), int(rows[2])))
            edges.append((int(rows[2]), int(rows[1])))
            # n_nb[int(rows[1]) - 1] += 1
            # n_nb[int(rows[2]) - 1] += 1
edges.sort()

# EdgesSort = Datatype('EdgesSort')
# EdgesSort.declare('EdgesSort', ArraySort(IntSort(), IntSort()))

coloring = Function('coloring', IntSort(), IntSort())
# neighbors = Function('neighbors', IntSort(), EdgesSort())
# conflict = Function('conflict', EdgesSort(), BoolSort())
k = Int('k')

o = Optimize()

# j = 0
# old_node = 0
# for i in range(1, m + 1):
#     if edges[i][0] != old_node:
#         j = 0
#         old_node = edges[i][0]
#     o.add(neighbors(edges[i][0])[j] == edges[i][1])
#     j += 1

# for i in range(1, n + 1):
#     o.add(And(coloring(i) >= 1, coloring(i) <= k))

#     o.add(neighbors(i).range() == n_nb[i - 1])

# for i in range(1, n + 1):
#     Int('j')
#     o.add(ForAll(neighbors(i)[j], coloring(i) != coloring(neighbors(i)[j])))

# minimize(o)

for i in range(1, n + 1):
    o.add(And(coloring(i) >= 1, coloring(i) <= k))

for i in range(0, m):
    o.add(coloring(edges[i][0]) != coloring(edges[i][1]))

o.minimize(k)
o.check()
o.model()