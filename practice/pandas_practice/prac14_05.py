# 실습 5
import pandas as pd

df = pd.read_csv('data/14_hydraulic.csv', encoding='utf-8')

# 냉각기상태로 그룹을 나눠 진동 평균 집계 - 소숫점이하 3자리
vib_mean = df.groupby('냉각기상태')['진동'].mean().round(3)

# 집계 결과에 정렬을 이어 붙여 내림차순으로 정렬
vib_mean_sorted = vib_mean.sort_values(ascending=False)
print(vib_mean_sorted)

# 가장 진동이 큰 냉각기상태를 맨 위에서 확인
print(vib_mean_sorted.index[0])
