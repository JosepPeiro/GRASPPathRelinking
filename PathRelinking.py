from constructives import cgrasp
from structure import solution

def ConstrucMultipleSolutions(inst, alpha = 0.1, nsol = 10):
    lsol = []
    bestSol = {"of":0}
    for _ in range(nsol):
        sol = cgrasp.construct(inst, alpha)
        # solution.printSolution(sol)
        lsol.append(sol)

        if sol["of"] > bestSol["of"]:
            bestSol = sol

    return bestSol, lsol


def findLowestIntersection(bestSol, lsol):
    intersec = 0x3f3f3f
    for scand in lsol:
        if scand != bestSol:
            if len(bestSol["sol"].intersection(scand["sol"])) < intersec:
                intersec = len(bestSol["sol"].intersection(scand["sol"]))
                cand = scand
    
    return cand


def PathRelinking(origin, dest):
    bestEver = dest
    while dest["sol"] != origin["sol"]:
        remove = None
        bestRemove = 0x3f3f3f
        add = None
        bestAdd = 0
        for elemR in origin["sol"]:
            if elemR not in dest["sol"]:
                d = solution.distanceToSol(origin, elemR)
                if d < bestRemove:
                    bestRemove = d
                    remove = elemR

        for elemA in dest["sol"]:
            if elemA not in origin["sol"]:
                d = solution.distanceToSol(origin, elemA, without=remove)
                if d > bestAdd:
                    bestAdd = d
                    add = elemA

        solution.removeFromSolution(origin, remove, bestRemove)
        solution.addToSolution(origin, add, bestAdd)

        if origin["of"] > bestEver["of"]:
            bestEver = origin.copy()
    
    return bestEver