# # # # print("real" == "real")  # True
# # # # print("real" != "Real")  # True
# # # # print(5 > 3)  # True
# # # # print(5 < 3)  # False
# # # # print(5 >= 3)  # True
# # # # print(5 <= 3)  # False
# # # # print(True > False)  # True - True는 1, False는 0으로 간주되어 비교됨
# # # # print(True < False)  # False
# # # # print("what" > "when")  # False - 문자열 비교는 사전순으로 이루어짐
# # # # print("what" < "when")  # True4

# # # # temp = 85
# # # # new_temp = (temp >= 60 and temp <= 90)
# # # # print(new_temp)  # True

# # # # pressure = 5
# # # # new_pressure = (pressure > 3 and pressure < 7)
# # # # print(new_pressure)  # True

# # # # print(new_temp and new_pressure)  # True

# # # # stock = 100
# # # # print(stock)  # 100
# # # # stock += 50
# # # # print(stock)  # 150
# # # # stock -= 30
# # # # print(stock)  # 120
# # # # stock += 5
# # # # print(stock)  # 125

# # # # total = 500
# # # # bad = 23
# # # # print(bad/total * 100)  # 4.6 - 불량률

# # # # run_time = 21
# # # # all_time = 24
# # # # print(run_time/all_time * 100)  # 87.5 - 가동률

# # # run_time = 500
# # # run_hour = run_time // 60
# # # run_minute = run_time % 60
# # # print(run_hour, run_minute)  # 8 20 - 8시간 20분

# # # material = 47
# # # box = 6
# # # print((material + box - 1) // box)  # 8 - 박스에 담을 수 있는 재료의 개수 

# # name = input("이름을 입력하세요: ")
# # print("안녕하세요 " + name + "님!")  # 안녕하세요, 최영준님!

# # birth_year = int(input("태어난 연도를 입력하세요: "))
# # age = 2026 - birth_year
# # print("당신의 나이는", age, "세 입니다.")  

# # name = input("이름을 입력하세요: ")
# # city = input("사는 도시를 입력하세요: ")
# # print(name, city)

# # a = int(input("첫 번째 숫자를 입력하세요: "))
# # b = int(input("두 번째 숫자를 입력하세요: "))
# # print(a + b)
# # print(a - b)
# # print(a * b)
# # print(a / b)

# # temp = int(input("온도를 입력하세요: "))
# # print("80도 초과", temp > 80)
# # print("0도 이상", temp >= 0)

# # score_1 = int(input("첫 번째 점수를 입력하세요: "))
# # score_2 = int(input("두 번째 점수를 입력하세요: "))
# # score_3 = int(input("세 번째 점수를 입력하세요: "))
# # average_score = (score_1 + score_2 + score_3) / 3
# # print("평균 점수 60점 이상", average_score >= 60)

# # country = str(input("거주 국가를 입력하세요: "))
# # city = str(input("거주 도시를 입력하세요: "))
# # print(country + "의 " + city + "에 사시는군요!")



# # == 실습 - 여러줄 , 이스케이프 다루기
# notice = """설비 점검 안내
# 1. 전원 확인
# 2. 센서 점검
# """
# print(notice)

# notice_escape = "설비 점검 안내\n1. 전원 확인\n2. 센서 점검"
# print(notice_escape)

# # == 실습 - 설비 라벨 문자열 만들기
# code = "MOTOR_A"
# state = "정상"
# date = "2026-07-16"
# print(code, state, date, sep=" / ")  # MOTOR_A / 정상 / 2026-07-16

# # == 실습 - 설비 정보 출력 카드 만들기
# code = "PUMP_A"
# state = "정상"
# hours = 1200
# date = "2026-07-16"
# card = "설비 코드: " + code + "\n상태: " + state + "\n가동 시간: " + str(hours) + "시간\n점검 일자: " + date
# print(card)

# abc = "abcdefghijklmnopqrstuvwxyz"
# print(abc[-2] + abc[14] + abc[-6] + abc[13] + abc[6] + " " + abc[9] + abc[20] + abc[13]) # young jun

# # 실습 - 음수 인덱스로 뒤에서 꺼내기
# word = "PYTHON"
# print(word[-1])  # N
# print(word[-2])  # O

# # 실습 - [start:end]로 구간 자르기
# word = "PYTHON"
# print(word[0:3])  # PYT
# print(word[2:5])  # THO

# # 실습 - [:n] start 생략
# word = "temp_sensor"
# print(word[:4])  # temp

# # 실습 - [n:] end 생략
# word = "temp_sensor"
# print(word[5:])  # sensor

# # 실습 - [-n:] 음수 슬라이싱 (뒤 n글자)
# word = "sensor_01"
# print(word[-2:])  # 01

# # 실습 - step으로 건너뛰기
# word = "PYTHON"
# print(word[::2])  # PTO

# # 실습 - 문자열 뒤집기
# word = "PYTHON"
# print(word[::-1])  # NOHTYP

# # 활용 - 날짜·번호·코드 구간 추출
# date = "20260716"
# year = date[:4]
# month = date[4:6]
# day = date[6:]
# print(year, month, day)

# phone = "01012345678"
# basic_num = phone[:3]
# middle_num = phone[3:7]
# last_num = phone[7:]
# print(basic_num, middle_num, last_num)

# # 실습 - len으로 길이 재기
# phone = "01012345678"
# print(len(phone))  # 11

# # 실습 - in 으로 포함 확인
# msg = "설비 고장 발생"
# print("고장" in msg)  # True
# print("정상" in msg)  # False

# # 실습 - count로 개수 세기
# word = "a,b,c,d"
# print(word.count(","))  # 3 

# # 실습 - find로 위치 찾기
# word = "a,b,c,d"
# print(word.find(","))  # 1
# print(word.find("x"))  # -1 (없으면 -1 반환)

# # 실습 - startswith, endswith
# c_name = "sensor_log.csv"
# print(c_name.startswith("sensor"))  # True
# print(c_name.endswith(".csv"))  # True

# # 실습 - ==로 대소문자 구분 비교
# label = "WARNING"
# print(label == "warning")  # False
# print(label == "WARNING")  # True 



