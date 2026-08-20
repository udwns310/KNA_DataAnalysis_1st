import pandas as pd

inj_grp = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 7. 그룹별 대체

inj_grp['최대사출속도'] = inj_grp.groupby('사출기')['최대사출속도'].transform(
    lambda x: x.fillna(x.mean())
)
remaining_median = inj_grp['최대사출속도'].median()
inj_grp['최대사출속도'] = inj_grp['최대사출속도'].fillna(remaining_median)
print(inj_grp['최대사출속도'].isna().sum())  # 0
