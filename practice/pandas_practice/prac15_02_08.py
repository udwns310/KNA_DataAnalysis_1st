import pandas as pd

df = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 8. 제거 vs 대체 비교

base = df.drop(columns=['최대사출속도', '감압시간'])
print(base.shape)  # (250, 20)

removed = base.dropna()
print(removed.shape)  # (110, 20)

filled = base.fillna(base.median(numeric_only=True))
print(filled.shape, filled.isna().sum().sum())  # (250, 20) 0
