# 선택문제 종합실습
import os
import sys
import csv

# 1. 파일을 연다
file_path = os.path.join("data", "09_ict_inspection_dirty.csv")


# 헤더와 데이터행을 분리하고, 데이터가 몇 행인지 출력하는 함수를 만든다.
def print_header_and_rows(reader):
    header = reader.fieldnames
    rows = list(reader)
    print(f"헤더 : {header}")
    print(f"행 개수 : {len(rows)}")
    return header, rows


# 1단계 데이터를 설비별로 분류해, 각 설비에 몇 개의 데이터가 있는지 출력한다.
def classify_by_equipment(rows):
    sensor_dict = {}
    for row in rows:
        equipment = row.get("부품명", "(설비명없음)")
        if equipment not in sensor_dict:
            sensor_dict[equipment] = []  # 처음 보는 설비명이면 빈 리스트부터 만듦
        sensor_dict[equipment].append(row)

    for equipment, equipment_rows in sensor_dict.items():
        print(f"{equipment} : {len(equipment_rows)}개")

    return sensor_dict


# 평균 구하는 함수
def calculate_average(values):
    if not values:
        return 0
    return sum(values) / len(values)


# 최댓값 구하는 함수
def calculate_max(values):
    if not values:
        return None
    return max(values)


# 최솟값 구하는 함수
def calculate_min(values):
    if not values:
        return None
    return min(values)


# 4단계. 불량 방어
def filter_valid_measurements(equipment_rows):
    valid_values = []
    faulty_records = {}
    for row in equipment_rows:
        try:
            value = float(row.get("측정값", ""))
            lower = float(row.get("하한치", "0"))
            upper = float(row.get("상한치", "9999"))
            if value < lower or value > upper:
                raise ValueError(
                    f"범위 이탈 (측정값={value}, 하한={lower}, 상한={upper})"
                )
            valid_values.append(value)
        except (ValueError, TypeError) as e:
            faulty_records[row.get("검사ID", "Unknown")] = str(e)
            continue  # 불량 줄은 건너뛰고 다음 줄로
    return valid_values, faulty_records


try:
    # 1단계. CSV 읽기
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header, rows = print_header_and_rows(reader)

    print()  # 단계 구분용 빈 줄

    # 2단계. 조건 분류
    sensor_dict = classify_by_equipment(rows)

    # 3단계. 통계 계산 + 4단계. 불량 방어
    # (설비별로 한 번씩만 계산하면서, 5단계에 쓸 요약 줄도 같이 모아둔다)
    detail_lines = []
    total_valid = 0
    total_faulty = 0
    for equipment, equipment_rows in sensor_dict.items():
        measurement_values, faulty_lines = filter_valid_measurements(equipment_rows)

        avg = calculate_average(measurement_values)
        max_value = calculate_max(measurement_values)
        min_value = calculate_min(measurement_values)

        print(f"{equipment} - 평균: {avg:.2f}, 최대: {max_value}, 최소: {min_value}")
        if faulty_lines:
            print(f"불량: {faulty_lines}")

        total_valid += len(measurement_values)
        total_faulty += len(faulty_lines)
        detail_lines.append(
            f"{equipment} - 평균: {avg:.2f}, 최대: {max_value}, 최소: {min_value}"
        )

    # 5단계. 리포트 저장 - 루프가 다 끝난 뒤 한 번만 실행
    # 핵심 요약은 위, 세부 통계는 구분선 아래
    report_lines = []
    report_lines.append("=== ICT 검사 데이터 분석 리포트 ===")
    report_lines.append(f"전체 {len(rows)}행 · 정상 {total_valid}개 · 불량 {total_faulty}개")
    report_lines.append("-" * 30)
    report_lines.extend(detail_lines)

    report_path = os.path.join("data", "ict_report.txt")
    with open(report_path, "w", encoding="utf-8") as report_file:
        for line in report_lines:
            report_file.write(line + "\n")

    # 저장 후 다시 열어서 내용 확인
    print(f"\n리포트 저장 완료: {report_path}")
    with open(report_path, "r", encoding="utf-8") as report_file:
        print(report_file.read())

    # 6단계 통계 검증 - 설비별 통계 온도 계산, 부품별 개수 합과 전체 정상 개수가 같은지 확인
    # sensor_dict.values()는 불량까지 포함한 원본 행이라, 정상 개수를 구하려면
    # filter_valid_measurements로 한 번 더 걸러낸 valid_values의 개수를 더해야 함
    total_count_by_part = 0
    for equipment_rows in sensor_dict.values():
        valid_values, _ = filter_valid_measurements(equipment_rows)
        total_count_by_part += len(valid_values)
    print(f"부품별 개수 합: {total_count_by_part}, 전체 정상 개수: {total_valid}, 일치 여부: {total_count_by_part == total_valid}")
    
except FileNotFoundError:
    print("파일을 찾지 못 했습니다.")
    header, rows, sensor_dict = [], [], {}
