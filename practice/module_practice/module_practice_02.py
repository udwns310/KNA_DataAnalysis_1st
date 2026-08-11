# =====================================================================
# [기본문제] 실습 2. 표준 라이브러리로 센서값 만들기
# =====================================================================
import random
import math

sensor_value = random.randint(1, 100)
print(sensor_value)  # 매번 다른 무작위 값

sensor_sqrt = math.sqrt(sensor_value)
print(sensor_sqrt)  # 그 값의 제곱근 (매번 다름)
