# [개념] 04-02 열화 유형과 철강 현장 신호 해석 - 마모/피로/부식/윤활불량/누유 및 철강 현장 사례
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(0)

# =====================================================================
# [개념] 01. 열화 신호를 읽는 기준
# =====================================================================

# [개념] 열화(Degradation) / 이상(Anomaly) / 고장(Failure)의 정의
#   열화: 성능·상태가 시간이 지나며 점차 나빠지는 "과정"
#   이상: 현재 운전조건에서 기대되는 정상 모습과 다르게 나타나는 "상태"
#   고장: 설비가 요구되는 기능을 제대로 수행하지 못하는 "상태"

# [개념] 원인 분류 vs 형태 분류 - 같은 현상도 목적에 따라 다르게 분류함
#   기계공학 관점(원인): 접촉 응력·반복 하중·전기화학 반응·유막 파괴·실 경화
#   데이터 관점(형태): 완만한 단조 상승·평탄 후 급변·환경 연동 상승·톱니형 반복·계단형 하강
#   -> 데이터 분석가는 "왜 열화가 생겼는지"보다 "데이터에 어떤 모양을 남기는지"로 먼저 좁혀 들어감


# =====================================================================
# [개념] 02. 열화 유형과 신호 형태
# =====================================================================

# ---- 마모(Wear) ----
# [개념] 마모 진행 3단계: 길들이기(초기 미세 돌기 제거) -> 안정 마모(완만한 진행) -> 급속 마모(가속)
# [개념] 마모의 선행 지표 4가지: 제품 치수 편차(가장 먼저 반응) · 제어 보상량 · 마모 입자(오일 속 금속) · 진동(반응 느림)
# [개념] 마모 시계열의 4가지 특징: 단조성(한 방향으로만 이동) · 완만함(주·월 단위로 봐야 보임) ·
#   예측성(기울기로 임계치 도달 시점 추정) · 리셋(부품 교체 시 원래 수준으로 급락)

# 마모의 "톱니 패턴" 재현 - 롤(부품) 교체마다 리셋되는 완만한 단조 상승
# * 이 시계열은 study/degradation_types.py의 "마모 시계열 특징" 개념을 숫자로 재현한 예시용
#   데이터이며, 실제 설비의 측정값은 아님
days_wear = np.arange(0, 240)
cycle_len = 80  # 한 교체 주기(일)
wear_signal = 0.02 + 0.0009 * (days_wear % cycle_len) + np.random.normal(0, 0.003, len(days_wear))
wear_df = pd.DataFrame({"day": days_wear, "product_dev_mm": wear_signal})
print(wear_df.iloc[[0, 79, 80, 159, 160]])

reset_days = [d for d in range(1, len(days_wear)) if wear_df["product_dev_mm"].iloc[d] < wear_df["product_dev_mm"].iloc[d - 1] - 0.02]
print(reset_days)
# - 80일·160일 지점에서 값이 급락(리셋)하는 것으로 확인됨 - 롤 교체 주기(cycle_len=80일)와
#   정확히 일치, "부품 교체 시 원래 수준으로 급락"이라는 마모 시계열 특징이 숫자로도 재현됨

# ---- 피로(Fatigue) ----
# [개념] 피로 진행 3단계: 균열 발생(표면 아래 잠복) -> 균열 진전(반복 하중마다 성장) -> 박리 확대(급가속)
# [개념] 피로 선행 지표의 순서: 초음파(고주파 응력파, 순회 점검) -> 결함 주파수(진동 스펙트럼 봉우리, 일부 설비만) ->
#   진동 실효값·온도(전체 진동 크기·발열, 대체로 있음)
# [개념] 실효값만 있을 때의 대안: 원시 파형에서 직접 계산 / 표준편차·최댓값 대 평균 비·기준선 이탈 횟수 같은
#   통계 지표 생성 / "이상적 데이터"를 요구하는 대신 현재 데이터의 한계를 협의로 제시
# [개념] 피로 시계열의 3가지 특징: 긴 평탄 구간(대부분 불변) · 산발적 스파이크(초기 신호) ·
#   급격한 상승(스파이크 빈도 증가 후 기준선 자체가 상승)

