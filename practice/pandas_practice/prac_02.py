# 실습 2 - 설비 센서 csv 불러오기
import pandas as pd
import os

file_path = os.path.join("data", "12_metro_compressor.csv")

df = pd.read_csv(
    file_path,
    encoding="utf-8",
    sep=",",
)
print(df.head(4))
print(df.shape)