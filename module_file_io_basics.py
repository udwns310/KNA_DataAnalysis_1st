# =====================================================================
# 모듈과 import - 코드를 가져다 쓰는 법
# =====================================================================

# [문제 상황] 같은 코드를 매번 다시 짜는 문제
# - 제곱근 계산만 해도 공식을 알아야 하고 정확도를 맞추기도 어려움
# - 다행히 이런 기능은 이미 잘 만들어져 있고, 우리는 가져다 쓰기만 하면 됨
# - 직접 만들기(공식 이해 + 정확도 확보 + 검증 책임 본인) vs 가져다 쓰기(import 한 줄,
#   NumPy·Pandas 같은 강력한 도구도 모두 이 방식) - 좋은 개발자는 검증된 도구를 잘 찾아 조합하는 사람

# [개념] 모듈 - 코드가 담긴 .py 파일 하나
# - 망치와 드라이버가 든 도구 상자처럼, math 모듈은 수학 도구 상자, os 모듈은 폴더·파일 도구 상자
# - 함수와 변수가 모여 있는 도구 상자를 가져와 필요한 도구를 꺼내 씀
# math.py 안에는 대략 이런 것들이 들어있다고 상상하면 됨:
# def sqrt(x): ...  def ceil(x): ...  def floor(x): ...  pi = 3.14159...  e = 2.71828...

# [정리] 모듈을 쓰는 세 가지 이유
# - 재사용: 복사-붙여넣기 없이 import 한 줄이면 다른 파일에서도 사용
# - 관리: 길어진 코드를 기능별 파일로 나눠 정리 - 찾기도 고치기도 쉬움
# - 검증: 전 세계 개발자가 검증한 코드를 그대로 사용 - 직접 만드는 것보다 안전

# [정리] 모듈·패키지·라이브러리 구분
# - 모듈: 코드가 담긴 .py 파일 한 개
# - 패키지: 관련 모듈을 모은 폴더
# - 라이브러리: 셋을 아우르는 통칭 - 셋 다 "가져와 쓴다"는 공통점, 방법은 import

# [개념] import 기본 사용법 - import 모듈명 한 줄로 그 모듈의 모든 기능 사용 준비 완료
import math

result = math.sqrt(16)
print(result)  # 4.0

# [개념] 점 표기법으로 기능 꺼내쓰기 - 점은 "~의 안에 있는"이라는 뜻
# math.sqrt -> 점 앞(math)은 출처, 점 뒤(sqrt)는 기능
# 앞으로 볼 pd.read_csv, np.mean도 모두 같은 원리 (pd=Pandas, np=NumPy)

# [개념] from import로 일부만 가져오기 - from 모듈명 import 기능명
from math import sqrt

print(sqrt(25))  # 5.0 (모듈명 없이 바로 사용, 대신 출처가 가려짐)

# [정리] import 방식 비교
# 구분 | import 모듈명        | from ... import
# 작성 | import math          | from math import sqrt
# 사용 | math.sqrt(16)        | sqrt(16)
# 장점 | 출처 명확            | 코드 간결
# 단점 | 매번 모듈명을 붙여야 함| 출처가 가려져 추적 어려움
# 기능을 골고루 쓰면 import 모듈명이, 한두 개만 쓰면 from ... import가 편함

# [강사님께 질문하기] import를 파일 맨 위가 아니라, 그 기능을 실제로 쓰는 코드 바로 위에
# 적어도 작동은 똑같이 하지 않나요? 왜 다들 맨 위에 몰아서 적으라고 하는 거예요?
# -> 답변: 함수 안이나 쓰는 자리 바로 위에 적어도 작동 자체는 문제없음. 하지만 그렇게
#    흩어놓으면 이 코드 파일이 어떤 도구들을 쓰는지 알려면 코드 전체를 처음부터 끝까지
#    다 훑어봐야 하는 불편함이 생김. 맨 위에 모아두면 파일을 열자마자 "이 코드는 이런
#    도구들을 쓰는구나"를 바로 알 수 있어서, 코드를 처음 읽는 사람(몇 주 뒤의 나 포함)
#    에게 미리 지도를 보여주는 셈 - 작동 여부와 무관하게 굳어진 관행

