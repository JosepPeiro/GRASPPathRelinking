from PathRelinking import ConstructMultipleSolutions, findLowestIntersection, PathRelinking, SelectRandomPair
from structure import instance, solution
import time

def ExecutePathRelinking(inst, alpha = 0.1, iters=100, max_time=10, nsols=10, prop_time_grasp=0.5,
                         local_search_before=False, local_search_after=False, random_pairs=None):
    t_start = time.time()                                                     # Start the timer
    it = 0                                                                    # Iteration counter
    best = None
    grasp_time = prop_time_grasp * max_time if prop_time_grasp > 0 or prop_time_grasp is None else None  # Time for GRASP

    while it < iters and time.time() - t_start < max_time:
        it += 1
        best_cons, lsol = ConstructMultipleSolutions(inst, alpha, nsols, max_time=grasp_time, local_search = local_search_before)
        if best is None or best['of'] < best_cons['of']:
            best = best_cons.copy()
            # solution.printSolution(best)

        alternative = findLowestIntersection(best, lsol)
        super = PathRelinking(alternative, best, local_search=local_search_after)
        if random_pairs and len(lsol) > 2 + random_pairs:
            avoid = [best, alternative]
            for _ in range(random_pairs):
                if len(avoid) + random_pairs <= len(lsol):
                    selected, avoid = SelectRandomPair(lsol, avoid)
                    farthest = findLowestIntersection(selected, lsol)
                    middle_point = PathRelinking(selected, farthest, local_search=local_search_after)
                    if best is None or best['of'] < middle_point['of']:
                        best = middle_point.copy()
                        # solution.printSolution(best)
        
        if best is None or best['of'] < super['of']:
            best = super.copy()
            # solution.printSolution(best)

    return best, time.time() - t_start


# if __name__ == "__main__":

#     alpha = 0.1
#     path = "instances/MDG-a_2_n500_m50.txt"
#     inst = instance.readInstance(path)

#     best, time_taken = ExecutePathRelinking(inst, alpha, iters=100, max_time=20, nsols=10, prop_time_grasp=0.1, local_search_before=True, local_search_after=True,
#                                             random_pairs=4)
#     print("Best solution found:")
#     solution.printSolution(best)
#     print(f"Time taken: {time_taken:.2f} seconds")