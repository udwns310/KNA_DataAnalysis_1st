# 실습 4
import numpy as np

rpm = np.array([1551, 1409, 1485, 1433, 1467, 2964])
torque = np.array([45.2, 44.8, 52.3, 49.5, 44.8, 6.2])
# 비교 연산으로 회전수가 2000 이상인 조건 생성
print(rpm[rpm >= 2000])  # [2964] - 회전수 과다 위험 시점 필터링

# 다중 조건으로 회전수 과다 또는 토크 과소 위험 시점 필터링
# rpm[0]의 데이터와 torque[0]의 데이터는 같은 시기의 상황을 다룸
print(
    (rpm >= 2000) | (torque < 10)
)  # [2964] - 회전수 과다 또는 토크 과소 위험 시점 필터링

high_torque = torque > 50
print(high_torque)  # [False False  True False False False] - 토크 과다 위험 시점 필터링
print(torque[torque > 50])  # [52.3] - 토크 과다 위험 시점 필터링
