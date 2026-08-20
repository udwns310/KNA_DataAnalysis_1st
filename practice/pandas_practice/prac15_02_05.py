import pandas as pd

inj = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 5. fillna 평균·중앙값 대체

mean_v = inj['사출압력'].mean()
median_v = inj['사출압력'].median()
print(round(mean_v, 3), round(median_v, 3))  # 1.338 1.34

filled_by_mean = inj['사출압력'].fillna(mean_v)
filled_by_median = inj['사출압력'].fillna(median_v)
print(filled_by_mean.isna().sum(), filled_by_median.isna().sum())  # 0 0
