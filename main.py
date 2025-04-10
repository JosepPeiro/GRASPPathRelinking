from structure import instance, solution
from algorithms import grasp
import random
import time
import os
from colorama import init, Fore
from analyze.utils import analyzeResults, writeExcel
import matplotlib.pyplot as plt
from tqdm import tqdm


# Initialize colorama
init(autoreset=True)

def writeResult(file_path, instance_name, alpha, obj_value, time_taken):
    header = "instance,alpha,obj_value,time\n"
    row = f"{instance_name},{alpha},{obj_value},{time_taken}\n"
    
    is_new_file = not os.path.exists(file_path)
    mode = "w" if is_new_file else "a"
    with open(file_path, mode) as f:
        if is_new_file:
            f.write(header)
        f.write(row)

def executeInstances(instance_files, iterations=10, alphas=[0], max_time=1, result_file=None):
    for i, instance_file in tqdm(enumerate(instance_files), leave=False, unit=" files", desc="Processing instances"):
        
        instance_name = instance_file.split(".")[0]
        path = "instances/" + instance_file
        inst = instance.readInstance(path)
        for alpha in alphas:
            # print(Fore.BLUE + "-"*30)
            # print(Fore.MAGENTA + f"Instance: {instance_name}, Alpha: {alpha}")

            # Execute the instance
            sol, time_taken = grasp.execute(inst, iterations, alpha, max_time)

            # print(Fore.CYAN + f"Time taken: {time_taken} seconds")
            # print(Fore.YELLOW + "\nBEST SOLUTION:")
            # solution.printSolution(sol)
            # print(Fore.BLUE + "-"*30 + "\n")

            if result_file is not None:
                writeResult(result_file, instance_name, alpha, sol["of"], time_taken)

def main():
    random.seed(1)
    
    if not os.path.exists("results/"):
        os.makedirs("results/")

    alphas = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, -1]
    max_time = 5
    iterations = 0x3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f
    time_start = time.time()
    time_start_str = time.strftime('%Y%m%d_%H%M%S')
    result_file = f"results/{time_start_str}-max_time-{int(max_time)}.csv"

    instance_files = [f for f in os.listdir("instances") if f.endswith(".txt")]
    executeInstances(instance_files, iterations=iterations, alphas=alphas, max_time=max_time, result_file=result_file)
    best_count, avg_dev = analyzeResults(result_file)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5)) # 1 fila, 2 columnas, tamaño de la figura
    ax1.bar(best_count.index.astype(str), best_count.values, color='blue')
    ax2.bar(avg_dev.index.astype(str), avg_dev.values, color='orange')

    ax1.set_title('Number of times alpha was the best')
    ax2.set_title('Average deviation from the best solution')
    ax2.set_xlabel('Alpha')
    ax1.grid(axis='y', linestyle='--')
    ax2.grid(axis='y', linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f'results/analyzed/{time_start_str}-max_time-{int(max_time)}-alphas.png')
    # plt.show()
    writeExcel(best_count, avg_dev, time_start_str, max_time)

    # print("\n" + Fore.GREEN + "Done!")
    # print(Fore.CYAN + "Total time taken: {:.2f} minutes".format((time.time() - time_start) / 60))

if __name__ == '__main__':
    main()