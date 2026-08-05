# =====================================================================
# [선택문제] 실습 5. 센서 통계 함수 만들기
# =====================================================================
def sensor_stats(values):
    return min(values), max(values), sum(values) / len(values)

low, high, avg = sensor_stats([78, 85, 92])
print(low, high, avg)  # 78 92 85.0
