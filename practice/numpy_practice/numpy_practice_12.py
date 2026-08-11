# 실습 9
import numpy as np
import os

file_path = os.path.join("data", "10_mct_tool.csv")

data = np.loadtxt(
    file_path, encoding="utf-8", delimiter=",", skiprows=1, usecols=[4, 5]
)
print(data)
rpm = data[:, 0]
torque = data[:, 1]
anomaly = rpm[rpm < 1000]
print(anomaly)
print(anomaly.size, round(anomaly.mean(), 2))
