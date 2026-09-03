# 실습 - 데이터 출처 추적과 손실 추정
# 목표: 워크시트로 원본과 가공본을 대조해 손실 차이를 찾고 추가 요청 항목을 도출
# CASE A: 압력 태그에서 짧은 서지의 잔존 여부 확인 / CASE B: 온도 태그에서 미세 변화의 잔존 여부 확인
#
# * 이 실습 데이터는 study/sensor_faults.py의 "정보 손실을 만드는 세 가지 방식" 개념을
#   숫자로 재현한 예시용 데이터이며, 실제 설비의 센서 실측값은 아님
import pandas as pd

# =====================================================================
# CASE A - 압력 태그, 짧은 서지의 잔존 여부
# =====================================================================

# STEP 1. 출처 정보 정리 - 원본은 10초 간격 원신호, 가공본은 1분 간격 솎아내기 결과
source_info_a = pd.DataFrame({
    "작성항목": ["출처·원래 주기", "저장 조건", "품질·데드밴드", "축소 비율"],
    "워크시트기록": ["현장 제어 계층, 10초 간격 원신호", "1분 간격 솎아내기(6개 중 1개만 선택)",
                "데드밴드 없음, 품질 코드 없음", "원래 주기 대비 6배 축소"],
})
print(source_info_a.to_string(index=False))

# 원본 - 10초 간격, 10분(60개 포인트), 평소 150bar 근처 + t=130~140초에 짧은 서지
raw_time = [i * 10 for i in range(60)]
raw_press = [150 + [-1, 0, 1][i % 3] for i in range(60)]
raw_press[13] = 190  # t=130s
raw_press[14] = 195  # t=140s
raw = pd.DataFrame({"time_s": raw_time, "pressure_bar": raw_press})
print(raw.iloc[10:17])

# 가공본 - 1분(60초) 간격으로 솎아낸 결과(6개 중 1개, t가 60의 배수인 행만 선택)
processed_a = raw[raw["time_s"] % 60 == 0].reset_index(drop=True)
print(processed_a)

# STEP 2. 원본과 가공본 대조
print(len(raw), len(processed_a))
print(raw["pressure_bar"].max(), processed_a["pressure_bar"].max())

# STEP 3. 손실 메커니즘 판정
surge_time = raw.loc[raw["pressure_bar"] == raw["pressure_bar"].max(), "time_s"].tolist()
nearest_grid = [t for t in processed_a["time_s"] if t <= surge_time[0]][-1]
print(surge_time, nearest_grid)
# - 원본에는 t=130·140초에 190·195bar 서지가 뚜렷이 남아 있지만, 가공본은 t=120초와
#   t=180초만 선택하므로 그 사이에 있던 서지가 통째로 빠짐 - 가공본 최댓값(149bar)이
#   원본 최댓값(195bar)보다 훨씬 낮게(오히려 평소 수준과 다를 바 없이) 나오는 게 그
#   증거. STEP1에서 정리한 대로 "솎아내기" 방식(일부 시점의 실제 측정값만 선택)이 원인

# STEP 4. 요청서 작성
request_a = pd.DataFrame({
    "작성항목": ["관측 가능", "관측 불가", "추가 요청", "우선순위·근거"],
    "정리내용": [
        "1분 간격의 완만한 압력 변화, 평소 대비 큰 폭의 지속적 이상",
        "60초 미만에서 끝나는 짧은 서지(이번 예시의 130~140초 서지 포함)",
        "1분 구간 내 최댓값 집계 컬럼 추가 저장",
        "서지가 유압 계통 이상의 조기 신호일 수 있어 우선순위 높음 - 최댓값 컬럼은 원신호를 전부 보관하지 않아도 서지 존재 여부를 알 수 있는 저비용 대안",
    ],
})
print(request_a.to_string(index=False))


# =====================================================================
# CASE B - 온도 태그, 미세 변화의 잔존 여부
# =====================================================================

