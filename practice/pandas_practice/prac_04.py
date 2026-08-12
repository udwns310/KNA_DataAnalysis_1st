# 실습 4
import pandas as pd

df_metro = pd.read_csv(
    "data/12_metro_compressor.csv",
    encoding="utf-8",
    sep=",",
    usecols=[
        "측정시각",
        "오일온도",
        "모터전류",
        "가동상태",
    ],
)
print(df_metro.shape)
print(df_metro.head(5))
