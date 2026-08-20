import pandas as pd

df = pd.read_csv('data/14_hydraulic_qc.csv', encoding='utf-8')

# 실습 3. 그룹별 상관 비교

print(df['지표07'].corr(df['지표08']).round(3))  # -0.969

pass_df = df[df['검사결과'] == '합격']
fail_df = df[df['검사결과'] == '불합격']
print(len(pass_df), pass_df['지표07'].corr(pass_df['지표08']).round(3))  # 188 0.385
print(len(fail_df), fail_df['지표07'].corr(fail_df['지표08']).round(3))  # 12 -0.998
