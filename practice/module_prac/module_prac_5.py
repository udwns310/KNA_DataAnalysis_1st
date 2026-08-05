# =====================================================================
# [기본문제] 실습 5. datetime으로 점검 기록 남기기
# =====================================================================
import os
from datetime import datetime

folder = "practice_data"
file_count = len(os.listdir(folder))

now = datetime.now()
print(f"파일 {file_count}개, 점검 시각 {now}")  # 파일 N개, 점검 시각 2026-... 형식 한 줄
