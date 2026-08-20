import pandas as pd

inj = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 8. 제거 vs 대체 비교

ratio = inj.isna().sum() / len(inj) * 100
over_40 = ratio[ratio > 40].index.tolist()
base = inj.drop(columns=over_40)

removed_version = base.dropna()
print(removed_version.shape)

filled_version = base.copy()
for col in filled_version.columns:
    if filled_version[col].isna().sum() > 0 and pd.api.types.is_numeric_dtype(filled_version[col]):
        filled_version[col] = filled_version[col].fillna(filled_version[col].median())
print(filled_version.shape)               # (250, 20)
print(filled_version.isna().sum().sum())  # 0
