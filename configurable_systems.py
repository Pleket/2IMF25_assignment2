from z3 import *
import numpy as np
import dd.autoref as bdd
import time

file = open("./feature-dimacs/toybox.dimacs", "r")
config = bdd.BDD()
sys.setrecursionlimit(10**5)

mode = str(input('what strategy should be used? \n'))

start = time.time()
print("Start parsing")
# Parsing
clauses = []
for row in file:
    match row[0]:
        case 'c':
            # Order of variables
            order = row[5:].split(' ')
        case 'p':
            vars = row.split(' ')
            for i in range(int(vars[2])):
                config.declare(f'v{i+1}')
        case _:
            clause = row.split(' ')
            clause.pop(-1)
            clauses.append(clause)

print("Start creating CNF")
# Create CNF expressions for the BDD
cnf = None #Final expression
for clause in clauses:
    # New clause in a new expression
    expression = ""
    for var in clause:
        # Positive -> var
        if int(var) > 0:
            expression += f"v{var} | "
        # Negative -> not(var), needs to be multiplied by -1 as well to receive the "positive" version of the number
        if int(var) < 0:
            expression += f"!v{-int(var)} | "
        # No case for var = 0 needed as no function 0 exists
    # Remove trailing or (|) sign:
    expression = expression[:-3]

    clause_new = config.add_expr(expression)

    # If no clause was added yet, the cnf is now the first clause,
    # Otherwise, add the new clause to the cnf
    if cnf == None:
        cnf = clause_new
    else:
        cnf = cnf & clause_new

print("Start decisionmaking")
active_vars = []
choices_made = 0
progress = 0
# CNF has been built, order of vars had been decided, now go through and make choices.
for variable in order:
    progress += 1
    print(f"Checking variable {variable} now. ({progress}/{len(order)})")
    included = cnf & config.add_expr(f"v{variable}")
    excluded = cnf & config.add_expr(f"!v{variable}")

    count_inc = config.count(included)
    count_exc = config.count(excluded)
    if count_inc == count_exc:
        continue

    # Choice needs to be made (variable is essential)
    match mode: # a,b,c or d for strategy with same name, i for interactive.
        case 'a':
            if count_inc > 0:
                # print(f"{variable} was included, {count_inc} valid models given the current choices")
                cnf = included
                active_vars.append(int(variable))
                choices_made += 1
            else:
                # print(f"{variable} was NOT included, {count_exc} valid models given the current choices")
                cnf = excluded
                active_vars.append(-int(variable))
                choices_made += 1
        case 'b':
            if count_exc > 0:
                cnf = excluded
                active_vars.append(-int(variable))
                choices_made += 1
            else:
                cnf = included
                active_vars.append(int(variable))
                choices_made += 1
        case 'c':
            if count_inc > count_exc:
                cnf = included
                active_vars.append(int(variable))
                choices_made += 1
            else:
                cnf = excluded
                active_vars.append(-int(variable))
                choices_made += 1
        case 'd':
            if count_exc > count_inc:
                cnf = excluded
                active_vars.append(-int(variable))
                choices_made += 1
            else:
                cnf = included
                active_vars.append(int(variable))
                choices_made += 1
        case 'i':
            answer = str(input(f"Should variable {variable} be included? (y/n)"))
            if answer == 'y':
                cnf = included
                active_vars.append(int(variable))
                choices_made += 1
            else:
                cnf = excluded
                active_vars.append(-int(variable))
                choices_made += 1
    
print("Final results:")
print("--- %s seconds ---" % (time.time() - start))
print(active_vars)
print(choices_made)