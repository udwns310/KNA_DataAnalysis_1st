import pandas as pd

dc = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 7. drop_duplicates로 중복 제거

dc_dedup = dc.drop_duplicates()
print(len(dc), len(dc_dedup))       # 202 200
print(dc_dedup.duplicated().sum())  # 0
