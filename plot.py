# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 08:53:48 2019

@author: Dell
"""

# import necessary module
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(12, 8))
ax = Axes3D(fig)
delta = 1
V = V_DQN
# 生成代表X轴数据的列表
y = np.arange(1, 22, 1)
# 生成代表Y轴数据的列表
x = np.arange(1, 10, 1)
# 对x、y数据执行网格化
X, Y = np.meshgrid(x, y)

# 绘制3D图形
ax.plot_surface(X, Y, V.T,
    rstride=1,  # rstride（row）指定行的跨度
    cstride=1,  # cstride(column)指定列的跨度
    cmap=plt.get_cmap('rainbow'))  # 设置颜色映射
# 设置Z轴范围
upperbound = np.max(V)
lowerbound = np.min(V)

ax.set_zlim(1.1*lowerbound, 0.9*upperbound)
# 设置标题
plt.title("3D图")
plt.show()