# =====================================================================
# [선택문제] 실습 4. 센서 분석 함수 세트 만들기
# =====================================================================
def get_average(values):
    return sum(values) / len(values)

def judge_status(avg, limit=90):
    if avg > limit:
        return "점검필요"
    return "정상"

sensor_avg = get_average([80, 90, 85])
final_status = judge_status(sensor_avg)
print(sensor_avg, final_status)  # 85.0 정상
