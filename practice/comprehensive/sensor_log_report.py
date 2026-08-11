# =====================================================================
# 종합 실습: 센서 로그 정리 리포트 만들기
# =====================================================================

# [정리] 정리 결과를 f-string으로 출력 (지금까지 배운 내용의 결론)
# 정리(strip/lower/replace/split) -> f-string 출력이 완성형
# 정리는 strip/lower/replace/split/join 같은 도구, 출력은 f-string이 담당


print("===================== 실습 4. 센서 로그 한 줄 정리 리포트 만들기 =====================")
# 목표: 지저분한 센서 로그 한 줄을 정리해 f-string 한 줄 판단 리포트로 출력
# 단계:
#   ① 문자열 '  5 , sensor_2 , WARNING , 0.78912  ' 저장
#   ② strip·split 후 각 조각 정리, 소수점은 두 번째 자리까지
# 예상 결과: [센서 sensor_2] 상태 warning, 측정값 0.79

raw = "  5 , sensor_2 , WARNING , 0.78912  "
parts = raw.strip().split(",")       # 앞뒤 공백 제거 후 쉼표로 분리
sid = parts[1].strip()               # 'sensor_2'
status = parts[2].strip().lower()    # 'warning'
value = float(parts[3].strip())      # 0.78912

print(f"[센서 {sid}] 상태 {status}, 측정값 {value:.2f}")

# =====================================================================
# [추가 학습] 응용 - 로그가 여러 줄일 때는 반복문(for)으로 한 번에 처리
# =====================================================================
# 실무에서는 로그가 한 줄이 아니라 여러 줄로 쌓여있는 경우가 대부분
# -> 지금 배운 정리 로직을 함수로 만들고, for문으로 여러 줄에 반복 적용

raw_logs = [
    "  5 , sensor_2 , WARNING , 0.78912  ",
    "  6 , sensor_1 , Normal  , 0.31500  ",
    "  7 , SENSOR_3 , critical, 0.95321  ",
]


def make_report(raw_log: str) -> str:
    """센서 로그 한 줄(raw)을 정리해서 리포트 문장으로 반환"""
    parts = raw_log.strip().split(",")
    sid = parts[1].strip().lower()
    status = parts[2].strip().lower()
    value = float(parts[3].strip())
    return f"[센서 {sid}] 상태 {status}, 측정값 {value:.2f}"


for log in raw_logs:
    print(make_report(log))

# 실행 결과:
# [센서 sensor_2] 상태 warning, 측정값 0.79
# [센서 sensor_1] 상태 normal, 측정값 0.32
# [센서 sensor_3] 상태 critical, 측정값 0.95


# =====================================================================
# [정리] 텍스트 도구 전체 요약
# =====================================================================
# 목적          | 도구
# --------------|------------------------------------------------
# 만들기·출력  | 따옴표, print, f-string
# 형변환       | str, int, float
# 꺼내기       | 인덱싱, 슬라이싱, split
# 확인·다듬기  | len, in, count, find / strip, lower, replace, join
#
# 정리 흐름: 공백제거(strip) -> 통일·치환(lower, replace) -> 나누기(split)
#           -> 조각정리(strip) -> 합치기(join) -> f-string으로 결과 출력
