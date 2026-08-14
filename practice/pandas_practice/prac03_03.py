# 실습 3
import pandas as pd

# data/13.diecasting_shot.csv 파일 읽기
df = pd.read_csv("data/13_diecasting_shot.csv")

# 한 센서 열을 Series로 선택
# '형체력' 열을 선택하기
df_shot = df["형체력"]

# 여러 feature 열을 DataFrame로 선택해 형태 확인
# df[["형체력", "실린더압력", "주조압력"]].shape 출력
print(df[["형체력", "실린더압력", "주조압력"]].shape)
