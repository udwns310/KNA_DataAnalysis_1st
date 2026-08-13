# 실습 1
import pandas as pd

df_metro = pd.read_csv(
    "data/12_metro_digital.csv",
    encoding="utf-8",
)

print(df_metro.shape)
print(df_metro.head())
print(df_metro.tail())
print(df_metro.head(10))
print(df_metro.tail(10))