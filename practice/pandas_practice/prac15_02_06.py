import pandas as pd

df = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 6. 최빈값·앞뒤 값 대체

print(df['사출기'].isna().sum())  # 0
print(df['사출기'].mode()[0])     # 1호기
df['사출기'] = df['사출기'].fillna(df['사출기'].mode()[0])
print(df['사출기'].isna().sum())  # 0

df = df.sort_values('측정시각')
print(df['전환압력'].isna().sum())  # 68
df['전환압력'] = df['전환압력'].ffill().bfill()
print(df['전환압력'].isna().sum())  # 0
