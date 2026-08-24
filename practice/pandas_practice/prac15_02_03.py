import pandas as pd

df = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 3. 결측 비율 기준 컬럼 제거

rate = df.isna().sum() / len(df)
over_40 = rate[rate > 0.4].index.tolist()
print(over_40)  # ['최대사출속도', '감압시간']

trimmed = df.drop(columns=over_40)
print(trimmed.shape)  # (250, 20)
