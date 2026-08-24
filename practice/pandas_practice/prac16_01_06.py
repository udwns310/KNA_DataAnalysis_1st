import pandas as pd

df = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 6. describe로 격차 큰 컬럼 찾기

print(df.describe())

report = df[['실린더압력', '주조압력', '사이클타임', '비스킷두께', '형체력']].describe().T
report['격차'] = (report['mean'] - report['50%']).abs()
print(report.sort_values('격차', ascending=False)[['mean', '50%', 'max', '격차']].head(3))
