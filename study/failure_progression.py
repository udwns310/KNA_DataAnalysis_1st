# [개념] 04-01 고장의 진행 구조 - 고장을 보는 관점 / P-F 곡선 / 고장 패턴과 예지보전
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =====================================================================
# [개념] 01. 고장을 보는 관점
# =====================================================================

# [개념] 고장은 사건이 아니라 시간에 걸친 변화의 누적 - 과정으로 볼 때 비로소 "예측 구간"이 생김
#   - 사건으로 보면: 어제까지 정상 -> 오늘 갑자기 고장 (예측 구간 없음)
#   - 과정으로 보면: 열화가 서서히 진행되다가 결국 고장 (열화 진행 구간 = 예측 구간)

# [개념] 관점마다 다른 "고장" 시점 - 같은 설비를 봐도 부서마다 고장으로 판정하는 순간이 다름
perspective_table = pd.DataFrame({
    "관점": ["생산", "정비", "품질"],
    "고장_시점": ["라인 정지", "요구 기능의 규정 성능 미달", "제품 규격 이탈"],
    "주된_기록처": ["생산 일지", "정비 이력", "품질 검사"],
    "데이터_흔적": ["가동 플래그 변화", "작업 오더 발행", "측정값 규격 이탈"],
})
print(perspective_table.to_string(index=False))

# [강사님께 질문하기] 같은 설비의 같은 순간인데 생산 관점에서는 "정상"이고 정비 관점에서는 "고장"일 수 있나요?
# -> 답변: 네. 예를 들어 라인은 계속 돌고 있어도(생산 관점 정상) 진동값이 정비 기준을 넘어섰다면
#    정비 관점에서는 이미 "요구 성능 미달"로 판정될 수 있음 - 이래서 데이터 분석 전에 "어느 관점의
#    고장 정의를 쓸 것인지"를 먼저 합의해야 함

# [개념] 정상 -> 잠재 고장 -> 기능 고장의 3단계
#   정상: 요구 기능 유지 + 관측 가능한 열화 흔적 없음
#   잠재 고장: 기능은 유지되지만 변화 신호가 최초로 관측됨
#   기능 고장: 요구 성능 기준 미달
#   예지보전이 실제로 개입할 수 있는 구간 -> 잠재 고장 신호가 보이기 시작한 뒤, 기능 고장 전까지
state_table = pd.DataFrame({
    "단계": ["정상", "잠재 고장", "기능 고장"],
    "설명": ["기능 수행 · 열화 흔적 미관측", "기능 유지 · 변화 신호 관측", "요구 성능 기준 미달"],
})
print(state_table.to_string(index=False))


# =====================================================================
# [개념] 02. P-F 곡선
# =====================================================================

# [개념] P-F 곡선의 축과 형태
#   가로축: 과거 -> 미래로 흐르는 시간 / 세로축: 위쪽 건강, 아래쪽 불량
#   곡선 형태: 초기 수평 -> 완만한 하강 -> 급격한 하강
#   P점: 열화가 "검출 가능"해진 최초 시점 (설비가 아닌 관측 수단의 검출 한계로 정해짐)
#   F점: 요구 성능 기준 미달 시점 (설비가 돌아가도 성능 미달이면 F점)
#   P-F 간격 = 대응 가능 시간

# 우리 실습용 열화 시뮬레이션 - 120일간 진동 RMS(mm/s)를 재현
# * 이 시계열은 study/failure_progression.py의 "P-F 곡선" 개념을 숫자로 재현한 예시용 데이터이며,
#   실제 설비의 센서 실측값은 아님
np.random.seed(0)
days = np.arange(0, 121)
baseline = 2.0
flat_days = 40  # 이 시점까지는 열화가 관측 수단으로 잡히지 않는 "수평" 구간
elapsed_after_flat = np.maximum(days - flat_days, 0)
vib = np.where(
    days <= flat_days,
    baseline,
    baseline + 0.045 * elapsed_after_flat ** 1.15,
)
noise = np.random.normal(0, 0.08, size=vib.shape)
vib_rms = vib + noise
degradation = pd.DataFrame({"day": days, "vib_rms": vib_rms})
print(degradation.head(3))
print(degradation.tail(3))

