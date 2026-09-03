# [개념] 04-03 이상의 정의와 판정 기준 - 이상 정의의 출발점 / 이상 판정의 세 가지 방식 / 판정 기준의 운영과 검증
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(0)

# =====================================================================
# [개념] 01. 이상 정의의 출발점
# =====================================================================

# [개념] 이상 정의는 사람의 판단에서 출발 - 데이터는 값만 제공할 뿐, 이상의 경계는 사람이 결정함
#   모델 학습 순서: 이상 정의 -> 라벨 생성 -> 모델 학습 (이상 정의가 가장 먼저)
#   핵심: "대다수와 다름" != "설비 문제" (통계적 이상 전체가 곧 설비 이상은 아님)

# [개념] 이상(Anomaly)과 고장(Failure)은 다른 개념 - 감시 대상은 두 개념의 교집합("열화 진행")
#   이상만 있고 고장은 아닌 예: 신제품 생산, 운전 조건 변경, 센서 오류(-> 설비는 정상)
#   고장만 있고 이상은 아닌 예: 돌발 고장(사전 신호 없음)
#   -> "평소와 다르면서 + 실제 열화가 진행되는" 구간에 감시를 집중해야 함
concept_table = pd.DataFrame({
    "영역": ["이상만(고장 아님)", "이상 ∩ 고장(감시 대상)", "고장만(이상 아님)"],
    "예시": ["신제품 생산·운전 조건 변경·센서 오류", "열화 진행", "돌발 고장(사전 신호 없음)"],
})
print(concept_table.to_string(index=False))

# [개념] 여러 조건으로 나뉘는 "정상" 상태 - 부하 조건(두꺼운/얇은 소재) · 속도 조건(고속/저속) ·
#   가동 상태(대기 중/소재 통과 중)에 따라 정상 범위 자체가 달라짐

# 부하율에 따라 달라지는 정상 범위 + 단일 임계선이 만드는 오탐·미탐을 우리 데이터로 재현
# * 아래 데이터는 "하나의 선이 만드는 오탐과 미탐" 개념을 숫자로 재현한 예시용 데이터이며
#   실제 설비의 진동 실측값은 아님
load_pct = np.arange(40, 101, 2)
normal_vib_by_load = 2.0 + 0.02 * (load_pct - 40)  # 부하가 높을수록 정상 진동값 자체가 커짐
noise = np.random.normal(0, 0.1, len(load_pct))
vib_reading = normal_vib_by_load + noise
load_df = pd.DataFrame({"load_pct": load_pct, "vib_rms": vib_reading, "normal_line": normal_vib_by_load})
load_df.loc[load_df["load_pct"] == 96, "vib_rms"] = 4.2  # 고부하에서도 실제로는 정상 범위인 값(오탐 후보)

single_threshold = 4.0
false_positive = load_df[(load_df["vib_rms"] >= single_threshold) & (load_df["load_pct"] >= 90)]
false_negative_load = 45
degraded_point_vib = 3.3  # 저부하 구간에서 실제로는 열화가 진행 중인 값(정상선보다 높음)
is_false_negative = degraded_point_vib < single_threshold and degraded_point_vib > (2.0 + 0.02 * (false_negative_load - 40))
print(len(false_positive), is_false_negative)
# - 96% 고부하에서는 4.2mm/s가 정상 범위(3.12 안팎) 안인데도 단일 임계선(4.0)을 넘어 "오탐"으로
#   잡힘(false_positive 1건). 반대로 저부하(45%) 구간에서는 정상 범위(2.1 근처)보다 높은
#   3.3이라는 열화 값도 임계선(4.0) 아래라서 "미탐"으로 놓침(is_false_negative=True) - 부하
#   조건을 무시한 단일 수평선이 오탐과 미탐을 동시에 만든다는 슬라이드 개념이 그대로 재현됨

