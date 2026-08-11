# =====================================================================
# [선택문제] 실습 6. 폴더에서 csv 파일만 골라내기
# =====================================================================
import os

folder = os.path.join("data", "module_practice")
files = os.listdir(folder)

csv_files = []
for file in files:
    if file.endswith(".csv"):
        csv_files.append(file)

csv_paths = []
for file in csv_files:
    csv_paths.append(os.path.join(folder, file))

print(csv_paths)  # [CSV] 목록 (csv 파일만)
