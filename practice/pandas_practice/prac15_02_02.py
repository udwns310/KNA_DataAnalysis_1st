import pandas as pd

inj = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 2. dropna 옵션 조절

print(inj.dropna(how='all').shape)          # (250, 22)
print(inj.dropna(thresh=20).shape)          # (162, 22)
print(inj.dropna(subset=['사출압력']).shape)  # (249, 22)
