# 실습 7
import pandas as pd

df_metro = pd.read_csv(
    "data/12_metro_compressor.csv",
    encoding="utf-8",
    sep=",",
)
df_metro.info()
print(df_metro.describe())
print(df_metro["오일온도"].describe())

# 평균 min max 중앙값 문장에 넣기
mean_temp = df_metro["오일온도"].mean()
min_temp = df_metro["오일온도"].min()
max_temp = df_metro["오일온도"].max()
median_temp = df_metro["오일온도"].median()

print(
    f"이 값은 평균 {mean_temp} 정도고, 가장 낮을 때 {min_temp}, 가장 높을 때 {max_temp}, 중앙값은 {median_temp} 입니다."
)

# 표준편차를 보고 안정성 판단 (AI 활용) 출처 : 클로드 AI
print(
    "압력계 2종(압축·저장)은 표준편차 기준으로 안정적, 오일온도는 무난한 수준, 배출압력은 이상치 1건 확인 필요, 모터전류는 상태 구분 없이 통계를 내면 안정성 판단이 왜곡되므로 재분석이 필요합니다."
)
