from structure import instance, solution
from constructives import cgrasp

alpha = 0.1
path = "instances/MDG-a_2_n500_m50.txt"
inst = instance.readInstance(path)

lsol = []
bestSol = {"of":0}
for _ in range(10):
    sol = cgrasp.construct(inst, alpha)
    # solution.printSolution(sol)
    lsol.append(sol)

    if sol["of"] > bestSol["of"]:
        bestSol = sol

intersec = 0x3f3f3f
for scand in lsol:
    if scand != bestSol:
        if len(bestSol["sol"].intersection(scand["sol"])) < intersec:
            intersec = len(bestSol["sol"].intersection(scand["sol"]))
            cand = scand

bestEver = bestSol
while bestSol["sol"] != cand["sol"]:
    remove = None
    bestRemove = 0x3f3f3f
    add = None
    bestAdd = 0
    for elemR in cand["sol"]:
        if elemR not in bestSol["sol"]:
            d = solution.distanceToSol(cand, elemR)
            if d < bestRemove:
                bestRemove = d
                remove = elemR

    for elemA in bestSol["sol"]:
        if elemA not in cand["sol"]:
            d = solution.distanceToSol(cand, elemA, without=remove)
            if d > bestAdd:
                bestAdd = d
                add = elemA

    solution.removeFromSolution(cand, remove, bestRemove)
    solution.addToSolution(cand, add, bestAdd)

    if cand["of"] > bestEver["of"]:
        bestEver = cand.copy()
