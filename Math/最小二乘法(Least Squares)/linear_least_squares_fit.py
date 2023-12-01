"""
最小二乘法线性拟合
"""
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
# 数据
years = ['2012年', '2013年', '2014年', '2015年', '2016年', '2017年', '2018年', '2019年', '2020年', '2021年']
num = [8838.60, 10501.68, 12339.36, 14099.10, 16330.22, 18515.11, 20574.93, 22508.99, 24291.19, 26152.02]

# 将年份转换为数值（从0开始）
x = np.arange(len(years))

# 计算最小二乘法的参数
N = len(x)
sum_x = np.sum(x)
sum_y = np.sum(num)
sum_xy = np.sum(x * num)
sum_x2 = np.sum(x**2)

# 计算斜率（m）和截距（b）
m = (N * sum_xy - sum_x * sum_y) / (N * sum_x2 - sum_x**2)
b = (sum_y - m * sum_x) / N

# 基于斜率和截距计算拟合线的 y 值
y_fit = m * x + b
plt.title("私有汽车拥有量")
plt.xlabel("年份")
plt.ylabel("拥有量")

plt.scatter(x, num)
# 绘制拟合的直线
plt.plot(x, y_fit, 'r--')

# 替换x轴上的标签并旋转以方便阅读
plt.xticks(x, years, rotation=45)

plt.tight_layout()
plt.show()