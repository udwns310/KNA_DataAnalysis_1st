# # # # # # # # else와 finally 코드

# # # # # # # # text = "24.5" # 문자열로 된 숫자

# # # # # # # # text = "영크크"
# # # # # # # # temp = 0
# # # # # # # # try:
# # # # # # # #     temp = float(text)  # 숫자로 바꾸기
# # # # # # # #     # # 만약 2배를 하고 싶다면?
# # # # # # # #     # print(text * 2) # 24.524.5 - 문자열이므로 그냥 이어붙임
# # # # # # # #     # print(temp * 2) # 49.0 - 숫자이므로 곱셈이 됨
# # # # # # # # except ValueError:
# # # # # # # #     print(f"'{text}'는 숫자로 바꿀 수 없습니다")
# # # # # # # # finally:
# # # # # # # #     print(temp * 2)
# # # # # # # # # csv 데이터 가져올 때 타입 변환 신경쓰자

# # # # # # # # try:
# # # # # # # #     f = open("data/test.csv", "w", encoding="utf-8")
# # # # # # # #     f.write("테스트")  # 작업을 하는 중인거임 절대 대충한거 아님
# # # # # # # #     temp = int("문제없나?")  # 문제있는 코드 발생! 오류가 나버린 것임
# # # # # # # # except ValueError:  # 그럼 여기로 들어오겠지
# # # # # # # #     print("문자열을 숫자로 바꿀 수 없습니다")
# # # # # # # # finally:
# # # # # # # #     print(f.close())  # close() 함수는 None을 반환하니까 None 나오면 잘 닫힌거임 ㅇㅇ

# # # # # # # # # 반복문 안에서 예외처리

# # # # # # # # my_list = ["123", "456", "영크크", "32", "53"]
# # # # # # # # # 문제 발생 경우를 세어봅시다
# # # # # # # # problems = 0

# # # # # # # # for text in my_list:
# # # # # # # #     # 반복을 하다가도 문제가 생긴 경우만 건너뛰고 계속 반복을 이어서 진행시키기
# # # # # # # #     try:
# # # # # # # #         my_number = int(text)
# # # # # # # #     except ValueError:
# # # # # # # #         # print(f"'{text}'는 숫자로 바꿀 수 없습니다.")
# # # # # # # #         problems += 1
# # # # # # # #         continue  # 건너뛰고 다음 반복으로 넘어가라
# # # # # # # #     print(my_number)
# # # # # # # # print(f"문제 발생 경우: {problems}건")

# # # # # # # # [실습 2] 반복문에서 불량줄 건너뛰기
# # # # # # # # 소수점 이하의 숫자가 포함된 숫자들을 20개 정도 만들어 배열에 담아주세요
# # # # # # # # 그 사이에 엉뚱한 글자들이 포함된 내용도 포함시켜 주세요

# # # # # # # # my_list = [
# # # # # # # #     "12.3",
# # # # # # # #     "45.6",
# # # # # # # #     "78.9",
# # # # # # # #     "영크크",
# # # # # # # #     "32.1",
# # # # # # # #     "53.2",
# # # # # # # #     "abc",
# # # # # # # #     "99.9",
# # # # # # # #     "0.1",
# # # # # # # #     "23.4",
# # # # # # # #     "56.7",
# # # # # # # #     "89.0",
# # # # # # # #     "12.3",
# # # # # # # #     "45.6",
# # # # # # # #     "78.9",
# # # # # # # #     "늙크크",
# # # # # # # #     "32.1",
# # # # # # # #     "53.2",
# # # # # # # #     "abc",
# # # # # # # #     "99.9",
# # # # # # # # ]

# # # # # # # # sum_list = 0
# # # # # # # # for text in my_list:
# # # # # # # #     try:
# # # # # # # #         my_number = float(text)
# # # # # # # #         sum_list += my_number
# # # # # # # #     except ValueError:
# # # # # # # #         continue

# # # # # # # # print(f"합계 : {sum_list}")


# # # # # # # # # [실습 3] 여러 파일 묶어 처리하기
# # # # # # # # # 다음과 같은 식의 리스트를 만들어 반복문으로 처리해봅시다
# # # # # # # # # for문으로 리스트의 문자열을 꺼내여 해당 이름의 파일들을 열어보기 시도하면 됩니다
# # # # # # # # file_names = ["08_press.csv", "09_ict.csv", "09_ict_dirty.csv"]

# # # # # # # # for f_name in file_names:
# # # # # # # #     try:
# # # # # # # #         f = open(f"data/{f_name}", "r", encoding="utf-8")
# # # # # # # #     except FileNotFoundError:
# # # # # # # #         continue
# # # # # # # #     finally:
# # # # # # # #         f.close()
# # # # # # # #     print(f"{f_name} 파일 열기 성공")


# # # # # # # # 학생들의 점수를 가져와서
# # # # # # # # 각 학생별 합계와
# # # # # # # # 모든 학생들의 평균 점수를 내는 코드

