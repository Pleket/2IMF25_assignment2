from z3 import *

file = open("example.col", "r")

n = 0
m = 0
edges = []
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

EdgesSort = Datatype('EdgesSort')
EdgesSort.declare('EdgesSort', IntSort(), ArraySort(IntSort()))

coloring = Function('coloring', IntSort(), IntSort())
conflict = Function('conflict', EdgesSort(), BoolSort())
k = Int('k')

o = Optimize()

for i in range(1, n + 1):
    o.add(And(coloring(i) >= 1, coloring(i) <= k))