# 피로의 "평지 후 절벽" 패턴 재현 - 산발적 스파이크가 늘어나다가 후반에 기준선 자체가 급등
fatigue_signal = np.full(180, 2.0) + np.random.normal(0, 0.1, 180)
for spike_day in [55, 80, 105, 120, 135]:
    fatigue_signal[spike_day] += np.random.uniform(1.0, 2.0)
fatigue_signal[150:] += np.linspace(0, 6.0, 30) ** 1.4 / 10
fatigue_df = pd.DataFrame({"day": np.arange(180), "vib_rms": fatigue_signal})
early_std = round(float(fatigue_df["vib_rms"].iloc[:50].std()), 3)
late_std = round(float(fatigue_df["vib_rms"].iloc[150:].std()), 3)
print(early_std, late_std)
# - 초반 50일의 변동성(표준편차)보다 후반 30일의 변동성이 훨씬 커짐 - "긴 평탄 구간" 뒤에
#   "급격한 상승"으로 이어지는 피로형의 특징이 그대로 드러남

fig, axes = plt.subplots(2, 1, sharex=True)
axes[0].plot(wear_df["day"], wear_df["product_dev_mm"], color="blue")
axes[0].set_title("마모형 - 톱니 패턴(완만한 단조 상승 + 교체 시 리셋)")
axes[1].plot(fatigue_df["day"][:180], fatigue_df["vib_rms"], color="red")
axes[1].set_title("피로형 - 평지 후 절벽(산발적 스파이크 + 후반 급상승)")
tmp_path = "data/_tmp_wear_fatigue.png"
fig.savefig(tmp_path)
print(os.path.exists(tmp_path))
os.remove(tmp_path)

# [퀴즈] 마모형과 피로형 둘 다 "결국 값이 올라간다"는 점은 같습니다. 데이터만 보고 두 유형을
#   가장 빠르게 구분할 수 있는 단서는 무엇일까요? 먼저 예상해보세요.
# -> 정답: "부품 교체 시 원래 수준으로 되돌아오는지" 여부. 마모형은 롤/부품을 교체하면 값이
#    급락해 리셋되지만(톱니 패턴), 피로형은 균열이 이미 진행된 상태라 교체 전까지는 절대
#    되돌아오지 않음("아니오" - 되돌아오는가 열 참고)

# ---- 부식(Corrosion) ----
# [개념] 부식이 마모·피로와 다른 점: 진행 조건이 "환경 노출 시간"이라 정지 중에도 진행되고, 계절성이 뚜렷함
corrosion_diff_table = pd.DataFrame({
    "구분": ["진행 조건", "정지 중 진행", "계절성"],
    "마모·피로": ["가동량, 하중 반복", "없음", "거의 없음"],
    "부식": ["환경 노출 시간", "있음", "뚜렷함"],
})
print(corrosion_diff_table.to_string(index=False))

# [개념] 부식이 데이터로 다루기 어려운 3가지 이유: 느린 진행(몇 달~몇 년) · 국소성(물 고이는 지점에
#   센서가 없음) · 계절 혼입(여름철 상승이 부식 때문인지 온도 때문인지 불분명)
# [개념] 부식 접근의 세 갈래: 환경 변수 결합(습도·온도·응축 데이터 확보) · 누적 노출량 생성(기준
#   초과 시간을 계속 더한 파생 변수) · 간접 지표 관찰(마찰 증가에 따른 구동 전류 상승)

# 부식형 신호의 "환경 연동 + 지연 반응 + 비회복" 재현 - 습도가 오른 뒤 전류가 뒤늦게 따라 오르고,
# 습도가 다시 낮아져도 전류는 높은 수준을 유지
month = np.arange(1, 13)
humidity = np.array([50, 48, 52, 50, 54, 68, 78, 82, 74, 60, 56, 53])
drive_current = np.array([12.0, 12.0, 12.1, 12.0, 12.1, 12.2, 12.7, 13.9, 14.4, 14.6, 14.7, 14.8])
corrosion_df = pd.DataFrame({"month": month, "humidity_pct": humidity, "current_A": drive_current})
print(corrosion_df)

