# =====================================================================
# 데이터 처리 파이프라인 - 종합 실습
# =====================================================================

import os
import csv

dirty_csv_path = os.path.join("data", "09_ict_inspection_dirty.csv")


print("\n===================== 1단계. CSV 읽기 =====================")
# 목표: 검사 CSV를 안전하게 열어 헤더와 데이터를 분리한다 (파일 없음에도 대비)
# 만들 것: 헤더와 데이터 행을 분리하고, 데이터가 몇 행인지 출력하는 함수 - 이후 단계에서 재사용
# 예외 처리: 파일이 없으면 FileNotFoundError - 안내 메시지 출력 후 빈 결과(빈 header, 빈 rows) 반환
# 예상 결과: 헤더 1줄과 데이터 행이 분리되고, 데이터 행 수가 출력된다
def read_ict_csv(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                if len(row) > 0:
                    rows.append(row)
            return header, rows
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {path}")
        return [], []


header, rows = read_ict_csv(dirty_csv_path)
print(header)  # ['검사ID', '부품명', '측정값', '기준값', '상한치', '하한치', '검사결과']
print(len(rows))

missing_header, missing_rows = read_ict_csv(os.path.join("data", "09_없는파일.csv"))
print(missing_header, missing_rows)  # [] [] - 파일이 없어도 프로그램은 멈추지 않음


print("\n===================== 2단계. 조건 분류 =====================")
# 목표: 읽어온 데이터를 부품별로 나누어 딕셔너리에 담는다
# 만들 것: 1단계 데이터를 부품별로 분류해, 각 부품에 몇 개의 데이터가 있는지 출력
# 핵심 패턴: 처음 보는 부품명이면 빈 리스트를 먼저 만들고, 거기에 행을 추가
# 예상 결과: 부품(E2/F2 등)별로 행이 묶인 딕셔너리가 만들어진다
def classify_by_part(rows):
    by_part = {}
    for row in rows:
        part_name = row[1]
        if part_name not in by_part:
            by_part[part_name] = []
        by_part[part_name].append(row)
    return by_part


by_part = classify_by_part(rows)
for part_name in by_part:
    print(part_name, len(by_part[part_name]))  # E2 4 / F2 4 / B2 4 / A2 4 / D2 3 / (빈 이름) 2


print("\n===================== 3단계. 통계 함수 =====================")
# 목표: 평균·최대·최소를 계산하는 함수를 만든다 (어떤 데이터에도 재사용 가능하게)
# 만들 것: 특정 칸의 숫자 데이터로 개수, 평균, 최솟값, 최댓값을 계산하는 함수
# 주의할 점: 숫자가 아닌 값은 건너뛴다 / 값이 하나도 없으면 None을 반환해 0으로 나누는 오류를 막는다
# 예상 결과: 측정값의 평균·최대·최소가 계산되고, 값이 없으면 None이 반환된다
def calc_stats(values):
    numbers = []
    for v in values:
        try:
            numbers.append(float(v))
        except ValueError:
            continue
    if len(numbers) == 0:
        return None
    count = len(numbers)
    average = sum(numbers) / count
    return {"count": count, "average": average, "min": min(numbers), "max": max(numbers)}


sample_stats = calc_stats(["0.0", "2939.61", "결측", "4366.23"])
print(sample_stats)  # {'count': 3, 'average': 2435.28, 'min': 0.0, 'max': 4366.23}

empty_stats = calc_stats(["결측", ""])
print(empty_stats)  # None - 값이 하나도 없으면 0으로 나누는 대신 None을 반환


print("\n===================== 4단계. 불량 방어 =====================")
# 목표: 불량 데이터를 걸러내고, 범위 밖 값은 raise로 차단한다 (예외처리 기법 총동원)
# 만들 것: 측정값을 처리하며 숫자로 못 바꾸는 값·칸이 부족한 행·정상 범위를 벗어난 값을 모두 걸러낸다
# 불량 줄은 번호와 이유를 함께 기록한다 - 정상 범위는 그 행 자신의 상한치·하한치 칸으로 판단한다
# 한 함수에 모이는 것: try-except · continue · raise · as e (그리고 칸이 부족할 때 나는 IndexError)
# 예상 결과: 정상 범위를 벗어난 행은 제외되고, 남은 정상 행만 모인다
def check_measurement_range(value, lower, upper):
    if value < lower or value > upper:
        raise ValueError(f"허용범위({lower}~{upper}) 밖의 값: {value}")
    return value


def defend_measurement(rows):
    valid_rows = []
    bad_log = []
    for i, row in enumerate(rows):
        try:
            value = float(row[2])
            upper = float(row[4])
            lower = float(row[5])
            check_measurement_range(value, lower, upper)
        except (ValueError, IndexError) as e:
            bad_log.append((i, str(e)))
            continue
        valid_rows.append(row)
    return valid_rows, bad_log


valid_rows, bad_log = defend_measurement(rows)
print(len(valid_rows))
for entry in bad_log:
    print(entry)  # (줄번호, 이유) - 결측·형식오류·범위이탈·칸부족이 뒤섞여 나옴


print("\n===================== 5단계. 리포트 저장 =====================")
# 목표: 분석 결과를 리포트 형식으로 정리해 txt 파일로 저장한다
# 만들 것: 4단계까지의 결과를 리포트 형식으로 정리해 txt 파일에 저장, 저장 후 다시 열어 확인
# 작성 방식: 리포트 줄들을 리스트에 차곡차곡 모은 뒤, 마지막에 반복문으로 한 번에 파일에 쓴다
# 좋은 리포트의 원칙: 핵심 먼저 / 단위 붙이기 / 구분선 활용
# 예상 결과: 리포트 문자열이 파일로 저장된다
def build_report(total_rows, valid_rows, bad_log):
    measurement_values = []
    for row in valid_rows:
        measurement_values.append(row[2])
    stats = calc_stats(measurement_values)

    lines = []
    lines.append("=== ICT 검사 데이터 분석 리포트 ===")
    lines.append(f"전체 {total_rows}행 · 정상 {len(valid_rows)}개 · 불량 {len(bad_log)}개")
    lines.append("-" * 30)
    if stats is not None:
        lines.append(f"측정값 평균 - {stats['average']:.2f}")
        lines.append(f"측정값 최고 - {stats['max']:.2f}")
        lines.append(f"측정값 최저 - {stats['min']:.2f}")
    return lines


report_lines = build_report(len(rows), valid_rows, bad_log)

report_path = os.path.join("data", "09_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    for line in report_lines:
        f.write(line + "\n")

with open(report_path, "r", encoding="utf-8") as f:
    print(f.read())


print("\n===================== 6단계. 통계 검증 =====================")
# 목표: 부품별 통계를 따로 내어 전체와 비교하고, 개수의 합이 맞는지 검증한다
# 만들 것: 2단계 딕셔너리와 3단계 함수를 재사용해 부품별 측정값 통계를 계산
# 왜 검증하는가: 숫자가 맞아떨어지면 파이프라인이 데이터를 빠뜨리거나 중복 없이 정확히 처리했다는 증거
# 예상 결과: 부품별 개수의 합과 전체 정상 개수가 같으면 True가 출력된다
by_part_valid = classify_by_part(valid_rows)

part_stats = {}
total_by_part = 0
for part_name in by_part_valid:
    part_rows = by_part_valid[part_name]
    part_values = []
    for row in part_rows:
        part_values.append(row[2])
    stats = calc_stats(part_values)
    part_stats[part_name] = stats
    total_by_part += stats["count"]
    print(part_name, stats)

print(total_by_part == len(valid_rows))  # True