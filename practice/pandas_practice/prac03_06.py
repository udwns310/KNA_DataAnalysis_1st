# 실습6. 특정구간추출종합
# 목표
# 열 선택·loc·iloc를 결합해 특정 구간을 추출하는 종합
# 단계
# · 여러 feature 열을 선택한 뒤 iloc로 앞 구간 추출
# · loc 라벨 범위로 두 열 구간 추출
# · iloc 위치 범위로 앞쪽 열 구간 추출
# 예상 결과
# (10, 5)·(11, 2)·(10, 6) 출력

import pandas as pd

df = pd.read_csv("data/13_diecasting_small.csv")

# 여러 feature 열을 선택한 뒤 iloc로 앞 구간 추출
df_sub = df[["품질등급", "형체력"]].iloc[0:10, 0:5]
print(df_sub.shape)

# loc 라벨 범위로 두 열 구간 추출
df_sub2 = df.loc[0:10, ["품질등급", "형체력"]]
print(df_sub2.shape)

# iloc 위치 범위로 앞쪽 열 구간 추출
df_sub3 = df.iloc[0:10, 0:6]
print(df_sub3.shape)
