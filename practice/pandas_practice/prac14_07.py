# 실습 7
import pandas as pd

df = pd.read_csv('data/14_hydraulic.csv', encoding='utf-8')

# value_counts로 냉각기상태 구성 파악
print(df['냉각기상태'].value_counts())

# value_counts로 result(검사결과) 정상·고장 비율 파악 - 소숫점이하 3자리
print(df['result'].value_counts(normalize=True).round(3))

# 고장 행만 걸러 냉각기상태별 고장 건수 집계
fail_df = df[df['result'] == '고장']
print(fail_df.groupby('냉각기상태').size())

# groupby로 냉각기상태별 온도·진동 평균까지 비교 - 소숫점이하 2자리
print(df.groupby('냉각기상태')[['온도', '진동']].mean().round(2))
