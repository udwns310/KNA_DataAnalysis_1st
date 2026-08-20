import pandas as pd

df = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 5. 결측 순위와 행별 분석

ratio = (df.isna().sum() / len(df) * 100).round(1)
print(ratio.sort_values(ascending=False).head(3))

row_na = df.isna().sum(axis=1)
print(f"결측없는 행 {(row_na == 0).sum()}개")
print(f"결측있는 행 {(row_na > 0).sum()}개")
print(f"결측 5개 이상인 행 {(row_na >= 5).sum()}개")
