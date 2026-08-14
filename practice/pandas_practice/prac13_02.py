# 실습 2
import pandas as pd

df = pd.read_csv("data/13_diecasting_small.csv")
df.info()

# 1. 비스킷두께 시리즈 추출
# 2. 추출된 시리즈 내용들이 16 이상이면 True, 아니면 False를 담는 Boolean Series 생성
# 3. Boolean Series와 비교해서 df의 내용 중에 True와 겹치는 행들을 추출 -> df_sub
df_sub = df[df["비스킷두께"] >= 16]
df_sub.info()
print(len(df_sub))  # 결과 : 5

print(df_sub.head(3))
print(df_sub["샷"].head(3))
print(df_sub["비스킷두께"].head(3))

print(df_sub[["샷", "비스킷두께"]])
