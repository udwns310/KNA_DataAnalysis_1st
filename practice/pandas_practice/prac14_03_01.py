import pandas as pd

df = pd.read_csv('data/14_hydraulic_qc.csv', encoding='utf-8')

# 실습 1. 상관계수와 상관 행렬

r1 = df['지표07'].corr(df['지표08'])
print(r1.round(3))  # -0.969

corr4 = df[['지표01', '지표02', '지표03', '지표04']].corr().round(3)
print(corr4)
# 지표01-04 칸이 -0.983으로 절댓값 최대
