# 실습 5
import pandas as pd

df = pd.read_csv("data/13_diecasting_shot.csv")
df.info()

# · sort_values로 비스킷두께를 큰 값부터 내림차순 정렬
df_sorted = df.sort_values(["비스킷두께"], ascending=False)

# · head로 상위 다섯 개만 추출해 값 확인
print(df_sorted.head(5))

# 리스트로 출력해보려면?
print(df_sorted["비스킷두께"].head(5).tolist())

# · 여러 열을 리스트로 묶어 우선순위 다중 정렬
# 품질등급을 우선 오름차순으로 정렬하고
# 형체력을 그 다음 순서로 내림차순 정렬하기
df_multi_sorted = df.sort_values(["품질등급", "형체력"], ascending=[True, False]) 
print(df_multi_sorted.head(3))

