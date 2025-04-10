from constructives import cgrasp
from localsearch import lsbestimp
import time
from colorama import Fore

def execute(inst, iters, alpha, max_time):
    t_start = time.time()
    best = None
    for i in range(iters):
        # print(Fore.CYAN + "Iter "+str(i+1)+": ", end="")
        sol = cgrasp.construct(inst, alpha)
        # print(Fore.GREEN + "C -> "+str(round(sol['of'], 2)), end=", ")
        lsbestimp.improve(sol)
        # print(Fore.YELLOW + "LS -> "+str(round(sol['of'], 2)))
        if best is None or best['of'] < sol['of']:
            best = sol
        t_end = time.time()
        if t_end - t_start > max_time:
            return best, t_end - t_start
    return best, t_end - t_start
