# 실습 3
import numpy as np

rpm = np.array([1551, 1409, 1485, 1433, 1467, 2964])
print(rpm.min())
print(rpm.max())

# 정규화 공식을 브로드캐스팅으로 적용해 변환
# 정규화 공식 - 정규화 된 X = (비교대상 - 최소값) / (최대값 - 최소값)
normalized_rpm = (rpm - rpm.min()) / (rpm.max() - rpm.min())
print(normalized_rpm)
# 소수점 이하 값이 너무 길어진다면 numpy 배열에서 제공하는 round 기능을 활용
print(np.round(normalized_rpm, 2))
