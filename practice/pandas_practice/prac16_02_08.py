import pandas as pd

dc = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 8. subset으로 특정 컬럼 기준 중복 제거

dc_dedup_subset = dc.drop_duplicates(subset=['샷'], keep='last')
print(len(dc_dedup_subset))  # 200