# STEP 1. 출처 정보 정리 - 원본은 1분 간격 원신호, 가공본은 0.5도 데드밴드 저장
source_info_b = pd.DataFrame({
    "작성항목": ["출처·원래 주기", "저장 조건", "품질·데드밴드", "축소 비율"],
    "워크시트기록": ["현장 제어 계층, 1분 간격 원신호", "변화 기준 기록(데드밴드 0.5도)",
                "데드밴드 0.5도, 품질 코드 없음", "행 수 기준 원래의 절반 이하로 축소"],
})
print(source_info_b.to_string(index=False))

# 원본 - 1분 간격 20개, 완만한 상승 추세 위에 작은 오르내림(0.5도 미만)이 섞여 있음
noise_b = [0.3, -0.2, 0.3, -0.2, 0.3, -0.1, 0.2, -0.3, 0.3, -0.2,
           0.3, -0.2, 0.2, -0.3, 0.3, -0.1, 0.3, -0.2, 0.3, -0.2]
raw_temp = [round(800 + i * 0.1 + noise_b[i], 2) for i in range(20)]
raw_b = pd.DataFrame({"minute": list(range(20)), "temp_c": raw_temp})
print(raw_b)

# 가공본 - 마지막 기록값과 0.5도 이상 차이 날 때만 새 값 기록(데드밴드)
recorded_b = []
last_recorded = raw_temp[0]
for v in raw_temp:
    if abs(v - last_recorded) >= 0.5:
        last_recorded = v
    recorded_b.append(last_recorded)
processed_b = pd.DataFrame({"minute": list(range(20)), "temp_c": recorded_b})
print(processed_b)

# STEP 2. 원본과 가공본 대조
diff_count_raw = raw_b["temp_c"].nunique()
diff_count_processed = processed_b["temp_c"].nunique()
print(diff_count_raw, diff_count_processed)
print(raw_temp[0], raw_temp[-1], recorded_b[0], recorded_b[-1])

# STEP 3. 손실 메커니즘 판정
lost_points = sum(1 for i in range(len(raw_temp)) if raw_temp[i] != recorded_b[i])
print(lost_points, "/", len(raw_temp))
# - 원본은 20분 동안 고유값이 16개(대부분 분마다 값이 다름)인데, 가공본은 값이 겹쳐서
#   고유값이 4개로 줄어듦 - 시작값·끝값은 두 데이터가 거의 같지만(추세 자체는 살아 있음),
#   그 사이의 작은 오르내림(0.5도 미만 변화)은 데드밴드를 넘지 못해 20분 중 16분이 직전
#   기록값 그대로 남음(lost_points) - "변화 기준 기록" 방식(기준 폭을 넘을 때만 새 값을
#   저장)이 원인

# STEP 4. 요청서 작성
request_b = pd.DataFrame({
    "작성항목": ["관측 가능", "관측 불가", "추가 요청", "우선순위·근거"],
    "정리내용": [
        "0.5도 이상의 뚜렷한 온도 변화, 전체적인 상승·하강 추세",
        "0.5도 미만의 미세한 오르내림(초기 열화 단계에서 흔한 크기)",
        "데드밴드 완화(예: 0.2도) 또는 원신호 병행 저장",
        "장기 열화 추세는 작은 변화가 누적된 결과라 조기 단계에서는 데드밴드 미만으로 묻히기 쉬움 - 예지보전 목적이라면 압력 서지보다 오히려 이쪽 완화 요청의 우선순위가 더 높을 수 있음",
    ],
})
print(request_b.to_string(index=False))

# 결과 해석
# - CASE A(솎아내기)와 CASE B(데드밴드)는 손실을 만드는 방식이 다름 - 솎아내기는 "그 시점에
#   가봤는지 여부"가 관건이라 짧고 강한 사건(서지)을 통째로 놓치기 쉽고, 데드밴드는 "변화
#   폭이 기준을 넘었는지"가 관건이라 작고 느린 변화(미세 상승)를 조금씩 깎아 먹음
# - 두 경우 모두 가공본만 보면 원본에 무엇이 있었는지 전혀 알 수 없음 - "데이터에 없다는
#   사실은 사건 부재의 증거가 아니다"라는 이 강의의 결론이 CASE A·B 모두에서 숫자로 확인됨
