import pandas as pd

df = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 7. 그룹별 대체

print(df.groupby('사출기')['감압시간'].mean())

df['감압시간'] = df.groupby('사출기')['감압시간'].transform(
    lambda s: s.fillna(s.mean())
)
print(df['감압시간'].isna().sum())  # 0

num_cols = df.select_dtypes('number')
df[num_cols.columns] = num_cols.fillna(num_cols.median())
print(df.isna().sum().sum())  # 0
