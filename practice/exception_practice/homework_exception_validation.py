# =====================================================================
# 20260807 실습과제 - PART 2 견고한 예외처리 + 데이터 파이프라인 종합실습
# =====================================================================
import os
import csv

print("\n===== 종합실습: 데이터 파이프라인 =====")

dirty_csv_path = os.path.join("data", "09_ict_inspection_dirty.csv")

# --- 1단계. CSV 읽기 --------------------------------------------------
# 목표: CSV를 안전하게 열어 헤더와 데이터를 분리, 파일이 없어도 멈추지 않기
def read_ict_csv(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = [row for row in reader if row]
            return header, rows
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {path}")
        return [], []

header, rows = read_ict_csv(dirty_csv_path)
print(f"[1단계] 헤더: {header}")
print(f"[1단계] 데이터 행 수: {len(rows)}")

# --- 2단계. 조건 분류 --------------------------------------------------
# 목표: 부품별로 나누어 딕셔너리에 담기 (처음 보는 부품이면 빈 리스트부터 생성)
def classify_by_part(rows):
    by_part = {}
    for row in rows:
        part_name = row[1]
        if part_name not in by_part:
            by_part[part_name] = []
        by_part[part_name].append(row)
    return by_part

by_part = classify_by_part(rows)
for part_name, part_rows in by_part.items():
    print(f"[2단계] {part_name}: {len(part_rows)}개")

# --- 3단계. 통계 함수 --------------------------------------------------
# 목표: 개수·평균·최솟값·최댓값 계산, 숫자 아닌 값은 건너뛰고, 값이 없으면 None
def calc_stats(values):
    numbers = []
    for v in values:
        try:
            numbers.append(float(v))
        except ValueError:
            continue
    if not numbers:
        return None
    return {
        "count": len(numbers),
        "average": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers),
    }

sample_values = [row[2] for row in rows]
print(f"[3단계] 측정값 전체 통계: {calc_stats(sample_values)}")

# --- 4단계. 불량 방어 --------------------------------------------------
# 목표: 숫자 변환 실패·범위 이탈 값을 raise로 걸러내고, 번호와 이유를 기록
def check_range(value, lower, upper):
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
            check_range(value, lower, upper)
        except (ValueError, IndexError) as e:
            bad_log.append((i, str(e)))
            continue
        valid_rows.append(row)
    return valid_rows, bad_log

valid_rows, bad_log = defend_measurement(rows)
print(f"[4단계] 정상 {len(valid_rows)}개 / 불량 {len(bad_log)}개")
for entry in bad_log:
    print(f"[4단계] 불량 - {entry}")

# --- 5단계. 리포트 저장 ------------------------------------------------
# 목표: 결과를 리포트 형식(txt)으로 저장하고, 다시 열어 내용을 확인
def build_report(total_rows, valid_rows, bad_log):
    stats = calc_stats([row[2] for row in valid_rows])
    lines = [
        "=== ICT 검사 데이터 분석 리포트 ===",
        f"전체 {total_rows}행 · 정상 {len(valid_rows)}개 · 불량 {len(bad_log)}개",
        "-" * 30,
    ]
    if stats:
        lines.append(f"측정값 평균 - {stats['average']:.2f}")
        lines.append(f"측정값 최고 - {stats['max']:.2f}")
        lines.append(f"측정값 최저 - {stats['min']:.2f}")
    return lines

report_lines = build_report(len(rows), valid_rows, bad_log)
report_path = os.path.join("data", "homework_0807_report.txt")
with open(report_path, "w", encoding="utf-8") as file:
    for line in report_lines:
        file.write(line + "\n")

with open(report_path, "r", encoding="utf-8") as file:
    print(f"[5단계] 저장된 리포트:\n{file.read()}")

# --- 6단계. 통계 검증 --------------------------------------------------
# 목표: 부품별 통계를 내어 개수의 합이 전체 정상 개수와 맞는지 검증
by_part_valid = classify_by_part(valid_rows)
total_by_part = 0
for part_name, part_rows in by_part_valid.items():
    stats = calc_stats([row[2] for row in part_rows])
    total_by_part += stats["count"]
    print(f"[6단계] {part_name}: {stats}")

print(f"[6단계] 부품별 합계 == 전체 정상 개수? {total_by_part} {total_by_part == len(valid_rows)}")
