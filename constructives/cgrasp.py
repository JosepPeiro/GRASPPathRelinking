from structure import solution
import random


def construct(inst, alpha):
    sol = solution.createEmptySolution(inst)
    n = inst['n']
    u = random.randint(0, n-1)                        # Choose a random node
    solution.addToSolution(sol, u)
    cl = createCandidateList(sol, u)
    alpha = alpha if alpha >= 0 else random.random()  # If alpha is negative, choose a random value
    while not solution.isFeasible(sol):
        gmin, gmax = evalGMinGMax(cl)                 # Take the maximum and minumum distnces of the candidate list
        threshold = gmax - alpha * (gmax - gmin)      # Calculate the threshold # alpha = 0 -> greedy, alpha = 1 -> random
        rcl = []
        for i in range(len(cl)):
            if cl[i][0] >= threshold:                 # If the distance is greater than the threshold, candidate
                rcl.append(cl[i])
        selIdx = random.randint(0, len(rcl)-1)        # Choose random candidate from the new list
        cSel = rcl[selIdx]
        solution.addToSolution(sol, cSel[1], cSel[0]) # Add the candidate to the solution
        cl.remove(cSel)                               # Remove the chosen from the candidate list
        updateCandidateList(sol, cl, cSel[1])
    return sol


def evalGMinGMax(cl):
    gmin = 0x3f3f3f
    gmax = 0
    for c in cl:
        gmin = min(gmin, c[0])
        gmax = max(gmax, c[0])
    return gmin, gmax


def createCandidateList(sol, first):
    n = sol['instance']['n']
    cl = []
    for c in range(n):
        if c != first:
            d = solution.distanceToSol(sol, c)
            cl.append([d, c])
    return cl


def updateCandidateList(sol, cl, added):
    for i in range(len(cl)):
        c = cl[i]
        c[0] += sol['instance']['d'][added][c[1]]

