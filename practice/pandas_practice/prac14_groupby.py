# 14_01 실습 1~3 문제를 풀고 올려주세요.

# 선택 문제 : 첨부된 CSV 파일을 통해 다음 통계들을 내는 코드를 작성해 제출해주세요.

# [문제 1] 이 학교의 전체 학생 수를 구하세요. (힌트: len 또는 shape)

# [문제 2] 학년별 학생 수를 구하세요. (힌트: groupby + count 또는 size)

# [문제 3] 학년 내 각 반별 학생 수를 구하세요. (힌트: 다중 컬럼 groupby)

# [문제 4] 각 반(학년, 반 조합)의 국어 점수 평균을 소수점 둘째 자리까지 구하세요.

# [문제 5] 각 학년의 영어 점수 평균을 소수점 둘째 자리까지 구하세요. 

# [문제 6] 학교 전체의 수학 점수 평균을 소수점 둘째 자리까지 구하세요.

import pandas as pd
import os

students_path = os.path.join("data", "students_groupby_practice.csv")
students = pd.read_csv(students_path)

# 문제 1: 전체 학생 수
total_count = len(students)
print(total_count)  # 60

# 문제 2: 학년별 학생 수
grade_count = students.groupby("학년").size()
print(grade_count)

# 문제 3: 학년 내 반별 학생 수
grade_class_count = students.groupby(["학년", "반"]).size()
print(grade_class_count)

# 문제 4: 반(학년, 반)별 국어 점수 평균
korean_mean = students.groupby(["학년", "반"])["국어"].mean().round(2)
print(korean_mean)

# 문제 5: 학년별 영어 점수 평균
english_mean = students.groupby("학년")["영어"].mean().round(2)
print(english_mean)

# 문제 6: 전체 수학 점수 평균
math_mean = round(students["수학"].mean(), 2)
print(math_mean)  # 68.95
