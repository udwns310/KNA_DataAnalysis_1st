import pandas as pd

inj = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 3. 결측 비율 기준 컬럼 제거

ratio = inj.isna().sum() / len(inj) * 100
over_40 = ratio[ratio > 40].index.tolist()
print(over_40)  # ['계량종료점', '감압시간']

trimmed = inj.drop(columns=over_40)
print(trimmed.shape)  # (250, 20)
