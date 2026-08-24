import pandas as pd

dc = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

ct_q1 = dc['사이클타임'].quantile(0.25)
ct_q3 = dc['사이클타임'].quantile(0.75)
ct_iqr = ct_q3 - ct_q1
ct_lower = ct_q1 - 1.5 * ct_iqr
ct_upper = ct_q3 + 1.5 * ct_iqr
ct_mask = (dc['사이클타임'] < ct_lower) | (dc['사이클타임'] > ct_upper)

# 실습 4. 처리 전후 평균·중앙값 비교표

ct_valid = dc.dropna(subset=['사이클타임'])
ct_mask_valid = (ct_valid['사이클타임'] < ct_lower) | (ct_valid['사이클타임'] > ct_upper)
ct_removed = ct_valid[~ct_mask_valid]

ct_clipped = dc['사이클타임'].clip(lower=ct_lower, upper=ct_upper)

ct_masked = dc['사이클타임'].mask(ct_mask)
ct_filled = ct_masked.fillna(ct_masked.median())

compare_table = pd.DataFrame({
    '방식': ['원본', '제거', '경계값 보정', '결측치 대체'],
    '평균': [
        round(dc['사이클타임'].mean(), 2),
        round(ct_removed['사이클타임'].mean(), 2),
        round(ct_clipped.mean(), 2),
        round(ct_filled.mean(), 2),
    ],
    '중앙값': [
        round(dc['사이클타임'].median(), 2),
        round(ct_removed['사이클타임'].median(), 2),
        round(ct_clipped.median(), 2),
        round(ct_filled.median(), 2),
    ],
})
print(compare_table)
