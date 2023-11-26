'''
求解函数f(x) = x*sin(x)*cos(2x) - 2*x*sin(3x) + 3*x*sin(4x) 在[0, 50]范围内的最小值
'''
import numpy as np

def f(x):
    return x * np.sin(x) * np.cos(2 * x) - 2 * x * np.sin(3 * x) + 3 * x * np.sin(4 * x)


## 初始化种群位置和速度
def initialize_population(N, d, limit):
    x = np.random.rand(N, d) * (limit[1] - limit[0]) + limit[0]
    v = np.random.rand(N, d)
    return x, v

## 更新速度
def update_velocity(v, x, xm, ym, w, c1, c2, vlimit):
    v = w * v + c1 * np.random.rand() * (xm - x) + c2 * np.random.rand() * (ym - x)
    return np.clip(v, vlimit[0], vlimit[1])

## 更新位置
def update_position(x, v, limit):
    x = x + v
    return np.clip(x, limit[0], limit[1])

## 单次迭代，更新最佳位置
def update_best_positions(N, x, fx, xm, fxm, ym, fym):
    # 更新个体最优值
    for i in range(N):
        if fx[i] < fxm[i]:
            fxm[i] = fx[i, 0]
            xm[i, :] = x[i, :]

    #更新群体最优值
    if np.min(fxm) < fym:
        fym = np.min(fxm)
        ym = xm[np.argmin(fxm), :]

    return xm, fxm, ym, fym

## 粒子群算法核心流程
def PSO(N = 20, d = 1, ger = 100, limit = [0, 50], vlimit = [-10, 10], w = 0.8, c1 = 0.5, c2 = 0.5):
    x, v = initialize_population(N, d, limit)
    xm = x.copy()
    ym = np.zeros(d)
    fxm = np.ones(N) * np.inf #因为求最小值, 所以初始化适应值为最大
    fym = np.inf

    for i in range(0, ger):
        fx = f(x)
        xm, fxm, ym, fym = update_best_positions(N, x, fx, xm, fxm, ym, fym)
        v = update_velocity(v, x, xm, ym, w, c1, c2, vlimit)
        x = update_position(x, v, limit)

    return fym, ym


print('最小值：%s, 个体值：%s' % PSO())