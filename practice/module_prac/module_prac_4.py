# =====================================================================
# [기본문제] 실습 4. os로 파일 존재 확인하기
# =====================================================================
import os

folder = "data"
file_path = os.path.join(folder, "08_press.csv")

exists = os.path.exists(file_path)
print(exists)  # True 또는 False

if exists:
    print("파일 있음")
else:
    print("파일 없음")
