# 실습 6
import pandas as pd

df = pd.read_csv("data/13_diecasting_shot.csv")

# · 고장 여부 조건으로 고장 설비만 먼저 거르기
# "품질등급" 컬럼 == "불량"
df_filtered = df[df["품질등급"] == "불량"]

# · 거른 결과에 sort_values를 점으로 이어 비스킷두께 내림차순 정렬
df_sorted = df_filtered.sort_values(["비스킷두께"], ascending=False)

# · head로 상위 다섯 개만 남겨 샷 확인
print(df_sorted.head(5))
