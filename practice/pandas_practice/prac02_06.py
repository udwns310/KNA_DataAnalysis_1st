# 실습 6
import pandas as pd

df = pd.read_csv("data/12_metro_compressor.csv")
print(df.shape)  # (200, 7)
print(df.head())
print(df.tail())

df.info()
print(df.describe())

# 1 온도의 평균과 최댓값 차이를 숫자로 적었는가
# 평균 75 대 max 75.0 — 차이를 기록
#  75.000000 - 63.181910 = ?
print(df["오일온도"].max() - df["오일온도"].mean())

# 2 75%와 max 차이가 큰 열을 두 개 이상 찾았는가
# 온도와 진동— max가 멀리 튄 열 찾기
# "CSV에서 직접 해당 row를 찾아서 주석으로 붙여주세요!"
print()

# 3 모터전류처럼 고른 열과 비교해 차이를 설명
# 모터전류는 75%와 max가 가까움— 온도와의 차이 설명
