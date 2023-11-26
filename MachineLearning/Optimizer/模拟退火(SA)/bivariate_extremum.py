'''
求解函数f(x, y) = 100 * (0.5 + (sin(√(x² + y²))^2 - 0.5) / (1.0 + 0.001 * (x² + y²))^2) 当x,y在[-1000, 1000]范围内的最小值
'''
import numpy as np


def fitness(v):
    return 100 * (0.5 + (np.sin(np.sqrt(v[0] * v[0] + v[1] * v[1]))**2 - 0.5) / (1.0 + 0.001 * (v[0] * v[0] + v[1] * v[1]))**2)

## 初始化数据
def initialize_population(d, limit):
    return np.random.rand(d) * (limit[1] - limit[0]) + limit[0]

def change(v):
    change_k = np.random.uniform([0.85, 1], [1, 1.15], 2)
    return v * change_k[(np.random.random(2) >= 0.5).astype(int)]

def SA(cur_tem = 100, tem_k = 0.95, iteration = 200, end_tem = 0.5, kv = 0.995, d = 2, limit = [-1000, 1000]):
    cur_pop = initialize_population(d, limit)
    cur_fitness = fitness(cur_pop)
    print("初始化解: %s, %f" % (cur_pop, cur_fitness))
    while cur_tem > end_tem:
        for i in range(iteration):
            new_pop = change(cur_pop)
            if not np.all((limit[0] <= new_pop) & (new_pop <= limit[1])):
                continue;
            new_fitness = fitness(new_pop)
            if new_fitness < cur_fitness:
                cur_pop = new_pop
                cur_fitness = new_fitness
            else:
                t = np.exp(-(new_fitness - cur_fitness) / (tem_k * cur_tem))
                if t >= np.random.random():
                    cur_pop = new_pop
                    cur_fitness = new_fitness
        tem_k = kv * tem_k
        cur_tem = tem_k * cur_tem
        print("{:<15.3f}{:<15.3f}{:<15.3f}{:<15.3f}".format(
            cur_pop[0], cur_pop[1], fitness(cur_pop), cur_tem
        ))

SA()