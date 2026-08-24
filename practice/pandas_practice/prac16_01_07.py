import pandas as pd

df = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 7. 여러 컬럼의 가운데 절반 폭 비교

df_q = df[['실린더압력', '사이클타임', '비스킷두께']].quantile([0.25, 0.50, 0.75])
print(df_q)

print(df_q.loc[0.75] - df_q.loc[0.25])
# 실린더압력 49.25, 사이클타임 15.12, 비스킷두께 6.0 (Q3-Q1 = IQR)
