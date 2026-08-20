import pandas as pd

df = pd.read_csv('data/14_hydraulic_qc.csv', encoding='utf-8')

# 실습 2. 강한 상관 쌍 찾기

feat = ['지표%02d' % i for i in range(1, 11)]
cm = df[feat].corr().round(3)
print(cm)

for i in range(len(cm.columns)):
    for j in range(i + 1, len(cm.columns)):
        c = cm.iloc[i, j]
        if abs(c) > 0.4:
            print(cm.columns[i], cm.columns[j], c)
# 지표01-지표10이 0.999로 최상위
