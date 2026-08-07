# =====================================================================
# 데이터 처리 파이프라인 - 종합 실습
# =====================================================================

# [문제 상황] 이 단원의 실데이터 - ICT 검사
# - ICT는 제조 부품의 전기 특성을 측정해 규격 안에 드는지 판정하는 검사 공정
# - 부품명별로 측정값·기준값·상한치/하한치를 기록 - 실제 현장 데이터에는 빈칸(결측)·형식 오류가 섞여 있음
# - 측정값이 비거나 문자·범위 밖이면 형변환·인덱스 오류가 남 - try·except로 불량 줄을 건너뛰고 견고하게 처리
# - data/09_ict_inspection_dirty.csv 파일을 그대로 사용 (열: 검사ID·부품명·측정값·기준값·상한치·하한치·검사결과)

# [개념] 종합 실습 개요 - 무엇을 만드는가
# - 배운 모든 문법(변수·조건문·반복문·함수·파일 입출력·예외처리)을 모아 완성된 분석 프로그램을 만듦
# - 읽고 정리하고 분석하고 결과를 남기는 한 줄기의 흐름을 직접 짬
# - 만들 프로그램: 설비 센서 CSV를 읽어 정리하고, 불량을 걸러내고, 통계를 내고, 리포트로 저장
# - 새 문법은 없음 - 이미 다 배운 부품을 조립해, 작동하는 한 대의 기계를 만드는 것

# [정리] 종합 실습의 성격 - 한 번에 완성하지 않는다, 단계로 쌓고 막힐 때마다 어느 단계인지 안다
# - 문법 통합: 따로 배운 문법들이 실제 문제를 풀 때 서로 어떻게 맞물려 돌아가는지 직접 체험
# - 단계 누적: 한 단계씩 쌓아 올리기 때문에 복잡해 보여도 중간에 막혀도 어느 단계인지 추적 가능
# - 포트폴리오: 완성된 분석 프로그램은 그 자체로 취업 준비 자산으로 남음

# [개념] 데이터 처리 파이프라인 설계 - 앞 단계 결과가 뒤 단계의 재료가 되는 연결 구조
# - 이 흐름을 파이프라인(pipeline)이라 부름 - 코드를 짜기 전에 흐름부터 그린다
# - 수도관과 같다: 수도관을 따라 물이 정수되듯, 지저분한 원본 데이터가 파이프라인을 거치며
#   분석 가능한 결과로 바뀜

# [정리] 파이프라인 단계별 흐름 - 읽기 -> 분류 -> 계산 -> 방어 -> 저장
# 각 단계는 앞 단계 결과를 이어받아 처리하고 다음으로 넘김
# CSV -> header, rows -> by_part -> stats -> valid -> report.txt
# STEP1 읽기: CSV 파일을 열고 파일 없음에 대비
# STEP2 분류: 부품별로 묶기 (조건문·딕셔너리)
# STEP3 계산: 평균·최대·최소 (함수로 만들기)
# STEP4 방어: 불량 데이터 거름 (예외처리 동원)
# STEP5 저장: 리포트를 파일로 기록

# [정리] 단계로 나누는 이유
# - 단계별 문법: 읽기는 파일, 분류는 딕셔너리, 방어는 예외처리 - 배운 문법이 단계마다 한 번씩 등장
# - 독립 검증: 각 단계를 따로 만들고 먼저 테스트한 뒤 붙임 - 오류가 난 단계를 찾기 쉬워짐
# - 부분 수정: 분석 항목이 늘어나도 나머지는 그대로 둠, 계산 단계만 손보면 됨 (NumPy·Pandas도
#   결국 이 단계를 빠르게 처리하는 도구)

# [강사님께 질문하기] 굳이 함수를 여러 개로 쪼개지 않고, 코드를 위에서 아래로 쭉 이어서
# 짜면 안 되나요? 결과는 똑같이 나올 것 같은데요.
# -> 답변: 결과만 보면 똑같이 나올 수 있음. 하지만 나중에 "통계 계산 방식만 바꾸고
#    싶다"거나 "파일 읽는 부분만 다른 파일로 바꾸고 싶다"는 상황이 오면, 쭉 이어진
#    코드는 어디부터 어디까지가 그 부분인지 찾아서 고치기가 어려움. 함수로 쪼개두면 그
#    함수 하나만 통째로 바꿔 끼우면 되고, 각 함수를 따로 테스트해볼 수도 있어서, 중간에
#    문제가 생겼을 때 어느 단계인지 훨씬 빨리 찾아낼 수 있음

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

