from PathRelinking import ConstrucMultipleSolutions, findLowestIntersection, PathRelinking
from structure import instance, solution
import time

def ExecutePathRelinking(inst, alpha, iters=100, max_time=10, nsols=10):
    t_start = time.time()                                  # Start the timer
    it = 0                                                 # Iteration counter
    best = None
    nsols = 10

    while it < iters and time.time() - t_start < max_time:
        it += 1
        best_cons, lsol = ConstrucMultipleSolutions(inst, alpha, nsols)
        if best is None or best['of'] < best_cons['of']:
            best = best_cons.copy()
            solution.printSolution(best)

        alternative = findLowestIntersection(best, lsol)
        super = PathRelinking(alternative, best)
        
        if best is None or best['of'] < super['of']:
            best = super.copy()
            solution.printSolution(best)

    return best, time.time() - t_start


if __name__ == "__main__":
    alpha = 0.1
    path = "instances/MDG-a_2_n500_m50.txt"
    inst = instance.readInstance(path)

    best, time_taken = ExecutePathRelinking(inst, alpha, iters=100, max_time=10, nsols=10)
    print("Best solution found:")
    solution.printSolution(best)
    print(f"Time taken: {time_taken:.2f} seconds")