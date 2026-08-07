# =====================================================================
# 오류와 예외의 이해
# =====================================================================

# [개념] 오류는 왜 생기는가
# - 빨간 글씨는 잘못의 신호가 아니라, 컴퓨터가 "여기서 시킨 일을 할 수가 없다"라고
#   알려주는 안내문에 가까움
# - 숙련된 개발자도 매일 오류를 만남 - 차이는 당황하지 않고 침착하게 대처하느냐에 있음
# - 중요한 건 오류를 없애는 것이 아니라, 다루는 것

# [정리] 오류가 생기는 세 가지 경우
# 종류     | 예시                          | 발견 시점
# 문법 오류 | 괄호·콜론 빠뜨림, 들여쓰기 어긋남 | 실행되기 전
# 실행 중 오류 | 0으로 나누기, 없는 파일 열기  | 실행 도중 (오늘의 핵심)
# 결과 오류 | 문법·실행은 되지만 결과가 틀림  | 가장 까다로움 (겉으로 안 드러남)

# [개념] 프로그램이 멈춘다는 것의 의미
# - 프로그램은 위에서 아래로 한 줄씩 실행되다가, 처리할 수 없는 상황을 만나면 그 자리에서 멈춤
# - 이것을 "예외가 발생했다", 영어로 Exception이라고 부름
# - 핵심: 예외가 난 줄 아래 코드는 단 한 줄도 실행되지 않음
#   (30번째 줄에서 멈추면 31번째부터 100번째까지 전부 무시됨)

# [개념] 단 한 줄이 전체를 멈춘다
# - 센서 파일 50줄 중 단 한 줄의 불량 데이터가 전체 처리를 멈추게 함
# - 1) 50줄을 위에서부터 한 줄씩 처리 -> 2) 10번째 줄에서 숫자 변환 실패
#   -> 3) 그 줄에서 멈춰 나머지 40줄은 처리되지 못함

# [강사님께 질문하기] 컴퓨터가 오류를 미리 다 알고 있으면서 그냥 조용히 알아서 고쳐서
# 실행해주면 안 되나요? 왜 굳이 멈추고 우리한테 알려주는 거예요?
# -> 답변: 컴퓨터가 알아서 짐작해서 고쳐버리면, 그 짐작이 우리가 원한 의도와 다를 수 있음.
#    예를 들어 온도값이 비어있는 칸을 컴퓨터가 마음대로 0으로 채워버리면, 그 설비가 진짜
#    0도인 것처럼 보여서 잘못된 판단으로 이어질 수 있음. 그래서 파이썬은 "이 부분은 네가
#    뭘 원하는지 모르겠으니, 네가 직접 정해라"는 뜻으로 멈추고 알려주는 쪽을 택함 - 조용히
#    틀리게 넘어가는 것보다, 멈춰서 물어보는 편이 훨씬 안전함

# [정리] 에러 메시지 읽는 법 - 빨간 글씨 안에 문제를 푸는 모든 단서가 있음, 읽는 순서만 알면 됨
# ① 먼저 읽기: 맨 아랫줄에서 오류 종류와 원인을 확인 (콜론 앞은 오류 종류, 콜론 뒤는 구체적 설명)
# ② 그 다음: 그 위 line 줄에서 발생 위치 확인 (몇 번째 줄에서 문제가 났는지 알려줌)

# [정리] 트레이스백 읽는 순서 - 맨 아래에 진짜 원인이 있음, 위로 갈수록 큰 줄기로 올라감
# Traceback (most recent call last):
#   File "sensor.py", line 10, in <module>
#     temp = int(value)
# ValueError: invalid literal for int() with base 10: '스물'
# ① 시작 알림: 맨 윗줄 Traceback...은 읽지 않아도 됨
# ② 그 다음 · 발생 위치: line 10 - 10번째 줄을 살펴보면 됨
# ③ 먼저 읽기 · 오류 종류·원인: 맨 아랫줄에 진짜 원인이 있음


print("\n===================== 실습 1. 트레이스백으로 에러 읽기 =====================")
# 목표: 일부러 에러를 내고 트레이스백을 읽어 오류 종류와 위치 찾기
# 단계: ① 글자를 숫자로 바꾸는 코드로 ValueError를 내 보기 -> ② 0으로 나누는 코드로 ZeroDivisionError를 내 보기
#      -> ③ 정의하지 않은 변수를 써서 NameError를 내 보기 -> ④ 각 트레이스백에서 오류 종류와 줄 위치를 읽기
# 예상 결과: ValueError / ZeroDivisionError / NameError
try:
    number = int("스물다섯")
except ValueError as e:
    print(type(e).__name__, "-", e)

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(type(e).__name__, "-", e)

try:
    print(undefined_reading)
except NameError as e:
    print(type(e).__name__, "-", e)


