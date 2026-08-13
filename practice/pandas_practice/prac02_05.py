# 실습 5
import pandas as pd

df_metro = pd.read_csv(
    "data/12_metro_digital.csv",
    encoding="utf-8",
    sep=",",
)
print(df_metro.info())