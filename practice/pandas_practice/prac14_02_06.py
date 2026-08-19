import pandas as pd

df = pd.read_csv('data/14_hydraulic.csv', encoding='utf-8')

# 실습 - 종합 산출물
# 한 페이지 분량의 통계 요약을 네 항목으로 작성

# 전체 온도의 평균·표준편차로 기준선 파악
overall = df['온도'].agg(['mean', 'std']).round(3)

# 냉각기상태(라인 대신)별 평균·표준편차 비교
line_stat = df.groupby('냉각기상태').agg(
    평균=('온도', 'mean'),
    표준편차=('온도', 'std'),
).round(3)

# 밸브상태(설비 대신) 진단표를 온도편차 순으로 정렬해 가장 불안정한 그룹 확인
diagnosis = df.groupby('밸브상태').agg(
    측정수=('온도', 'count'),
    평균온도=('온도', 'mean'),
    온도편차=('온도', 'std'),
    평균진동=('진동', 'mean'),
    평균압력=('압력', 'mean'),
).round(3).sort_values('온도편차', ascending=False)

print(overall)
print(line_stat)
print(diagnosis)

worst_line = line_stat['표준편차'].idxmax()
worst_valve = diagnosis.index[0]

# 01 · 전반 상태 - 전체 통계로 본 데이터 상태 1문장
print(f"[전반 상태] 전체 온도는 평균 {overall['mean']}도, 표준편차 {overall['std']}도로, "
      f"평균만 보면 상온 범위처럼 보이지만 흩어짐이 커서 냉각기상태·밸브상태별로 나눠 봐야 진짜 상태가 드러남")

# 02 · 핵심 차이 - 그룹 비교에서 발견한 차이 1가지
print(f"[핵심 차이] 냉각기상태별로 보면 {worst_line}이(가) 평균 {line_stat.loc[worst_line, '평균']}도, "
      f"표준편차 {line_stat.loc[worst_line, '표준편차']}로 평균도 가장 높고 흩어짐도 가장 커서 가장 불안정함")

# 03 · 주의 그룹 - 평균-편차로 본 주의 그룹과 근거
print(f"[주의 그룹] 밸브상태 진단표에서 {worst_valve}이(가) 온도편차 {diagnosis.loc[worst_valve, '온도편차']}로 "
      f"가장 커서, 평균 온도는 두드러지지 않지만 들쭉날쭉함이 커 가장 먼저 점검해야 할 상태로 판단됨")

# 04 · 추가 분석 - 더 살펴봐야 할 항목 1가지
print(f"[추가 분석] {worst_valve} 밸브상태가 냉각기상태·운전부하와 겹쳐 나타나는지, "
      f"두 기준을 함께 묶어(groupby) 살펴봐야 진짜 원인을 좁힐 수 있음")