fig, ax = plt.subplots()
ax.scatter(load_df["load_pct"], load_df["vib_rms"], s=10, color="gray", label="정상 관측치")
ax.plot(load_df["load_pct"], load_df["normal_line"], color="blue", label="부하별 정상선")
ax.axhline(single_threshold, color="red", linestyle="--", label="단일 임계선")
ax.set_xlabel("부하율(%)")
ax.set_ylabel("진동 RMS(mm/s)")
ax.legend()
tmp_path = "data/_tmp_load_threshold.png"
fig.savefig(tmp_path)
print(os.path.exists(tmp_path))
os.remove(tmp_path)

# [퀴즈] "부하율 90%에서 진동 4.2mm/s"와 "부하율 45%에서 진동 3.3mm/s" 중 실제로 더 위험한
#   신호는 어느 쪽일까요? 먼저 예상해보세요.
# -> 정답: 부하율 45%에서 진동 3.3mm/s 쪽. 절대값은 더 작지만, 45% 부하에서 정상 범위는
#    2.1 안팎이라 3.3은 정상 대비 훨씬 크게 벗어난 값 - 반면 90% 부하에서 4.2는 정상 범위(3.0
#    안팎)보다 조금 높은 정도. "선의 위치보다 조건 정보"가 중요하다는 개념의 핵심


# =====================================================================
# [개념] 02. 이상 판정의 세 가지 방식
# =====================================================================

# ---- 임계치 ----
# [개념] 임계치 방식이 널리 쓰이는 3가지 이유: 즉시성(지연 없이 판정) · 설명 가능성(값과 기준선
#   비교로 명확한 근거) · 안전 직결(설계 한계 초과 시 즉시 정지)
# [개념] 임계치의 판정 구조 - 열화 시작보다 "늦은" 이상 판정 (기준선 아래 진행 구간은 계속 정상 분류)
# [개념] 임계치의 3가지 한계: 조건 취약(고정선으로 여러 조건 감당 불가 -> 오탐·미탐 동시) /
#   반응 지연(값이 크게 나빠진 뒤에야 반응 -> P-F 곡선의 오른쪽) / 관계 무시(각 신호를 개별
#   판정 -> 관계 변화 탐지 불가)
threshold_type_table = pd.DataFrame({
    "종류": ["설계값", "규격값", "경험값", "통계값"],
    "초과_의미": ["파손과 사고 위험", "장기 수명 단축", "과거 사례 재발", "설비 고유 기준 이탈"],
    "실무_용도": ["즉시 정지", "상태 등급 보고", "참조 기준", "조기 경보"],
})
print(threshold_type_table.to_string(index=False))

# ---- 추세 이탈 ----
# [개념] 추세 이탈로 바뀌는 관점: "절대 크기"에서 "평소 대비 변화"로 이동
#   질문 변화: "지금 값이 큰가" -> "평소보다 얼마나 큰가" (편차·기울기·도달 예상 시점으로 P점을 앞당김)

# 임계치 방식 vs 추세 이탈 방식의 검출 시점 차이를 우리 열화 시계열로 직접 비교
# * 아래 시계열은 04-01 P-F 곡선 데모와 같은 방식으로 재현한 예시용 데이터이며 실제 측정값은 아님
days = np.arange(0, 121)
flat_days = 40
elapsed = np.maximum(days - flat_days, 0)
vib = np.where(days <= flat_days, 2.0, 2.0 + 0.045 * elapsed ** 1.15) + np.random.normal(0, 0.08, len(days))
trend_df = pd.DataFrame({"day": days, "vib_rms": vib})

baseline_mean = trend_df.loc[trend_df["day"] <= flat_days, "vib_rms"].mean()
baseline_std = trend_df.loc[trend_df["day"] <= flat_days, "vib_rms"].std()
trend_threshold = baseline_mean + 3 * baseline_std  # 평소(기준선) 대비 +3표준편차를 벗어나면 추세 이탈로 판정
fixed_threshold = 4.5  # 절대 크기 기준의 고정 임계치

