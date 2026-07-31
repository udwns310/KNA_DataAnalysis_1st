# =====================================================================
# 종합 실습 2. 실시간 측정값 입력 시스템
# 요구사항 자세히는 practice_guide.md 참고
# =====================================================================

# 이 실습은 사용자한테 입력받는 거라 미리 주는 데이터 없음
# while로 계속 입력받다가 q 입력하면 종료 > 통계 출력

LIMIT = 100  # 임계값 (100 초과 시 즉시 경고)
measurements = []
limit_count = 0
print("=== 실시간 측정값 입력 시스템 ===")
print("측정값을 입력하세요. 종료하려면 q 입력.")
while True:
    measurement = input("측정값: ")
    if measurement == "q":
        break
    value = float(measurement)
    measurements.append(value)
    if value > LIMIT:
        limit_count += 1
        print(f"  🚨 임계값({LIMIT}) 초과! 현재까지 초과 {limit_count}회")
print("-" * 40)
if len(measurements) == 0:
    print("입력된 측정값이 없습니다.")
else:
    print(f"총 입력 개수: {len(measurements)}개")
    max_value = measurements[0]
    min_value = measurements[0]
    for value in measurements:
        if value > max_value:
            max_value = value
        if value < min_value:
            min_value = value
    print(f"최댓값: {max_value} / 최솟값: {min_value}")
    avg_value = sum(measurements) / len(measurements)
    print(f"평균값: {round(avg_value, 2)}")
    print(f"임계값 초과 개수: {limit_count}개")
    count_above_avg = 0
    for value in measurements:
        if value > avg_value:
            count_above_avg += 1
    print(f"평균 초과 개수: {count_above_avg}개")
    measurements.sort(reverse=True)
    print(f"상위 3개 값: {measurements[:3]}")


# TODO 1. while로 "측정값: " 계속 입력받기, q면 break
#         (입력값은 숫자 아니면 q 라고 가정)
#         값은 리스트에 .append() 로 모으기


# TODO 2. 입력값이 LIMIT 초과하면 즉시 경고 + 지금까지 초과 횟수 출력


# TODO 3. q로 끝난 뒤:
#   - 입력값이 하나도 없으면 "입력된 측정값이 없습니다." 출력하고 끝
#   - 값이 있으면 아래 출력
#       · 총 입력 개수 (len)
#       · 최댓값 / 최솟값 (반복문으로 직접 찾기)
#       · 평균값 (round, 소수 둘째 자리)
#       · 임계값 초과 개수
#       · 평균보다 큰 값의 개수  > 평균 먼저 구한 뒤 리스트 다시 돌기
#       · 상위 3개 값 (.sort(reverse=True) 후 슬라이싱 [:3])


# 도전) q 대신 그냥 Enter(빈 입력 "") 치면 무시하고 다시 받기
