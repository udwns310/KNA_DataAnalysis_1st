# # print("real" == "real")  # True
# # print("real" != "Real")  # True
# # print(5 > 3)  # True
# # print(5 < 3)  # False
# # print(5 >= 3)  # True
# # print(5 <= 3)  # False
# # print(True > False)  # True - True는 1, False는 0으로 간주되어 비교됨
# # print(True < False)  # False
# # print("what" > "when")  # False - 문자열 비교는 사전순으로 이루어짐
# # print("what" < "when")  # True4

# # temp = 85
# # new_temp = (temp >= 60 and temp <= 90)
# # print(new_temp)  # True

# # pressure = 5
# # new_pressure = (pressure > 3 and pressure < 7)
# # print(new_pressure)  # True

# # print(new_temp and new_pressure)  # True

# # stock = 100
# # print(stock)  # 100
# # stock += 50
# # print(stock)  # 150
# # stock -= 30
# # print(stock)  # 120
# # stock += 5
# # print(stock)  # 125

# # total = 500
# # bad = 23
# # print(bad/total * 100)  # 4.6 - 불량률

# # run_time = 21
# # all_time = 24
# # print(run_time/all_time * 100)  # 87.5 - 가동률

# run_time = 500
# run_hour = run_time // 60
# run_minute = run_time % 60
# print(run_hour, run_minute)  # 8 20 - 8시간 20분

# material = 47
# box = 6
# print((material + box - 1) // box)  # 8 - 박스에 담을 수 있는 재료의 개수 

name = input("이름을 입력하세요: ")
print("안녕하세요 " + name + "님!")  # 안녕하세요, 최영준님!

birth_year = int(input("태어난 연도를 입력하세요: "))
age = 2026 - birth_year
print("당신의 나이는", age, "세 입니다.")  

name = input("이름을 입력하세요: ")
city = input("사는 도시를 입력하세요: ")
print(name, city)

a = int(input("첫 번째 숫자를 입력하세요: "))
b = int(input("두 번째 숫자를 입력하세요: "))
print(a + b)
print(a - b)
print(a * b)
print(a / b)

temp = int(input("온도를 입력하세요: "))
print("80도 초과", temp > 80)
print("0도 이상", temp >= 0)

score_1 = int(input("첫 번째 점수를 입력하세요: "))
score_2 = int(input("두 번째 점수를 입력하세요: "))
score_3 = int(input("세 번째 점수를 입력하세요: "))
average_score = (score_1 + score_2 + score_3) / 3
print("평균 점수 60점 이상", average_score >= 60)

country = str(input("거주 국가를 입력하세요: "))
city = str(input("거주 도시를 입력하세요: "))
print(country + "의 " + city + "에 사시는군요!")



