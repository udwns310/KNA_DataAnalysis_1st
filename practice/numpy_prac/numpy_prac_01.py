# 미국식 속도(Miles)를 우리가 쓰는 속도(km)로 변환시켜주는
# NumPy 배열 예제 코드

import numpy as np

miles = np.array([94, 104, 105])

# km/h = miles * 1.60934
print(type(miles[0]))
print(miles * 1.60934)  # [152.451298 168.14503  169.79857 ]
print(type(miles[0] * 1.60934))  # <class 'numpy.float64'>
