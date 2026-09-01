# 실습1 - 컬럼 목록 3요소 분해
# 목표: 태그 목록과 측정 데이터로 컬럼별 물리량·설치 위치·샘플링 주기 표 완성
# CASE A: MTR(회전기계) 태그 / CASE B: HYD·FUR(유압·열설비) 태그
#
# * 이 실습 데이터는 study/measurement_basics.py의 "3요소로 완성하는 컬럼 설명" 개념을
#   숫자로 재현한 예시용 데이터이며, 실제 설비의 센서 실측값은 아님
import pandas as pd

# STEP 1. 1분 간격 16개 시각에 여섯 컬럼을 측정한 예시 데이터 준비
timestamp = pd.date_range("2026-09-01 09:00:00", periods=16, freq="1min")

data = pd.DataFrame({
    "timestamp": timestamp,
    # CASE A - 회전기계(모터) 태그: 매 분 값이 계속 바뀜(빠르게 움직이는 물리량)
    "MTR01_VIB_RMS_H": [2.8, 2.9, 2.8, 3.0, 2.9, 3.1, 3.0, 2.9, 3.2, 3.1, 3.0, 3.3, 3.2, 3.1, 3.4, 3.3],
    "MTR01_CUR": [412, 415, 410, 418, 414, 420, 416, 413, 422, 417, 415, 425, 420, 416, 428, 422],
    # CASE B - 유압(HYD01_PRS)은 5~8행에서 190bar에 멈춰 상한에 걸린 모습을 보여줌
    "HYD01_PRS": [165, 172, 178, 183, 187, 190, 190, 190, 190, 186, 180, 175, 169, 163, 158, 152],
    "HYD01_FLW": [42, 41, 43, 40, 44, 39, 45, 38, 46, 37, 47, 36, 48, 35, 49, 34],
    # CASE B - 열설비(FUR01_TMP_Z1)는 3분마다만 값이 바뀌는 계단형 변화(느린 반응)
    "FUR01_TMP_Z1": [845, 845, 845, 846, 846, 846, 847, 847, 847, 848, 848, 848, 849, 849, 849, 850],
})
print(data)

# STEP 2. 시간 간격 확인 - 모든 행이 60초 간격인지 확인
gaps = data["timestamp"].diff().dt.total_seconds()
print(gaps.tolist())
print((gaps.dropna() == 60).all())

# STEP 3. CASE A - MTR 태그를 물리량·집계방식·방향으로 분해
case_a_cols = ["MTR01_VIB_RMS_H", "MTR01_CUR"]
case_a = pd.DataFrame({"tag": case_a_cols})
case_a[["equip", "phys_rest"]] = case_a["tag"].str.split("_", n=1, expand=True)
print(case_a)

# STEP 4. CASE B - HYD·FUR 태그를 설비종류·호기·물리량으로 분해
case_b_cols = ["HYD01_PRS", "HYD01_FLW", "FUR01_TMP_Z1"]
case_b = pd.DataFrame({"tag": case_b_cols})
case_b["equip_type"] = case_b["tag"].str[:3]     # HYD / FUR
case_b["no"] = case_b["tag"].str[3:5]            # 01
case_b["phys_rest"] = case_b["tag"].str.split("_", n=1).str[1]
print(case_b)

# STEP 5. 계단형 변화 컬럼 찾기 - 연속으로 같은 값이 이어지는 최대 길이를 계산
value_cols = ["MTR01_VIB_RMS_H", "MTR01_CUR", "HYD01_PRS", "HYD01_FLW", "FUR01_TMP_Z1"]


def max_repeat_run(series):
    run = best = 1
    for i in range(1, len(series)):
        if series.iloc[i] == series.iloc[i - 1]:
            run += 1
            best = max(best, run)
        else:
            run = 1
    return best


repeat_runs = {col: max_repeat_run(data[col]) for col in value_cols}
print(repeat_runs)

# STEP 6. 상한 반복 컬럼 찾기 - 최댓값과 같은 값이 연속으로 나오는 컬럼
for col in value_cols:
    at_max_run = max_repeat_run(data.loc[data[col] == data[col].max(), col])
    if at_max_run >= 3:
        print(col, "상한 반복 의심 -", at_max_run, "회 연속")

# STEP 7. 표 완성 - 컬럼별 3요소(물리량·설치위치·주기) 정리
col_summary = pd.DataFrame({
    "tag": value_cols,
    "물리량": ["진동 속도", "전류", "압력", "유량", "온도"],
    "설치위치": ["1번 모터 수평 방향", "1번 모터", "1번 유압펌프 토출측", "1번 유압펌프 토출측", "1번 가열로 1존"],
    "사양주기_초": [60, 60, 60, 60, 60],
    "실제최소변화간격_분": [1, 1, 1, 1, 3],
})
print(col_summary.to_string(index=False))

# 결과 해석
# - MTR01_VIB_RMS_H·MTR01_CUR·HYD01_FLW는 사양 주기(60초)와 실제 값 변화 간격이 일치함 -
#   "빠르게 움직이는 물리량"이라는 걸 값의 움직임만 보고도 확인할 수 있음
# - FUR01_TMP_Z1은 사양상 60초마다 저장되지만 실제로는 3분(3행)마다만 값이 바뀜(계단형 변화,
#   STEP 5의 max_repeat_run 결과가 3) - 온도는 원래 느리게 반응하는 물리량이라 저장 주기보다
#   원래 신호 자체가 느린 경우임
# - HYD01_PRS는 5~8행에서 190이 4회 연속 반복됨(STEP 6) - 값이 정말 딱 멈춘 게 실제 압력이
#   변하지 않아서인지, 센서의 측정 상한(190bar)에 걸려 더는 못 올라간 것인지는 이 표만으로는
#   구분이 안 됨 - "측정값의 한계" 개념대로, 이런 경우는 현장에 센서 사양(측정 상한이 몇
#   bar인지)을 직접 물어봐야 하는 빈칸으로 남겨 둠
