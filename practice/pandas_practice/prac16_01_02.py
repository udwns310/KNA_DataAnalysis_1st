import pandas as pd

df = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')
print(df.head(3))

# 실습 2. 한 컬럼의 최소·최대·범위

print(df['실린더압력'].min())  # 108.0
print(df['실린더압력'].max())  # 265.0

range_ = df['실린더압력'].max() - df['실린더압력'].min()
print(range_)  # 157.0
