import pandas as pd

df = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 9. 종합 처리

base = df.drop(columns=['최대사출속도', '감압시간'])
filled = base.fillna(base.median(numeric_only=True))
print(filled.isna().sum().sum())  # 0

filled.to_csv('data/15_02_사출성형_공정_clean.csv', index=False, encoding='utf-8')
