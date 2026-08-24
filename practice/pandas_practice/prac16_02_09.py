import pandas as pd

dc = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 9. reset_index로 인덱스 정리

dc_dedup = dc.drop_duplicates()
print(dc_dedup.index.max())  # 201

dc_final = dc_dedup.reset_index(drop=True)
print(dc_final.index.min(), dc_final.index.max())  # 0 199
