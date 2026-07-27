# index() 특정 문자열 위치 반환, 사용법은 find와 동일 (단, 없으면 오류)
# 차이 : find는 없으면 -1 반환, index는 없으면 ValueError 발생
# 값이 없어도 멈추면 안 되면 find / 반드시 있는 값이면 index 사용

print('=== index() ===')

email = 'layla@spreatics.com'
at = email.index('@') # 5 
print(email[:at]) # layla
print(email[at+1:]) # spreatics.com , 5번 인덱스부터 출력하기 때문에 +1 안하면 @부터 출력함


print('=== count() ===')
str = 'a,b,c,d,e,a, a'
print(str.count('a')) # 3
print(str.count('a', 3)) # 2 , 3번 인덱스부터 a 개수 세기

sqe = "SQE-00Q8"
print(sqe.find("SQE")) # 0
print(sqe.find("-")) # 3
print(sqe[:3]) # SQE

# find에서 했던 SQE를 index로 해보기
print(sqe.index("SQE")) # 0
result = sqe.index("-") # 3
print(sqe[:result]) # SQE

print("=== startswith() ===")
print("EQP-001".startswith("EQP")) # True
print()

print("=== endswith() ===")
print("EQP-001".endswith(" 001")) # True
print("안녕하세요 오늘 하루가".endswith(" 하루가")) # True

f_name = "sensor_log.csv"
print(f_name.startswith("sensor")) # True
print(f_name.endswith(".csv")) # True


# startswith() : 문자열이 특정 문자열로 시작하는지 확인
# in과 차이 : in은 어디든 포함, startswith는 시작하는지 확인
# 'data_log'에서 in은 True, startswith는 False

# endswith() : 문자열이 특정 문자열로 끝나는지 확인
# 파일명 같은거 확인할 때 많이 씀