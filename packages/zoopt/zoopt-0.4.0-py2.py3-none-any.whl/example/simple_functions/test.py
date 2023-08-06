import numpy as np
from zoopt import Objective, Parameter, ExpOpt, Dimension
from simple_function import ackley, sphere


def griewank(solution):
    """
        griewank function
    """
    x = solution.get_x()
    x_len = len(x)
    seq = 0
    cos = 1
    for i in range(x_len):
        seq += (x[i] - 0.2) * (x[i] - 0.2)
        cos *= np.cos((x[i] - 0.2) / np.sqrt(i+1))
    value = seq / 4000.0 - cos + 1
    return value


def rastrigin(solution):
    """
        rastrigin function
    """
    x = solution.get_x()
    x_len = len(x)
    seq = 0
    cos = 0
    for i in range(x_len):
        seq += (x[i] - 0.2) * (x[i] - 0.2)
        cos += np.cos(2.0 * np.pi * (x[i] - 0.2))
    value = 10 * x_len + seq - 10 * cos
    return value


if __name__ == '__main__':
    dim = 100  # dimension
    objective = Objective(ackley, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    parameter = Parameter(budget=3000, sequential=False)  # init with init_samples
    print("Ackley Function")
    solution_list = ExpOpt.min(objective, parameter, repeat=10, plot=False)
    print("Sphere Function")
    objective = Objective(sphere, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    solution_list = ExpOpt.min(objective, parameter, repeat=10, plot=False)
    print("Rastrigin Function")
    objective = Objective(rastrigin, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    solution_list = ExpOpt.min(objective, parameter, repeat=10, plot=False)
    print("Griewank Function")
    objective = Objective(griewank, Dimension(dim, [[-1, 1]] * dim, [True] * dim))  # setup objective
    solution_list = ExpOpt.min(objective, parameter, repeat=10, plot=False)
