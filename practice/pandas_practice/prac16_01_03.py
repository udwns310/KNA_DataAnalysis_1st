import pandas as pd

df = pd.read_csv('data/16_diecasting.csv', encoding='utf-8')

# 실습 3. 정렬해서 이상치 후보 찾기

s_sorted = df.sort_values('사이클타임', ascending=False)
print(s_sorted.head())  # 6170.0, 652.3 발견
# 맨 위 6170초는 준비 샷(이상 1), 정상 사이클은 20~35초 부근
