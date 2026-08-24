import pandas as pd

dc = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 6. keep 옵션으로 기준 바꾸기

first_dup = dc.duplicated(keep='first').sum()
last_dup = dc.duplicated(keep='last').sum()
all_dup = dc.duplicated(keep=False).sum()
print(first_dup, last_dup, all_dup)  # 2 2 4