# =====================================================================
# try-except 구조
# =====================================================================

# [개념] try-except 기본 구조
# - 발상의 전환: "위험한 일이 안 일어나게 막는다"가 아니라, "일어나면 그때 대응한다"
# - try에 위험한 코드, except에 대처 방법을 적음 - 오류가 나도 프로그램은 멈추지 않고 계속 실행됨
# - TRY(시도해봐): 실패할 수도 있는 위험한 코드를 try 블록 안에 넣음
# - EXCEPT(문제 생기면 이렇게): 예외가 발생했을 때 어떻게 대처할지를 except 블록에 적음
try:
    temp = int("스물")
except:
    print("못 바꿈")  # 오류가 나면 except로 점프, "못 바꿈" 출력 후 프로그램은 계속 실행

# [강사님께 질문하기] try 블록 안에 위험한 코드를 여러 줄 넣었는데, 그중 첫 번째 줄에서
# 오류가 나면 그 아래 줄들은 어떻게 되나요? 그래도 다 실행이 되나요?
# -> 답변: 안 됨. try 블록 안에서도 예외가 발생한 그 줄에서 바로 멈추고 except로 건너뜀.
#    즉 try 안에 두 번째, 세 번째 줄이 있었어도 첫 줄에서 이미 멈췄다면 나머지는 실행되지
#    않음. 그래서 "try는 작게 - 위험한 코드만 담아라"고 하는 이유가 여기 있음. 여러 위험한
#    작업을 한 try에 다 몰아넣으면, 정확히 어디서 멈췄는지 헷갈리기 쉬움

# [정리] try-except 사용 원칙 - 들여쓰기·작게·다 잡지 않기
# - 들여쓰기: 콜론으로 끝내고 안쪽 코드는 한 단계 들여쓰기 (if문·for문과 동일한 규칙)
# - try는 작게: 위험한 코드만 담아 오류 위치 파악에 유리하게 (너무 많이 감싸면 파악이 어려움)
# - 다 잡지 않기: 모든 코드를 try로 감싸면 잘못된 결과를 그대로 믿게 됨 - 진짜 버그까지 숨김


print("\n===================== 실습 2. try-except로 오류 넘기기 =====================")
# 목표: try-except로 오류가 나도 프로그램이 멈추지 않게 하기
# 단계: ① 오류가 날 수 있는 코드를 try 블록에 넣기 -> ② except 블록에 오류 시 실행할 안내를 작성
#      -> ③ 정상 값과 오류 나는 값을 각각 넣어 실행 -> ④ 오류가 나도 프로그램이 계속 진행되는지 확인
# 예상 결과: 정상값 -> 결과 / 오류값 -> 안내 후 계속 진행
def convert_measurement(text):
    try:
        return float(text)
    except ValueError:
        print(f"'{text}'는 숫자로 바꿀 수 없습니다")
        return None

print(convert_measurement("62.5"))  # 62.5
print(convert_measurement("abc"))  # 안내 후 None
print("프로그램 계속 진행")  # 오류가 나도 여기까지 정상적으로 도달함


# =====================================================================
# 구체적 예외 처리
# =====================================================================

# [개념] 값이 잘못됐을 때 - ValueError
# - 데이터 전처리에서 가장 많이 만나는 예외 - 타입은 맞지만 값이 부적절할 때 발생
# - 글자를 숫자로 바꿀 때 가장 자주 만남
int("62")  # 정상
# int("스물")  # ValueError - 문자열이라는 "종류"는 맞지만, "내용"이 숫자로 바꿀 수 없어 거부됨

# [정리] ValueError와 TypeError 구분 - "종류"가 틀린 것과 "내용"이 부적절한 것은 다름
# - ValueError: 종류는 맞고 내용이 부적절한 경우 (int("abc"), int("3.5")도 ValueError - int는 정수만 받음)
# - TypeError: 값의 종류 자체가 틀린 경우 (10 + "개" - 숫자와 문자열을 더하려 하면 발생)

# [개념] 파일이 없을 때 - FileNotFoundError
# - "파일을 찾을 수 없음" 오류 - open으로 열 때 그 파일이 그 위치에 없으면 발생
# - 파일명 오타와 경로 문제가 주요 원인
# - 실무 포인트: 설비 데이터는 거의 항상 CSV 파일을 열며 시작하므로, 첫 단계에서 이 예외에 대비하는 것이 중요

# [정리] FileNotFoundError 주요 원인 세 가지
# - 파일명 오타: sensor를 senser로 쓰거나 확장자 .csv를 빠뜨림 (가장 흔한 원인)
# - 경로 문제: 파일은 있는데 다른 폴더에 있음 (os.getcwd(), os.listdir()로 확인)
# - 확장자 숨김: 윈도우에서 .csv가 안 보일 수 있음 - 눈엔 sensor지만 실제론 sensor.csv일 수 있음

