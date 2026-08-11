# =====================================================================
# Pandas 기초 - 입문 / DataFrame 구조
# =====================================================================

# [문제 상황] 이 과정의 실데이터 - 지하철 공기압축기(MetroPT-3)
# - 공정: 지하철 전동차의 공기압축기(APU)가 브레이크·출입문에 쓰는 압축공기를 만듦
# - 압력·온도·전류를 1초마다 기록한 대용량 설비 로그
# - 핵심 변수: 측정시각 · 압축/배출/저장 압력(bar) · 오일온도(℃) · 모터전류(A) · 가동상태(가동/정지)
#   - 시각·문자·숫자가 한 표에 섞여 있음
# - 정상과 이상: 가동하면 모터전류가 오르고 압력이 차오름 - 오일온도가 비정상적으로 오르거나
#   압력이 안 차오르면 고장 신호로 봄
# - 왜 Pandas인가: 시각·문자·숫자가 섞인 대용량 로그를 표(DataFrame)로 불러와 head·shape·
#   dtypes·describe로 구조와 상태를 빠르게 파악하기 위해

# [개념] 표 데이터를 코드로 다뤄야 하는 이유 - 설비 데이터는 손이 아닌 코드로 다뤄야 처리 가능
# - 1초에 한 번 측정 -> 하루 86,400줄, 센서 수십 개 -> 하루 수백만 줄
# - 엑셀로 스크롤하며 눈으로 보기에는 불가능한 양 - 코드로 다루면 데이터가 늘어나도 같은 명령 한 줄로 처리

# [정리] 코드로 데이터를 다루는 세 가지 이점
# - 대량 처리: 수백만 줄도 명령 한 줄로 (데이터 규모와 무관한 처리 속도)
# - 재사용: 한 번 짠 코드를 새 데이터에 그대로 재실행 (엑셀은 매번 처음부터, 코드는 다시 돌리기만 하면 끝)
# - 정확성: 코드는 오차 없이 정확히 반복 (고장 신호 하나가 큰 사고로 이어지는 설비 분야에서 특히 중요)

# [정리] 엑셀의 한계와 Pandas의 강점 - 엑셀과 Pandas는 경쟁자가 아니라 역할이 다른 도구
# - 엑셀은 언제 좋은가: 수백 줄 데이터를 눈으로 보며 직접 고치고 색칠할 때
# - 엑셀의 한계는: 한 시트 최대 104만 행, 수십만 줄만 돼도 느려짐
# - Pandas의 강점은: 수백만 줄도 빠르게, 복잡한 작업도 코드 몇 줄로 반복

# [정리] 엑셀과 Pandas의 역할 구분 - 실무에서는 둘을 함께, 무거운 처리는 Pandas, 보기 좋게는 엑셀
# - 엑셀: 적은 데이터를 눈으로 보기 (칼·도마 같은 도구) - 수백 줄·시각 점검·색칠
# - Pandas: 대용량 반복 처리 (재료가 많을수록 진가가 드러나는 주방 기계) - 수백만 줄·반복 자동화
# - 함께: Pandas로 무거운 처리를 끝내고 엑셀로 보기 좋게 다듬는 조합이 실무 표준

# [개념] 설비 데이터가 표로 쌓이는 방식 - 행은 한 시점의 측정 기록, 열은 하나의 측정 항목
# index | 측정시각  | 오일온도 | 모터전류 | 가동상태
# 0     | 06:38:47 | 51.3    | 6.04    | 가동
# 1     | 07:28:21 | 56.8    | 0.04    | 정지
# 2     | 08:17:54 | 55.7    | 0.03    | 정지
# 3     | 09:07:27 | NaN     | 3.81    | 가동
# 4     | 09:57:01 | 55.3    | 0.04    | 정지
# 행은 시간이 지나며 늘어나고, 열은 측정 항목 수만큼 고정 - 다른 설비 데이터도 같은 구조

