"""
蚁群算法解决TSP问题
"""
import numpy as np

# 四个城市间的距离矩阵，自己到自己的距离标为无穷大
distances = np.array([[np.inf, 2, 9, 10],
                      [1, np.inf, 6, 4],
                      [15, 7, np.inf, 8],
                      [6, 3, 12, np.inf]])
# 蚁群算法中蚂蚁的数量
ants = 20
# 每一代中用于更新信息素的路径数，表现最好的2条路径
best = 2
# 算法的迭代次数
iterations = 10
# 信息素的挥发率，每次迭代之后信息素会衰减为原来的0.95倍
decay = 0.95
# 信息素重要程度的参数，决定了信息素在蚂蚁决策中的权重
alpha = 1
# 启发式因子的参数，决定了启发信息（例如城市间的相对距离）在蚂蚁决策中的权重
beta = 2
# 信息素矩阵的初始状态，开始时每条路径上的信息素浓度设为相同的值
pheromone = np.ones(distances.shape) / len(distances)
# 所有城市的索引列表，用于蚂蚁选择路径时迭代
all_inds = list(range(len(distances)))

def gen_path_dist(path):
    total_dist = 0
    for ele in path:
        total_dist += distances[ele]
    return total_dist

def gen_all_paths():
    all_paths = []
    for i in range(ants):
        path = gen_path(0)
        all_paths.append((path, gen_path_dist(path)))
    return all_paths

def gen_path(start):
    path = []
    visited = set()
    visited.add(start)
    prev = start
    for i in range(len(distances) - 1):
        move = pick_move(pheromone[prev], distances[prev], visited)
        path.append((prev, move))
        prev = move
        visited.add(move)
    path.append((prev, start))  # going back to where we started
    return path

def pick_move(phero, dist, visited):
    phero = np.copy(phero)
    phero[list(visited)] = 0
    row = phero ** alpha * ((1.0 / dist) ** beta)
    norm_row = row / row.sum()
    move = np_choice(all_inds, norm_row)
    return move

def np_choice(a, p):
    r = np.random.rand()
    cumsum = np.cumsum(p)
    return a[np.where(r < cumsum)[0][0]]

def spread_pheronome(all_paths, n_best):
    sorted_paths = sorted(all_paths, key=lambda x: x[1])
    for path, dist in sorted_paths[:n_best]:
        for move in path:
            pheromone[move] += 1.0 / distances[move]
M
def ACA():
    global pheromone
    all_time_shortest_path = ("placeholder", np.inf)
    for i in range(iterations):
        all_paths = gen_all_paths()
        spread_pheronome(all_paths, best)
        shortest_path = min(all_paths, key=lambda x: x[1])
        if shortest_path[1] < all_time_shortest_path[1]:
            all_time_shortest_path = shortest_path
        pheromone *= decay
    return all_time_shortest_path

best_path = ACA()
print("Shortest path: {}".format(best_path))