# [정리] as 별칭 - 긴 모듈명에 짧은 별명 붙이기 (데이터 분석에는 전 세계가 따르는 공통 약속)
# import numpy as np / import pandas as pd / import matplotlib.pyplot as plt
import datetime as dt

now = dt.datetime.now()
print(type(now).__name__)  # datetime

# [주의] import 별표(from math import *)는 실무에서 회피
# - 모든 기능을 한꺼번에 가져와 내 변수와 이름이 충돌할 수 있고, 어디서 왔는지도 알 수 없게 됨


print(
    "\n===================== 실습 1. import 세 방식으로 모듈 가져오기 ====================="
)
# 목표: import·from import·as 세 방식으로 같은 기능을 가져와 써 보기
# 단계: ① import 모듈명으로 통째로 가져와 모듈명.기능()으로 사용 -> ② from 모듈 import 기능으로 일부만 가져와 모듈명 없이 사용
#      -> ③ import 모듈 as 별명으로 별명.기능()으로 사용 -> ④ 세 방식의 출력이 같은지 확인
# 예상 결과: 세 방식 모두 4.0 5 출력
import math

print(math.sqrt(16))  # 4.0

from math import sqrt as square_root

print(square_root(16))  # 4.0

import math as m

print(m.ceil(4.2))  # 5


# =====================================================================
# 표준 라이브러리
# =====================================================================

# [개념] 표준 라이브러리 - 파이썬 설치 시 함께 깔리는 검증된 모듈 모음
# "Batteries Included" - 장난감에 건전지까지 들어 있어 바로 가지고 놀 수 있다는 뜻
# 따로 설치하지 않아도 import만 하면 바로 사용 가능 - math·random·datetime·os·csv가 여기 속함

# [정리] 자주 쓰는 표준 라이브러리 다섯 가지
# 모듈     | 하는 일   | 활용 예
# math     | 수학 계산 | 제곱근·원주율 - 통계 계산
# random   | 무작위 처리| 가짜 센서값 - 실제 데이터 없을 때 연습용
# datetime | 날짜·시간 | 점검 시각 - 언제 했는지 기록
# os       | 폴더·파일 | 파일 목록 - 데이터 폴더 탐색
# csv      | 표 데이터 | 센서 CSV - 표 형태 파일 입출력

# [개념] math 모듈 - 한 단계 전문적인 계산에 꺼내 쓰는 도구
print(math.sqrt(9))  # 3.0 (제곱근)
print(math.ceil(4.2))  # 5 (올림)
print(math.floor(4.8))  # 4 (내림)
print(2**3)  # 8 (거듭제곱은 math 없이 바로 사용)
print(abs(-3))  # 3 (절댓값도 math 없이 바로 사용)

# [개념] random 모듈 - randint는 양 끝 포함, choice는 무작위 선택
import random

print(random.randint(1, 10))  # 1~10 중 무작위 정수 (1과 10도 포함)
print(random.choice(["정상", "경고", "위험"]))  # 셋 중 무작위 (실행마다 다름)

# [강사님께 질문하기] 컴퓨터는 정해진 규칙대로만 계산하는 기계라고 알고 있는데,
# random.randint는 어떻게 매번 다른 값을 뽑아내는 거예요? 진짜로 무작위인가요?
# -> 답변: 완전히 순수하게 아무 규칙 없는 무작위는 아님. 겉보기엔 무작위처럼 보이지만
#    사실은 아주 복잡한 계산식으로 뽑아내는 숫자이고, 그 계산의 출발점으로 현재 시각처럼
#    매번 달라지는 값을 넣어서 사람이 규칙을 못 찾을 정도로 뒤죽박죽인 숫자를 만들어냄.
#    그래서 게임이나 연습용 데이터 만들기에는 충분히 무작위처럼 쓸 수 있지만, 보안처럼
#    "절대로 예측되면 안 되는" 곳에는 이것보다 더 강력한 별도의 방식을 씀

# [개념] datetime 모듈 - 앞 datetime은 모듈 이름, 뒤 datetime은 그 안의 도구
import datetime