# # # # # # # # [제출 안 하는 실습]
# # # # # # # # 1. 실행 끝날 때 최고점 학생, 최저점 학생도 찾아서 출력해보세요.
# # # # # # # # 2. 실행 끝날 떄 각 과목별 평균도 출력해보세요.(선택)

# # # # # # # import os
# # # # # # # import sys
# # # # # # # import csv

# # # # # # # # 0. 미리 전체 합산 점수 낼 준비를 한다
# # # # # # # total_all = 0
# # # # # # # student_count = 0
# # # # # # # max_score = 0
# # # # # # # max_name = ""
# # # # # # # min_score = 100
# # # # # # # min_name = ""
# # # # # # # kor_total = 0
# # # # # # # eng_total = 0
# # # # # # # math_total = 0

# # # # # # # # 1. 파일을 연다
# # # # # # # file_path = os.path.join("data", "student_scores.csv")

# # # # # # # if not os.path.exists(file_path):
# # # # # # #     print("파일을 찾지 못 했습니다.")
# # # # # # #     sys.exit(1)

# # # # # # # # 2. 파일 내용으로부터 리스트 데이터를 얻는다
# # # # # # # with open(file_path, "r", encoding="utf-8-sig") as f:
# # # # # # #     reader = csv.DictReader(f)

# # # # # # #     for row in reader:
# # # # # # #         name = row.get("이름", "(이름없음)")
# # # # # # #         kor = int(row.get("국어", "0"))
# # # # # # #         eng = int(row.get("영어", "0"))
# # # # # # #         math = int(row.get("수학", "0"))

# # # # # # #         total = (kor + eng + math) / 3
# # # # # # #         student_count += 1
# # # # # # #         print(f"{student_count}. {name} | {kor} | {eng} | {math} | {total:.2f}")

# # # # # # #         if total > max_score:
# # # # # # #             max_score = total
# # # # # # #             max_name = name
# # # # # # #         if total < min_score:
# # # # # # #             min_score = total
# # # # # # #             min_name = name

# # # # # # #         kor_total += kor
# # # # # # #         eng_total += eng
# # # # # # #         math_total += math
# # # # # # #         # 3. 점수 계산(합계, 평균)
# # # # # # #         total_all += total

# # # # # # # # 4. 결과를 화면에 보여주기
# # # # # # # print(f"최고점 학생: {max_name} ({max_score:.2f})")
# # # # # # # print(f"최저점 학생: {min_name} ({min_score:.2f})")

# # # # # # # avg_all = total_all / student_count
# # # # # # # print(f"전체 {student_count}명 | 평균 {avg_all:.2f}")

# # # # # # # print(f"국어 평균: {kor_total / student_count:.2f}")
# # # # # # # print(f"영어 평균: {eng_total / student_count:.2f}")
# # # # # # # print(f"수학 평균: {math_total / student_count:.2f}")


# # # # # # # 실습 1단계 csv 읽기

# # # # # # import os, sys, csv

# # # # # # file_path = os.path.join("data", "09_ict_inspection_dirty.csv")

# # # # # # header = []
# # # # # # rows = []


# # # # # # def read_file_ict(file_path):
# # # # # #     try:
# # # # # #         with open(file_path, "r", encoding="utf-8-sig") as file:
# # # # # #             reader = csv.DictReader(file)
# # # # # #             header = reader.fieldnames
# # # # # #             rows = list(reader)

# # # # # #         return header, rows

# # # # # #     except FileNotFoundError:
# # # # # #         print("파일을 찾을 수 없습니다.")
# # # # # #         return [], []


# # # # # # header, rows = read_file_ict("data/09_ict_inspection_dirty.csv")
# # # # # # print(header)
# # # # # # print(f"데이터 행 수 : {len(rows)} 행")

# # # # # # # 실습 2단계 csv 읽기


# # # # # # def classify_by_equipment(rows):

# # # # # #     classified_data = {}

# # # # # #     for row in rows:
# # # # # #         if not row:
# # # # # #             continue
# # # # # #         print(row)
# # # # # #         equipment_name = row.get("부품명", "(설비명없음)")
# # # # # #         equipment_list = classified_data.get(equipment_name, [])

# # # # # #         equipment_list.append(row)

# # # # # #         classified_data[equipment_name] = equipment_list

# # # # # #     for eq_name, eq_rows in classified_data.items():
# # # # # #         print(f"{eq_name}: {len(eq_rows)}")

# # # # # #     return classified_data


# # # # # # classify_by_equipment(rows)


# # # # # # Numpy 기초
# # # # # numbers = [1, 2, 3, 4, 5]

# # # # # numbers_10 = []


# # # # # for rnumber in numbers:
# # # # #     # print(number)
# # # # #     numbers_10.append(rnumber * 10)

# # # # # # print(numbers_10)

# # # # # # Numpy는 모든 데이터 분석의 기초 -> Pandas, Matplotlib 모두 Numpy 기반으로 만들어짐