# [개념] Series - 한 줄짜리 데이터, Pandas의 두 그릇 중 작은 그릇 (표의 한 열에 해당)
# - 정의: 같은 종류 값이 일렬로 늘어선 한 열 (온도 열 전체처럼 한 가지 의미의 값이 순서대로 모인 것)
# - 인덱스: 각 값에 붙는 번호표, 0·1·2 순서로 부여 (출석부 학생 번호에 점수가 적힌 것처럼 빠른 접근의 키)
# - 활용: DataFrame의 열 한 개가 Series - 따로 외울 개념이 아니라 우리가 늘 다루는 표의 한 조각

# [개념] DataFrame - 표 전체를 담는 그릇, 여러 Series가 모이면 우리가 아는 엑셀 표
# - 정의: 여러 Series가 옆으로 모인 표 (설비 데이터 7개 열이 옆으로 붙으면 하나의 DataFrame)
# - 강점: 원하는 행·열을 자유롭게 선택 (온도 열만 보기·100도 넘는 행만 골라내기 같은 작업이 간단한 코드로)
# - 핵심: CSV를 불러오면 바로 DataFrame - 앞으로 df라고 쓰면 거의 항상 이 DataFrame을 가리킴

# [정리] 행 · 열 · 인덱스 개념 잡기
# - ROW(행): 가로 한 줄 - 특정 시점의 한 건 기록 (그 시각의 오일온도·모터전류·압력이 함께 담김)
# - COLUMN(열): 세로 한 칸 - 하나의 측정 항목 (오일온도면 오일온도값만 죽 들어감)
# - INDEX(인덱스): 각 행에 붙은 번호표 - 0부터 시작 (엑셀의 왼쪽 행 번호와 같은 역할)
# - 가로로 자르면 행, 세로로 자르면 열, 왼쪽 끝 번호가 인덱스

# [강사님께 질문하기] DataFrame의 열 하나를 꺼내면 Series가 된다고 했는데, 그럼 Series는
# DataFrame과 완전히 다른 별개의 자료구조인가요, 아니면 DataFrame이 Series 여러 개를 그냥
# 리스트처럼 모아둔 것뿐인가요?
# -> 답변: 완전히 별개는 아니고, DataFrame 내부는 실제로 각 열이 하나씩 독립된 Series로
#    존재하고 그 Series들이 같은 인덱스를 공유하며 옆으로 나란히 묶여 있는 구조에 가까움.
#    그래서 열 하나를 꺼내면 그 열을 담당하던 Series가 그대로 나오는 것이고, 반대로
#    Series 여러 개를 나란히 붙이면 DataFrame이 됨. 즉 DataFrame은 Series를 감싸는 별도의
#    새로운 상자라기보다는, 여러 Series를 같은 인덱스 기준으로 정렬해서 보여주는 하나의
#    "표 형태 뷰"에 가까움

# [정리] Jupyter에서 DataFrame 출력 읽기 - 셀에 변수만 적으면 표가 자동 정렬됨 (이 파일은
# .py 스크립트라 실제로는 print()를 써야 값이 보이지만, Jupyter 노트북 셀에서는 변수 이름만
# 적어도 표가 자동으로 예쁘게 출력됨 - 이 차이를 알아두면 나중에 노트북에서 헷갈리지 않음)
# - 가운데 생략: 행이 많으면 가운데가 ...로 줄어들어 보임 (위·아래 5줄만 보이고, 데이터는 그대로)
# - 빈 칸 표시: 값이 없는 칸은 NaN(Not a Number)으로 표시되는 결측치 - 측정값이 빠진 자리