# datetime 모듈 안의 datetime 클래스 안의 now() 메서드로 현재 시각을 가져옴
now2 = datetime.datetime.now()
print(now2)  # 예: 2026-08-05 09:00:00.123456

# [정리] 모듈 문서 읽는 법 - 다 외울 필요 없음, 필요할 때 찾는 법만 알면 됨
# dir(math) -> 모듈 안 기능 목록을 펼쳐 보여줌 (예: ['ceil', 'e', 'floor', 'pi', 'sqrt', ...])
# help(math.sqrt) -> 그 기능을 어떻게 쓰는지 설명서를 보여줌

# [정리] 표준 라이브러리 vs 외부 라이브러리
# 구분 | 표준 라이브러리                   | 외부 라이브러리
# 예시 | math·os·csv·random·datetime      | NumPy·Pandas·Matplotlib
# 설치 | 불필요 - 파이썬과 함께 설치됨      | pip install로 따로 설치
# 사용 | import로 바로 사용                | 설치 후 import
# "No module named ..." 오류는 대개 외부 라이브러리 미설치가 원인


print(
    "\n===================== 실습 2. 표준 라이브러리로 센서값 만들기 ====================="
)
# 목표: random·math 모듈로 무작위 센서값을 만들고 가공하기
# 단계: ① random 모듈을 import -> ② randint로 무작위 센서값을 만들어 출력
#      -> ③ math 모듈로 그 값을 가공(제곱근) -> ④ 다시 실행하면 값이 달라지는지 확인
# 예상 결과: (매번 다른) 무작위 값과 그 제곱근
rand_sensor = random.randint(1, 100)
print(rand_sensor)  # 예: 57 (실행마다 다름)
print(math.sqrt(rand_sensor))  # 그 값의 제곱근


# =====================================================================
# 경로와 os 모듈
# =====================================================================

# [개념] 폴더 구조와 경로 표기 - 슬래시는 "폴더 안으로 들어간다"는 의미
# documents/ -> project/ -> data/ -> 08_press.csv
# 경로: documents/project/data/08_press.csv
# 폴더는 나무를 거꾸로 세운 계층 구조이고, 경로는 그 가지를 따라가는 길을 적은 것
# 윈도우는 역슬래시(\), 맥·리눅스는 슬래시(/) - 이 차이는 os.path.join이 자동으로 맞춰줌

# [정리] 절대경로와 상대경로
# 구분 | 절대경로                        | 상대경로
# 기준 | 최상위 폴더부터 끝까지 적음      | 현재 위치에서 출발
# 예시 | C:\Users\me\project\data\a.csv | data/a.csv
# 길이 | 길다 - 우편 주소처럼            | 짧다 - "여기서 오른쪽으로" 식
# 이동 | 옮기면 오류                     | 옮겨도 동작
# 점 하나(.) = 현재 폴더, 점 두 개(..) = 상위 폴더 - 실무는 상대경로를 더 자주 사용

# [개념] 작업 디렉토리(cwd) - 코드가 "지금 여기 서 있다"고 여기는 폴더, 상대경로는 모두 여기서 출발
# [주의] 작업 디렉토리는 코드 파일 위치와 항상 같지는 않음
# - 파일 바로 옆에 데이터를 뒀는데도 못 찾는 일이 생길 수 있음 - 읽기 전에 현재 위치부터 확인하는 습관

# [개념] os 모듈 - Operating System과 대화하는 도구, 표준 라이브러리라 import os만 쓰면 바로 사용
import os

cwd = os.getcwd()
print(cwd)  # 현재 폴더의 절대경로

file_list = os.listdir()
for file_name in file_list:
    print(file_name)  # 현재 폴더 안 파일·폴더 이름을 모두 보여줌

# [설정] 이 파일의 os·csv 실습이 항상 똑같이 재현되도록, 강의의 data/08_press.csv와
# 같은 구조(설비ID·시각·진동X·진동Y·전류·상태)를 가진 표본 CSV를 코드로 직접 만들어 둔다
practice_dir = "practice_data"
os.makedirs(practice_dir, exist_ok=True)

