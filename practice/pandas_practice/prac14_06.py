# 실습 6
import pandas as pd

df = pd.read_csv('data/14_hydraulic.csv', encoding='utf-8')

# groupby로 냉각기상태마다 평균 온도 - 소숫점이하 2자리
print(df.groupby('냉각기상태')['온도'].mean().round(2))


# groupby로 운전부하마다 평균 진동 - 소숫점이하 3자리
print(df.groupby('운전부하')['진동'].mean().round(3))

# 냉각기상태별로 다시 운전부하별 그룹을 나누어 평균 온도 
print(df.groupby(['냉각기상태', '운전부하'])['온도'].mean().round(2))


# 냉각기상태별로 얼마나 많은 항목이 있을까?
print(len(df[df['냉각기상태'] == '고장'])) # 40
print(df.groupby('냉각기상태').size())
