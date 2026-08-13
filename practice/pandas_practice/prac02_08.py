# 실습 8 . 압축기와 디지털 신호 구조 비교
import pandas as pd

df_digital = pd.read_csv(
    "data/12_metro_digital.csv",
    encoding="utf-8",
    sep=",",
)

df_compressor = pd.read_csv(
    "data/12_metro_compressor.csv",
    encoding="utf-8",
    sep=",",
)

print(df_digital.shape)
print(df_compressor.shape)
print("=" * 50)
print(df_digital.info())
print(df_compressor.info())
print("=" * 50)
print(df_digital.describe())
print(df_compressor.describe())
print("=" * 50)
