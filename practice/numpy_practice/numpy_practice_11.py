# 실습 8 - 필터링과 통계 결합하기
# 조건으로 값을 골라낸 뒤 그 값들의 통게 계산

# 토크 배열 준비 - 불리언 인덱싱으로 기준이 넘는 값만 추출 - 추출한 값들의 평균과 개수 계산
# 기준 초과 값들의 평균과 개수가 출력
import numpy as np

torque = np.array([45.2, 44.8, 52.3, 48.7, 50.1, 52.3, 58.9, 60.1, 61.2, 4.6])
high_torque = torque[torque > 50]  # 50 초과 값만 추출
print(high_torque)

print(round(high_torque.mean(), 2))  # 평균
print(high_torque.size)  # 개수

