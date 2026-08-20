import pandas as pd

mlog = pd.read_csv('data/15_사출성형_로그.csv', encoding='utf-8')

# 실습 6. 최빈값·앞뒤 값 대체

mode_value = mlog['사출기'].mode()[0]
machine_filled = mlog['사출기'].fillna(mode_value)
print(machine_filled.isna().sum())  # 0

time_sorted = mlog.sort_values('측정시각')
temp_filled = time_sorted['배럴온도'].ffill().bfill()
print(temp_filled.isna().sum())  # 0
