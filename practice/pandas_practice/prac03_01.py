# 실습 01
import pandas as pd

df = pd.read_csv("data/13_diecasting_small.csv")
# shape 확인
# columns 열 이름 출력 확인
# 실제 csv 파일 열어보고 shape, columns 그대로 나온건지 비교
print(df.shape)
print(df.columns)
# Index(['샷', '실린더압력', '주조압력', '사이클타임', '비스킷두께', '형체력', '품질등급'], dtype='str')
# 샷,실린더압력,주조압력,사이클타임,비스킷두께,형체력,품질등급