# [정리] 자주 만나는 그 밖의 에러 - 프로그래밍은 암기 과목이 아님
# - 큰 그림을 갖고, 빨간 글씨를 만나면 맨 아랫줄을 읽어 종류를 확인하면 됨 - 두세 번 만나면 자연스레 외워짐

# [정리] 자주 만나는 예외 정리 - 이 종류들만 알아도 초보 단계 예외의 대부분을 커버
# 예외                | 발생 상황     | 예시
# ValueError          | 값이 부적절   | int("스물")
# FileNotFoundError   | 파일이 없음   | open 실패
# ZeroDivisionError   | 0으로 나눔    | 평균 계산 시 데이터 0개
# IndexError          | 범위 초과     | 칸이 부족한 줄
# KeyError            | 없는 키 접근  | 딕셔너리 검색
# TypeError           | 값 종류가 틀림 | 10 + "개"


print("\n===================== 실습 3. 구체적 예외로 입력 검증하기 =====================")
# 목표: 구체적 예외(ValueError·ZeroDivisionError)를 지정해 입력을 검증하기
# 단계: ① 입력을 int로 바꾸는 코드를 try에 넣기 -> ② ValueError를 except로 잡아 안내
#      -> ③ 여러 except로 ZeroDivisionError도 구분해 처리 -> ④ 잘못된 입력을 넣어 프로그램이 멈추지 않는지 확인
# 예상 결과: 잘못된 입력 -> 안내 후 계속
def safe_divide(text, divisor):
    try:
        number = int(text)
        return number / divisor
    except ValueError:
        print(f"'{text}'는 숫자가 아닙니다")
    except ZeroDivisionError:
        print("0으로는 나눌 수 없습니다")

print(safe_divide("100", 5))  # 20.0
print(safe_divide("스물", 5))  # 안내 후 None
print(safe_divide("100", 0))  # 안내 후 None


# =====================================================================
# 견고한 예외처리 - else와 finally
# =====================================================================

# [문제 상황] 이 단원의 실데이터 - ICT 검사
# - ICT는 제조 부품의 전기 특성을 측정해 규격 안에 드는지 판정하는 검사 공정
# - 부품명별로 측정값·기준값·상한/하한을 기록 - 실제 현장 데이터에는 빈칸(결측)·형식 오류가 섞여 있음
# - 측정값이 비거나 문자·범위 밖이면 형변환·인덱스 오류가 남 - try·except로 불량 줄을 건너뛰고 견고하게 처리

# if-else문과는 다른 else. 성공했을 때만 실행되는 코드 (왜 와이. try를 하고 except문에 안 걸리면 else로 간다. 이거임)
# finally는 그럼 뭐겠어. 마침내 라는 뜻처럼 성공하든 실패하든 무조건 마지막에 실행된다.
# 파일 닫기처럼 반드시 해야하는 일처럼 여겨진다. 앞에서 어떤 데서 오셨든 상관없고, fianlly 문을 실행시키고 try문을 마감해주세요.
# 꼼꼼한 개발자를 나누는 기준이 되기도 한다

# [개념] else와 finally - 지난 시간에 배운 try/except에 두 형제가 더 붙음
# - else는 조건문의 else와 같은 단어로, try에서 예외가 하나도 발생하지 않았을 때만 실행됨
# - finally는 '마지막으로'라는 뜻 그대로, 성공하든 실패하든 무조건 마지막에 실행됨
# - 이 성질 덕분에 finally는 파일 닫기처럼 반드시 처리해야 할 마무리 작업에 자주 쓰임
def report_measurement(text):
    try:
        value = float(text)
    except ValueError:
        print(f"'{text}' 변환 실패")
    else:
        print(f"'{text}' -> {value} 변환 성공")  # 예외가 없을 때만 실행
    finally:
        print("처리 종료")  # 성공·실패 무조건 실행

report_measurement("62.5")  # 변환 성공 / 처리 종료
report_measurement("abc")  # 변환 실패 / 처리 종료

# [정리] 네 블록의 실행 정리
# CASE 01 성공 경로: try를 끝까지 실행한 뒤 else로 이동하고, 마지막에 finally가 실행됨
# CASE 02 실패 경로: try가 중단되면 except로 이동하고, 마지막에 finally가 실행됨
# CASE 03 자주 쓰는 것: 넷을 다 쓸 필요는 없음 - 초보 단계에서는 finally가 가장 유용

