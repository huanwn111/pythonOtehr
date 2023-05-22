#!/usr/bin/python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt

#rcParams设定整体参数

plt.rcParams["font.sans-serif"]=("Microsoft yahei")
plt.rcParams['axes.unicode_minus'] = False
#print(plt.rcParams)


plt.plot([0, -1], [0, 1])      # plot a line from (0, 0) to (1, 1)
plt.title("一条线")
plt.xlabel("x value")
plt.ylabel("y value")

#现实图表
plt.show()