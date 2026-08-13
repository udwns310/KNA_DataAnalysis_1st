# 실습 2
import pandas as pd

df_metro = pd.read_csv(
    "data/12_metro_compressor.csv",
    encoding="utf-8",
)

print(df_metro.head(1))
print(df_metro.head(10))
print(df_metro.tail(7))
print(df_metro.head(500))

