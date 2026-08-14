# 실습 3
import pandas as pd

df = pd.read_csv("data/13_diecasting_small.csv")
df.info()

# · 비스킷두께 조건과 사이클타임 조건을 각각 괄호로 감싸기

# · 두 조건을 그리고 기호 & 로 묶어 모두 만족하는 행 추출
df_sub1 = df[(df["비스킷두께"] >= 13)]
print(len(df_sub1))  # 결과 : 6

df_sub2 = df[(df["사이클타임"] >= 25)]
print(len(df_sub2))  # 결과 : 6

df_and = df[(df["비스킷두께"] >= 13) & (df["사이클타임"] >= 25)]
print(len(df_and))  # 결과 : 5

# · 같은 두 조건을 또는 기호 | 로 묶어 결과 수 비교
df_or = df[(df["비스킷두께"] >= 13) | (df["사이클타임"] >= 25)]
print(len(df_or))  # 결과 : 7
