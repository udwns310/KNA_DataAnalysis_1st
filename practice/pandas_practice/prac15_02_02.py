import pandas as pd

df = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 2. dropna 옵션 조절

print(df.dropna(how='all').shape)          # (250, 22)
print(df.dropna(thresh=20).shape)          # (162, 22)
print(df.dropna(subset=['불량여부']).shape)  # (250, 22)
