# 실습 4
import pandas as pd

df = pd.read_csv("data/13_diecasting_shot.csv")
df.info()

# · 물결 기호로 고장이 아닌 설비만 뒤집어 추출
print(df[df["품질등급"] == "불량"].head())

print(df[~(df["품질등급"] == "불량")].head())  # 조건이 여러개로 복잡해지면 ~ 이 좋음
print(len(df[~(df["품질등급"] == "불량")]))

print(df[(df["품질등급"] != "불량")].head())  # 조건이 단일이라면 != 이 좋음

# · isin으로 품질등급이 특정 목록에 속하는 행 추출 - 품질등급 : 양품 또는 주의
print(df[df["품질등급"].isin(["양품", "주의"])].head())
print(len(df[df["품질등급"].isin(["양품", "주의"])]))

# · between으로 실린더압력가 지정 범위에 든 행 추출 - 210 ~ 230
print(df[df["실린더압력"].between(210, 230)].head())
print(len(df[df["실린더압력"].between(210, 230)]))

# 그 외의 것들이 200 - 89 = 111개 나오는지 확인하기
print(len(df[~(df["실린더압력"].between(210, 230))]))  # 111개

print()