# [강사님께 질문하기] finally 안에서 또 오류가 나면 어떻게 되나요? 예를 들어 finally에서
# 파일을 닫으려는데 그 파일 닫기 자체에서 문제가 생기면요?
# -> 답변: finally 안에서 새로 발생한 오류는 원래 있던 오류를 덮어버리고, 그 새 오류가
#    프로그램을 멈추게 만듦. 즉 원래 except에서 처리하려던 문제가 있었어도, finally 안에서
#    또 다른 문제가 터지면 그 새로운 문제가 최종적으로 드러남. 그래서 finally 안에는 정말
#    "반드시 해야 하는 간단한 마무리 작업"만 넣는 것이 안전함 - 파일 닫기처럼 실패할 가능성이
#    매우 낮은 작업이 적합한 이유가 여기 있음

# [정리] 리소스 정리가 필요한 이유 - 정리는 선택이 아니라 의무
# - 파일을 열면 운영체제가 프로그램에 연결 통로를 내어줌 - 이 통로는 한정된 자원이라
#   닫지 않고 계속 쌓이면 결국 고갈됨
# - 파일에 쓴 내용은 닫는 순간 실제로 저장되기 때문에, 닫지 않으면 저장 대기 중인 데이터가 사라질 수 있음

# [정리] 파일을 안 닫으면 생기는 문제 세 가지
# - 통로 고갈: 파일을 계속 열고 닫지 않으면 운영체제가 더 이상 통로를 내주지 못하는 오류 발생
# - 데이터 손실: 저장 대기 중인 내용이 그대로 사라질 수 있음 - 파일은 닫는 순간 실제로 저장됨
# - 예외 시 위험: 읽다가 예외가 나면 그 아래 close가 실행되지 않음 - 그래서 finally에 닫기를 넣어야 함

import os

exc_dir = "exception_practice"
os.makedirs(exc_dir, exist_ok=True)


print("\n===================== 실습 4. finally로 파일 안전하게 닫기 =====================")
# 목표: try-finally로 오류가 나도 파일을 반드시 닫기
# 단계: ① try 블록에서 파일을 열어 처리 -> ② 처리 도중 오류가 날 수 있음을 가정
#      -> ③ finally 블록에 close를 넣어 오류 여부와 상관없이 닫기 -> ④ 일부러 오류를 내도 finally가 실행되는지 확인
# 예상 결과: 오류가 나도 파일이 안전하게 닫힘
log_path = os.path.join(exc_dir, "check_log.txt")
f = open(log_path, "w", encoding="utf-8")
try:
    f.write("1번 부품 측정 완료\n")
    dummy = int("이상없음")  # 일부러 오류를 냄 (문자를 정수로 변환 시도)
    f.write("2번 부품 측정 완료\n")  # 위에서 멈췄으므로 이 줄은 실행되지 않음
except ValueError:
    print("측정값 변환 중 오류 발생")
finally:
    f.close()
    print("파일 닫기 완료")

print(f.closed)  # True - 오류가 나도 파일은 안전하게 닫힘


# [개념] with open으로 더 안전하게 - with open을 쓰면 자동으로 닫힘, 파일 처리의 표준
# with open(name) as f:
#     data = f.readlines()  # 블록 끝나면 자동으로 닫힘
# - with open as f 형태로 쓰면, 들여쓴 블록이 끝나는 순간 파이썬이 알아서 파일을 닫아줌
# - 심지어 블록 안에서 예외가 나도 빠져나가기 전에 반드시 닫아줌 - finally를 직접 쓴 것과 같은 효과
with open(log_path, "a", encoding="utf-8") as f2:
    try:
        f2.write("3번 부품 측정 완료\n")
        raise ValueError("강제로 발생시킨 오류")
    except ValueError as e:
        print("오류 발생:", e)
print(f2.closed)  # True - with 블록을 빠져나가면 예외가 나도 자동으로 닫힘

# [정리] with open 사용 시 주의점
# - 자동 닫힘: 블록이 끝나면 예외가 나도 무조건 닫힘 - 닫기를 자동화해 주는 가장 큰 장점
# - 블록 밖 주의: 블록 밖에서 쓸 값은 블록 안에서 리스트나 변수에 담아두어야 함 (밖에서는 이미 닫혀 있음)
# - 열기 실패 대비: with는 닫기만 자동임 - 파일 없음은 여전히 try-except로 따로 처리해야 함


# =====================================================================
# CSV 읽기 정답 - 두 겹의 try-except
# =====================================================================

import csv

ict_sample_path = os.path.join(exc_dir, "ict_sample.csv")
with open(ict_sample_path, "w", encoding="utf-8", newline="") as f:
    f.write("부품명,측정값,기준값,상한,하한\n")
    f.write("R-1001,62.3,60,65,55\n")
    f.write("R-1002,58.1,60,65,55\n")
    f.write("R-1003,,60,65,55\n")  # 결측 (빈칸)
    f.write("R-1004,61.0,60,65,55\n")
    f.write("R-1005,NG,60,65,55\n")  # 형식 오류 (문자)
    f.write("R-1006,63.4,60,65,55\n")
    f.write("R-1007,59.9,60,65,55\n")
    f.write("R-1008,60.2,60,65,55\n")
    f.write("R-1009,57.8,60,65,55\n")
    f.write("R-1010,64.1,60,65,55\n")