# [개념] 검출 수단별 P점 이동 - 민감한 관측 수단일수록 P점이 앞당겨지고 P-F 간격이 길어짐
#   여기서는 서로 다른 "민감도"를 서로 다른 임계치로 흉내냄 (임계치가 낮을수록 더 민감한 수단)
sensitivity_thresholds = {"고민감(예: 초음파)": 2.3, "중민감(예: 진동 분석)": 3.0, "저민감(예: 임계치 경보)": 4.5}
f_threshold = 6.0  # 요구 성능 기준 미달로 보는 F점 임계치

detection = {}
for name, th in sensitivity_thresholds.items():
    hit = degradation.index[degradation["vib_rms"] >= th]
    detection[name] = int(hit[0]) if len(hit) else None
f_hit = degradation.index[degradation["vib_rms"] >= f_threshold]
f_day = int(f_hit[0]) if len(f_hit) else None
print(detection, f_day)

pf_intervals = {name: (f_day - p_day) for name, p_day in detection.items()}
print(pf_intervals)
# - 임계치가 낮은(민감한) 수단일수록 P점이 더 이르게 잡히고, 그만큼 P-F 간격(대응 가능 시간)도
#   길어짐 - "고민감" 수단의 P-F 간격이 "저민감" 수단보다 길게 나온 것으로 확인됨(위 출력 참고)

fig, ax = plt.subplots()
ax.plot(degradation["day"], degradation["vib_rms"], color="black", linewidth=1)
for name, p_day in detection.items():
    ax.axvline(p_day, linestyle="--", alpha=0.5)
ax.axvline(f_day, color="red", linestyle="-", label="F점(요구 성능 미달)")
ax.set_xlabel("시간(일)")
ax.set_ylabel("진동 RMS (mm/s)")
ax.set_title("검출 수단별 P점과 F점")
tmp_path = "data/_tmp_pf_curve.png"
fig.savefig(tmp_path)
print(os.path.exists(tmp_path))
os.remove(tmp_path)

# [퀴즈] 아래 세 문장 중 맞는 것을 먼저 예상해보세요.
#   ① P점은 설비 고유의 물리적 특성으로 고정된 값이다.
#   ② P점은 관측 수단(센서 종류·설치 위치·저장 주기)에 따라 달라진다.
#   ③ F점은 설비가 멈춰야만 발생한다.
# -> 정답: ②. P점은 "설비가 아닌 관측 수단의 검출 한계"로 정해짐. F점도 설비가 돌아가는 중에도
#    요구 성능 미달이면 성립하므로 ③도 틀림(F점 해석의 오해 중 하나: "멈춤과 별개")

# [개념] F점 설정에 따른 데이터셋 성격 - 목적에 맞는 F점을 선택해야 함
f_point_table = pd.DataFrame({
    "F점_설정": ["라인 정지", "성능 미달", "품질 이탈"],
    "사건_빈도": ["매우 낮음", "중간", "높음"],
    "주된_한계": ["정지 전 품질 손실 누락", "부서 간 기준선 합의", "설비 외 원인의 혼입"],
})
print(f_point_table.to_string(index=False))

# [개념] P-F 간격의 시간 예산 - 진단·조달 + 정지·정비로 구성
#   진단·조달: 이상 확인 -> 원인 진단 -> 부품 조달
#   정지·정비: 정지 기회 -> 정비 작업 -> 시운전
#   리드타임(목표 시점) = 이상 감지부터 조치 완료까지 필요한 시간 예산
#   리드타임보다 짧은 예고는 아무리 정확도가 높아도 현장 가치가 낮음

# [개념] 조기 검출 수단 vs 늦은 검출 수단
detection_lead_table = pd.DataFrame({
    "수단": ["초음파", "진동 분석", "유분 분석", "열화상", "사람의 청각·촉각"],
    "선행_기간": ["3~12개월", "2~6개월", "6~12개월", "4~6주", "수일 이내"],
    "비고": ["고주파 음향, 순회 점검", "결함 주파수·진폭, 상시 센서", "마모 입자·점도, 순회 점검",
           "전기 접촉 불량에 유효", "사실상 F점 직전"],
})
print(detection_lead_table.to_string(index=False))

# [개념] 점검 주기의 절반 규칙: 점검 주기 <= P-F 간격 / 2
#   P점 직후에 놓친 최악의 경우에도 대응 여유를 확보하기 위함 - 리드타임이 길수록 3분의 1, 4분의 1로 단축
pf_interval_days = 40  # 우리 예시 설비의 P-F 간격(일)
max_inspection_interval = pf_interval_days / 2
print(max_inspection_interval)