peak_humidity_month = int(corrosion_df.loc[corrosion_df["humidity_pct"].idxmax(), "month"])
peak_current_month = int(corrosion_df.loc[corrosion_df["current_A"].idxmax(), "month"])
recovered = drive_current[-1] <= drive_current[5]  # 습도가 낮아진 12월 값이 6월(습도 상승 초입) 수준으로 돌아왔는가
print(peak_humidity_month, peak_current_month, recovered)
# - 습도는 8월(peak_humidity_month)에 최고치를 찍는데 전류는 그보다 늦은 12월까지도 계속
#   오르며 최고치(peak_current_month)를 찍음 - "지연 반응"이 확인됨. 또한 습도가 12월에
#   53%까지 낮아져도 전류는 6월 수준(12.2A)으로 돌아오지 않음(recovered=False) - "비회복"이
#   확인됨

# [강사님께 질문하기] 부식은 왜 마모나 피로처럼 "선행 지표"가 정리되어 있지 않나요?
# -> 답변: 마모·피로는 가동할 때마다 반복되는 물리 과정이라 짧은 기간의 데이터로도 추세가
#    보이지만, 부식은 진행이 너무 느리고(몇 달~몇 년) 계절 요인과 섞여서, 몇 달치 데이터만으로는
#    "이게 부식 때문인지, 그냥 여름이라 그런지" 구분이 안 될 때가 많음 - 그래서 환경 변수를
#    같이 모으거나 누적 노출량 같은 파생 변수를 새로 만드는 "접근 전략"이 필요한 것

# ---- 윤활 불량(Lubrication failure) ----
# [개념] 윤활유가 하는 세 가지 일: 분리(유막으로 접촉 차단) · 냉각(마찰열 방출) · 차단(수분·이물 차단)
# [개념] 윤활 불량을 가르는 두 표식: 유온과 진동의 동반 상승(같은 시점에 같은 방향으로 이동) /
#   손상 누적(급유 뒤 최저점이 이전 수준까지 회복되지 않는 패턴)

