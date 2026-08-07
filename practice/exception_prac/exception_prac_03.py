# 실습3. 여러 파일 묶어 처리하기

file_names = ["08_press.csv", "09_ict.csv", "09_ict_dirty.csv"]

for f_name in file_names:
    try:
        f = open(f"data/{f_name}", "r", encoding="utf-8")
    except FileNotFoundError:
        continue
    finally:
        f.close()
    print(f"{f_name} 파일 열기 성공")
