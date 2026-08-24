import pandas as pd

df = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 4. 평균·중앙값으로 이상치 영향 확인

print(df['사이클타임'].mean())    # 64.75
print(df['사이클타임'].median())  # 22.6
print(df['사이클타임'].agg(['mean', 'median']))

df_ok = df[df['상태'] == 0]
print(df_ok['사이클타임'].mean().round(2))  # 27.67
