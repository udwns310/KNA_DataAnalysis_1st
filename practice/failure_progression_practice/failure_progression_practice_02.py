# 실습 - 돌발·점진 분류
# 목표: 사례 8건을 판정 3문항(물리 과정/시간 여유/데이터 저장)으로 분류하고 대응 방향을 도출
# CASE A: 리드타임 7일 · 예비품 상시 보유 · 잦은 정지 기회
# CASE B: 리드타임 30일 · 해외 발주 · 정기 보수 시 정지
#
# * 이 실습 데이터는 study/failure_progression.py의 "돌발·점진을 가르는 세 질문" 개념을
#   숫자로 재현한 예시용 데이터이며, 실제 설비의 고장 이력이 아님
import pandas as pd

LEAD_TIME_A = 7
LEAD_TIME_B = 30

# STEP 1. 사례 8건 정리 - 설비마다 "물리 과정 존재 여부", "P-F 간격(일)", "데이터 저장 여부"가 다름
cases = pd.DataFrame({
    "설비": ["압연 구동모터 베어링", "유압 실린더 실링", "보호 릴레이 접점", "컨베이어 벨트 텐셔너",
           "냉각팬 베어링", "비상 압력 스위치", "전기로 히터 엘리먼트", "감속기 오일 씰"],
    "물리_과정_존재": [True, True, False, True, True, False, True, True],
    "P_F_간격_일": [45, 25, None, 15, 60, None, 5, 20],
    "데이터_저장": [True, True, False, False, True, False, True, False],
})
print(cases.to_string(index=False))


def classify_case(has_physics, pf_interval, has_data, lead_time):
    """돌발·점진 판정 3문항(물리 과정 -> 시간 여유 -> 데이터 저장)을 그대로 코드화한 재사용 가능한 함수"""
    if not has_physics:
        return "물리적 돌발"
    if pf_interval < lead_time:
        return "간격 부족형"
    if not has_data:
        return "측정 부재형"
    return "예측 가능형"


action_by_class = {
    "물리적 돌발": "설계 개선·이중화",
    "간격 부족형": "운전 조건 관리·보호 장치",
    "측정 부재형": "센서 추가·저장 주기 조정",
    "예측 가능형": "예지보전 모델 개발",
}

# STEP 2. 판정 3문항을 CASE A(리드타임 7일)와 CASE B(리드타임 30일)에 각각 적용
result = cases.copy()
result["분류_CASE_A(리드타임7일)"] = [
    classify_case(hp, pf if pf is not None else -1, hd, LEAD_TIME_A)
    for hp, pf, hd in zip(cases["물리_과정_존재"], cases["P_F_간격_일"], cases["데이터_저장"])
]
result["분류_CASE_B(리드타임30일)"] = [
    classify_case(hp, pf if pf is not None else -1, hd, LEAD_TIME_B)
    for hp, pf, hd in zip(cases["물리_과정_존재"], cases["P_F_간격_일"], cases["데이터_저장"])
]
result["대응방향_CASE_A"] = result["분류_CASE_A(리드타임7일)"].map(action_by_class)
result["대응방향_CASE_B"] = result["분류_CASE_B(리드타임30일)"].map(action_by_class)
print(result[["설비", "분류_CASE_A(리드타임7일)", "분류_CASE_B(리드타임30일)"]].to_string(index=False))

# STEP 3. 리드타임에 따라 판정이 "뒤집힌" 사례 찾기
result["판정_뒤집힘"] = result["분류_CASE_A(리드타임7일)"] != result["분류_CASE_B(리드타임30일)"]
flipped = result[result["판정_뒤집힘"]][["설비", "P_F_간격_일", "분류_CASE_A(리드타임7일)", "분류_CASE_B(리드타임30일)"]]
print(flipped.to_string(index=False))
print(len(flipped))
# - 유압 실린더 실링(P-F 25일)·컨베이어 벨트 텐셔너(15일)·감속기 오일 씰(20일) 3건에서 판정이
#   뒤집힘 - 공통점은 세 사례 모두 P-F 간격이 "7일보다는 길지만 30일보다는 짧은" 구간(7~30일
#   사이)에 있다는 것 - 이 구간에 걸친 설비는 예비품을 상시 보유해 리드타임을 7일까지 줄일 수
#   있느냐 없느냐에 따라 예지보전 대상 여부 자체가 달라짐
# - 물리적 돌발(보호 릴레이 접점·비상 압력 스위치)은 리드타임과 무관하게 항상 같은 분류로
#   남고, 전기로 히터 엘리먼트(5일)는 리드타임 7일에서도 이미 부족해 CASE A·B 모두 "간격
#   부족형"으로 동일함 - 즉 판정이 뒤집히는 사례는 "P-F 간격이 두 리드타임 사이에 낀" 경우로
#   한정됨

# STEP 4. 예측 가능형 사례의 목표 경보 시점 설정 - P점과 F점(0일 기준) 사이 어딘가로 잡되,
#   진단·조달·정지·정비에 필요한 리드타임만큼은 F점 전에 여유를 둬야 함
predictable = result[result["분류_CASE_B(리드타임30일)"] == "예측 가능형"].copy()
predictable["목표_경보_day"] = -(predictable["P_F_간격_일"] - LEAD_TIME_B)  # F점(0일) 기준, 리드타임만큼 앞선 시점
print(predictable[["설비", "P_F_간격_일", "목표_경보_day"]].to_string(index=False))
# - 압연 구동모터 베어링(45일)은 F점 15일 전에만 경보를 울려도 리드타임 30일을 확보할 수 있고,
#   냉각팬 베어링(60일)은 F점 30일 전에 경보를 울려도 충분함 - "목표 경보 시점은 P점과 F점
#   사이에 위치해야 한다"는 체크포인트가 두 사례 모두에서 확인됨(45>=15, 60>=30이므로 목표
#   경보 day가 P점보다 늦고 F점보다는 이름)

# 결과 정리 - 최종 판정표(CASE B 리드타임 30일 기준)
final_table = result[["설비", "P_F_간격_일", "분류_CASE_B(리드타임30일)", "대응방향_CASE_B"]]
print(final_table.to_string(index=False))
