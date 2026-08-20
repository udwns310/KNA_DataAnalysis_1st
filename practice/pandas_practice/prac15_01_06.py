import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

inj = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 6. 결측 시각화

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

na_sorted = inj.isna().sum().sort_values(ascending=False)
na_sorted = na_sorted[na_sorted > 0]

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(na_sorted.index, na_sorted.values)
ax.set_title('컬럼별 결측 개수')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
bar_path = 'data/15_missing_bar_temp.png'
plt.savefig(bar_path)
plt.close(fig)
print(os.path.exists(bar_path))

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.imshow(inj.isna().to_numpy().T, aspect='auto', cmap='cividis')
ax2.set_yticks(range(len(inj.columns)))
ax2.set_yticklabels(inj.columns, fontsize=6)
plt.tight_layout()
heatmap_path = 'data/15_missing_heatmap_temp.png'
plt.savefig(heatmap_path)
plt.close(fig2)
print(os.path.exists(heatmap_path))

os.remove(bar_path)
os.remove(heatmap_path)
