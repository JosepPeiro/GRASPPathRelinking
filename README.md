# GRASPPathRelinking

Project developed jointly by **[Josep Peiró Ramos](https://github.com/JosepPeiro)** and **[Olaf Meneses Albalá](https://github.com/olafmeneses)**.

In this project we compare different methods to herustically address the maximum diversity problem (MDP). This problem consists of, given a set of $N$ elements and the distances between all of them, we must select the $n$, (with $n<<<N$), that maximize the distance sums between all the selected elements.

We start from a constructive GRASP algorithm accompanied with local search originally developed by **[Jesús Sánchez Oro](https://github.com/jesussanchezoro)**, which we have used as a reference and on which we have implemented several versions of Path Relinking to compare its performance.

We have taken multiple parameters into account when designing the Path Relinking variants. First, we focused on generating solutions and building paths between them and the best solutions found so far. From there, we explored different strategies, such as applying local search during the construction using GRASP and before executing Path Relinking, as well as allowing local search during the Path Relinking process itself.

To define how many constructive solutions to generate with GRASP, we considered two approaches: using a portion of the total time available, or setting a fixed number of solutions.

In addition, we include the possibility of generating pairs of non-optimal solutions, with the goal of constructing paths between them and thus extending the exploration of the solution space, even far from the previously found local optima.

A more detailed explanation of the algorithm, the implemented variants, and the results analysis can be found in the attached PDF document.


## Operating Instructions

The input data, as it appears in the files in the _instances_ folder, should first be the number of items and the size of the selection set in the first row. Then the distance between each pair of objects should be specified in three columns, so that the first two columns identify the subjects and the third column is the distance between them. The result should resemble filling a lower triangular matrix, where the main diagonal is also empty. In this algorithm Euclidean and therefore symmetric distances are assumed, i.e., there is the same distance from $a$ to $b$ as from $b$ to $a$.

To use the algorithm in a simple way, the path to the data must be specified for the instance.readInstance function, and the ExecutePathRelinking function must be executed.

This function has these parameters:
- alpha: The parameter for the GRASP construction as generally used.
- iters: maximum number of iterations between GRASP and Path Relinking (and Local Search), ideally keep this value as high as possible to allow it to converge.
- max_time: time limit (in seconds) for the algorithm to find the best possible solution, works in a complementary way to iters.
- nsols: Number of solutions initially created in the GRASP construct that will later be used in Path Relinking (integer number).
- prop_time_grasp: Complementary parameter to nsols in which the number of solutions is limited to a portion of the total time set in max_time (must be between 0 and 1).
- local_search_before: If local search is applied to the solutions of the construct before path relinking.
- local_search_after: If local seach is applied to the good solutions found during path relinking.
- random_pairs: Random pairs to perform path relinking away from the maximum found.
