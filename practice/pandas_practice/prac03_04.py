# 실습 4
# loc과 iloc으로 행 선택하기
# 라벨 기준 loc과 번호 기반 iloc으로 행 선택, 범위 차이 확인
import pandas as pd

df = pd.read_csv("data/13_diecasting_small.csv")

# loc으로 라벨 기준 단일 행 선택
print(df.loc[0, "품질등급"])

# iloc으로 번호 기반 단일 행 선택
print(df.iloc[0]["품질등급"])

# 범위 선택으로 loc 끝 포함, iloc 끝 제외 차이 확인
print(len(df.loc[0:2]))
print(len(df.iloc[0:2]))
