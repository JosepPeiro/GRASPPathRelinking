from ExecutePathRelinking import ExecutePathRelinking
import os
import time
from structure import instance, solution



if not os.path.exists("results/"):
    os.makedirs("results/")

alpha = 0.1
iters = 999999
time_start_str = time.strftime('%Y%m%d_%H%M%S')
result_file = f"results/{time_start_str}-PathRelinking_results.csv"
f = open(result_file, "w")
f.write("path,alpha,iters,max_time,nsols,prop_time_grasp,local_search_before,local_search_after,random_pairs,obj_value,time_taken\n")
instance_files = [f for f in os.listdir("instances") if f.endswith(".txt")]
for path in instance_files:
    inst = instance.readInstance("instances/" + path)

    for max_time in [0.1, 1, 5, 10, 15, 60]:
        for constrain_constructive in [0.05, 0.1, 0.2, 10, 20, 30]:
            for random_pairs in [None, 2, 3, 4, 5, 6]:
                for local_search_before in [True, False]:
                    for local_search_after in [True, False]:

                        if constrain_constructive < 1:
                            nsols = 999999
                            prop_time_grasp = constrain_constructive
                        else:
                            nsols = int(constrain_constructive)
                            prop_time_grasp = -1

                        best, time_taken = ExecutePathRelinking(inst,
                                                                alpha = alpha,
                                                                iters=iters,
                                                                max_time=max_time,
                                                                nsols=nsols,
                                                                prop_time_grasp=prop_time_grasp,
                                                                local_search_before=local_search_before,
                                                                local_search_after=local_search_after,
                                                                random_pairs=random_pairs)

                        f.write(f"{path},{alpha},{iters},{max_time},{nsols},{prop_time_grasp},{local_search_before},{local_search_after},{random_pairs},{best['of']},{time_taken}\n")

    # print("Best solution found:")
    # solution.printSolution(best)
    # print(f"Time taken: {time_taken:.2f} seconds")