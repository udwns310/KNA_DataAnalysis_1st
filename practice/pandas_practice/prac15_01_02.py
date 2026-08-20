import pandas as pd

df = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 2. 첫 탐색

print(df.head())
print(df.shape)  # (250, 22)
df.info()
print(df.describe())
