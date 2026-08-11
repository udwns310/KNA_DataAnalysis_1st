# =====================================================================
# [선택문제] (PART 3) 실습 3. 구체적 예외로 입력 검증하기
# =====================================================================
def safe_divide(text, divisor):
    try:
        number = int(text)
        return number / divisor
    except ValueError:
        print(f"'{text}'는 숫자가 아닙니다")
    except ZeroDivisionError:
        print("0으로는 나눌 수 없습니다")


# print(safe_divide("100", 5))  # 20.0
# print(safe_divide("스물", 5))  # 안내 후 None
print(safe_divide("100", 0))  # 안내 후 None


def dict_warning(dict_obj, key):
    try:
        return dict_obj[key]
    except KeyError:
        print(f"'{key}'는 딕셔너리에 없습니다")


# print(dict_warning({"a": 1, "b": 2}, "a"))  # 1
# print(dict_warning({"a": 1, "b": 2}, "c"))
