# 실습 1. finally로 파일 안전하게 닫기

try:
    f = open("data/test.csv", "w", encoding="utf-8")
    f.write("테스트")  
    temp = int("문제없나?")  
except ValueError: 
    print("문자열을 숫자로 바꿀 수 없습니다")
finally:
    print(f.close())  # close() 함수는 None을 반환하니까 확인 가능