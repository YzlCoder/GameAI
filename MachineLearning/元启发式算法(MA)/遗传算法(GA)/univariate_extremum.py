"""
一元函数极值求解
"""
import numpy as np

# 二进制转十进制
def bintodec(pop, chromlength, xlim):
    # 生成每个二进制位的权重（2的幂次方）
    powers_of_two = 2 ** np.arange(chromlength - 1, -1, -1)
    # 将二进制转换为十进制：将每个位乘以相应的权重并求和
    decimal_values = np.sum(pop * powers_of_two, axis=1)
    # 将十进制值映射到指定的xlim范围
    scaled_values = xlim[0] + decimal_values * (xlim[1] - xlim[0]) / (2 ** chromlength - 1)
    return scaled_values

# 计算目标函数值
def calobjvalue(decpop):
    # 目标函数
    f = lambda x: np.abs(x * np.sin(x) * np.cos(2 * x) - 2 * x * np.sin(3 * x) + 3 * x * np.sin(4 * x))
    return f(decpop)

# 计算个体适应值
# 因为这个case就是y值越高就越好，所以就返回fx
def calfitvalue(fx):
    return fx

# 赋值个体
# 参数pop:当前总群所有个体, fitvalue:当前总群所有个体的适应值
# 返回的是新总群，个体数和pop相同。但是是根据每个个体的fitvalue值来复制的，适应值越大的个体被复制多次的概率越大
def copyx(pop, fitvalue):
    newx = np.copy(pop)
    total_fit = np.sum(fitvalue)
    p = fitvalue / total_fit
    Cs = np.cumsum(p)
    R = np.sort(np.random.rand(pop.shape[0]))
    i, j = 0, 0
    while j < pop.shape[0]:
        if R[j] < Cs[i]:
            newx[j, :] = pop[i, :]
            j += 1
        else:
            i += 1
    return newx

#交叉
def crossover(pop, pc, chromlength):
    newx = np.copy(pop)
    i = 1
    while i + 1 < pop.shape[0]:
        if np.random.rand() < pc:
            r1, r2 = sorted(np.random.choice(range(chromlength), 2, replace=False))
            newx[[i, i + 1], r1:r2 + 1] = newx[[i + 1, i], r1:r2 + 1] #这里是交换
        i += 2
    return newx

#变异
def mutation(pop, pm, chromlength):
    for i in range(pop.shape[0]):
        if np.random.rand() < pm:
            r = np.random.randint(0, chromlength)
            pop[i, r] = 1 - pop[i, r]
    return pop


def GA(popsize=20, chromlength=20, pc=0.6, pm=0.1, generations=100, xlim=[0, 50]):
    # 初始化种群
    pop = np.random.randint(0, 2, size=(popsize, chromlength))
    best_fitness = np.zeros(generations)
    best_solution = np.zeros(generations)

    for gen in range(generations):
        decpop = bintodec(pop, chromlength, xlim)
        fx = calobjvalue(decpop)

        # 记录最优解
        best_fitness[gen] = np.max(fx)
        best_solution[gen] = decpop[np.argmax(fx)]

        # 赋值个体
        fitvalue = fx / np.sum(fx)
        newpop = copyx(pop, fitvalue)

        # 交叉和变异
        newpop = crossover(newpop, pc, chromlength)
        newpop = mutation(newpop, pm, chromlength)
        pop = newpop

        print(f"最优解位置：{best_solution[gen]} 对应最优解：{best_fitness[gen]}")

    ymax, max_index = np.max(best_fitness), np.argmax(best_fitness)
    print(f"最优解位置：{best_solution[max_index]} 对应最优解：{ymax}")


# 运行遗传算法
GA()