"""
在一个有限的数字集合中找到一组数字，使其和尽可能接近该集合所有元素和的十分之一
"""

import numpy as np


# 随机选择100个解，每个解都是从数组中随机选择10个数
def generate_population(nums_set, size):
    return np.array([np.random.choice(nums_set, 10, replace=False) for _ in range(size)])


def evaluate_fitness(solutions, target):
    errors = np.abs(target - np.sum(solutions, axis=1))
    return np.where(errors == 0, float('inf'), 1 / errors)


def genetic_algorithm(nums_set, iterations=10000, population_size=1000, mutation_rate=0.1):
    target = np.sum(nums_set) / 10
    population = generate_population(nums_set, population_size)
    for _ in range(iterations):
        fitness = evaluate_fitness(population, target)
        fitness_probs = fitness / fitness.sum()

        ## 随机选择一半作为子代，根据适应度作为概率，适应度越高概率越高
        parents_indices = np.random.choice(population_size, size=population_size // 2, p=fitness_probs)
        parents = population[parents_indices]

        ## 交叉得到另外一半的子代
        crossover_points = np.random.randint(0, 7, size=(population_size // 2, 1))
        children = []
        for i in range(0, len(parents), 2):
            p1, p2 = parents[i], parents[i + 1]
            cp = crossover_points[i // 2][0]
            # 交换三个元素
            child1 = np.concatenate([p1[:cp], p2[cp:cp + 3], p1[cp + 3:]])
            child2 = np.concatenate([p2[:cp], p1[cp:cp + 3], p2[cp + 3:]])
            children.append(child1)
            children.append(child2)

        children = np.array(children)

        # 变异
        for child in children:
            if np.random.rand() < mutation_rate:
                mutation_index = np.random.randint(10)
                child[mutation_index] = np.random.choice(nums_set)

        ## 合并两个部分的子代,成为新的种群(总数是一致的)
        population = np.vstack((parents, children))

        best_idx = np.argmax(evaluate_fitness(population, target))
        return population[best_idx]


# 0~1000 选50个数作为基础数组
numbers_set = np.random.choice(range(1000), 50, replace=False)
best_solution = genetic_algorithm(numbers_set)

# Output results
print("Target Sum:", np.sum(numbers_set) / 10)

print("Best Solution:", best_solution)
print("Solution Sum:", np.sum(best_solution))
