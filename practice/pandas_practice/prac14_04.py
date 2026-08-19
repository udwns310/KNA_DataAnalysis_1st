# 실습 4
import pandas as pd

df = pd.read_csv('data/14_hydraulic.csv', encoding='utf-8')

# 밸브상태로 그룹을 나눠 압력 열의 평균 집계 - 소숫점이하 2자리
print(df.groupby('밸브상태')['압력'].mean().round(2))


# 집계 함수를 바꿔 운전부하별 최고 온도 확인
print(df.groupby('운전부하')['온도'].max())

# size로 밸브상태별 측정 건수까지 확인
print(df.groupby('밸브상태').size())
