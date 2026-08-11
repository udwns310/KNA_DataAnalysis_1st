# 실습 1
import numpy as np

rotation_readings = np.array([1200, 1250, 1180, 1050, 1220, 1195, 1210])
print(rotation_readings[0])  # 1200 - 첫 시점
print(rotation_readings[-1])  # 1210 - 마지막 시점
print(rotation_readings[:3])  # [1200 1250 1180] - 앞 구간
print(rotation_readings[::2])  # [1200 1180 1220 1210] - 두 칸 간격
