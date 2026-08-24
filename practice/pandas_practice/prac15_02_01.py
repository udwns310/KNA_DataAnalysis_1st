import pandas as pd

df = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 1. dropna로 행·열 삭제

print(df.shape)                 # (250, 22)
print(df.dropna().shape)        # (76, 22)
print(df.dropna(axis=1).shape)  # (250, 10)
