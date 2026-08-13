# 실습 종합
# data/12_metro_compressor.csv
# data/12_metro_digital.csv
# data/12_metro_small.csv
import pandas as pd

df_compressor = pd.read_csv(
    "data/12_metro_compressor.csv",
    encoding="utf-8",
    sep=",",
)
df_digital = pd.read_csv(
    "data/12_metro_digital.csv",
    encoding="utf-8",
    sep=",",
)
df_small = pd.read_csv(
    "data/12_metro_small.csv",
    encoding="utf-8",
    sep=",",
)

# step 1. 불러온뒤 head·shape·columns·dtypes·info로 구조파악
print(df_compressor.head())
print(df_compressor.shape)
print(df_compressor.columns)
print(df_compressor.dtypes)
print(df_compressor.info())
print("=" * 50)
print(df_digital.head())
print(df_digital.shape)
print(df_digital.columns)
print(df_digital.dtypes)
print(df_digital.info())
print("=" * 50)
print(df_small.head())
print(df_small.shape)
print(df_small.columns)
print(df_small.dtypes)
print(df_small.info())

# step 2. describe 후 평균·표준편차·min·max로 이상신호 찾기
print("=" * 50)
print(df_compressor.describe())
print("=" * 50)
print(df_digital.describe())
print("=" * 50)
print(df_small.describe())

# 탐색결과를 하나의 리포트로 정리
# 6개 항목을 채워 리포트 완성
# 개요· 열구성· 결측· 통계· 이상신호· 종합의견
print("=== 설비 데이터 분석 리포트 ===")
# 개요
print("1. 개요")
print("- 압축기 데이터")
print("- 디지털 데이터")
print("- 소형 데이터")
# 열구성
print("2. 열구성")
print(df_compressor.columns.tolist())
print(df_digital.columns.tolist())
print(df_small.columns.tolist())
# 결측
print("3. 결측")
print("압축기 데이터:")
print(df_compressor.isnull().sum())
print("디지털 데이터:")
print(df_digital.isnull().sum())
print("소형 데이터:")
print(df_small.isnull().sum())
# 통계
print("4. 통계")
print("압축기 데이터:")
print(df_compressor.describe())
print("디지털 데이터:")
print(df_digital.describe())
print("소형 데이터:")
print(df_small.describe())
# 이상신호
print("5. 이상신호")
print("압축기 데이터:")