sample_path = os.path.join(practice_dir, "08_press.csv")
with open(sample_path, "w", encoding="utf-8", newline="") as f:
    f.write("설비ID,시각,진동X,진동Y,전류,상태\n")
    f.write("PRESS-01,09:00:00,0.30,0.28,78.2,0\n")
    f.write("PRESS-02,09:01:00,0.31,0.29,81.5,0\n")
    f.write("PRESS-03,09:02:00,0.33,0.30,95.4,1\n")
    f.write("PRESS-04,09:03:00,0.29,0.27,76.8,0\n")
    f.write("PRESS-05,09:04:00,0.34,0.31,92.1,1\n")
    f.write("PRESS-06,09:05:00,0.30,0.28,80.0,0\n")


# [개념] os.listdir로 폴더 들여다보기 - 폴더 안 파일·폴더 이름을 리스트로 반환
files_in_dir = os.listdir(practice_dir)
for name in files_in_dir:
    print(name)  # listdir은 파일과 폴더를 구분 없이 모두 보여줌
# CSV만 고르려면 이름이 .csv로 끝나는지 조건문으로 확인해야 함

# [정리] 파일 존재 확인의 필요성
# - 바로 열기(NO CHECK): 없는 파일을 읽으면 그 자리에서 멈춤 (파일 100개 중 50번째가
#   없으면 나머지 50개도 처리되지 않음)
# - 존재 확인(CHECK FIRST): 읽기 전에 있는지 확인하고, 있으면 읽고 없으면 건너뜀

# [개념] os.path.exists() - 경로에 파일이 있으면 True, 없으면 False
# [개념] os.path.join() - 폴더명과 파일명을 합쳐 완전한 경로로 만듦 (OS에 맞는 구분자를 자동으로 넣어줌)
check_path = os.path.join(practice_dir, "08_press.csv")
if os.path.exists(check_path):
    print("파일 있음:", check_path)

# [강사님께 질문하기] os.path.join을 안 쓰고 그냥 "data" + "/" + "08_press.csv"처럼
# 슬래시를 직접 이어붙이면 안 되나요? 결과는 똑같아 보이는데요.
# -> 답변: 평소엔 똑같아 보이지만, 윈도우는 폴더를 나눌 때 역슬래시(\)를 쓰고 맥·리눅스는
#    슬래시(/)를 씀. 슬래시를 직접 이어붙이면 그 코드는 한쪽 운영체제에서만 제대로
#    동작하고, 다른 운영체제로 옮기면 경로를 못 찾는 문제가 생길 수 있음. os.path.join은
#    지금 이 코드가 어떤 운영체제에서 실행되는지 보고 그에 맞는 구분자를 알아서 골라
#    주기 때문에, 코드를 그대로 다른 컴퓨터로 옮겨도 안전하게 동작함


print("\n===================== 실습 3. os로 폴더 목록 살펴보기 =====================")
# 목표: os로 현재 위치를 확인하고 폴더 안 파일 목록을 순회하기
# 단계: ① os 모듈을 import -> ② getcwd로 현재 작업 폴더를 확인 -> ③ listdir로 폴더 안 목록을 변수에 담기
#      -> ④ for로 목록을 하나씩 출력하고 csv만 골라 출력
# 예상 결과: 현재 경로 / 폴더 안 파일들 / .csv 파일만
print(os.getcwd())
data_list = os.listdir(practice_dir)
for item in data_list:
    print(item)
    if item.endswith(".csv"):
        print("[csv]", item)


print("\n===================== 실습 4. os로 파일 존재 확인하기 =====================")
# 목표: os.path.join으로 경로를 만들고 exists로 파일 존재를 판단하기
# 단계: ① os를 import -> ② path.join으로 폴더와 파일 이름을 이어 경로를 만들기
#      -> ③ path.exists로 그 경로가 있는지 참·거짓 확인 -> ④ if로 있으면·없으면 다른 메시지 출력
# 예상 결과: True 또는 False / 파일 있음 또는 파일 없음
target_path = os.path.join(practice_dir, "08_press_sample.csv")
found = os.path.exists(target_path)
print(found)  # True
if found:
    print("파일 있음")
else:
    print("파일 없음")

missing_path = os.path.join(practice_dir, "08_없는파일.csv")
print(os.path.exists(missing_path))  # False