trend_hit = trend_df.index[trend_df["vib_rms"] >= trend_threshold]
fixed_hit = trend_df.index[trend_df["vib_rms"] >= fixed_threshold]
trend_detect_day = int(trend_hit[0]) if len(trend_hit) else None
fixed_detect_day = int(fixed_hit[0]) if len(fixed_hit) else None
gap_days = fixed_detect_day - trend_detect_day
print(round(trend_threshold, 3), trend_detect_day, fixed_detect_day, gap_days)
# - 추세 이탈(기준선 평균+3표준편차)은 임계치(고정 4.5)보다 더 이른 날에 이상을 검출함 - 두
#   방식의 검출 시점 차이(gap_days)만큼 대응 시간을 더 확보할 수 있다는 것이 숫자로 확인됨.
#   단, "도달 예상 시점"은 현재 추세가 계속 유지된다는 가정에 의존한다는 한계도 함께 기억해야 함

# [개념] 기준선 설정의 3가지 문제: 이미 열화된 기간(기준선이 높게 잡힘) / 특이 운전 혼입(과도한
#   변동 폭) / 기간 부족(계절 변동 누락) - 대응: 정비 이력 확인, 생산 실적 확인 후 구간 제외, 동일
#   기종 데이터 참조
# [개념] 추세 이탈의 3가지 한계: 기준선 의존(기준선 오류가 전체 판정에 확산) / 급변형 취약(평탄
#   뒤 급변하는 피로형에 늦게 반응) / 관계 미반영(개별 추세에 집중, 신호 간 관계는 못 봄)

# [강사님께 질문하기] 그럼 항상 추세 이탈 방식이 임계치 방식보다 더 좋은 건가요?
# -> 답변: 아니요. 임계치는 반응이 늦지만 "왜 이상인지"가 누구에게나 명확하고 안전 정지처럼
#    즉시성이 중요한 곳에는 꼭 필요함. 추세 이탈은 더 일찍 잡아내지만 기준선을 잘못 잡으면
#    전체가 틀어지고, 피로형처럼 평탄하다가 갑자기 튀는 신호에는 오히려 약함 - 그래서 이 강의는
#    "경쟁 관계가 아니라 겹쳐 쓰는 감시 층"이라고 설명함

# ---- 패턴 변화 ----
# [개념] 패턴 변화를 보는 두 갈래: 신호 간 관계(비율·예측 잔차로 정상 관계 이탈 측정) / 시간적
#   모양(기동 곡선·동작 파형·하루 변화 패턴의 형태 비교)

# "값은 정상인데 관계가 깨진 상태"를 우리 데이터로 재현 - 부하율과 전류가 정상적으로는 함께
# 움직이지만, 한 시점만 부하 대비 전류가 과도하게 높음
load_pct2 = np.arange(40, 101, 2)
normal_current = 100 + 0.9 * (load_pct2 - 40) + np.random.normal(0, 3, len(load_pct2))
current_df = pd.DataFrame({"load_pct": load_pct2, "current_A": normal_current})
anomaly_idx = 15  # 부하율 70% 지점
current_df.loc[anomaly_idx, "current_A"] = 175  # 같은 부하에서 정상 범위(약 130~140)를 크게 벗어난 값
expected_at_same_load = round(float(current_df.loc[current_df.index != anomaly_idx, "current_A"]
                                     [(current_df["load_pct"] >= 65) & (current_df["load_pct"] <= 75)].mean()), 1)
observed = float(current_df.loc[anomaly_idx, "current_A"])
print(expected_at_same_load, observed, round(observed - expected_at_same_load, 1))
# - 부하율 70% 근처의 다른 정상점 평균 전류(expected_at_same_load)보다 관측값(175A)이 훨씬 큼
#   - 전류값 자체(175A)만 보면 설비 정격 범위 안일 수 있어 임계치로는 못 잡지만, "이 부하에서는
#   이 정도 전류가 나오면 안 된다"는 관계 기준으로 보면 뚜렷한 이상으로 잡힘("값은 정상, 관계는
#   비정상")

# [개념] 이상 판정 - 계층적 감시: 패턴 변화가 가장 이른 반응(대신 설명 난도 높음) / 세 방식은
#   경쟁 관계가 아니라 겹쳐 쓰는 감시 층(아래층은 안전 보호, 위층은 조기 경보)

