import pandas as pd

dc = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 5. duplicated로 완전 중복 확인

dup_count = dc.duplicated().sum()
print(dup_count)  # 2
print(dc[dc.duplicated()][['샷', '사이클타임', '상태']])
