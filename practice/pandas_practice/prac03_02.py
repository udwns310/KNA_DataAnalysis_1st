# 실습 2
import pandas as pd

# data/13.diecasting_small.csv 파일 읽기
df = pd.read_csv("data/13_diecasting_small.csv")
# 대괄호 한 겹으로 단일 열을 series로 선택
# 형체력 컬럼 하나만 선택하기
df_small = df["형체력"]

# 대괄호 두 겹으로 복수 열을 dataframe으로 선택
# 형체력, 실린더압력 두 개를 선택하기
print(df[["형체력", "실린더압력"]])

# 선택한 열에 mean으로 평균 계산
# df.["형체력"].mean() -> round로 소수점 이하 1자리까지만 나오게 조정하기
print(f"형체력 평균 : {df_small.mean():.1f}")
