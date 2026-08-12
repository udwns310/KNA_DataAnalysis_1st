import pandas as pd
import os

file_path = os.path.join("data", "12    _metro_small.csv")

try:
    df = pd.read_csv(
        file_path,
        encoding="utf-8",
        sep=",",
        index_col="측정시각",
        nrows=5,
        usecols=["측정시각", "가동상태"],
    )
    print(df.shape)

    print(df.head(1))
except FileNotFoundError as e:
    print(f"에러 발생: {file_path}가 존재하지 않습니다. {e}")
