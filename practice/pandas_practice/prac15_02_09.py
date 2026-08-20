import os
import pandas as pd

inj = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')
inj_grp = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 9. 종합 처리

ratio = inj.isna().sum() / len(inj) * 100
over_40 = ratio[ratio > 40].index.tolist()

final_inj = inj.drop(columns=over_40)
for col in final_inj.columns:
    if final_inj[col].isna().sum() > 0 and pd.api.types.is_numeric_dtype(final_inj[col]):
        final_inj[col] = final_inj[col].fillna(final_inj[col].median())
print(final_inj.shape, final_inj.isna().sum().sum())

final_grp = inj_grp.copy()
for col in final_grp.columns:
    if final_grp[col].isna().sum() > 0 and pd.api.types.is_numeric_dtype(final_grp[col]):
        final_grp[col] = final_grp.groupby('사출기')[col].transform(lambda x: x.fillna(x.mean()))
        final_grp[col] = final_grp[col].fillna(final_grp[col].median())
print(final_grp.shape, final_grp.isna().sum().sum())

final_path = 'data/15_injection_processed_temp.csv'
final_inj.to_csv(final_path, index=False, encoding='utf-8-sig')
print(os.path.exists(final_path))
os.remove(final_path)
