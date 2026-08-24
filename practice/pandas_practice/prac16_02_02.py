import pandas as pd

dc = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

ct_q1 = dc['사이클타임'].quantile(0.25)
ct_q3 = dc['사이클타임'].quantile(0.75)
ct_iqr = ct_q3 - ct_q1
ct_lower = ct_q1 - 1.5 * ct_iqr
ct_upper = ct_q3 + 1.5 * ct_iqr

# 실습 2. 경계값 보정(clip)

ct_clipped = dc['사이클타임'].clip(lower=ct_lower, upper=ct_upper)
print(dc['사이클타임'].max(), ct_clipped.max())  # 6170.0 58.6125
print(round(ct_clipped.mean(), 2))               # 28.28
print(len(dc), ct_clipped.notna().sum())         # 202 188
