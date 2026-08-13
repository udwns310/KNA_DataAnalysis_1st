# 실습 4
import pandas as pd

df_metro = pd.read_csv(
    "data/12_metro_compressor.csv",
    encoding="utf-8",
    sep=",",
)

print(df_metro.columns)
print(df_metro.columns.tolist())
print(df_metro.dtypes)