from constructives import cgrasp
from localsearch import lsbestimp
import time

def execute(inst, iters, alpha, max_time):
    t_start = time.time()                                  # Start the timer
    it = 0                                                 # Iteration counter
    best = None
    while it < iters and time.time() - t_start < max_time: # If we reach the max of iterations or the max time, stop
        it += 1
        sol = cgrasp.construct(inst, alpha)                # Constructive grasp
        lsbestimp.improve(sol)                             # Local search
        if best is None or best['of'] < sol['of']:
            best = sol
    return best, time.time() - t_start