# =====================================================================
# [선택문제] 실습 3. os로 폴더 목록 살펴보기
# =====================================================================
import os

print(os.getcwd())  # 현재 작업 폴더 경로

folder = "practice_data"
files = os.listdir(folder)

for file in files:
    print(file)  # 폴더 안 파일들

for file in files:
    if file.endswith(".csv"):
        print(file)  # .csv 파일만