candidate_intervals = [15, 20, 25]
inspection_check = pd.DataFrame({
    "점검_주기(일)": candidate_intervals,
    "절반_규칙_충족": [c <= max_inspection_interval for c in candidate_intervals],
})
print(inspection_check.to_string(index=False))
# - P-F 간격이 40일이면 절반 규칙상 점검 주기는 20일 이하여야 함 - 15일·20일 주기는 규칙을
#   충족하지만 25일 주기는 규칙을 벗어나 P점 직후에 놓치면 대응 여유가 부족해질 수 있음


# =====================================================================
# [개념] 03. 고장 패턴과 예지보전
# =====================================================================

# [개념] 돌발 고장의 네 발생 경로 - 사전 열화 흔적이 없거나 부족해 예측이 어려움
sudden_failure_table = pd.DataFrame({
    "발생_경로": ["과부하", "이물 유입", "전기·전자", "인적 요인"],
    "대표_상황": ["설계 하중 초과의 순간 작용", "밸브 고착·회전부 끼임", "기판·릴레이·제어 로직 오류", "오조작·설정 오입력·조립 불량"],
    "예측_한계": ["사전 열화 흔적 부재", "정상에서 즉시 기능 상실", "외부 관측 신호 부족", "데이터 밖 원인"],
})
print(sudden_failure_table.to_string(index=False))

# [개념] 점진 열화의 세 특징: 축적성(조금씩 쌓임) · 추세성(한 방향 이동 + 변동 폭 확대) · 가속성(후반 가속)

# [개념] 돌발 vs 점진을 가르는 세 질문 -> 네 분류
#   STEP1 물리 과정: 시간에 따라 축적되는 열화 메커니즘이 있는가
#   STEP2 시간 여유: P-F 간격이 현장 리드타임보다 긴가
#   STEP3 데이터 흔적: 관련 물리량의 센서·위치·저장 주기가 확보돼 있는가
classification_table = pd.DataFrame({
    "분류": ["물리적 돌발", "간격 부족형", "측정 부재형", "예측 가능형"],
    "판정_조건": ["열화 과정 부재", "진행 시간이 리드타임보다 짧음", "열화와 시간은 있으나 데이터 부재", "세 질문 모두 통과"],
    "대응_방향": ["설계 개선·이중화", "운전 조건 관리·보호 장치", "센서 추가·저장 주기 조정", "예지보전 모델 개발"],
})
print(classification_table.to_string(index=False))

# 돌발형 vs 점진형 시계열을 우리 데이터로 직접 재현해서 비교
# * 아래 두 시계열도 마찬가지로 개념을 숫자로 재현한 예시용 데이터이며 실제 측정값은 아님
sudden_signal = np.concatenate([np.random.normal(2.0, 0.1, 89), [7.8]])  # 89일 평온 -> 90일째 급변
gradual_signal = degradation["vib_rms"].to_numpy()  # 위에서 만든 완만한 상승 시계열 재사용

sudden_std_before = round(float(np.std(sudden_signal[:-1])), 3)
sudden_jump = round(float(sudden_signal[-1] - np.mean(sudden_signal[:-1])), 3)
gradual_slope_early = round(float(gradual_signal[45] - gradual_signal[41]), 3)
gradual_slope_late = round(float(gradual_signal[119] - gradual_signal[115]), 3)
print(sudden_std_before, sudden_jump)
print(gradual_slope_early, gradual_slope_late)
# - 돌발형은 마지막 날 전까지 표준편차가 매우 작다가(사전 흔적 거의 없음) 마지막에만 큰 폭으로
#   튐 - 반면 점진형은 초반 4일 변화폭보다 후반 4일 변화폭이 더 커서(가속성) 서서히 진행되는
#   모양이 숫자로도 드러남

# [개념] 데이터에 흔적이 없는 고장 - 센서 추가로 해결되지 않는 유형들
no_trace_table = pd.DataFrame({
    "유형": ["전자 기판", "소프트웨어", "인적 요인", "외부 요인"],
    "데이터_특징": ["반도체 소자의 외부 관측 신호 부족", "특정 조건 조합의 로직 오류",
                "설정 오입력·조립 불량·절차 미준수", "정전·원료 급변·이물 혼입"],
    "주된_대응": ["이중화·정기 교체", "검증·테스트 강화", "절차·교육 개선", "외부 요인 관리"],
})
print(no_trace_table.to_string(index=False))

