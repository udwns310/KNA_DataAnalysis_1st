import pandas as pd

inj = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 4. 삭제 손실 비교

n_original = len(inj)
n_any = len(inj.dropna())
n_thresh = len(inj.dropna(thresh=20))

loss_table = pd.DataFrame({
    '방식': ['원본', 'dropna()', 'dropna(thresh=20)'],
    '남는 행 수': [n_original, n_any, n_thresh],
})
loss_table['손실률(%)'] = ((n_original - loss_table['남는 행 수']) / n_original * 100).round(1)
print(loss_table)