# [강사님께 질문하기] NaN은 "값이 없다"는 뜻이라고 했는데, 그럼 그냥 빈 문자열("")이나
# 0을 넣어서 "없음"을 표시하면 안 되나요? 왜 굳이 NaN이라는 걸 따로 만들었나요?
# -> 답변: 빈 문자열이나 0은 이미 "다른 의미"로 쓰이고 있어서 결측과 헷갈림. 예를 들어
#    모터전류가 0이면 그건 진짜로 "전류가 0A로 측정됐다"는 정상적인 값일 수도 있는데,
#    결측을 표시하려고 0을 쓰면 "측정을 안 했다"와 "측정했더니 0이었다"를 구분할 수 없게
#    됨. NaN은 숫자 자리에 들어갈 수 있으면서도 어떤 진짜 숫자와도 겹치지 않는 특별한
#    표시라서, 계산에 실제 값으로 섞여 들어가는 일 없이 "이 자리는 비어 있다"는 사실만
#    정확하게 남길 수 있음

# [정리] Pandas 데이터 분석 4단계 작업 흐름 - 불러오기 -> 구조확인 -> 미리보기 -> 통계요약
# ① 불러오기: CSV 파일을 read_csv로 읽어 DataFrame으로 변환 (문 열고 들어가기)
# ② 구조 확인: 행·열 수, 자료형 같은 데이터 뼈대 확인 (구조 둘러보기)
# ③ 미리보기: head·tail로 실제 값을 직접 눈으로 확인 (방 들여다보기)
# ④ 통계 요약: describe로 평균·최대·최소를 한 번에 추출 (평수 확인)
# 집을 살펴보는 것과 같음 - 베테랑 분석가도 이 순서를 밟음
# (②③④는 다음 실습 파일에서 본격적으로 다룸 - 오늘은 ①에 집중)

import os
import csv


print("\n===================== 실습 1. CSV 불러오기 워밍업 =====================")
# 목표: 작은 설비 데이터를 CSV로 만들고, 메모장으로 볼 때와 표로 볼 때가 어떻게 다른지 확인
# 단계: ① 설비 3대의 측정시각·오일온도·모터전류를 쉼표로 이어 CSV로 저장
#      -> ② 메모장처럼 원본 텍스트 그대로 읽어 쉼표가 살아있는 모습 확인
#      -> ③ 엑셀처럼 줄 단위로 쪼개 칸이 나뉜 모습 확인
# 예상 결과: 같은 파일이 원본 텍스트로 볼 때와 표로 볼 때 다르게 보임
os.makedirs("data", exist_ok=True)

warmup_path = os.path.join("data", "12_warmup_compressor.csv")
with open(warmup_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["측정시각", "오일온도", "모터전류"])
    writer.writerow(["06:38:47", "51.3", "6.04"])
    writer.writerow(["07:28:21", "56.8", "0.04"])
    writer.writerow(["08:17:54", "55.7", "0.03"])

with open(warmup_path, "r", encoding="utf-8-sig") as f:
    print(f.read())  # 메모장으로 열면 이렇게 쉼표가 그대로 보임 - CSV의 진짜 속살

