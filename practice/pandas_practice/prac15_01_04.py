import pandas as pd

df = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 4. 컬럼별 결측 개수와 비율

counts = df.isna().sum()
print(counts)

ratio = (counts / len(df) * 100).round(1)
print(ratio)

table = pd.DataFrame({'개수': counts, '비율': ratio})
print(table[table['개수'] > 0])