# # # # # # 파이썬에서 기본 제공하는 기능들 외에 다양한 외부 라이브러리들을 가져오려면
# # # # # # pypi.org 사이트에서 검색부터 합시다

# # # # # # 터미널에서 바로 pip로 설치를 시도하면
# # # # # # 전체 시스템에 영향을 주는 설치로 생각되어 거절당한다
# # # # # # 그래서 개별 working directory마다 별도의 환경을 구축해
# # # # # # 그 안에 개별 프로젝트가 사용할 pip 라이브러리를 따로 받아쓰게 한다
# # # # # # 이것이 바로 가상환경(venv)

# # # # # # 1. 현재 경로에 가상 환경 생성
# # # # # # python -m venv .venv

# # # # # # 2. 가상 환경을 활성화
# # # # # # source .venv/Scripts/activate

# # # # # # 3. (작업 끝난 뒤) 가상 환경 종료
# # # # # # deactivate

# # # # # import numpy as np

# # # # # numbers = [1, 2, 3, 4, 5]
# # # # # # 위 int값들의 리스트를 사용해서 numpy의 배열 만들기
# # # # # np_numbers = np.array(numbers)
# # # # # print(np_numbers)

# # # # import numpy as np

# # # # # 파이썬의 리스트로부터 Numpy 배열 만들기
# # # # temp = np.array([70.5, 69.8, 73.7])
# # # # print(temp)
# # # # print(temp + 5)

# # # # # 소수점 이하가 없는 숫자 타입들로 가득찬 배열
# # # # print(np.array([1, 2, 3, 4, 5]))

# # # # # 소수점 이하가 있는 숫자 타입들로 가득찬 배열
# # # # print(np.array([3.14, 6.7, 7.67]))

# # # # # 소수점 이하가 있는 것, 없는 것이 섞여있다면?
# # # # # 모두 소수점 이하가 있는 것으로 배열 생성
# # # # print(np.array([1, 3, 5, 3.14, 6, 7, 4]))

# # # import numpy as np

# # # under_five = np.arange(5)
# # # print(under_five)  # [0 1 2 3 4]
# # # # 0부터 8까지 2 간격 (8보다 큰 숫자가 만들어지면 덧붙이지 않고 끝)
# # # gab_two = np.arange(0, 10, 2)
# # # print(gab_two)  # [0 2 4 6 8]

# # # linspace
# # # 개수 중심 균등 분할
# # # 시작과 끝 구간을 지정한 개수만큼 정확히 나눕니다
# # # 간격은 알아서 계산하도록 함

# # import numpy as np

# # # 0부터 1까지 5개로 균등 분할
# # div_five = np.linspace(0, 1, 5)  # [0.   0.25 0.5  0.75 1.  ]
# # print(div_five)

# # # 0으로 채우기
# # zero_array = np.zeros(5)  # [0. 0. 0. 0. 0.]
# # print(zero_array / 0)
# # # 명시적으로 7.0처럼 float 값을 지정해줘야 float 타입 값들로 채워지는 배열이 만들어진다
# # seven_array = np.full(4, 7.0)  # [7. 7. 7. 7.]
# # print(seven_array)

# # seven_list = [7.0] * 4
# # for i in seven_list:
# #     print(i / 0)

# # # 2차원
# # import numpy as np
# # # 기존 파이썬 리스트로 2차원을 표현
# # dim_2_list = [[1, 2, 3], [4, 5, 6]]


# # dtype, shape ... pandas에서 또 나옴

# import numpy as np

# table = np.array([[72, 2.3], [95, 6.8]])
# base = np.array([70, 2.0])
# print(table - base)

# print("=" * 50)

# v = np.array([70, 95, 71, 88, 73])
# print(v > 85)

# # Boolean indexing
# # 불리언 배열로 조건에 맞는 값만 골라내기
# print(v[v > 85])  # [95 88]


# # np.where() 함수
# print(np.where(v > 85, 1, 0))  # (array([1, 3]),) - 조건에 맞는 값들의 인덱스 반환

# # 다중 조건 결합
# print(v)
# v_step1 = v[v > 70]
# print(v_step1)
# v_step2 = v_step1[v_step1 < 90]
# print(v_step2)
# v_mixed = v[(v > 70) & (v < 90)]
# print(v_mixed)

# # 단일 컬럼 선택
# import pandas as pd

# df = pd.read_csv("data/13_diecasting_small.csv")
# df.info()

# df_sub = df["형체력"]
# df_sub.info()

# loc, iloc 사용
# import pandas as pd

# df = pd.read_csv("data/13_diecasting_shot.csv")
# s = df.loc[0]
# s2 = df.loc[0:2]
# print(s)
# print(s2)

# df_sub2 = df.loc[0:2, ["품질등급", "형체력"]]
# df_sub2.info()
# print(df_sub2)

# Boolean Series 코드
import pandas as pd

df = pd.read_csv("data/13_diecasting_small.csv")
