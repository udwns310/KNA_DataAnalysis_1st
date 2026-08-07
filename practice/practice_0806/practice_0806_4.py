# =====================================================================
# [기본문제] 실습 4. csv.reader로 CSV 읽기
# =====================================================================
import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
csv_path = os.path.join(DATA_DIR, "press.csv")

with open(csv_path, "w", encoding="utf-8", newline="") as f:
    f.write("설비ID,전류\n")
    f.write("PRESS-01,78.2\n")
    f.write("PRESS-02,95.4\n")

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # 각 행이 리스트로 출력
