import pandas as pd

df = pd.read_csv('data/15_사출성형_로그.csv', encoding='utf-8')
print(df.describe())

# 실습 1. 눈으로 결측 찾기

print(df.isna().sum())  # 사출기1 배럴온도2 사출압력1 스크루속도1

print((df['사출압력'] == 0).sum())      # 2
print((df['스크루속도'] == -999).sum())  # 2