# 윤활 불량의 "톱니 패턴" 재현 - 급유할 때마다 유온·진동이 함께 회복되지만 주기별 바닥값은 점진 상승
lube_days = np.arange(0, 120)
cycle = 28
oil_temp = 55 + 0.6 * (lube_days % cycle) + 0.05 * (lube_days // cycle) * cycle
vib_lube = 2.0 + 0.045 * (lube_days % cycle) + 0.02 * (lube_days // cycle) * cycle / 4
lube_df = pd.DataFrame({"day": lube_days, "oil_temp_c": oil_temp, "vib_rms": vib_lube})
refill_days = [0, cycle, cycle * 2, cycle * 3]
baseline_at_refill = lube_df.loc[lube_df["day"].isin(refill_days), ["day", "oil_temp_c", "vib_rms"]]
print(baseline_at_refill.to_string(index=False))
# - 급유 직후(0·28·56·84일)의 유온·진동 "바닥값"이 회차를 거듭할수록 조금씩 상승함 - 급유로
#   완전히 회복되는 게 아니라 회복 못한 손상이 조금씩 누적되고 있다는 뜻(손상 누적 표식)

corr_temp_vib = round(float(np.corrcoef(lube_df["oil_temp_c"], lube_df["vib_rms"])[0, 1]), 3)
print(corr_temp_vib)
# - 유온과 진동의 상관계수가 1에 가까움 - 두 물리량이 같은 시점에 같은 방향으로 함께
#   움직인다는 "판별 단서"가 숫자로도 확인됨

# ---- 누유(Leakage) ----
# [개념] 외부 누유(육안 점검 가능, 미끄럼·화재 위험) vs 내부 누유(고압->저압 이동, 외부 흔적
#   없이 성능 저하로만 발현) - 데이터 분석의 핵심 대상은 눈에 보이지 않는 내부 누유
# [개념] 누유가 지표에 나타나는 순서: 압력 유지(하강률 증가) -> 펌프 보상(기동 횟수 증가) ->
#   유온 상승(유동 손실이 열로 전환) -> 성능 저하(동작 속도·힘 저하)
# [개념] 누유의 관측 지표 4가지: 압력 하강률(유지 구간 기울기) · 펌프 가동률(가동 시간·기동 횟수) ·
#   보충 간격(유면 급등 사이 간격) · 조건 보정 유온(온도·부하 맞춘 뒤 비교)

# 누유의 "역톱니 패턴" 재현 - 유면이 내려가다가 보충으로 회복되지만, 보충 간격은 점점 짧아짐
refill_intervals = [45, 35, 25, 20, 15]  # 일
oil_level = [100.0]
for interval in refill_intervals:
    drop = np.linspace(oil_level[-1], oil_level[-1] - (100 / 5), interval + 1)[1:]
    oil_level.extend(drop.tolist())
    oil_level.append(100.0)  # 보충
leak_df = pd.DataFrame({"step": range(len(oil_level)), "oil_level_pct": oil_level})
print(leak_df.tail(3))

interval_check = pd.DataFrame({"보충_회차": range(1, len(refill_intervals) + 1), "간격(일)": refill_intervals})
interval_check["직전_대비_단축"] = interval_check["간격(일)"].diff().fillna(0) < 0
print(interval_check.to_string(index=False))
# - 1회차 45일 -> 5회차 15일로 보충 간격이 계속 짧아짐(2~5회차 모두 "직전 대비 단축"=True) -
#   "보충 간격 단축 = 누유 진행"이라는 역톱니 패턴의 핵심 증거

fig2, ax2 = plt.subplots()
ax2.plot(leak_df["step"], leak_df["oil_level_pct"], color="darkorange")
ax2.set_title("누유의 역톱니 패턴(보충으로 회복 + 간격 단축)")
tmp_path2 = "data/_tmp_leak_pattern.png"
fig2.savefig(tmp_path2)
print(os.path.exists(tmp_path2))
os.remove(tmp_path2)


# =====================================================================
# [개념] 03. 판별과 데이터 분석
# =====================================================================

# [개념] 열화 판별의 세 질문: STEP1 회복 여부(회복형/비회복형) -> STEP2 변화 속도(완만한 추세/급격한
#   상승) -> STEP3 동반 변수(함께 움직이는 물리량·사건 확인)
type_shape_table = pd.DataFrame({
    "유형": ["마모", "피로", "부식", "윤활 불량", "누유"],
    "되돌아오는가": ["교체 시에만", "아니오", "아니오", "급유 시(부분 회복)", "보충 시"],
    "대표_신호_모양": ["완만한 단조 상승", "평지 후 절벽", "환경 연동 상승", "톱니(동반 상승)", "역톱니(간격 단축)"],
})
print(type_shape_table.to_string(index=False))


def classify_degradation(recovers, gradual, companion_signal):
    """세 질문(회복 여부/변화 속도/동반 변수)으로 열화 유형 후보를 좁히는 재사용 가능한 판별 함수"""
    if recovers and companion_signal == "온도·진동 동반":
        return "윤활 불량 후보(회복 + 온도·진동 동반)"
    if recovers and companion_signal == "압력·유면 동반":
        return "누유 후보(회복 + 압력·유면 동반)"
    if not recovers and gradual and companion_signal == "품질":
        return "마모 후보(비회복 + 완만함 + 품질 선행)"
    if not recovers and gradual and companion_signal == "환경":
        return "부식 후보(비회복 + 환경 연동)"
    if not recovers and gradual:
        return "피로 후보(비회복 + 급변)"
    return "추가 확인 필요"


# 앞서 만든 다섯 시계열에 판별 함수를 그대로 적용해 검증
print(classify_degradation(recovers=False, gradual=True, companion_signal="품질"))
print(classify_degradation(recovers=False, gradual=True, companion_signal="환경"))
print(classify_degradation(recovers=True, gradual=True, companion_signal="온도·진동 동반"))
print(classify_degradation(recovers=True, gradual=True, companion_signal="압력·유면 동반"))

# [개념] 회복형 두 유형의 구분
recovery_table = pd.DataFrame({
    "유형": ["윤활 불량", "누유"],
    "회복_계기": ["급유", "보충"],
    "함께_움직이는_것": ["유온과 진동 동반 상승", "압력과 유면 동반 하강"],
})
print(recovery_table.to_string(index=False))

# [개념] 물리량별로 볼 수 있는 열화
physical_quantity_table = pd.DataFrame({
    "물리량": ["진동", "전류", "압력·유량", "품질값·환경"],
    "관측_가능한_열화": ["마모·윤활 불량에 직접 반응, 피로는 주파수 성분으로 관측",
                     "마찰 증가 전반에 반응, 별도 센서 없이 확보 가능",
                     "유압·공압 전용, 누유에 가장 직접적",
                     "품질값은 마모, 환경 변수는 부식 전용"],
})
print(physical_quantity_table.to_string(index=False))

# [개념] 다변량으로 보는 세 가지 방법: 조합 관찰(함께 움직인 패턴) / 관계 변화(안정적 관계가
#   틀어졌는지) / 시간 순서(어느 신호가 먼저 반응했는지)

# [개념] 복합 열화의 두 가지 연쇄 - 마지막 현상보다 "연쇄를 시작한 원인"을 추적해야 함
#   윤활 연쇄: 윤활 부족 -> 마모 가속 -> 금속 입자 증가 -> 피로 균열 확대
#   부식 연쇄: 로드 부식 -> 실 손상 -> 누유 -> 유온 상승 -> 실 경화

# [강사님께 질문하기] 겹쳐진 신호를 마모 성분과 윤활 톱니 성분으로 "분해"한다는 게 실제로 어떻게
#   가능한가요?
# -> 답변: 이번 강의에서는 개념 수준(완만한 추세 성분 + 주기적 톱니 성분으로 나눠 보인다는 것)까지만
#    다룸 - 실제로는 이동평균으로 추세 성분을 뽑아내고 남은 잔차에서 주기 성분을 보는 식의 시계열
#    분해 기법을 쓰는데, 그 구체적 방법은 이후 실습 과정에서 다룰 예정


# =====================================================================
# [개념] 04. 철강 현장 열화 사례
# =====================================================================

# ---- 압연롤 마모 ----
# [개념] 압연 공정의 스탠드 흐름: 소재 투입 -> 1스탠드(1차 압하) -> 2스탠드(추가 압하) -> 출측 두께계(실측)
# [개념] 작업롤(소재 접촉, 마모 가장 빠름) / 받침롤(휨 방지) / 자동 두께 제어(하중 변화 읽어 롤 간격 실시간 보정)
# [개념] 압연롤 마모의 세 요인: 기계적 마모(스케일이 갉아냄) · 열적 손상(가열·냉각 반복 미세 균열) ·
#   표면 조도 변화(매끈해지면 제품 표면 특성 변화)

rolling_indicator_table = pd.DataFrame({
    "지표": ["롤 간격 보정량", "압하력", "두께 편차 변동 폭", "폭 방향 두께 차"],
    "관측_변화": ["한 방향 이동", "같은 조건에서 완만한 상승", "변동 폭 확대", "중앙·단부 차이 확대"],
    "해석_조건": ["1순위 제어 출력", "강종·목표 두께 정규화", "평균보다 변동 폭 중심", "폭별 품질 측정"],
})
print(rolling_indicator_table.to_string(index=False))

# 압연롤 마모 4지표 재현 - 롤 간격 보정량이 한 방향(마이너스)으로 계속 이동
# * 아래 시계열은 압연롤 마모 개념을 숫자로 재현한 예시용 데이터이며 실제 조업 데이터가 아님
rolling_days = np.arange(0, 60)
gap_correction = -0.001 * rolling_days + np.random.normal(0, 0.005, len(rolling_days))
thickness_dev_std = 0.01 + 0.0006 * rolling_days
rolling_df = pd.DataFrame({"day": rolling_days, "gap_correction_mm": gap_correction, "thickness_dev_std": thickness_dev_std})
early_gap = round(float(rolling_df["gap_correction_mm"].iloc[:10].mean()), 4)
late_gap = round(float(rolling_df["gap_correction_mm"].iloc[-10:].mean()), 4)
early_dev = round(float(rolling_df["thickness_dev_std"].iloc[0]), 4)
late_dev = round(float(rolling_df["thickness_dev_std"].iloc[-1]), 4)
print(early_gap, late_gap)
print(early_dev, late_dev)
# - 롤 간격 보정량의 평균이 초반 -0.0037mm 안팎에서 후반 -0.0531mm 안팎으로 한 방향(마이너스)
#   으로 계속 이동 - "롤 간격 보정량"이 마모를 가장 먼저 드러내는 1순위 제어 출력이라는 개념이
#   숫자로도 재현됨. 두께 편차 변동 폭(표준편차)도 0.01(day0)에서 0.0454(day59)로 초반보다
#   후반이 더 커짐

# [개념] 계획 교체가 만드는 고장 데이터 부족 - 한계 도달 전에 교체해 실제 고장 사례가 거의 없는
#   현장(계획 교체의 역설) -> 분석 목표를 "고장 분류"에서 "마모 진행 정도·교체 도달 시점 추정"으로 전환
# [개념] 압연롤 사례의 판별 3질문: 회복 조건(롤 교체 시점에만 복귀) -> 진행 속도(교체 주기 동안
#   완만한 진행, 말기 가속) -> 동반 변수(누적 압연량과 품질 편차의 동반 변화)

# ---- 베어링 손상 ----
# [개념] 베어링이 예지보전 대표 사례인 이유: 잦은 교체 · 점진적 열화(전동 피로+윤활 불량) ·
#   명확한 신호(손상 부위마다 특정 주파수에서 규칙적 충격)
# [개념] 베어링 구조와 손상 부위 - 손상 부위마다 충격 반복 주기가 달라 주파수로 위치를 특정
bearing_location_table = pd.DataFrame({
    "손상_부위": ["외륜 궤도면", "내륜 궤도면", "구름 요소 표면", "케이지·리테이너"],
    "약어": ["BPFO", "BPFI", "BSF", "FTF"],
})
print(bearing_location_table.to_string(index=False))

# [개념] 베어링 손상 4단계
#   1단계 초음파: 20~60kHz 대역, 윤활 부족 가능성, 급유 점검
#   2단계 결함 주파수: 고유 진동수 여기, 결함 주파수 출현, 계획 정비 최적 구간
#   3단계 주파수 변동: 결함 주파수 배수 성분, 진동 크기·온도 상승 시작
#   4단계 광대역 소음: 결함 봉우리 약화, 불규칙 마찰음 확대, 온도 급상승
#   -> 결함 봉우리 감소를 "회복"으로 오판하지 않도록 다중 지표(진동+온도)를 함께 확인해야 함
# [개념] 진동 실효값만 확보된 경우 - 1~2단계는 사실상 관측 불가. 대안 지표: 이동 표준편차 ·
#   최댓값 대 평균 비 · 기준선 이탈 횟수. 최댓값 태그가 함께 저장되는지 먼저 점검

# 실효값만으로 3~4단계를 감지하는 대안 지표 재현
bearing_days = np.arange(0, 40)
bearing_vib = np.full(40, 2.0) + np.random.normal(0, 0.1, 40)
bearing_vib[25:] += np.random.normal(0, 0.9, 15)  # 3~4단계: 불규칙 마찰음(광대역 소음)으로 변동성 급증
bearing_df = pd.DataFrame({"day": bearing_days, "vib_rms": bearing_vib})
rolling_std = bearing_df["vib_rms"].rolling(5).std()
max_over_mean = round(float(bearing_df["vib_rms"].max() / bearing_df["vib_rms"].mean()), 3)
early_rolling_std = round(float(rolling_std.iloc[10]), 3)
late_rolling_std = round(float(rolling_std.iloc[-1]), 3)
print(early_rolling_std, late_rolling_std, max_over_mean)
# - 실효값 하나만 봐서는 평균 수준만 비슷해 보이지만, 이동 표준편차는 초반 약 0.065에서
#   후반(3~4단계 구간) 약 0.575로 뚜렷이 커짐 - "실효값만 있을 때의 대안 지표"가 실제로 후기
#   단계를 더 민감하게 잡아낸다는 것이 확인됨

# [강사님께 질문하기] BPFO·BPFI 같은 결함 주파수는 어떻게 계산하나요?
# -> 답변: 베어링의 볼(롤러) 개수, 볼 지름, 피치 지름, 접촉각과 축 회전수로 계산하는 고정된
#    공식이 있음(이번 강의 슬라이드에는 공식 자체는 나오지 않고 "위치마다 다른 주파수가 나온다"는
#    개념만 소개됨) - 실무에서는 베어링 제조사가 제공하는 규격표의 값을 그대로 사용하는 경우가 많음

# ---- 유압 누유(철강 현장) ----
# [개념] 유압 계통의 흐름과 누유 범위: 유압 유닛(압력·유온·유면·펌프 상태) -> 주 배관(계통 전체 공급) ->
#   실린더(밀봉·배관·밸브 누유 후보) -> 말단 동작(동작별 압력 강하 차이)
# [개념] 철강 현장 유압 계통의 가혹 조건 3가지: 복사열(고온 소재 열로 밀봉재 경화) · 분진과
#   스케일(실린더 로드에 부착돼 밀봉재 손상) · 진동(배관 접합부 풀림 가속)
# [개념] 압력 하강률을 만드는 절차: 유지 구간 식별(동작 지령 없고 변화 작은 구간) -> 압력 기울기
#   계산(유지 구간 안에서만) -> 파생 시계열 생성(구간별 기울기를 시간순 연결)

# 압력 하강률 계산 절차를 그대로 코드로 재현
# * 아래 데이터는 유압 실린더 압력을 재현한 예시용 데이터이며 실제 설비 실측값이 아님
t_sec = np.arange(0, 60)
hold_pressure = 150 - 0.15 * t_sec + np.random.normal(0, 0.3, len(t_sec))  # "유지 구간" 60초
hold_df = pd.DataFrame({"t_sec": t_sec, "pressure_bar": hold_pressure})
slope_bar_per_sec = round(float(np.polyfit(hold_df["t_sec"], hold_df["pressure_bar"], 1)[0]), 4)
print(slope_bar_per_sec)
# - 유지 구간 60초 동안의 압력 기울기(1차 회귀 계수)가 약 -0.15bar/s로 계산됨 - 이 값을 여러
#   유지 구간에서 반복 계산해 시간순으로 이으면 "압력 하강률" 파생 시계열이 됨(3단계 STEP3)

leak_indicator_table = pd.DataFrame({
    "지표": ["압력 하강률", "펌프 가동률", "보충 간격", "조건 보정 유온"],
    "필요한_원본_데이터": ["압력·동작 신호", "펌프 가동 신호", "유면 또는 급유 이력", "유온·외기·생산량"],
    "난이도": ["높음", "낮음", "낮음", "중간"],
})
print(leak_indicator_table.to_string(index=False))

# [개념] 누유 신호가 늦게 나타나는 세 이유: 설계 여유(큰 펌프·배관이 초기 누유 흡수) · 축압기
#   완충(압력 변동 완충으로 작은 누유가 가려짐) · 측정 위치(계측은 중앙, 누유는 말단)

# [개념] 현장 사례에서 반복되는 분석 구조 - 결과가 정상이어도(롤 간격 보정량·펌프 가동률처럼)
#   정상을 "유지하기 위한" 제어 노력 자체가 커질 수 있음 -> 조건 정규화(강종·회전수·유지 구간·
#   운전 대수를 맞춘 비교) + 데이터 결합(생산·제어·품질·정비 정보 연결)

# [개념] 데이터 확보를 판정하는 세 항목: 태그 존재(이름만 말고 실제 값 확인) · 저장 주기(변화
#   속도 대비 충분히 촘촘한지) · 결합 필요성(품질·정비·생산·동작 신호의 위치·담당 시스템 파악)

# [강사님께 질문하기] 압연롤·베어링·유압 누유 세 사례를 배우는 이유가 각각 다른 열화 유형을
#   대표해서인가요?
# -> 답변: 맞음. 압연롤은 "회복형이 아닌 마모"(교체 전까지 단조 상승), 베어링은 "피로+윤활
#    복합 열화"(초음파부터 결함 주파수까지 단계적으로 진행), 유압 누유는 "회복형"(보충하면
#    일시적으로 돌아오는 역톱니)의 대표 사례로 골라서, 세 유형의 판별 논리를 실제 철강 설비에
#    각각 대응시켜 보여주는 구성임
