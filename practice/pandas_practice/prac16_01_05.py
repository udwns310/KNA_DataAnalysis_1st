import pandas as pd

df = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 5. quantile로 Q1·Q2·Q3

print(df['실린더압력'].quantile(0.25))  # 215.75
print(df['실린더압력'].quantile(0.50))  # 218.0
print(df['실린더압력'].median())        # 218.0
print(df['실린더압력'].quantile(0.75))  # 265.0
