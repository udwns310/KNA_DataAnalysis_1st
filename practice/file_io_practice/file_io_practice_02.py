# =====================================================================
# [기본문제] 실습 3. a 모드로 기록 이어붙이기
# =====================================================================
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
log_path = os.path.join(DATA_DIR, "check_log.txt")

with open(log_path, "w", encoding="utf-8") as f:
    f.write("1번 설비 점검 완료\n")

with open(log_path, "a", encoding="utf-8") as f:
    f.write("2번 설비 점검 완료\n")

with open(log_path, "r", encoding="utf-8") as f:
    print(f.read())  # 기존 내용 + 새 기록이 함께 남음
