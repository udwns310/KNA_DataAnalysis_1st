import pandas as pd

df = pd.read_csv('data/15_02_사출성형_공정.csv', encoding='utf-8')

# 실습 4. 삭제 손실 비교

loss_table = pd.DataFrame({
    '방식': ['원본', '행삭제', 'thresh20'],
    '행': [len(df), len(df.dropna()), len(df.dropna(thresh=20))],
})
loss_table['손실률'] = ((1 - loss_table['행'] / len(df)) * 100).round(2)
print(loss_table)