print(
    "\n===================== 실습 5. datetime으로 점검 기록 남기기 ====================="
)
# 목표: os와 datetime으로 폴더 파일 수와 점검 시각을 한 줄로 기록하기
# 단계: ① os와 datetime을 import -> ② listdir로 폴더 파일 수를 구하기
#      -> ③ datetime.now로 현재 시각을 담기 -> ④ f-string으로 파일 수와 시각을 한 문장으로 출력
# 예상 결과: 파일 3개, 점검 시각 2026-... 형식 한 줄
file_count = len(os.listdir(practice_dir))
check_time = datetime.datetime.now()
print(f"파일 {file_count}개, 점검 시각 {check_time}")


print(
    "\n===================== 실습 6. 폴더에서 csv 파일만 골라내기 ====================="
)
# 목표: os로 폴더에서 csv 파일만 골라 새 리스트로 모으고 경로를 만들기
# 단계: ① os를 import하고 listdir로 폴더 목록을 구하기 -> ② for-if로 .csv로 끝나는 이름만 빈 리스트에 모으기
#      -> ③ 모은 csv마다 path.join으로 전체 경로를 만들기 -> ④ 골라낸 csv 목록을 출력
# 예상 결과: [CSV] 목록 (csv 파일만)
csv_names = []
for name in os.listdir(practice_dir):
    if name.endswith(".csv"):
        csv_names.append(name)

csv_full_paths = []
for name in csv_names:
    csv_full_paths.append(os.path.join(practice_dir, name))
print(csv_full_paths)


# =====================================================================
# 파일 입출력 - txt 다루기
# =====================================================================

# [개념] 데이터를 파일로 주고받는 이유 - 데이터는 파일에, 코드는 따로
# - 설비 데이터는 하루에도 수만 줄 - 코드에 직접 적을 수 없음
# - 데이터는 파일에 저장하고, 코드는 그 파일을 열어 읽는다 (데이터와 코드의 분리)
# - 코드 고정: 데이터가 바뀌어도 코드는 그대로 (오늘 파일이든 어제 파일이든 같은 코드로 분석)
# - 공유: 만든 결과를 파일로 저장해 전달·재사용, 다음 작업에 이어 쓰기 좋음

# [개념] open() 함수 구조 - open(파일명, 모드, 인코딩)으로 파일을 연다
# - open은 내장 함수 - import가 필요 없음
# - 결과로 받는 것은 파일이 아니라, 파일을 다룰 연결 통로 (파일 객체)
f = open(sample_path, "r", encoding="utf-8")
print(type(f).__name__)  # TextIOWrapper
f.close()

# [개념] 인코딩(utf-8)이 중요한 이유 - 인코딩은 글자를 숫자로 바꾸는 약속
# - 저장과 읽기의 약속(인코딩)이 다르면 한글이 깨짐
# - 오늘날 표준은 utf-8, 윈도우 엑셀로 저장한 CSV는 cp949일 수 있음 - 깨지면 서로 바꿔 봄

# [정리] 파일 모드 r·w·a 차이 - w와 a를 헷갈리면 데이터가 날아감
# 모드 | 의미     | 동작
# r    | 읽기     | 내용 읽기 (기본값)
# w    | 새로 쓰기 | 기존 내용을 삭제하고 새로 작성
# a    | 이어 쓰기 | 기존 내용 뒤에 추가
# 새로 만들 때만 w, 이어 붙일 때는 a

