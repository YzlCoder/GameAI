'''
求解函数f(x, y) = 100 * (0.5 + (sin(√(x² + y²))^2 - 0.5) / (1.0 + 0.001 * (x² + y²))^2) 当x,y在[-1000, 1000]范围内的最小值
'''
import numpy as np

def fitness(v):
    return 100 * (0.5 + (np.sin(np.sqrt(v[0] ** 2 + v[1] * v[1]))**2 - 0.5)
                  / (1.0 + 0.001 * (v[0] ** 2 + v[1] * v[1]))**2)

## 初始化数据
def initialize_solution(dimensions, limit):
    return np.random.rand(dimensions) * (limit[1] - limit[0]) + limit[0]

def perturb_solution(v):
    return v + np.random.uniform(-5, 5, 2)

def SA(cur_tem = 100, tem_k = 0.95, iteration = 1000, end_tem = 0.5, kv = 0.995, dimensions = 2, limit = [-100, 100], fk = 5):
    cur_solution = initialize_solution(dimensions, limit)
    cur_fitness = fitness(cur_solution)
    print("初始化解: %s, %f" % (cur_solution, cur_fitness))
    while cur_tem > end_tem:
        for i in range(iteration):
            new_solution = perturb_solution(cur_solution)
            if not np.all((limit[0] <= new_solution) & (new_solution <= limit[1])):
                continue;
            new_fitness = fitness(new_solution)
            if new_fitness < cur_fitness or \
                np.exp(-fk * (new_fitness - cur_fitness) / (tem_k * cur_tem)) >= np.random.random():
                cur_solution = new_solution
                cur_fitness = new_fitness
        tem_k = kv * tem_k
        cur_tem = tem_k * cur_tem
        print("{:<15.3f}{:<15.3f}{:<15.3f}{:<15.3f}".format(
            cur_solution[0], cur_solution[1], cur_fitness, cur_tem
        ))

SA()
