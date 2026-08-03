print(
    "\n===================== 실습 2. update로 여러 값 한 번에 갱신하기 ====================="
)
sensor_dict = {"온도": 78, "진동": 0.5, "유량": 95}
new_sensor_dict = {"온도": 82, "압력": 95}
sensor_dict.update(new_sensor_dict)
print(sensor_dict)  # {'온도': 82, '진동': 0.5, '유량': 95, '압력': 95}
del sensor_dict["진동"]
print("센서 수:", len(sensor_dict))  # 센서 수: 3

print("\n===================== 실습 3. 딕셔너리에서 통계 내기 =====================")
sensor_name_dict = {"온도": 78, "진동": 0.5, "유량": 95}
sensor_measure_dict = {"온도": 78, "진동": 0.5, "유량": 95}
sum_value = 0
for name, value in sensor_measure_dict.items():
    sum_value += value
avg_value = sum_value / len(sensor_measure_dict)
print(f"평균: {avg_value:.1f}")  # 57.833333333333336

print("\n===================== 실습 4. zip으로 센서명-값 매핑하기 =====================")
sensor_name_dict = {"온도": 78, "진동": 0.5, "유량": 95}
sensor_measure_dict = {"온도": 78, "진동": 0.5, "유량": 95}
new_dict = dict(zip(sensor_name_dict.keys(), sensor_measure_dict.values()))
for name, value in new_dict.items():
    print(f"{name}: {value}")

print(
    "\n===================== 실습 5. 임계값으로 경고 센서 분류하기 ====================="
)
measure_dict = {"온도": 95, "압력": 88}
threshold_dict = {"온도": 90, "압력": 90}
warning_sensors = []
for name, value in measure_dict.items():
    if value > threshold_dict[name]:
        warning_sensors.append(name)
print("경고 센서:", warning_sensors)  # 경고 센서: ['온도']

print("\n===================== 실습 6. 중첩 딕셔너리로 설비 관리하기 =====================")
doubled_dict = {"1번 펌프": {"온도": 78, "압력": 90, "상태": "정상"}, "2번 펌프": {"온도": 82, "압력": 95, "상태": "경고"}}
print(doubled_dict["1번 펌프"]["온도"])  # 78
for name, measure_dict in doubled_dict.items():
    if measure_dict["상태"] == "경고":
        print(f"{name} 점검 필요")

print("\n===================== 실습 7. 표 데이터를 딕셔너리로 변환하기 =====================")
sensor_list =["온도,78", "압력,90", "진동,0.5"]
new_sensor_dict = {}
for sensor in sensor_list:
    name, value = sensor.split(",")
    new_sensor_dict[name] = float(value)
print(new_sensor_dict)  # {'온도': 78.0, '압력': 90.0, '진동': 0.5}

print("\n===================== 실습 8. 센서 데이터 통합 정리 =====================")
sensor_measure_dict = {"온도": 90, "압력": 98, "진동": 92.5}
limits_dict = {"온도": 87, "압력": 90, "진동": 95}
final_avg = sum(sensor_measure_dict.values()) / len(sensor_measure_dict)
print(f"평균: {final_avg:.1f}")  # 평균: 93.5

caution_sensors = set()
for name, value in sensor_measure_dict.items():
    if value > limits_dict[name]:
        caution_sensors.add(name)
print("주의 센서:", sorted(caution_sensors))  # 주의 센서: ['압력', '온도']