# [개념] 열화 유형별 감시 대상과 방식
degradation_monitor_table = pd.DataFrame({
    "열화_유형": ["마모", "피로", "부식"],
    "감시_대상": ["조건 보정한 원본 값", "변동성 지표", "환경 대비 예측 잔차"],
    "정의_방식": ["추세 이탈", "변동성의 추세 이탈", "패턴 변화"],
})
print(degradation_monitor_table.to_string(index=False))

# [개념] 회복형 두 유형의 감시 대상 - 원본 값보다 "열화 모양을 드러내는 관계·파생 변수"를 우선함
recovery_monitor_table = pd.DataFrame({
    "열화_유형": ["윤활 불량", "누유"],
    "감시_대상": ["유온과 진동의 관계", "보충 간격·압력 하강률"],
    "정의_방식": ["패턴 변화", "파생 변수의 추세 이탈"],
})
print(recovery_monitor_table.to_string(index=False))


# =====================================================================
# [개념] 03. 판정 기준의 운영과 검증
# =====================================================================

# [개념] 신호 변화의 4가지 원인 - 이상 정의가 진짜로 찾아야 할 것은 "설비 열화"뿐, 나머지 세
#   원인은 걸러내야 함
signal_change_cause_table = pd.DataFrame({
    "원인": ["설비 열화", "운전 조건 변화", "센서 문제", "데이터 처리 문제"],
    "대표_변화": ["이상 정의가 찾아야 할 핵심 대상", "부하·제품·속도 변경",
              "드리프트·고착·단선·스파이크", "통신 끊김·시각 동기 오류·집계 변경"],
})
print(signal_change_cause_table.to_string(index=False))

# [개념] 정상 구간을 잘라내는 4단계 - 이 순서를 지키지 않으면 "설비 열화가 아닌 변화"까지
#   기준선에 섞여 들어감
#   Step1 가동 구간(정지 시간 제외) -> Step2 과도 구간(기동 직후·정지 직전 제외) ->
#   Step3 이상 이력(고장·알람 주변 제외) -> Step4 정비 직후(이력에 따라 포함 여부 판단)

# 4단계 필터링을 우리 예시 운전 로그에 그대로 적용
# * 아래 로그는 "정상 구간을 잘라내는 4단계" 개념을 숫자로 재현한 예시용 데이터이며 실제 운전
#   기록이 아님
minute = np.arange(0, 30)
run_flag = np.array([0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1])
has_alarm = np.zeros(30, dtype=bool)
has_alarm[13] = True  # 13분 지점에서 알람 발생
after_maintenance = np.zeros(30, dtype=bool)
after_maintenance[26:28] = True  # 24~25분 정지 후 정비, 26~27분은 정비 직후 시운전 구간
log_df = pd.DataFrame({"minute": minute, "run_flag": run_flag, "has_alarm": has_alarm, "after_maintenance": after_maintenance})

step1 = log_df[log_df["run_flag"] == 1].copy()
transient_minutes = set()
for m in minute[1:]:
    if run_flag[m] != run_flag[m - 1]:
        transient_minutes.update([m, m + 1])  # 상태가 바뀐 시점의 앞뒤 1분을 "과도 구간"으로 취급
step2 = step1[~step1["minute"].isin(transient_minutes)]
alarm_minutes = set(log_df.loc[log_df["has_alarm"], "minute"])
alarm_window = set()
for m in alarm_minutes:
    alarm_window.update(range(m - 1, m + 2))
step3 = step2[~step2["minute"].isin(alarm_window)]
step4 = step3[~step3["minute"].isin(log_df.loc[log_df["after_maintenance"], "minute"])]
print(len(log_df), len(step1), len(step2), len(step3), len(step4))
# - 전체 30분 중 정지 구간을 빼면(Step1) 남는 게 26분, 과도 구간(상태 전환 앞뒤)까지 빼면 더
#   줄고, 알람 주변(Step3)과 정비 직후(Step4)까지 차례로 걸러내면 최종적으로 "순수 정상
#   운전" 구간만 남음 - 각 단계를 거칠 때마다 남는 행 수가 줄어드는 것이 그대로 확인됨

