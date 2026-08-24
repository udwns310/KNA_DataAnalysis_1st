import pandas as pd

dc = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

ct_q1 = dc['사이클타임'].quantile(0.25)
ct_q3 = dc['사이클타임'].quantile(0.75)
ct_iqr = ct_q3 - ct_q1
ct_lower = ct_q1 - 1.5 * ct_iqr
ct_upper = ct_q3 + 1.5 * ct_iqr

# 실습 1. 이상치 제거

before_mean = round(dc['사이클타임'].mean(), 2)

ct_valid = dc.dropna(subset=['사이클타임'])
ct_mask_valid = (ct_valid['사이클타임'] < ct_lower) | (ct_valid['사이클타임'] > ct_upper)
ct_removed = ct_valid[~ct_mask_valid]

removed_mean = round(ct_removed['사이클타임'].mean(), 2)
print(before_mean, removed_mean)  # 64.75 27.28
print(ct_removed.shape)  # (182, 7)
