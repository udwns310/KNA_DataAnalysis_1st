# 실습 - 고장 사례의 P-F 배치
# 목표: Case별 사례 4건의 P점·F점을 정의하고 P-F 간격으로 대응 가능성 판정(리드타임 20일 기준)
# CASE A: 회전기계 4건(모터·팬·압축기·감속기) / CASE B: 유틸리티·반송 4건(유압·가열로·컨베이어·롤러)
#
# * 이 실습 데이터는 study/failure_progression.py의 "P-F 곡선" 개념을 숫자로 재현한 예시용
#   데이터이며, 실제 설비의 고장 이력이 아님
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

LEAD_TIME_DAYS = 20

# =====================================================================
# CASE A - 회전기계 4건(모터·팬·압축기·감속기)
# =====================================================================

# STEP 1. P점·F점 정의 - P점은 최초 관측(잠재 고장 신호가 처음 보인 날), F점은 요구 성능 미달(일차 기준 0일=현재)
case_a = pd.DataFrame({
    "설비": ["모터", "팬", "압축기", "감속기"],
    "고장_모드": ["베어링 마모", "임펠러 불평형", "밸브 누설", "기어 피팅"],
    "관측_신호": ["진동 실효값", "진동(수평)", "토출 압력", "오일 내 금속 입자"],
    "P점_day": [-55, -12, -25, -70],  # F점(0일) 기준 며칠 전에 처음 관측됐는지
    "F점_day": [0, 0, 0, 0],
})
case_a["P_F_간격_일"] = case_a["F점_day"] - case_a["P점_day"]
print(case_a.to_string(index=False))

# STEP 2. 대응 가능성 판정 - P-F 간격과 리드타임 20일 비교
case_a["대응_가능"] = case_a["P_F_간격_일"] >= LEAD_TIME_DAYS
print(case_a[["설비", "P_F_간격_일", "대응_가능"]].to_string(index=False))
# - 모터(55일)·감속기(70일)는 리드타임 20일보다 P-F 간격이 훨씬 길어 대응 가능 - 반면 팬(12일)은
#   리드타임 20일보다 짧아 "관측은 됐지만 대응은 불가능"한 사례에 해당함

# STEP 3. 점검 주기 계산(절반 규칙) - 점검 주기 <= P-F 간격 / 2
case_a["최대_점검주기_일"] = case_a["P_F_간격_일"] / 2
print(case_a[["설비", "P_F_간격_일", "최대_점검주기_일"]].to_string(index=False))
# - 팬처럼 P-F 간격이 12일인 설비는 절반 규칙상 점검 주기가 6일 이하여야 함 - 월 1회 점검
#   주기(약 30일)로는 절대로 이 설비의 잠재 고장을 놓치지 않을 수 없다는 것이 숫자로 드러남

# 사례별 P점 시각화 - F점(0일)부터 며칠 전인지 나타내는 역방향 시간축에 겹쳐 표시
fig, ax = plt.subplots()
for _, row in case_a.iterrows():
    ax.plot([row["P점_day"], row["F점_day"]], [1, 1], marker="o")
    ax.annotate(row["설비"], (row["P점_day"], 1), textcoords="offset points", xytext=(0, 8))
ax.axvline(-LEAD_TIME_DAYS, color="red", linestyle="--", label="리드타임 20일 경계")
ax.set_xlabel("F점 기준 경과일(음수=과거)")
ax.set_yticks([])
ax.legend()
tmp_path = "data/_tmp_pf_case_a.png"
fig.savefig(tmp_path)
print(os.path.exists(tmp_path))
os.remove(tmp_path)


# =====================================================================
# CASE B - 유틸리티·반송 4건(유압·가열로·컨베이어·롤러)
# =====================================================================

# STEP 1. P점·F점 정의
case_b = pd.DataFrame({
    "설비": ["유압 유닛", "가열로", "컨베이어", "롤러"],
    "고장_모드": ["실린더 내부 누유", "버너 노즐 막힘", "벨트 편마모", "베어링 고착"],
    "관측_신호": ["압력 하강률", "연료 압력 보상량", "벨트 사행 센서", "구동 전류"],
    "P점_day": [-40, -9, -18, -30],
    "F점_day": [0, 0, 0, 0],
})
case_b["P_F_간격_일"] = case_b["F점_day"] - case_b["P점_day"]
print(case_b.to_string(index=False))

# STEP 2. 대응 가능성 판정
case_b["대응_가능"] = case_b["P_F_간격_일"] >= LEAD_TIME_DAYS
print(case_b[["설비", "P_F_간격_일", "대응_가능"]].to_string(index=False))
# - 유압 유닛(40일)·롤러(30일)는 대응 가능하지만, 가열로(9일)·컨베이어(18일)는 리드타임 20일에
#   못 미쳐 대응 불가 사례로 분류됨 - CASE A의 "팬"과 마찬가지로 P점을 관측했다고 해서 항상
#   조치까지 이어지는 것은 아님을 보여줌

# STEP 3. 점검 주기 계산
case_b["최대_점검주기_일"] = case_b["P_F_간격_일"] / 2
print(case_b[["설비", "P_F_간격_일", "최대_점검주기_일"]].to_string(index=False))

# 결과 정리표 - 두 CASE를 하나로 합쳐 P점 정의·F점 기준·대응 가능성·점검 주기를 한눈에 비교
combined = pd.concat([case_a.assign(CASE="A"), case_b.assign(CASE="B")], ignore_index=True)
summary = combined[["CASE", "설비", "고장_모드", "P_F_간격_일", "대응_가능", "최대_점검주기_일"]]
print(summary.to_string(index=False))

# 결과 해석
# - 8건 중 리드타임 20일 기준으로 "대응 불가"에 해당하는 사례는 팬(12일)·가열로(9일)·
#   컨베이어(18일) 3건 - 공통점은 모두 P-F 간격이 20일 미만이라는 점으로, "P점을 더 일찍
#   당길 수 있는 민감한 관측 수단"을 도입하거나(예: 진동 대신 초음파), 애초에 리드타임 자체를
#   줄일 수 있는 예비품 상시 보유·정지 기회 확대 같은 운영 대응이 필요함
# - "대응 가능"으로 분류된 설비들도 최대 점검 주기가 P-F 간격의 절반에 불과해, 실제 점검
#   계획을 세울 때는 이 표의 "최대_점검주기_일" 열을 그대로 상한선으로 사용해야 함