# [개념] 경보 3단계와 조치
alarm_table = pd.DataFrame({
    "단계": ["주의", "경고", "정지"],
    "기준_산정": ["추세 이탈 감지", "규격 상한과 통계 기준 중 낮은 값", "설계값 또는 규격 위험 구역"],
    "조치와_담당": ["감시 강화 · 데이터 담당", "정비 계획 · 정비 담당", "즉시 정지 · 운전 담당"],
})
print(alarm_table.to_string(index=False))


def judge_alarm_level(value, design_limit, spec_limit, stat_limit):
    """경보 3단계 기준을 그대로 코드화한 재사용 가능한 판정 함수"""
    warn_limit = min(spec_limit, stat_limit)
    if value >= design_limit or value >= spec_limit:
        return "정지"
    if value >= warn_limit:
        return "경고"
    stat_trend_limit = stat_limit * 0.85  # 통계 기준의 85% 지점부터 "추세 이탈 감지"로 간주
    if value >= stat_trend_limit:
        return "주의"
    return "정상"


# 우리 예시 설비 값 몇 개에 판정 함수를 적용해 검증
sample_readings = pd.DataFrame({
    "측정값": [3.0, 4.9, 6.3, 8.5],
    "판정": [judge_alarm_level(v, design_limit=9.0, spec_limit=7.0, stat_limit=5.5) for v in [3.0, 4.9, 6.3, 8.5]],
})
print(sample_readings.to_string(index=False))
# - 3.0(정상 범위) -> "정상", 4.9(통계 기준 5.5의 85%인 4.675 이상) -> "주의", 6.3(경고
#   기준인 min(7.0, 5.5)=5.5 이상) -> "경고", 8.5(설계값 9.0에는 못 미치지만 규격값 7.0을
#   넘음) -> "정지"로 판정됨 - 경보 3단계 조건이 실제로 값에 따라 올바르게 갈리는 것이 확인됨

# [개념] 이상 판정을 라벨로 만드는 두 방법: 이력 기반(정비 이력의 고장 시점 기준으로 선행 구간을
#   이상으로 표시) / 규칙 기반(정의한 이상 규칙을 전체 데이터에 적용해 라벨 자동 생성 - 타당성
#   검증을 먼저 요구)
# [개념] 판정 기준은 실제 이력으로 검증 - 정의(열화 유형 확정 -> 감시 대상 선정 -> 이상 정의
#   결정) -> 생성(규칙 적용 라벨 생성) -> 검증(정비 이력과 대조) -> 겹침 부족 시 이상 정의로
#   되돌아가 수정하는 반복(폐쇄형 흐름)

# [강사님께 질문하기] "규칙 기반 라벨은 타당성 검증을 먼저 요구한다"는 게 정확히 무슨 뜻인가요?
# -> 답변: 규칙(예: "3표준편차 초과면 이상")을 정하고 그걸로 전체 데이터에 자동으로 라벨을
#    붙이기 전에, 그 규칙이 실제 정비 이력과 얼마나 겹치는지부터 확인해야 한다는 뜻 - 검증 없이
#    규칙을 바로 전체에 적용하면, 규칙 자체가 틀렸을 때 그 오류가 라벨 전체에 그대로 퍼짐(위
#    "정의·생성·검증의 반복" 흐름도 참고)

# [개념] 핵심 체크포인트 - 정상 조건(동일 부하·속도·가동 상태에서 비교) / 감시 대상(원본 값·
#   변동성·파생 변수·신호 관계를 구분) / P-F 위치(필요한 대응 시간을 확보하도록 검출 위치 선택) /
#   검증(정비 이력과 과거 사례로 오탐·누락 확인)
checkpoint_table = pd.DataFrame({
    "관점": ["정상 조건", "감시 대상", "P-F 위치", "검증"],
    "핵심_기준": [
        "동일한 부하·속도·가동 상태에서 비교",
        "원본 값·변동성·파생 변수·신호 관계를 구분",
        "필요한 대응 시간을 확보하도록 검출 위치를 선택",
        "정비 이력과 과거 사례로 오탐과 누락을 확인",
    ],
})
print(checkpoint_table.to_string(index=False))
