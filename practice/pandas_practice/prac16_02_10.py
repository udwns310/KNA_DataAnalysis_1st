import pandas as pd

weld = pd.read_csv('data/16_welding.csv', encoding='utf-8')
print(weld.shape)  # (162, 6)

# 실습 10. 다른 현장(용접) 데이터로 종합 실습

wc_q1 = weld['통전전류'].quantile(0.25)
wc_q3 = weld['통전전류'].quantile(0.75)
wc_iqr = wc_q3 - wc_q1
wc_lower = wc_q1 - 1.5 * wc_iqr
wc_upper = wc_q3 + 1.5 * wc_iqr
print(wc_q1, wc_q3, round(wc_iqr, 2))  # 5948.0 6054.0 106.0

wc_mask = (weld['통전전류'] < wc_lower) | (weld['통전전류'] > wc_upper)
print(wc_mask.sum(), round(wc_mask.mean() * 100, 2))  # 24 14.81

wc_clipped = weld['통전전류'].clip(lower=wc_lower, upper=wc_upper)
print(round(weld['통전전류'].mean(), 2), round(wc_clipped.mean(), 2))  # 5785.5 5990.39

weld_dup = weld.duplicated().sum()
weld_dedup = weld.drop_duplicates().reset_index(drop=True)
print(weld_dup, len(weld), len(weld_dedup))  # 3 162 159
