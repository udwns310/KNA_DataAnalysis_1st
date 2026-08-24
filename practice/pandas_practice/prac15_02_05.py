import pandas as pd

df = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 5. fillna 평균·중앙값 대체

print(df['최대사출압'].isna().sum())  # 60

mean = df['최대사출압'].mean()
median = df['최대사출압'].median()
print(round(mean, 2), round(median, 2))

df['최대사출압'] = df['최대사출압'].fillna(mean)
print(df['최대사출압'].isna().sum())  # 0

df['최대사출압'] = df['최대사출압'].fillna(median)
print(df['최대사출압'].isna().sum())  # 0