# 바깥 try-except는 파일이 없는 경우를 막고, 안쪽 try-except는 각 칸을 숫자로
# 못 바꾸는 경우를 막는다 - 두 위험을 각각 다른 위치에서 처리하는 것이 핵심
good_values = []
bad_count = 0
try:
    with open(ict_sample_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # 헤더 건너뛰기
        for row in reader:
            try:
                good_values.append(float(row[1]))
            except ValueError:
                bad_count += 1  # 숫자로 못 바꾸는 칸은 건너뜀
except FileNotFoundError:
    print("파일을 찾을 수 없습니다")

print(f"정상 {len(good_values)}개, 불량 {bad_count}개")  # 정상 8개, 불량 2개


# =====================================================================
# 반복문 안에서의 예외처리
# =====================================================================

# [개념] 반복문 안에 try-except를 넣고 continue로 불량 줄만 건너뛰기
# - 대용량 데이터를 안전하게 처리하는 핵심 패턴 - 가장 실용적인 패턴
# - 수천 줄에서 불량 줄만 쏙 빼고 나머지는 모두 처리함
# - 데이터를 한 줄씩 반복하며 각 줄의 처리를 try로 감싸고, 문제가 생기면 except에서 continue로 다음 줄로 넘어감
sample_measurements = ["62.3", "58.1", "", "61.0", "NG", "63.4"]
demo_total = 0
demo_count = 0
for value in sample_measurements:
    try:
        number = float(value)
    except ValueError:
        continue  # 불량 값은 건너뛰고 다음 값으로
    demo_total += number
    demo_count += 1
print(demo_total, demo_count)  # 244.8 4

# [정리] 반복문 예외처리 포인트
# - continue 역할: 이번 회차를 멈추고 다음 회차로 넘어가라는 명령 ('이 줄 건너뛰고 다음 줄로')
# - try 위치: 반복문 안쪽에 두어야 불량 줄만 건너뜀 - 바깥에 두면 첫 불량에서 전체가 중단됨
# - 불량 기록: 나중에 어떤 데이터가 불량이었는지 점검할 수 있도록 줄 번호를 모아두면 좋음

# [강사님께 질문하기] continue가 없어도 반복문은 어차피 다음 값으로 계속 넘어가지
# 않나요? 왜 굳이 continue를 써줘야 하나요?
# -> 답변: 반복문 자체는 continue 없이도 다음 회차로 넘어감 - 맞는 말임. 하지만 continue의
#    진짜 역할은 "반복을 계속 돌게 하는 것"이 아니라 "이번 회차의 남은 코드를 건너뛰는 것".
#    except 아래에 그 값을 이어서 쓰는 코드(합계에 더하기, 출력하기 등)가 있다면, continue가
#    없을 때 그 코드가 실패한 값이 아니라 "직전 회차에 성공했던 값"을 조용히 재사용해버림 -
#    변수가 새로 대입되지 않았을 뿐 여전히 메모리에 남아있기 때문. 아래 실습으로 직접 확인

# [실습] continue를 빼면 어떤 문제가 생기는지 직접 확인
buggy_list = ["123", "456", "영크크", "32", "53"]
for text in buggy_list:
    try:
        my_number = int(text)
    except ValueError:
        print(f"'{text}'는 숫자로 바꿀 수 없습니다.")
        # continue를 일부러 빼봄
    else:
        print(f"'{text}'는 숫자로 바꿀 수 있습니다.")
    print(my_number, type(my_number))
# 출력: 123 / 456 / 456(!) / 32 / 53
# "영크크"는 실패했는데도 직전 회차("456")의 my_number가 그대로 남아있어서 456이 또
# 출력됨 - 마치 "영크크"가 456으로 정상 변환된 것처럼 보이는 잘못된 기록이 남음

# [퀴즈] 아래 리스트로 위와 같은 코드(continue 없이)를 돌리면 무슨 일이 벌어질까?
# no_continue_list = ["영크크", "10", "20"]
# for text in no_continue_list:
#     try:
#         my_number = int(text)
#     except ValueError:
#         print(f"'{text}'는 숫자로 바꿀 수 없습니다.")
#     else:
#         print(f"'{text}'는 숫자로 바꿀 수 있습니다.")
#     print(my_number)
# 정답: 첫 번째 값부터 실패라서 NameError
# ('영크크'는 실패 -> my_number가 이전에 단 한 번도 만들어진 적이 없어서
#  print(my_number)에서 존재하지 않는 이름을 참조 -> NameError)


print("\n===================== 실습 5. 반복문에서 불량 줄 건너뛰기 =====================")
# 목표: 반복문 안에서 try-except와 continue로 불량 줄만 건너뛰기
# 단계: ① 여러 측정값(일부는 숫자가 아님)을 반복 -> ② try에서 float로 변환
#      -> ③ 변환 실패(ValueError) 시 continue로 그 줄만 건너뛰기 -> ④ 정상 값만 합계에 더해 출력
# 예상 결과: 불량 줄은 건너뛰고 정상값만 합산
readings = ["62.3", "58.1", "", "61.0", "NG", "63.4", "59.9"]
total_sum = 0
for reading in readings:
    try:
        total_sum += float(reading)
    except ValueError:
        continue
print(total_sum)  # 304.7
print(total_sum / 5)  # 60.94 (정상값 5개의 평균)


print("\n===================== 실습 6. 여러 파일 묶어 처리하기 =====================")
# 목표: 여러 파일을 묶어 처리하되 없는 파일은 건너뛰기
# 단계: ① 여러 파일 이름을 반복 -> ② try에서 파일을 열어 처리
#      -> ③ 없는 파일(FileNotFoundError) 시 continue로 건너뛰기 -> ④ 처리한 파일 수를 세어 출력
# 예상 결과: 없는 파일은 건너뛰고 있는 파일만 처리
with open(os.path.join(exc_dir, "part_a.csv"), "w", encoding="utf-8") as f:
    f.write("데이터 A\n")
with open(os.path.join(exc_dir, "part_b.csv"), "w", encoding="utf-8") as f:
    f.write("데이터 B\n")
# part_c.csv는 일부러 만들지 않음 - 없는 파일을 열려고 하면 어떻게 되는지 확인하기 위함

file_names = ["part_a.csv", "part_b.csv", "part_c.csv"]
processed_count = 0
for name in file_names:
    file_path = os.path.join(exc_dir, name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        continue
    processed_count += 1
print(processed_count)  # 2 (part_c.csv는 없어서 건너뜀)


# =====================================================================
# bare except의 위험
# =====================================================================

# [개념] bare except - 모든 예외를 뭉뚱그려 잡는 except는 진짜 버그를 숨김
# - except 뒤에 아무것도 안 붙이고 그냥 except만 써도 동작함 - 모든 예외를 다 잡는 이것을
#   bare except라고 부르며, 피해야 할 나쁜 습관
# - bare except는 예상한 예외뿐 아니라 변수 오타 같은 진짜 버그까지 잡아 조용히 넘어가 버림
# - except 뒤에는 반드시 ValueError처럼 구체적인 이름을 적어야 함

# bare except가 위험한 이유를 직접 확인
try:
    typo_result = mistyped_reading_variable + 1  # 오타로 존재하지 않는 변수를 사용 - 진짜 버그
except:
    pass  # bare except: 무슨 문제인지 몰라도 그냥 넘어가 버림 -> 버그를 발견하지 못함
print("bare except 이후에도 아무 경고 없이 진행됨 (버그를 놓친 상태)")

try:
    typo_result2 = mistyped_reading_variable + 1
except NameError as e:
    print("구체적으로 지정하면 진짜 버그가 드러남:", e)

# [정리] bare except를 피해야 하는 이유
# - RISK 01 버그 숨김: 변수 오타 등 진짜 버그도 잡아서 못 찾게 됨 - 경고등을 테이프로 가리는 격
# - RISK 02 중단 신호까지: 강제 종료 신호마저 잡아 프로그램을 못 멈출 수 있음
# - DO INSTEAD 대안: 예상 예외만 적고, 새 예외를 만날 때마다 하나씩 추가

# [강사님께 질문하기] except를 아예 안 쓰고 그냥 코드가 오류로 멈추게 놔두는 것과,
# bare except로 일단 다 잡아버리는 것 중에 뭐가 더 나은가요? 둘 다 안 좋다면서요.
# -> 답변: 놀랍게도 그냥 멈추게 놔두는 쪽이 더 나음. 코드가 멈추면 적어도 "여기서 문제가
#    생겼다"는 사실을 바로 알 수 있고, 어디를 고쳐야 하는지도 명확함. 반면 bare except로
#    다 잡아버리면 프로그램은 계속 돌아가지만 사실은 잘못된 상태로 흘러가고 있을 수 있음 -
#    마치 계기판 경고등을 테이프로 가려버린 채 운전하는 것과 비슷함. 그래서 "아무것도 안
#    하는 것"보다 "잘못 처리하는 것"이 더 위험할 수 있다는 게 핵심 - 결국 가장 좋은 답은
#    예상되는 오류만 정확히 짚어서 처리하는 것


# =====================================================================
# 좋은 예외처리 원칙
# =====================================================================

# [개념] 좋은 예외처리 원칙 - 문법을 아는 것과 잘 쓰는 것은 다름
# - 핵심: 예상한 문제는 우아하게 처리하고, 예상 못한 문제는 숨기지 말고 드러내라
# - 이 균형 감각이 견고한 프로그램과 위험한 프로그램을 가름

# [정리] 나쁜 예외처리 vs 좋은 예외처리
# 구분     | 나쁜 예   | 좋은 예
# 예외 지정 | 전부 잡기 | 구체적 지정
# try 범위 | 전체 감쌈 | 위험한 줄만
# 문제 처리 | 무시     | 줄 번호 기록

# [정리] 좋은 예외처리 4원칙 - 구체적으로 · 작게 · 기록 · 드러내기
# - 구체적으로: bare except 대신 예상되는 예외만 정확히 지정
# - 작게: 위험한 코드만 try에 담아 오류 위치를 명확히 함
# - 기록: 어떤 데이터가 왜 빠졌는지 기록해야 분석 신뢰도가 올라감
# - 드러내기: 예상 못한 예외는 잡지 말고 드러내서 코드를 고치게 둠

# [개념] 에러 정보 꺼내 쓰기 - as e
# - except 뒤에 as e를 붙이면 e에 예외 정보가 담김
# - e를 출력하면 트레이스백 맨 아랫줄에서 봤던 그 구체적인 설명이 나옴
# - 단순히 '문제 발생'이 아니라 어떤 값이 왜 문제인지를 기록할 수 있음
try:
    temp = float("이상")
except ValueError as e:
    print(e)  # invalid literal for float(): '이상' 형태의 구체적 메시지

# [정리] as e 활용 포인트
# - 맥락 결합: 내가 아는 줄 번호와 파이썬이 주는 원인을 합치면 더 정확한 기록이 됨
# - 사용자용: 사용자에겐 '온도 값이 올바르지 않습니다'처럼 이해하기 쉬운 우리말 안내를 제공
# - 개발자용: 기록에는 e의 구체적 원인을 남겨 나중에 원인을 추적

# [개념] raise로 직접 예외 발생시키기
# - 영하 999도 같은 값은 파이썬 입장에선 정상 숫자 - 아무 예외도 나지 않음
# - 하지만 우리는 이 값이 센서 오류인 것을 알고 있음
# - 우리가 정한 범위를 벗어나면 raise로 직접 ValueError를 일으킴 - 이렇게 일으킨 예외도 try-except로 잡을 수 있음
# - raise는 파이썬이 못 잡는 우리만의 규칙을 코드로 강제하는 도구
def check_temperature(temp):
    if temp > 200:
        raise ValueError("비정상 온도")
    return temp

try:
    check_temperature(999)
except ValueError as e:
    print("검증 실패:", e)

print(check_temperature(80))  # 80 (정상 범위라 그대로 반환)

# [정리] raise 활용 포인트
# - 현실 규칙: 온도·압력·진동마다 현실적인 정상 범위가 있음 - raise로 이 범위를 강제
# - 역할 분리: 검증 함수는 raise로 예외만 일으키고, 호출하는 쪽이 try-except로 대응을 정함
# - 예외 종류: 값이 부적절한 경우이니 ValueError를 쓰는 것이 자연스러움

# [강사님께 질문하기] raise로 내가 직접 예외를 일으키면, 그건 파이썬이 원래 알려주는
# 오류랑 뭐가 다른가요? 겉보기엔 똑같이 빨간 글씨가 뜨는데요.
# -> 답변: 겉모습은 똑같이 빨간 글씨로 멈추지만, 누가 그 판단을 내렸는지가 다름. 파이썬이
#    스스로 내는 오류는 "문법이나 계산 자체가 불가능하다"는 파이썬의 판단이고, raise로
#    우리가 직접 내는 오류는 "파이썬 입장에서는 멀쩡한 값이지만, 우리가 정한 현실 규칙
#    (예: 온도는 200도를 넘으면 안 됨)에는 어긋난다"는 우리의 판단. 즉 raise는 파이썬이
#    못 알아채는, 우리 업무 지식에서 나온 규칙을 코드에 심어 넣는 방법 - 그래서 raise로
#    만든 오류도 try-except로 똑같이 잡아서 대응할 수 있음


print("\n===================== 실습 7. 함수 안에서 입력값 검증하기 =====================")
# 목표: 함수 안에서 잘못된 입력을 직접 검증하고 안전하게 처리하기
# 단계: ① 입력값을 받는 함수를 정의 -> ② try에서 float로 변환해 검증
#      -> ③ 변환 실패 시 except로 안내하고 기본값 처리 -> ④ 정상·비정상 입력을 각각 넣어 확인
# 예상 결과: 정상 입력 -> 값 / 잘못된 입력 -> 안내 후 기본값
def validate_reading(text):
    try:
        value = float(text)
    except ValueError:
        print(f"'{text}'는 올바른 측정값이 아닙니다 - 기본값 0.0으로 처리")
        return 0.0
    return value

print(validate_reading("62.3"))  # 62.3
print(validate_reading("NG"))  # 안내 후 0.0


# =====================================================================
# [흔한 질문 진단] 예외처리하면서 헷갈리기 쉬운 것들
# =====================================================================

# Q1. else 블록은 except가 없을 때도 실행되나요? try가 성공만 하면 무조건 실행되나요?
# -> A. try가 예외 없이 끝까지 실행됐을 때만 실행됨. except를 안 만들었어도 try에서
#       예외가 나면 프로그램이 그 자리에서 멈추므로(예외를 처리할 except가 없어서) else까지
#       도달하지도 못함. else는 "try가 무사히 끝났을 때"라는 조건이 핵심

# Q2. try 블록 안에서 값을 여러 개 계산했는데, 중간에 예외가 나면 그전까지 계산한 값들은
#     남아있나요?
# -> A. 남아있음. 예외가 나기 전에 이미 실행된 줄들의 결과(변수에 저장된 값)는 그대로
#       메모리에 남음. 다만 예외가 난 줄 이후의 코드가 실행되지 않을 뿐이라, 그 뒤에서
#       쓰려던 값들만 만들어지지 않은 상태로 남게 됨

# Q3. try 안에서 return을 만나면 finally는 실행되나요, 건너뛰나요?
# -> A. 실행됨. finally는 함수가 어떤 경로로 끝나든(정상 return이든 예외든) 반드시
#       마지막에 실행되도록 설계된 블록이라, return으로 함수를 빠져나가려는 순간에도
#       finally를 먼저 실행한 뒤에 실제로 함수를 빠져나감

# Q4. finally에서 쓸 변수는 except 안에서 초기화하는 게 나을까, try 앞에서 미리
#     초기화하는 게 나을까?
# -> A. 둘 다 가능하지만 안전성은 다름.
#    - except 안에서만 초기화: try가 성공하면 실제 값, 실패하면 그 except가 넣은 기본값이
#      들어감. 하지만 except가 여러 개면 각 except마다 빠짐없이 넣어줘야 하고, 예상 못 한
#      예외 타입이 와서 그 except에 안 걸리면 여전히 finally에서 NameError가 남
#    - try 앞에서 미리 초기화: 성공하든, 예상한 예외든, 심지어 못 잡은 예외든 변수가 이미
#      존재하므로 finally에서 절대 NameError가 나지 않음 - 더 안전한 기본 선택
#    실무 팁: 기본값은 0보다 None이 나을 때가 많음. 0은 "진짜 0값"과 "실패해서 넣은
#    기본값"을 구분 못 하지만, None은 나중에 `if temp is not None:`으로 성공·실패를
#    명확히 구분할 수 있음
def demo_pre_init(text):
    temp = None  # try 앞에서 미리 초기화 - 실패 여부를 구분하는 sentinel 값
    try:
        temp = float(text)
    except ValueError:
        print(f"'{text}' 변환 실패")
    finally:
        if temp is not None:
            print(temp * 2)
        else:
            print("계산 불가 (변환 실패)")

demo_pre_init("31.0")  # 62.0
demo_pre_init("영크크")  # 변환 실패 / 계산 불가 (변환 실패)

# [퀴즈] 아래 코드에서 두 번째 호출은 무슨 일이 벌어질까? (except가 엉뚱한 예외를 잡고 있음)
# def risky(text):
#     try:
#         temp = float(text)
#     except TypeError:  # 일부러 ValueError가 아닌 다른 예외만 잡음
#         temp = 0
#     finally:
#         print(temp * 2)
#
# risky("10")
# risky("abc")
# 정답:
# 20.0
# NameError: name 'temp' is not defined
# (float("abc")는 ValueError를 내는데 except는 TypeError만 잡고 있어서 못 잡음
#  -> temp 대입 자체가 실패해 변수가 아예 안 생김 -> finally의 print(temp*2)가
#  존재한 적 없는 temp를 참조하려다 NameError. except 안에서만 초기화하는 방식의
#  약점이 바로 이것 - try 앞에서 미리 초기화했다면 이 상황에서도 안전했을 것)


# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# def test(text):
#     try:
#         val = float(text)
#     except ValueError:
#         print("실패")
#     else:
#         print("성공:", val)
#     finally:
#         print("종료")
#
# test("10")
# test("abc")
# 정답:
# 성공: 10.0
# 종료
# 실패
# 종료
# (실패했을 때는 else가 건너뛰어지지만, finally는 성공·실패 상관없이 항상 실행됨)

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# values = ["10", "", "20"]
# total = 0
# for v in values:
#     try:
#         total += int(v)
#     except ValueError:
#         continue
# print(total)
# 정답: 30 ("" 는 int로 못 바꿔 ValueError가 나서 건너뛰고, 10과 20만 더해짐)
