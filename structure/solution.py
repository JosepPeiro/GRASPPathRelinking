def createEmptySolution(instance):
    sol = {}
    sol['instance'] = instance
    sol['sol'] = set()
    sol['of'] = 0               # Objective Value
    return sol


def addToSolution(sol, u, ofVariation = -1):
    if ofVariation < 0:
        for s in sol['sol']:
            sol['of'] += sol['instance']['d'][u][s]
    else:
        sol['of'] += ofVariation
    sol['sol'].add(u)


def removeFromSolution(sol, u, ofVariation = -1):
    sol['sol'].remove(u)
    if ofVariation < 0:
        for s in sol['sol']:
            sol['of'] -= sol['instance']['d'][u][s]
    else:
        sol['of'] -= ofVariation


def evaluate(sol):
    of = 0
    for s1 in sol['sol']:
        for s2 in sol['sol']:
            if s1 < s2:
                of += sol['instance']['d'][s1][s2]
    return of


def isFeasible(sol):
    return len(sol['sol']) == sol['instance']['p']


def contains(sol, u):
    return u in sol['sol']


def distanceToSol(sol, u, without = -1):
    d = 0
    for s in sol['sol']:
        if s != u and s != without:
            d += sol['instance']['d'][s][u]
    return round(d, 2)


def printSolution(sol):
    print("Solution: ", end="")
    for s in sol['sol']:
        print(str(s), end=" ")
    print()
    print("Objective Value: "+str(round(sol['of'], 2)))