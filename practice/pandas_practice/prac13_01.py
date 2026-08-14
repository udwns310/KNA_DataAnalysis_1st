# 실습 1
import pandas as pd

df = pd.read_csv("data/13_diecasting_small.csv")

df_sub = df[df["실린더압력"] >= 230]
df_sub.info()

print(len(df_sub))
