# 실습 3
import pandas as pd
import os

file_path = os.path.join("data", "12_metro_compressor_semicolon.csv")

df_metro1 = pd.read_csv(
    file_path,
    encoding="utf-8",
)
print(df_metro1.head(1))
print(df_metro1.shape)

df_metro2 = pd.read_csv(
    file_path,
    encoding="utf-8",
    sep=";",
)
print(df_metro2.head(1))
print(df_metro2.shape)
