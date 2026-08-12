# 실습 5
import pandas as pd

try:
    df_metro = pd.read_csv(
        "data/12_metro_compressor.csv",
        encoding="utf-8",
        sep=",",
    )
except FileNotFoundError as e:
    print(e)
except UnicodeDecodeError as e:
    print(e)
except ValueError as e:
    print(e)
    