# [강사님께 질문하기] 4단계에서 벗어난 값을 걸러낼 때 continue로 그냥 건너뛰면 되는데,
# 왜 굳이 raise까지 함께 쓰나요? 둘 다 결국 그 값을 안 쓰게 되는 건 같아 보이는데요.
# -> 답변: 겉으로 보이는 결과(그 값을 안 쓴다는 것)는 비슷하지만, 목적이 다름. continue는
#    "이 값은 형식 자체가 틀렸다(숫자가 아니다)"는 이미 파이썬이 알려주는 문제를 건너뛰는
#    것이고, raise는 "형식은 숫자로 멀쩡한데 우리가 정한 현실 규칙(그 부품의 허용 범위)에는
#    어긋난다"는, 파이썬은 모르고 우리만 아는 문제를 우리가 직접 알려주는 것. 두 가지를
#    구분해서 처리하면, 나중에 "형식 오류가 몇 건, 범위 오류가 몇 건"처럼 문제의 원인별로
#    따로 집계할 수 있어서 더 정확한 진단이 가능해짐

# [강사님께 질문하기] 어떤 행은 칸이 아예 부족해서 상한치·하한치 자리가 없는데, 이런 행은
# ValueError가 아니라 다른 종류의 오류가 난다면서요? 왜 종류가 다른가요?
# -> 답변: 문제의 성격이 다르기 때문. ValueError는 "칸은 있는데 그 안의 내용이 숫자로
#    바뀌지 않는다"는 문제이고, 칸이 아예 없어서 row[4]처럼 없는 위치를 꺼내려 하면
#    "애초에 그 번호의 칸 자체가 존재하지 않는다"는 전혀 다른 문제가 됨. 파이썬은 이걸
#    IndexError라는 별개의 이름으로 구분해서 알려줌. 그래서 이 함수는 ValueError뿐 아니라
#    IndexError도 함께 잡아야 칸이 부족한 행까지 안전하게 건너뛸 수 있음


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

# [강사님께 질문하기] 부품별 개수를 다 더한 값이 전체 정상 개수랑 다르게 나오는 경우가
# 실제로 있나요? 애초에 같은 데이터를 나눈 것뿐인데 왜 달라질 수 있죠?
# -> 답변: 이론적으로는 같아야 하지만, 실제로는 코드에 숨은 실수가 있으면 달라질 수
#    있음. 예를 들어 분류 단계에서 어떤 부품명을 조건문으로 놓쳐서 그 데이터가 어느
#    딕셔너리 키에도 안 들어갔거나, 반대로 같은 행이 실수로 두 번 들어갔다면 합계가
#    어긋남. 그래서 이 검증은 "내 분류 코드가 데이터를 하나도 빠뜨리거나 중복하지
#    않았다"는 것을 스스로 확인하는 장치이고, 실무에서는 이런 자기 검증 단계를 넣는
#    습관이 매우 중요하게 여겨짐


# =====================================================================
# [흔한 질문 진단] 파이프라인을 짜면서 헷갈리기 쉬운 것들
# =====================================================================

# Q1. 1단계 함수에서 파일이 없을 때 빈 리스트를 반환하게 했는데, 그냥 프로그램을
#     즉시 종료시키면 안 되나요?
# -> A. 그렇게 할 수도 있지만, 빈 결과를 반환하는 방식은 그 이후 단계(분류, 통계 등)가
#       "데이터가 0개인 경우"를 자연스럽게 처리하도록 만들어 프로그램 전체가 죽지 않고
#       "처리할 데이터가 없습니다" 같은 안내까지 이어서 보여줄 수 있음. 파일 하나가
#       없다고 프로그램 전체가 즉시 멈춰버리면, 여러 파일을 순서대로 처리하려는 상황에서
#       나머지 파일들까지 다 처리 못 하게 되는 문제가 생김

# Q2. 3단계 통계 함수가 값이 하나도 없으면 0이 아니라 None을 반환하게 했는데, 왜
#     0을 쓰면 안 되나요?
# -> A. 0은 "평균이 진짜로 0이다"라는 결과와 "계산할 데이터가 아예 없다"는 상황을
#       구분하지 못하게 만듦. 만약 0을 반환하면 나중에 이 값을 보는 사람이 "측정값이
#       0이었구나"라고 착각할 수 있음. None은 "값이 없다"는 것을 명확하게 표시하는
#       파이썬의 특별한 값이라, 이후 코드에서 `if 결과 is None:`처럼 확인해 "데이터가
#       없어서 계산 못 함"이라고 정확하게 구분해 처리할 수 있음

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# rows = [["E2", "65.0"], ["E2", "off"], ["E2", ""]]
# valid_count = 0
# for row in rows:
#     try:
#         value = float(row[1])
#     except ValueError:
#         continue
#     valid_count += 1
# print(valid_count)
# 정답: 1
# ("off"와 ""는 둘 다 float로 못 바꿔 ValueError가 나서 건너뛰고, "65.0" 하나만
#  성공적으로 세어짐)