# [정리] read·readline·readlines 차이 - 끝의 s 한 글자가 결과를 바꿈
# 방법      | 읽는 범위 | 돌려주는 것
# read      | 전체      | 한 덩어리 문자열
# readline  | 한 줄     | 한 줄 문자열
# readlines | 전체      | 줄 단위 리스트
# 줄 단위 센서 로그에는 readlines 또는 파일 직접 반복이 잘 어울림
with open(sample_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(type(lines).__name__, len(lines))  # list 7 (헤더 1줄 + 데이터 6줄)


print("\n===================== 실습 7. open으로 파일 읽기 =====================")
# 목표: open으로 파일을 열어 read·readlines로 내용을 읽기
# 단계: ① open으로 파일을 읽기 모드 r, utf-8로 열기 -> ② read로 전체를 한 문자열로 읽어 출력
#      -> ③ readlines로 줄 리스트로 읽어 출력 -> ④ 두 방식의 결과 차이를 비교하고 파일을 close
# 예상 결과: read는 한 덩어리 문자열 / readlines는 줄 리스트
f1 = open(sample_path, "r", encoding="utf-8")
whole_text = f1.read()
print(whole_text)
f1.close()

f2 = open(sample_path, "r", encoding="utf-8")
line_list = f2.readlines()
print(line_list)
f2.close()


# [정리] 파일을 닫아야 하는 이유 - 열었으면 닫는다
# ① 자원 반납 - 안 닫으면 쌓여서 나중에 파일을 못 열 수 있음
# ② 저장 보장 - 쓰기에서 닫지 않으면 임시 공간의 내용이 실제 파일에 기록되지 못하고 사라짐
# 닫기는 안전장치지만 깜빡하기 쉬워, with가 이를 자동으로 해결

# [개념] with open() 컨텍스트 매니저 - 블록이 끝나면 파일이 자동으로 닫힘 (실무의 기본 형태)
# 오류가 나도 안전하게 닫히므로 close()가 불필요
with open(sample_path, "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())  # 블록 밖으로 나가면 자동 닫힘


print("\n===================== 실습 8. with open으로 파일에 쓰기 =====================")
# 목표: with open의 w 모드로 파일에 내용을 쓰고 다시 읽어 확인하기
# 단계: ① with open으로 파일을 쓰기 모드 w, utf-8로 열기 -> ② write로 내용을 쓰기(줄을 나눌 땐 줄바꿈 기호)
#      -> ③ with 블록이 끝나면 파일이 자동으로 닫힘 -> ④ r 모드로 다시 열어 쓴 내용을 확인
# 예상 결과: 쓴 내용이 그대로 읽힘
import os
log_path = os.path.join("practice_data", "check_log.txt")
with open(log_path, "w", encoding="utf-8") as f:
    f.write("1번 설비 점검 완료\n")
    f.write("2번 설비 점검 완료\n")
    f.write("3번 설비 점검 완료\n")

with open(log_path, "r", encoding="utf-8") as f:
    print(f.read())


print("\n===================== 실습 9. a 모드로 기록 이어붙이기 =====================")
# 목표: a 모드로 기존 내용을 지우지 않고 새 기록을 이어 붙이기
# 단계: ① with open으로 파일을 추가 모드 a로 열기 -> ② write로 새 기록 문장을 쓰기
#      -> ③ w 모드와 달리 기존 내용이 보존됨을 확인 -> ④ r 모드로 열어 전체가 쌓였는지 확인
# 예상 결과: 기존 내용 + 새 기록이 함께 남음
with open(log_path, "a", encoding="utf-8") as f:
    f.write("4번 설비 점검 완료\n")

with open(log_path, "r", encoding="utf-8") as f:
    print(f.read())  # 1·2·3·4번 기록이 이어 붙어 총 네 줄


# =====================================================================
# 파일 입출력 - csv 읽기·쓰기
# =====================================================================

# [개념] csv가 제조 데이터의 기본 형식인 이유 - 쉼표로 구분된 표 형식 텍스트
# - 표를 텍스트로 옮긴 형태 - 행은 줄바꿈, 열은 쉼표로 나뉨
# - 표준이 된 이유는 가볍고·호환성 높고·단순하다는 세 가지 - 엑셀·파이  썬·DB 어디서나 읽고 씀

# [정리] csv 구조 - 헤더(열 제목) · 행(한 건 기록) · 열(값 종류) · 구분자(쉼표)
# 읽기 전에 첫 줄이 헤더인지 확인하는 습관이 필요

# [개념] csv.reader 구조 - 각 행은 리스트로, 모든 값은 문자열로 반환됨
import csv

with open(sample_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # 각 행이 리스트로 출력됨

# [정리] 읽은 데이터를 리스트로 다루기
# - 인덱스 추출: 행은 리스트라 0부터 시작하는 번호로 열을 고름 (전류는 인덱스 4)
# - 형변환: 문자열 값은 float로 바꿔야 계산됨 - 빠뜨리면 문자열끼리 비교해 오류


print("\n===================== 실습 10. csv.reader로 CSV 읽기 =====================")
# 목표: csv.reader로 CSV 파일을 행 단위로 읽기
# 단계: ① csv 모듈을 import -> ② with open으로 CSV를 읽기 모드 utf-8로 열기
#      -> ③ csv.reader로 reader 객체를 만들기 -> ④ for로 각 행(리스트)을 하나씩 꺼내 출력
# 예상 결과: 각 행이 리스트로 출력
with open(sample_path, "r", encoding="utf-8") as f:
    press_reader = csv.reader(f)
    for row in press_reader:
        print(row)


# [개념] csv.writer 구조 - csv.reader의 정확히 반대, 리스트를 행으로 써 줌
# with open을 w 모드로 열되 newline='' 옵션을 더함
result_path = os.path.join("practice_data", "result_sample.csv")
with open(result_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["시각", "설비"])
    writer.writerow(["09:00", "PUMP-01"])

# [정리] 행 단위 준비와 newline 옵션
# - 한 행의 값들을 리스트로 묶고, 모든 행의 열 개수를 맞춰야 표가 어긋나지 않음
# - CSV 쓰기에는 항상 newline='' - 패턴으로 기억

# [강사님께 질문하기] newline=''을 안 주면 정확히 어떤 문제가 생기나요? 그냥 무시해도
# 되는 옵션 아닌가요?
# -> 답변: 무시하면 안 됨. 윈도우에서는 줄바꿈을 처리하는 방식이 살짝 다른데, csv.writer가
#    자기 나름대로도 줄바꿈을 넣어주기 때문에, open이 또 한 번 줄바꿈을 끼워 넣으면
#    결과 파일에 한 줄씩 건너뛰어 빈 줄이 끼어버림. newline=''으로 열면 "여기서는 내가
#    줄바꿈을 처리하지 않을 테니 csv.writer한테 맡긴다"는 뜻이 되어 이 문제가 사라짐 -
#    몰라도 코드는 돌아가지만, 결과 파일을 열어보면 이상하게 뭉텅뭉텅 비어 보이는 원인이 됨


print("\n===================== 실습 11. csv.writer로 CSV 쓰기 =====================")
# 목표: csv.writer로 데이터를 CSV 파일에 행 단위로 쓰기
# 단계: ① csv를 import -> ② with open으로 w·utf-8·newline 옵션으로 열기
#      -> ③ csv.writer로 writer 객체를 만들기 -> ④ writerow로 헤더와 각 데이터 행을 쓰기
# 예상 결과: 새 CSV에 헤더+데이터 행이 저장됨
check_result_path = os.path.join("practice_data", "check_result.csv")
with open(check_result_path, "w", encoding="utf-8", newline="") as f:
    check_writer = csv.writer(f)
    check_writer.writerow(["설비ID", "전류"])
    check_writer.writerow(["PRESS-01", 95.4])
    check_writer.writerow(["PRESS-01", 92.1])

with open(check_result_path, "r", encoding="utf-8") as f:
    print(f.read())


# [개념] csv.DictReader 맛보기 - 번호 대신 이름으로, 열 순서가 바뀌어도 안전
with open(sample_path, "r", encoding="utf-8") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        print(row["설비ID"], row["전류"])

# [정리] csv 다룰 때 흔한 오류
# 증상     | 원인       | 해결
# 한글 깨짐| 인코딩 불일치| utf-8 / cp949 바꿔 보기
# 빈 줄 끼임| newline 누락| 쓰기 open에 newline=''
# 계산 오류| 문자열 상태 | float·int 변환
# 첫 줄 오류| 헤더 포함  | 헤더 건너뛰기

# [정리] 파일 입출력 전체 흐름 - 파일 열기(with open) -> 모드 선택(r·w·a) -> 다루기
#        (reader/writer) -> 자동 닫힘 (블록 종료 시)
# [정리] with open으로 열고 reader로 읽어 형변환 - writer로 리스트를 행으로 저장
#        (이후 배울 Pandas도 이 흐름 위에 있음)


print("\n===================== 실습 12. CSV 읽어 조건 저장하기 =====================")
# 목표: CSV를 읽어 조건에 맞는 데이터만 골라 새 CSV로 저장하기
# 단계: ① csv를 import -> ② csv.reader로 읽고 첫 줄 헤더는 건너뛰기
#      -> ③ 값을 float로 변환해 기준(90) 초과 행만 리스트에 모으기 -> ④ csv.writer로 모은 행들을 새 CSV에 저장
# 예상 결과: 기준 초과 센서만 담긴 새 CSV
filtered_rows = []
with open(sample_path, "r", encoding="utf-8") as f:
    press_reader2 = csv.reader(f)
    header = next(press_reader2)  # 헤더 건너뛰기
    for row in press_reader2:
        current_value = float(row[4])  # 전류 열
        if current_value > 90:
            filtered_rows.append(row)

over_90_path = os.path.join(practice_dir, "over_90.csv")
with open(over_90_path, "w", encoding="utf-8", newline="") as f:
    over_writer = csv.writer(f)
    over_writer.writerow(header)
    over_writer.writerows(filtered_rows)

with open(over_90_path, "r", encoding="utf-8") as f:
    print(f.read())  # 전류 95.4, 92.1 두 행만 남음


# =====================================================================
# [흔한 질문 진단] 모듈·경로·파일 다루면서 헷갈리기 쉬운 것들
# =====================================================================

# Q1. w 모드로 파일을 열면 기존 내용이 정말로 통째로 사라지나요?
# -> A. 사라짐. w는 "새로 쓰기" 모드라서, 열자마자 기존 내용을 지우고 시작함. 이어 붙이고
#       싶다면 반드시 a 모드를 써야 함
overwrite_path = os.path.join(practice_dir, "overwrite_test.txt")
with open(overwrite_path, "w", encoding="utf-8") as f:
    f.write("첫 번째 내용\n")
with open(overwrite_path, "w", encoding="utf-8") as f:  # w로 또 열면 위 내용이 사라짐
    f.write("두 번째 내용\n")
with open(overwrite_path, "r", encoding="utf-8") as f:
    print(f.read())  # 두 번째 내용만 남음 (첫 번째 내용은 사라짐)

# Q2. csv.reader로 읽은 값을 바로 계산에 쓰면 어떻게 되나요?
# -> A. csv.reader가 돌려주는 값은 전부 문자열이라서, 숫자처럼 보여도 그냥 더하면
#       숫자 덧셈이 아니라 문자열 이어붙이기가 됨. 반드시 float나 int로 형변환해야 함
sample_row = ["PRESS-01", "09:00:00", "0.30", "0.28", "78.2", "0"]
print(sample_row[4] + sample_row[4])  # "78.278.2" (문자열이 이어붙여짐 - 계산 아님!)
print(float(sample_row[4]) + float(sample_row[4]))  # 156.4 (형변환하면 진짜 계산됨)

# Q3. open()만 쓰고 close()를 깜빡하면 무조건 문제가 생기나요?
# -> A. 당장은 안 터질 수도 있지만 안전하지 않음. 특히 쓰기 모드에서는 close()를
#       깜빡하면 쓴 내용이 실제 파일에 반영이 안 될 수 있음. with open을 쓰면 이 실수
#       자체가 원천 차단되므로, 실무에서는 open()+close() 대신 with open을 기본으로 씀

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# with open("temp_quiz.txt", "w", encoding="utf-8") as f:
#     f.write("A\n")
# with open("temp_quiz.txt", "a", encoding="utf-8") as f:
#     f.write("B\n")
# with open("temp_quiz.txt", "r", encoding="utf-8") as f:
#     print(f.read())
# 정답: A\nB\n (w로 "A"를 쓰고, a로 "B"를 이어 붙였으므로 둘 다 남음)

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# row = ["10", "20"]
# print(row[0] + row[1])
# print(int(row[0]) + int(row[1]))
# 정답: 1020 / 30 (형변환 전엔 문자열이 이어붙고, int로 바꾼 뒤에야 진짜 덧셈이 됨)
