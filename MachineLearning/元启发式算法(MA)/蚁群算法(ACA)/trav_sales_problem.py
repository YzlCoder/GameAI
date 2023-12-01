"""
蚁群算法解决TSP问题
"""
import numpy as np

np.random.seed(382235)

# Dummy distances matrix
distances = np.array([[np.inf, 2, 9, 10],
                      [1, np.inf, 6, 4],
                      [15, 7, np.inf, 8],
                      [6, 3, 12, np.inf]])
ants = 20
best = 2
iterations = 10
decay = 0.95
alpha = 1
beta = 2
pheromone = np.ones(distances.shape) / len(distances)
all_inds = list(range(len(distances)))


def spread_pheronome(all_paths, n_best):
    sorted_paths = sorted(all_paths, key=lambda x: x[1])
    for path, dist in sorted_paths[:n_best]:
        for move in path:
            pheromone[move] += 1.0 / distances[move]

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