# [강사님께 질문하기] 센서를 더 많이 달면 돌발 고장도 결국 예측할 수 있게 되나요?
# -> 답변: 유형에 따라 다름. "측정 부재형"(열화는 있는데 데이터가 없는 경우)은 센서 추가로
#    계측 가능해질 여지가 있지만, "열화 부재형"(애초에 축적되는 물리 과정이 없는 돌발)은 센서를
#    아무리 추가해도 효과가 없어서 이중화나 정기 교체 같은 다른 전략이 필요함

# [개념] 욕조 곡선(초기 고장/우발 고장/마모 고장)과 P-F 곡선의 차이
#   욕조 곡선: 같은 종류의 "설비 집단"에서 사용 기간에 따른 고장률 분포 (가로축=사용 기간)
#   P-F 곡선: "개별 설비 한 대"의 시간에 따른 상태 저하 과정 (가로축=시간)
bathtub_table = pd.DataFrame({
    "구간": ["초기 고장", "우발 고장", "마모 고장"],
    "원인": ["제작·조립 결함, 초기 설정 오류", "외부 충격·이물, 순간 과부하", "누적 마모·피로·부식"],
})
print(bathtub_table.to_string(index=False))

# [개념] 1978년 Nowlan & Heap 연구 - 항공기 부품 분석 결과 약 89%에서 마모 구간이 확인되지 않았고,
#   마모 특성이 뚜렷한 패턴은 여섯 유형(A~F) 중 두 가지뿐이었음
#   -> 시간 기준의 일괄 "연령 교체"는 고장률이 늘지 않는 부품에는 예방 효과가 낮음
#   -> 대안: 사용 기간이 아닌 "현재 상태"를 기준으로 하는 상태 기반 보전

# [개념] 예지보전 대상 판정 5문항 - "아니오"가 나오는 지점마다 다른 전략으로 갈라짐
pm_checklist = pd.DataFrame({
    "문항": ["1. 열화 존재", "2. 시간 충분성", "3. 신호 저장", "4. 고장 이력", "5. 경제성"],
    "질문": [
        "축적되는 열화 과정이 있는가",
        "P-F 간격이 현장 리드타임보다 충분히 긴가",
        "관련 물리량이 센서로 저장되고 있는가",
        "참조할 고장 사례가 있는가",
        "정지 비용이 대응 비용보다 큰가",
    ],
    "아니오일_때": [
        "이중화·정기 교체", "보호 로직·자동 정지", "센서·위치·주기 개선",
        "정상 패턴 학습 또는 동종 설비 활용", "사후 보전으로 충분",
    ],
})
print(pm_checklist.to_string(index=False))

# 우리 예시 설비 셋에 5문항을 직접 적용해보기
# * 아래 판정표는 study/failure_progression.py의 5문항 체크리스트를 임의의 예시 설비 3종에
#   적용한 것으로, 실제 설비 판정 결과가 아님
equipment_cases = pd.DataFrame({
    "설비": ["압연 구동모터 베어링", "긴급 차단 솔레노이드", "냉각수 배관 이음부"],
    "열화_존재": [True, False, True],
    "시간_충분성": [True, False, True],
    "신호_저장": [True, False, False],
    "고장_이력": [True, True, False],
    "경제성": [True, True, True],
})
equipment_cases["예지보전_적합"] = equipment_cases[["열화_존재", "시간_충분성", "신호_저장", "고장_이력", "경제성"]].all(axis=1)
print(equipment_cases.to_string(index=False))
# - 압연 구동모터 베어링만 5문항 모두 통과해 예지보전 모델 개발 대상으로 적합 - 솔레노이드는
#   열화 과정 자체가 없는 돌발형이라 애초에 예지보전 대상이 아니고, 냉각수 배관 이음부는 열화는
#   있지만 신호 저장이 안 돼 있어 "측정 부재형"(센서·주기 개선이 먼저 필요)에 해당함

# [강사님께 질문하기] 5문항 중 하나라도 "아니오"면 예지보전을 아예 포기해야 하나요?
# -> 답변: 아니요. "아니오" 항목은 포기 신호가 아니라 다음 행동을 알려주는 신호임 - 신호 저장이
#    안 됐다면 센서를 늘리고, 시간 여유가 없다면 보호 로직을 넣는 식으로 "아니오"마다 정해진
#    대응 방향이 있음(위 표의 "아니오일 때" 열 참고)
