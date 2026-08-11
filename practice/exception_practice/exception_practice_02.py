# 실습 2. 반복문에서 불량 줄 건너뛰기

my_list = [
    "12.3",
    "45.6",
    "78.9",
    "영크크",
    "32.1",
    "53.2",
    "abc",
    "99.9",
    "0.1",
    "23.4",
    "56.7",
    "89.0",
    "12.3",
    "45.6",
    "78.9",
    "늙크크",
    "32.1",
    "53.2",
    "abc",
    "99.9",
]

sum_list = 0
for text in my_list:
    try:
        my_number = float(text)
        sum_list += my_number
    except ValueError:
        continue

print(f"합계 : {sum_list}")
