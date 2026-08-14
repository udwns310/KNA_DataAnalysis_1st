# 실습 1
import pandas as pd

df = pd.read_csv("data/13_diecasting_small.csv")
df.info()

# · 비교 연산자로 실린더압력 기준의 조건식을 만들어 Boolean Series 생성
s = df["실린더압력"]
s.info()
s_boolean = s >= 230
s_boolean.info()  # dtypes: bool(1) -> Boolean Serise 확인

# · sum으로 조건을 만족하는 행 개수 확인
print(s_boolean.sum())  # True = 1, False = 0 -> 합계로 True 갯수 파악
# 결과 : 5

# · 만든 조건을 데이터프레임 대괄호에 넣어 행 추출 -> 행의 갯수 출력
# 전체 df를 대상으로 앞서 특정 컬럼에 대한 불리언 시리즈를
# 컬럼 요구하는 [] 사이에 넣어주면,
# 각 줄마다 비교를 해서 T인 경우만 추려 새로운 DF를 만든다.
df_sub = df[df["실린더압력"] >= 230]
df_sub.info()
# df의 행의 갯수를 확인할 땐 len() 사용도 가능
print(len(df_sub))
# 결과 : 5
