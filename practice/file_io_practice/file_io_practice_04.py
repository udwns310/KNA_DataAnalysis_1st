# =====================================================================
# [기본문제] 실습 5. csv.writer로 CSV 쓰기
# =====================================================================
import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
result_path = os.path.join(DATA_DIR, "result.csv")

with open(result_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["설비ID", "전류"])
    writer.writerow(["PRESS-01", 78.2])
    writer.writerow(["PRESS-02", 95.4])

with open(result_path, "r", encoding="utf-8") as f:
    print(f.read())  # 새 CSV에 헤더+데이터 행이 저장됨
