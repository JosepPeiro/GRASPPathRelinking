from structure import solution

def improve(sol):
    improve = True
    while improve:
        improve = tryImprove(sol)


def tryImprove(sol):
    sel, ofVarSel, unsel, ofVarUnsel = selectInterchange(sol)
    print("sel: ", sel, "ofVarSel: ", ofVarSel)
    if ofVarSel < ofVarUnsel:
        solution.removeFromSolution(sol, sel, ofVarSel)
        solution.addToSolution(sol, unsel, ofVarUnsel)
        return True
    return False


def selectInterchange(sol):
    n = sol['instance']['n']
    sel = -1
    bestSel = 0x3f3f3f                                       # Best distance for interchange (We search the lowest distance, so undesirable)
    unsel = -1
    bestUnsel = 0
    for v in sol['sol']:
        d = solution.distanceToSol(sol, v)
        if d < bestSel:
            bestSel = d
            sel = v                                          # Best node to remove -> Minimum distance
    for v in range(n):
        if not solution.contains(sol, v):
            d = solution.distanceToSol(sol, v, without=sel)  ##### We changed the position of this line #####
            if d > bestUnsel:
                bestUnsel = d
                unsel = v                                    # Best node to add -> Maximum distance
    return sel, round(bestSel,2), unsel, round(bestUnsel,2)  # Return: best node to remove and its distance, best node to add and its distance