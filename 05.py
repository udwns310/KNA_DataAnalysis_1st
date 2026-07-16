# print("real" == "real")  # True
# print("real" != "Real")  # True
# print(5 > 3)  # True
# print(5 < 3)  # False
# print(5 >= 3)  # True
# print(5 <= 3)  # False
# print(True > False)  # True - True는 1, False는 0으로 간주되어 비교됨
# print(True < False)  # False
# print("what" > "when")  # False - 문자열 비교는 사전순으로 이루어짐
# print("what" < "when")  # True4

# temp = 85
# new_temp = (temp >= 60 and temp <= 90)
# print(new_temp)  # True

# pressure = 5
# new_pressure = (pressure > 3 and pressure < 7)
# print(new_pressure)  # True

# print(new_temp and new_pressure)  # True

# stock = 100
# print(stock)  # 100
# stock += 50
# print(stock)  # 150
# stock -= 30
# print(stock)  # 120
# stock += 5
# print(stock)  # 125

# total = 500
# bad = 23
# print(bad/total * 100)  # 4.6 - 불량률

# run_time = 21
# all_time = 24
# print(run_time/all_time * 100)  # 87.5 - 가동률

run_time = 500
run_hour = run_time // 60
run_minute = run_time % 60
print(run_hour, run_minute)  # 8 20 - 8시간 20분

material = 47
box = 6
print((material + box - 1) // box)  # 8 - 박스에 담을 수 있는 재료의 개수 