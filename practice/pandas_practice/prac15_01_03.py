import pandas as pd

df = pd.read_csv('data/15_사출성형_로그.csv', encoding='utf-8', na_values=[-999, 999])

# 실습 3. 위장 결측 사냥

print((df['배럴온도'] == 999.0).sum())    # 1 -> 0
print((df['스크루속도'] == -999.0).sum())  # 2 -> 0

print(df.isna().sum().sum())  # 5 -> 8