with open(warmup_path, "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)  # 엑셀처럼 쉼표 기준으로 칸이 나뉜 모습


# =====================================================================
# Pandas 기초 - CSV 불러오기 / read_csv 옵션
# =====================================================================

# [개념] CSV 파일이란 무엇인가 - 값을 쉼표로 구분해 저장한 단순한 텍스트 파일
# - 구조: 한 줄이 표의 한 행, 줄 안에서 값들이 쉼표로 나뉨 (Comma-Separated Values)
# - 헤더: 첫 줄은 보통 열 이름, 그 아래 줄들이 데이터
# - 호환성: 엑셀·메모장·파이썬 어디서나 열리는 범용 형식 - 설비 시스템·공정 DB·공공데이터 거의 다 CSV

# [정리] CSV를 메모장 · 엑셀로 열어보기 - 같은 파일도 도구에 따라 다르게 보임 (내용은 똑같음)
# - 메모장으로 열면: 쉼표로 이어진 값이 그대로 보임
# - 엑셀로 열면: 쉼표 기준으로 칸이 자동으로 나뉘어 깔끔한 표로 보임
# - Pandas가 하는 일은: 엑셀처럼 쉼표로 칸을 나눠 DataFrame 표로 변환
# 문제가 생기면 메모장으로 원본 확인 - 가장 확실한 습관

# [개념] import pandas as pd - Pandas를 pd라는 별명으로 불러오는 코드, 모든 분석의 첫 줄
import pandas as pd
import numpy as np
# import = 외부 도구 불러오기, as pd = pandas를 pd라는 별명으로 부르겠다는 약속
# 실행해도 출력은 없음 - 오류 없이 넘어가면 성공

# [정리] import의 약속, pd - 전 세계 분석가가 통일해서 사용하는 별명
# - 다른 별명을 쓰지 않아야 다른 사람 코드도 쉽게 읽힘
# - 긴 pandas 대신 짧은 pd로 모든 기능 호출 - pandas.read_csv 대신 pd.read_csv
# - import 줄은 노트북(파일) 맨 위에 한 번만 작성, 한 번 불러오면 계속 사용 가능


# [설정] 이 파일의 read_csv 실습이 항상 재현되도록, 강의의 지하철 공기압축기(MetroPT-3) 로그와
# 같은 구조(측정시각·압축압력·배출압력·저장압력·오일온도·모터전류·가동상태)를 가진 200행짜리
# 표본 데이터를 코드로 직접 만들어 저장해 둔다 (인덱스 3번 행의 오일온도만 결측으로 비워둠)
np.random.seed(42)
n_rows = 200
start_time = pd.Timestamp("2020-02-27 06:38:47")
interval = pd.Timedelta(seconds=2974)  # 실측 로그와 같은 약 49분 34초 간격
timestamps = [start_time + i * interval for i in range(n_rows)]

given_status = ["가동", "정지", "정지", "가동", "정지"]
given_compressed = [9.3, 8.55, 8.2, 8.9, 8.1]
given_oil = [51.3, 56.8, 55.7, np.nan, 55.3]
given_current = [6.04, 0.04, 0.03, 3.81, 0.04]

statuses, compressed_pressure, discharge_pressure = [], [], []
storage_pressure, oil_temp, motor_current = [], [], []

for i in range(n_rows):
    if i < 5:
        status = given_status[i]
        c_pressure = given_compressed[i]
        oil = given_oil[i]
        current = given_current[i]
    else:
        status = np.random.choice(["가동", "정지"], p=[0.3, 0.7])
        running = status == "가동"
        c_pressure = round(np.random.uniform(8.0, 9.5) if running else np.random.uniform(6.5, 8.0), 2)
        oil = round(np.random.uniform(50.0, 58.0), 1)
        current = round(np.random.uniform(3.0, 7.0) if running else np.random.uniform(0.02, 0.05), 2)

    statuses.append(status)
    compressed_pressure.append(c_pressure)
    discharge_pressure.append(round(c_pressure - np.random.uniform(0.3, 0.8), 2))
    storage_pressure.append(round(np.random.uniform(7.0, 9.0), 2))
    oil_temp.append(oil)
    motor_current.append(current)

metro_df = pd.DataFrame({
    "측정시각": timestamps,
    "압축압력": compressed_pressure,
    "배출압력": discharge_pressure,
    "저장압력": storage_pressure,
    "오일온도": oil_temp,
    "모터전류": motor_current,
    "가동상태": statuses,
})

comma_path = os.path.join("data", "12_metro_compressor.csv")
metro_df.to_csv(comma_path, index=False, encoding="utf-8-sig")

semi_path = os.path.join("data", "12_metro_compressor_semicolon.csv")
metro_df.to_csv(semi_path, index=False, sep=";", encoding="utf-8-sig")

cp949_path = os.path.join("data", "12_metro_compressor_cp949.csv")
metro_df.head(5).to_csv(cp949_path, index=False, encoding="cp949")


# [개념] pd.read_csv() 기본 사용법 - 파일 이름을 따옴표로 감싸 넣으면 결과가 DataFrame으로 반환
df = pd.read_csv(comma_path)
print(df.head())
# 괄호 안에 파일 이름을 따옴표로 감싸 넣으면 Pandas가 읽어 DataFrame으로 돌려줌 - 결과를 df에 담음

# [정리] read_csv 결과는 반드시 변수에 - 변수에 담지 않으면 읽은 데이터가 곧바로 사라짐
# - 안 담으면: pd.read_csv만 실행하면 읽기는 하지만 저장이 안 돼 사라짐
# - 담는 법: df = pd.read_csv(...) - 등호는 오른쪽 결과를 왼쪽 이름에 담는 의미
# - 비유: 도서관에서 책을 꺼내 책상(변수) 위에 올려두는 일 - 꺼내기만 하면 사라지지만 올려두면 계속 사용 가능

# [강사님께 질문하기] pd.read_csv(...)만 실행하면 결과가 사라진다고 했는데, 그럼 파이썬은
# 왜 그 결과를 자동으로 어딘가에 기억해두지 않고 굳이 변수에 담아야만 계속 쓸 수 있게
# 만들었나요?
# -> 답변: 만약 파이썬이 모든 계산 결과를 알아서 다 기억해뒀다가 나중에 쓸 수 있게 하면,
#    프로그램이 실행되는 동안 안 쓰는 결과물까지 계속 쌓여서 메모리가 끝없이 늘어나 버림.
#    변수에 담는다는 건 "이 결과는 내가 계속 쓸 거니까 이름을 붙여서 남겨두겠다"는 명시적인
#    선언이고, 반대로 변수에 담지 않은 결과는 "이번 한 번만 보고 버려도 된다"는 뜻이 됨.
#    그래서 계속 쓸 것만 골라서 이름(변수)을 붙여 남기고, 나머지는 자동으로 정리되도록
#    설계된 것

# [정리] 변수에 담기 - df 관례 (DataFrame의 줄임말, 가장 흔히 쓰이는 변수 이름)
# - pd와 마찬가지로 의무는 아니지만 모두 이렇게 사용 (글로벌 관용 표기)
# - 여러 파일을 동시에 다루면 df_comp, df_dig처럼 의미를 붙여 구분
# - 한 번 담으면 df로 모든 작업 - head로 보고, shape로 재고, describe로 뽑고, 모두 df에서 출발


# [개념] 파일 경로 이해 - read_csv가 안 된다는 분의 90%는 경로 문제
# - 상대경로란: 지금 작업 폴더 기준 위치, 예: data/12_metro_compressor.csv
# - 절대경로란: 파일의 전체 주소를 처음부터, 예: C:/Users/.../data/...
# - 어느 것을 쓰나: 보통 상대경로 - 짧고 다른 컴퓨터에서도 잘 작동
# - 경로는 항상 슬래시(/)로 - 윈도우 역슬래시(\)는 오류의 원인이 될 수 있음

# [강사님께 질문하기] 상대경로가 "현재 작업 폴더 기준"이라고 했는데, 같은 코드 파일을
# 다른 폴더에서 실행하면 상대경로도 같이 안전하게 안 바뀌나요? 코드 파일이 있는 위치를
# 기준으로 삼는 게 아닌가요?
# -> 답변: 상대경로의 기준은 "코드 파일이 저장된 위치"가 아니라 "지금 이 프로그램을
#    실행하고 있는 위치(작업 디렉터리)"임. 이 둘은 대부분 같아서 헷갈리기 쉽지만, 예를
#    들어 다른 폴더에서 터미널을 열고 그 안에서 이 코드 파일의 경로를 지정해서 실행하면,
#    코드 파일은 그대로인데 상대경로의 기준점만 바뀌어서 파일을 못 찾는 일이 생길 수
#    있음. 그래서 상대경로를 쓸 때는 "이 코드가 어디 있는지"가 아니라 "이 코드를 어디서
#    실행하는지"를 항상 함께 생각해야 함

# [개념] 경로 오류 - FileNotFoundError, 파일을 못 찾으면 나는 오류 (마지막 줄을 먼저 읽기)
try:
    pd.read_csv("12_metro_compressor.csv")  # data/ 경로를 생략 - 실제로는 이 자리에 없음
except FileNotFoundError as e:
    print(e)  # 문법 오류가 아니라 그 경로에 파일이 없다는 의미

# [정리] FileNotFoundError 점검 3단계
# ① 파일 이름 철자 - 오타·대소문자 확인 (equipment ↔ equpment)
# ② 확장자 .csv - 빠뜨리지 않았는지 확인 (data.csv ↔ data)
# ③ 위치 확인 - 작업 폴더인지 data 하위 폴더인지


# [개념] read_csv 옵션 - encoding, 한글이 깨지면 encoding 지정 (안 되면 cp949 시도)
try:
    pd.read_csv(cp949_path, encoding="utf-8")  # cp949로 저장된 파일을 utf-8로 잘못 읽으면
except UnicodeDecodeError as e:
    print(e)  # UnicodeDecodeError - 저장 방식과 읽기 방식이 다르면 이렇게 드러남

cp949_fixed = pd.read_csv(cp949_path, encoding="cp949")
print(cp949_fixed.head())
# 인코딩 = 컴퓨터가 글자를 해석하는 약속 - 저장 방식과 읽기 방식이 다르면 깨짐

# [정리] 한글 깨짐 해결 순서 - 어떤 인코딩인지 미리 알기 어려움, 하나씩 시도해 맞는 것 찾기
# - 1순위: utf-8 또는 utf-8-sig - 대부분 해결
# - 2순위: cp949 - 윈도우 엑셀에서 저장한 파일은 보통 cp949

# [강사님께 질문하기] 같은 한글 파일인데 utf-8로 저장한 것과 cp949로 저장한 것은 겉으로
# 보면 둘 다 그냥 "파일"인데, 컴퓨터는 그 파일을 열어보지 않고도 어떤 인코딩으로
# 저장됐는지 미리 알 방법이 없나요?
# -> 답변: 파일 자체에는 보통 "나는 utf-8이다"라는 표시가 따로 붙어있지 않고, 그냥
#    저장된 바이트(숫자)들만 있을 뿐이라서 컴퓨터가 열어보기 전에는 정확히 알 방법이
#    없음. (일부 파일은 맨 앞에 아주 작은 표시를 붙여서 힌트를 주기도 하는데, 그것도
#    모든 파일에 있는 건 아님.) 그래서 우리가 직접 "이 파일은 이 인코딩일 것"이라고
#    알려줘야 하고, 모르면 흔한 것부터(utf-8, 그다음 cp949) 하나씩 시도해보는 방식이
#    현실적인 대응이 되는 것


# [개념] read_csv 옵션 - sep · index_col, 구분자가 쉼표가 아니면 sep으로 지정
df_no_sep = pd.read_csv(semi_path)
print(df_no_sep.shape)  # (200, 1) - 구분자를 안 맞추면 모든 값이 한 열에 뭉침

df_semi = pd.read_csv(semi_path, sep=";")
print(df_semi.shape)  # (200, 7) - sep로 세미콜론을 지정하면 정상적으로 나뉨

df_indexed = pd.read_csv(comma_path, index_col="측정시각")
print(df_indexed.head())  # 측정시각 열을 인덱스(행 이름표)로 사용
# sep = separator, 값을 나누는 기호 / index_col = 특정 열을 행 이름표로

# [정리] 칸이 뭉치면 구분자 문제 - 값이 한 열에 뭉쳐 나오면 거의 확실히 구분자가 안 맞은 것
# - 증상: df.shape가 (200, 1)로 보임 - 정상은 (200, 7)
# - 확인: 메모장으로 열어 무슨 기호로 나뉘었는지 확인
# - 해결: 확인한 기호를 sep에 지정


# [개념] read_csv 옵션 - nrows · usecols, 큰 파일은 nrows로 일부 행, usecols로 필요한 열만
df_10 = pd.read_csv(comma_path, nrows=10)
print(df_10.shape)  # (10, 7) - 위에서 10줄만 빠르게

df_selected_cols = pd.read_csv(comma_path, usecols=["측정시각"])
print(df_selected_cols.shape)  # (200, 1) - 필요한 열만 골라 읽기
# nrows = 위에서 몇 줄만 / usecols = 필요한 열만 골라 읽기

# [정리] 큰 데이터를 다루는 습관 - 수백만 줄도 위 몇 줄 빠르게 보고 -> 필요한 열만 본격 분석
# - 처음 보는 큰 파일: nrows로 구조만 빠르게 확인
# - 본격 분석: usecols로 필요한 열만 가져오기 (화면도 메모리도 절약)
# - 주의: nrows는 일부일 뿐 - 실제 분석은 전체 데이터로 (위쪽 일부만 본 것을 전체로 착각하면 안 됨)

# [정리] 데이터 불러오기 점검 루틴 - 경로 -> 인코딩 -> 구분자 -> 확인, 네 단계의 진단 흐름
# ① 경로: 파일이 안 보이면 철자·확장자·위치 점검 (FileNotFoundError)
# ② 인코딩: 한글 깨짐 -> utf-8 계열 먼저, 안 되면 cp949 (encoding 옵션)
# ③ 구분자: 값이 한 열에 뭉치면 sep으로 맞춤 (sep 옵션)
# ④ 확인: 반드시 head로 제대로 읽혔는지 눈으로 확인 (오류가 없다고 제대로 읽힌 게 아님 -
#    구분자가 안 맞아도 오류 없이 뭉칠 수 있음)


print("\n===================== 실습 2. 설비 센서 CSV 불러오기 =====================")
# 목표: read_csv로 데이터를 불러와 head로 확인
# 단계: ① import 후 read_csv로 담고 head로 확인
# 예상 결과: 200행 7열 - 인덱스 3번 행 오일온도가 NaN
sensor = pd.read_csv(comma_path)
print(sensor.shape)  # (200, 7)
print(sensor.head())  # head는 앞 5줄을 보여주므로 인덱스 3번 행의 NaN이 그대로 보임


print("\n===================== 실습 3. 한글·구분자 깨짐 옵션 다루기 =====================")
# 목표: encoding과 sep으로 깨진 파일을 직접 해결
# 단계: ① 세미콜론 구분 파일을 sep 없이 읽어 문제 확인 -> ② sep·encoding 옵션으로 해결
# 예상 결과: sep 없이 읽으면 200행 1열, sep=";"이면 200행 7열
broken = pd.read_csv(semi_path)
print(broken.shape)  # (200, 1)

fixed = pd.read_csv(semi_path, sep=";", encoding="utf-8-sig")
print(fixed.shape)  # (200, 7)
print(fixed.head())


print("\n===================== 실습 4. 필요한 열만 골라 불러오기 =====================")
# 목표: usecols와 nrows로 열 많은 데이터에서 필요한 부분만 불러오기
# 단계: ① usecols로 필요한 열만 읽어 shape 변화 확인 -> ② nrows로 행 수를 제한해 shape 변화 확인
# 예상 결과: 열이 7개에서 4개로, 행이 200개에서 20개로 줄어든 결과가 각각 출력
picked_cols = pd.read_csv(comma_path, usecols=["측정시각", "오일온도", "모터전류", "가동상태"])
print(picked_cols.shape)  # (200, 4)

picked_rows = pd.read_csv(comma_path, nrows=20)
print(picked_rows.shape)  # (20, 7)


print("\n===================== 실습 5. 경로·옵션 오류 고치기 =====================")
# 목표: 오류 메시지를 읽고 스스로 원인을 찾아 고치기
# 단계: ① 경로 누락·철자 오타·확장자 누락 세 가지 오류를 순서대로 일으켜 메시지 확인
#      -> ② 셋을 모두 바로잡은 정상 경로로 다시 읽어 확인
# 예상 결과: 세 가지 오류가 각각 출력되고, 바로잡은 뒤에는 200행 7열로 정상 출력
broken_paths = [
    "12_metro_compressor.csv",  # data/ 경로 누락
    os.path.join("data", "12_metro_compresser.csv"),  # 철자 오타 (compresser)
    os.path.join("data", "12_metro_compressor"),  # 확장자 누락
]
for path in broken_paths:
    try:
        pd.read_csv(path)
    except FileNotFoundError as e:
        print(e)

fixed_df = pd.read_csv(os.path.join("data", "12_metro_compressor.csv"))  # 경로·철자·확장자 모두 바로잡음
print(fixed_df.shape)  # (200, 7)


print("\n===================== 실습 6. read_csv 옵션 종합 연습 =====================")
# 목표: 경로 · 인코딩 · 구분자 · 열 선택을 한 번에 적용
# 단계: ① 세미콜론+한글 파일에서 sep·encoding·usecols를 함께 지정해 필요한 열만 불러오기
# 예상 결과: sep + encoding + usecols를 함께 쓰면 200행 3열
final_df = pd.read_csv(
    semi_path,
    sep=";",
    encoding="utf-8-sig",
    usecols=["측정시각", "오일온도", "모터전류"],
)
print(final_df.shape)  # (200, 3)
print(final_df.head(3))


# =====================================================================
# [흔한 질문 진단] Pandas 입문과 데이터 불러오기에서 헷갈리기 쉬운 것들
# =====================================================================

# Q1. read_csv에 옵션을 여러 개 동시에 쓸 때 순서가 상관있나요?
# -> A. 상관없음. sep, encoding, usecols, nrows 같은 옵션은 각각 이름(키워드)으로
#       지정하기 때문에 어떤 순서로 나열해도 pandas가 이름을 보고 알아서 맞는 자리에
#       적용함. 다만 사람이 읽을 때는 관례적으로 파일 경로 다음에 자주 쓰는 옵션부터
#       적는 게 편함

# Q2. usecols로 존재하지 않는 열 이름을 적으면 어떻게 되나요?
# -> A. 오류가 남. usecols는 "이 이름의 열들만 골라줘"라는 뜻인데, 그 이름의 열이
#       애초에 파일 안에 없으면 pandas가 뭘 골라야 할지 알 수 없어서 오류를 냄. 그래서
#       usecols를 쓰기 전에 먼저 한 번 전체를 읽어 정확한 열 이름을 확인해두는 습관이
#       안전함

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# try:
#     pd.read_csv("data/없는파일.csv")
# except FileNotFoundError as e:
#     print("A")
# else:
#     print("B")
# finally:
#     print("C")
# 정답: A / C
# (파일이 없어 FileNotFoundError가 나서 except가 실행되고, else는 예외가 없을 때만
#  실행되므로 건너뛰고, finally는 성공·실패와 상관없이 항상 실행됨)

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# df = pd.read_csv("data/12_metro_compressor.csv")
# print(type(df))
# col = df["오일온도"]
# print(type(col))
# 정답: <class 'pandas.core.frame.DataFrame'> / <class 'pandas.core.series.Series'>
# (DataFrame에서 열 하나를 꺼내면 그 열을 담당하던 Series가 그대로 나옴)
