# 실습 - 회전기계 컬럼 매핑
# 목표: 목표 고장에 필요한 컬럼을 도출하고 보유 컬럼과 대조해 요청 문서를 작성
# CASE A: 1번 모터 베어링 손상 조기 경보 / CASE B: 1번 팬 분진 축적 불평형 감지
import pandas as pd

# STEP 1. 실제 회전기계 태그 목록(보유 컬럼 현황) 불러오기
tags = pd.read_csv("data/03-01_회전기계_신호_회전기계태그목록.csv")
print(tags.shape)

# CASE A. 1번 모터 베어링 손상 조기 경보
# - "충실" 수준(회전기계 컬럼 세트의 세 수준)이 요구하는 다섯 항목: 진동 3방향·가속도·
#   전압·온도·회전수 - 조기 경보와 유형 후보 판별이 목표이므로 최고 수준이 필요함
mtr_required = {"진동_수평", "진동_수직", "진동_축방향", "진동_가속도", "전압", "온도", "회전수"}

mtr_tags = tags[tags["equipment"] == "1번 모터"]
print(mtr_tags[["tag", "physical_qty", "direction"]])

mtr_have = set()
for _, row in mtr_tags.iterrows():
    if row["physical_qty"] == "진동":
        mtr_have.add("진동_" + {"수평": "수평", "수직": "수직", "축방향": "축방향"}.get(row["direction"], row["direction"]))
    else:
        mtr_have.add(row["physical_qty"])
# 가속도는 physical_qty가 "진동"이면서 indicator가 "가속도"인 태그로 별도 표시
if (mtr_tags["indicator"] == "가속도").any():
    mtr_have.add("진동_가속도")

mtr_missing = mtr_required - mtr_have
print("CASE A 보유:", sorted(mtr_have))
print("CASE A 미보유:", sorted(mtr_missing))

# CASE B. 1번 팬 분진 축적 불평형 감지
# - 대응표(대응표 핵심 항목과 적용 예시)의 "팬 분진 축적" 행 기준: 물리량=진동, 측정지표=
#   속도, 위치=구동측 수평, 주기=일 단위가 최소 요건. 다만 불평형(1배 성분)과 다른 원인을
#   구분하려면 수직 방향도 함께 있어야 함(불평형과 정렬불량의 차이 - 진동방향 기준)
fan_required = {"진동_수평", "진동_수직"}

fan_tags = tags[tags["equipment"] == "1번 팬"]
print(fan_tags[["tag", "physical_qty", "direction"]])

fan_have = set()
for _, row in fan_tags.iterrows():
    if row["physical_qty"] == "진동":
        fan_have.add("진동_" + row["direction"])

fan_missing = fan_required - fan_have
print("CASE B 보유:", sorted(fan_have))
print("CASE B 미보유:", sorted(fan_missing))

# STEP 2. 미보유 컬럼 요청서 작성
request_sheet = pd.DataFrame({
    "케이스": ["CASE A", "CASE B"],
    "목표": ["1번 모터 베어링 손상 조기 경보", "1번 팬 분진 축적 불평형 감지"],
    "미보유_컬럼": [", ".join(sorted(mtr_missing)) or "없음", ", ".join(sorted(fan_missing)) or "없음"],
    "달성가능한_감시목표": [
        "미보유 컬럼(전압) 없이도 진동 3방향·가속도·온도·회전수로 조기 경보는 가능 - 다만 전압까지 있으면 전기 계통 이상(권선)까지 구분 가능",
        "수직 방향이 없어 지금은 수평 하나로만 감시 - 불평형(수평·수직 동시 증가)과 다른 원인의 구분이 불가능하므로 수직 방향 센서 추가가 필요",
    ],
})
print(request_sheet.to_string(index=False))

# 결과 해석
# - CASE A: 1번 모터는 진동 3방향(H·V·A)·가속도(PEAK)·전류·온도·회전수까지 다 갖추고 있어
#   "충실" 수준 다섯 항목 중 전압 하나만 빠짐 - 조기 경보 자체는 지금 데이터로도 가능하고,
#   전압은 "부하 증가 또는 전기 계통 이상" 판정을 더 세밀하게 나누고 싶을 때 추가 요청할 항목
# - CASE B: 1번 팬은 진동이 수평(H) 하나뿐 - 대응표의 최소 요건(수평·속도)은 만족하지만,
#   불평형과 정렬불량의 차이 표에서 배운 대로 진동방향(수평·수직 vs 축방향)을 비교해야
#   원인을 구분할 수 있으므로, 최소 요건을 넘어 수직 방향 센서를 추가로 요청해야 함
