import pandas as pd

inj = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 1. dropna로 행·열 삭제

print(inj.shape)                 # (250, 22)
print(inj.dropna().shape)        # (76, 22)
print(inj.dropna(axis=1).shape)  # (250, 10)
