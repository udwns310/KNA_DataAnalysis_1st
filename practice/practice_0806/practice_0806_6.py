# =====================================================================
# [선택문제] 실습 6. CSV 읽어 조건 저장하기
# =====================================================================
import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
source_path = os.path.join(DATA_DIR, "press.csv")

with open(source_path, "w", encoding="utf-8", newline="") as f:
    f.write("설비ID,전류\n")
    f.write("PRESS-01,78.2\n")
    f.write("PRESS-02,95.4\n")
    f.write("PRESS-03,92.1\n")
    f.write("PRESS-04,80.0\n")

filtered_rows = []
with open(source_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # 헤더는 건너뛰기
    for row in reader:
        if float(row[1]) > 90:
            filtered_rows.append(row)

over_path = os.path.join(DATA_DIR, "over_90.csv")
with open(over_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(filtered_rows)

with open(over_path, "r", encoding="utf-8") as f:
    print(f.read())  # 기준(90) 초과 센서만 담긴 새 CSV
