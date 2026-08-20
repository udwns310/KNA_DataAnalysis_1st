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


# =====================================================================
# Pandas 기초 - DataFrame 구조와 통계 미리보기
# =====================================================================

# [문제 상황] 이 단원에서 새로 보는 실데이터 - 같은 설비의 디지털 신호
# - 압축기 로그(측정시각·압축/배출/저장 압력·오일온도·모터전류·가동상태)에 더해,
#   같은 설비의 디지털 신호(압축기·타워·저압스위치)는 0 또는 1 정수로 켜짐/꺼짐 상태만 기록
digital_signal_path = os.path.join("data", "12_metro_digital.csv")
digital_signal_preview = pd.read_csv(digital_signal_path)
print(digital_signal_preview.head())
print(digital_signal_preview.dtypes)  # 압축기·타워·저압스위치 모두 int64 - 0/1로만 채워진 디지털 신호

# [개념] 데이터를 처음 받으면 무엇부터 보나 - 처음 보는 데이터는 눈으로 직접 확인하는 것부터
# - 탐색(EXPLORE): 데이터를 불러온 다음 거창한 분석으로 바로 가지 않고, 먼저 눈으로 살펴봄
# - 크기·내용·이상값 세 가지를 빠르게 훑어 데이터의 첫인상 잡기 - 탐색을 건너뛰면 잘못된 데이터로 분석하게 됨

# [정리] 탐색 단계 - 무엇을 보나
# - 크기: 몇 줄, 몇 열짜리 데이터인가 (재료가 얼마나 왔는지 펼쳐 보는 일)
# - 내용: 실제 값은 어떻게 생겼는가 (열 이름과 값을 직접 눈으로 확인)
# - 이상: 빈 칸이나 이상한 값은 없는가 (결측·이상값을 미리 발견해야 분석 오류 예방)

# [개념] head() - 앞부분 미리보기, 데이터를 불러오면 가장 먼저 치는 확인 명령 (앞에서 5줄)
print(df.head())  # 수백만 줄이어도 위 5줄만 빠르게 보여줌 - 열 이름·값·빈 칸을 한눈에 확인

# [정리] head로 무엇을 보나 - 앞 5줄만 봐도 결측 신호까지 함께 잡힘
# - CHECK 01: 열 이름이 제대로 나왔는지, 값이 칸에 맞는지 확인
# - CHECK 02: 빈 칸(NaN)이나 이상한 값이 없는지 빠르게 점검 (인덱스 3번 행 오일온도가 NaN - 앞부분만 봐도 눈치챔)

# [개념] 미리보기에서 NaN(결측) 알아보기 - 오류가 아니라 결측치를 나타내는 정상 표시
# - 인덱스 3번 행 오일온도가 NaN = 그 시점에 측정값이 없음(결측) - 센서 고장·통신 끊김·점검 중일 때 발생
# - NaN은 숫자 0과 다름 - 0은 측정값, NaN은 측정 자체가 없음

# [강사님께 질문하기] head()가 앞 5줄만 보여주는데, 만약 결측치가 앞 5줄엔 하나도 없고
# 6번째 줄부터 몰려있으면 head만 보고 "이 데이터는 깨끗하다"고 잘못 판단할 위험이
# 있지 않나요?
# -> 답변: 맞음, 그게 head 하나만 믿으면 안 되는 이유. head는 "어떻게 생겼는지 감을
#    잡는" 용도지 "전체가 이렇다"를 보장하는 도구가 아님. 그래서 head와 tail을 짝으로
#    쓰고, 그걸로도 부족해서 뒤에서 배울 info의 Non-Null Count처럼 전체 행을 다 세어서
#    정확한 결측 개수를 알려주는 도구를 따로 씀. head는 "첫인상", info는 "전수조사"라고
#    구분해서 기억하면, 언제 head만으로 충분하고 언제 info까지 봐야 하는지 판단하기 쉬워짐

# [개념] tail() - 뒷부분 미리보기, 데이터가 끝까지 제대로 쌓였는지 확인 (뒤에서 5줄)
print(df.tail())  # 뒤에서 5줄 - 기본
print(df.tail(3))  # 뒤에서 3줄만 - 숫자 지정
# 파일 끝 깨짐·엉뚱한 줄 점검에 필수, 시간 데이터는 tail로 가장 최근 상태 확인

# [정리] head와 tail은 짝꿍 - 데이터를 받으면 두 명령을 함께 치는 것이 좋은 습관
# - HABIT 01: head로 시작을, tail로 끝을 확인 (양 끝만 깨끗하면 가운데 신뢰도 상승)
# - HABIT 02: 처음과 끝이 멀쩡하면 가운데도 대체로 믿을 만함 (빠른 1차 점검 도구)

# [개념] head·tail 행 개수 조절 - 괄호 안에 숫자를 넣으면 그만큼 출력 (이 숫자를 인자라 부름)
print(df.head(10))  # 위에서 10줄
print(df.head(3))  # 위에서 3줄
print(df.tail(7))  # 아래에서 7줄
# 처음 받은 데이터는 head(20) 정도로 넉넉히 봐서 패턴 잡기

# [정리] 행 개수 조절 - 알아둘 점
# - RULE 01: 괄호 안 숫자 = 볼 줄 수 (head(10) = 위 10줄)
# - RULE 02: 데이터보다 큰 숫자를 넣어도 오류 없이 있는 만큼만 (head(500)을 쳐도 있는 만큼만 나옴)
print(len(df.head(500)))  # 200 - 데이터가 200줄뿐이라 500을 넣어도 200줄까지만


# [설정] 실습 1·3·5·9가 항상 재현되도록, "결측이 많은 25열짜리 디지털 신호 데이터"라는
# 이 단원의 실습용 표본을 코드로 직접 만들어 둔다 (sensor_15 열이 결측 40개로 가장 많도록 설계)
np.random.seed(7)
n_digital_rows = 300
n_sensors = 23

lot_ids = [f"LOT-{1000 + i}" for i in range(n_digital_rows)]
digital_timestamps = [pd.Timestamp("2020-03-01") + pd.Timedelta(minutes=5 * i) for i in range(n_digital_rows)]

digital_sample_data = {"lot_id": lot_ids, "timestamp": digital_timestamps}
for s in range(1, n_sensors + 1):
    digital_sample_data[f"sensor_{s}"] = np.random.choice([0.0, 1.0], size=n_digital_rows, p=[0.7, 0.3])

digital_sample_df = pd.DataFrame(digital_sample_data)

for s in range(1, n_sensors + 1):
    col_name = f"sensor_{s}"
    missing_count = 40 if s == 15 else int(np.random.randint(0, 15))
    missing_idx = np.random.choice(n_digital_rows, size=missing_count, replace=False)
    digital_sample_df.loc[missing_idx, col_name] = np.nan

digital_sample_path = os.path.join("data", "12_metro_digital_sample.csv")
digital_sample_df.to_csv(digital_sample_path, index=False, encoding="utf-8-sig")


print("\n===================== 실습 1. head·tail로 디지털 신호 살펴보기 =====================")
# 목표: head와 tail로 데이터 첫인상과 결측치 확인
# 단계: ① 디지털 신호 표본 데이터를 불러오기 -> ② head·tail·head(10)으로 NaN 위치 찾기
# 예상 결과: 25열 300행, 앞부분과 뒷부분에서 각각 결측 신호를 확인
digital = pd.read_csv(digital_sample_path)
print(digital.shape)  # (300, 25)
print(digital.head())  # 열이 많아 가운데가 ...로 생략됨
print(digital.tail())
print(digital.head(10))


print("\n===================== 실습 2. head·tail 행 개수 조절 =====================")
# 목표: 숫자 인자를 바꿔가며 원하는 만큼 보는 감각 익히기
# 단계: ① 설비 센서 데이터로 head(1)·head(10)·tail(7)·head(500) 출력 비교
# 예상 결과: 인자 숫자만큼 줄 수가 달라지고, 데이터보다 큰 숫자는 있는 만큼만 나옴
print(len(df.head(1)))  # 1
print(len(df.head(10)))  # 10
print(len(df.tail(7)))  # 7
print(len(df.head(500)))  # 200 - 오류 없이 있는 만큼만


# [개념] .shape - 행·열 크기, 괄호 없는 속성 (앞이 행, 뒤가 열)
print(df.shape)  # (200, 7)
# head와 달리 괄호를 안 붙임 - 속성이라서, 행 먼저 열 나중은 Pandas 전체에서 같은 순서

try:
    df.shape()  # 속성에 괄호를 붙이면 오류
except TypeError as e:
    print(e)

# [정리] shape - 기억할 점
# - RULE 01: 결과 (200, 7)에서 앞이 행, 뒤가 열
# - RULE 02: 속성이라 괄호 없이 df.shape (df.shape()는 오류)


# [개념] .columns - 열 이름 목록, 데이터를 골라내는 열쇠 (정확한 이름 확인)
print(df.columns)  # ['측정시각', '압축압력', '배출압력', '저장압력', '오일온도', '모터전류', '가동상태']
# 모든 열 이름을 목록으로 보여주는 속성

# [정리] columns - 왜 중요한가
# - 온도 열을 보려면 정확히 그 이름 그대로 써야 함 - 철자·공백이 조금만 달라도 못 찾음
# - 열이 많을 때 전체 목록 확인에 유용 - head로는 가운데 열이 생략되지만 columns는 모든 열 이름을 표시


# [개념] .index - 행 인덱스, columns가 열 이름이면 index는 행 이름 (0부터 시작)
print(df.index)  # RangeIndex(start=0, stop=200, step=1) - 0번부터 199번까지
# 컴퓨터는 0부터 세서 행이 200개여도 마지막은 199

# [정리] index - 0부터 시작
# - 인덱스 번호는 0부터 시작 (행 200개면 0~199, 첫 행이 0번 마지막이 199번)
# - 사람은 1부터, 컴퓨터는 0부터 셈 - 파이썬 전체 규칙(리스트·문자열에서도 동일)


# [개념] .dtypes - 열별 자료형, int64 정수·float64 소수·object/str 글자 세 가지면 충분
print(df.dtypes)
# 오일온도 float64(소수점 숫자), 모터전류 float64(소수점 숫자), 가동상태 object(글자)

# [정리] dtypes - 세 가지 자료형
# - INT64: 소수점 없는 정수
# - FLOAT64: 소수점 있는 숫자 (온도·진동·전류처럼)
# - OBJECT/STR: 글자 (측정시각·가동상태처럼, 버전에 따라 object나 str로 표시되지만 같은 뜻)

# [강사님께 질문하기] dtypes가 "가동상태" 열을 object라고 알려주는데, 이 열에는 사실
# "가동"이랑 "정지" 딱 두 종류의 값만 반복해서 들어있잖아요. 그럼 그냥 문자열 취급하지
# 말고 애초에 "이런 값만 가능하다"는 걸 자료형 단계에서부터 알 수는 없나요?
# -> 답변: 좋은 지적. pandas에는 실제로 category라는 자료형이 따로 있어서, "이 열은
#    정해진 몇 가지 값 중 하나만 가능하다"는 걸 명시적으로 표시할 수 있음. 하지만
#    read_csv로 처음 불러올 때는 pandas가 그 열의 내용을 다 읽어서 "이게 몇 가지 값만
#    반복되는 열인지" 미리 알지 못하기 때문에, 일단 안전하게 "그냥 글자"라는 뜻의
#    object로 잡아둠. 나중에 우리가 "이 열은 사실 몇 가지 값만 반복되는 걸 알고 있다"고
#    직접 알려주면 category로 바꿀 수 있는데, 이런 자료형 다듬기는 오늘 범위를 넘어서는
#    다음 단계의 이야기

# [정리] 자료형이 분석에 미치는 영향 - 자료형이 틀리면 계산이 아예 안 되는 경우 발생
# - Q1. 온도가 글자로 읽히면? A. 평균을 못 구함 - 글자끼리는 계산 불가 (특수문자가 섞이면 이렇게 됨)
temp_as_text = pd.Series(["70.5", "72도", "71.0"])
try:
    print(temp_as_text.astype(float).mean())
except ValueError as e:
    print(e)  # 문자 "도"가 섞인 값 하나 때문에 전체를 숫자로 못 바꿈
# - Q2. ID가 숫자로 읽히면? A. '001'의 앞자리 0이 사라져 '1'로 망가짐 - 우편번호·제품 코드도 같은 문제
print(int("001"))  # 1 - 앞자리 0이 사라짐

# [정리] 자료형 - 점검 습관, 점검은 1초 안 하면 몇 시간
# - 숫자 열: 온도·진동·전류가 float/int인지 확인
# - 글자 열: 측정시각·가동상태가 object/str인지 확인
# - 점검 시점: 분석 시작 전 dtypes로 미리 확인


print("\n===================== 실습 3. 구조 파악 3종 도구 =====================")
# 목표: shape · columns · dtypes로 데이터 뼈대 읽기
# 단계: ① 디지털 신호 데이터의 shape·columns·dtypes를 확인 -> ② 크기·열·자료형을 한 문장으로 정리
# 예상 결과: 디지털 신호 300행 25열, 글자 열은 lot_id·timestamp뿐이고 나머지는 모두 숫자 열
print(digital.shape)  # (300, 25)
print(digital.columns)
print(digital.dtypes)


print("\n===================== 실습 4. 열 이름·자료형 점검 =====================")
# 목표: 자료형이 의도와 맞는지 빠르게 판단
# 단계: ① 설비 센서 데이터의 dtypes로 숫자·글자 열이 의도와 맞는지 판단
# 예상 결과: 오일온도·모터전류는 float64, 가동상태는 object로 의도와 일치
print(df.dtypes)


# [개념] .info() - 전체 구조 한눈에, shape·columns·dtypes·결측을 종합한 만능 도구
df.info()
# shape와 달리 괄호 필요 - head와 info만 쳐도 데이터의 절반은 파악한 셈

# [정리] info - Non-Null Count가 핵심
# - POINT 01: info는 행 수·열·자료형·결측을 한 번에 (shape·columns·dtypes를 따로 칠 필요 없이 종합)
# - POINT 02: Non-Null Count가 전체보다 작으면 결측 있음 (전체 200인데 오일온도가 199면 결측 1개)

# [정리] info() 출력 읽기
# - 행 수: RangeIndex: 200 entries -> 200행 (shape의 앞 숫자와 동일)
# - 열 수: total 7 columns -> 7열 (shape의 뒤 숫자와 동일)
# - Non-Null Count: 빈 칸 아닌 값 개수 - 전체 행보다 작으면 결측 있음 (결측 발견의 핵심, head보다 정확)
# - Dtype: 각 열의 자료형 - dtypes로 봤던 자료형이 함께 표시됨

# [강사님께 질문하기] describe의 count는 info의 Non-Null Count랑 똑같은 값이라고
# 했는데, 그럼 이 둘은 완전히 같은 계산을 두 번 하는 건가요? 하나로 합치면 안 되나요?
# -> 답변: 계산 결과가 같더라도 두 도구는 "보려는 목적"이 달라서 따로 존재하는 것.
#    info는 "이 데이터가 통째로 건강한가"를 구조 관점에서 훑어보는 도구라서 모든
#    열(글자 열 포함)의 결측을 보여주고, describe는 "숫자 열들의 값 자체가 어떤
#    분포인가"를 보여주는 도구라서 글자 열은 아예 계산에서 빼버리고 그 대신 평균·
#    표준편차·분위수 같은 값 중심의 정보를 얹어서 보여줌. count는 describe 입장에서
#    "지금 계산에 쓰인 값이 몇 개인지" 알려주는 부가 정보로 딸려 나오는 것이지, info의
#    결측 확인 기능을 대체하려는 목적이 아님

# [정리] info()로 결측 신호 발견하기 - 전체 행에서 Non-Null을 뺀 값이 결측 개수
digital_missing = digital.isna().sum()
print(digital_missing[digital_missing > 0].sort_values(ascending=False))
# sensor_15가 40개로 결측이 가장 많음 - 단순한 뺄셈 하나로 결측을 잡아냄


print("\n===================== 실습 5. info로 데이터 건강검진 =====================")
# 목표: info로 행 수·자료형·결측을 종합 점검하고 진단
# 단계: ① 디지털 신호 데이터에 info를 실행 -> ② 결측 개수를 계산해 어느 열이 가장 심각한지 진단
# 예상 결과: 여러 열에 결측이 있고, sensor_15가 40개로 가장 많음
digital.info()
digital_missing_counts = digital.isna().sum()
print((digital_missing_counts > 0).sum())  # 결측이 있는 열의 개수
print(digital_missing_counts.idxmax(), digital_missing_counts.max())  # 결측이 가장 많은 열과 그 개수


# =====================================================================
# Pandas 기초 - 통계 미리보기 / 첫 탐색 종합
# =====================================================================

# [문제 상황] 이 단원에서 통계로 살펴볼 실데이터 - 설비 센서 데이터(온도·진동·회전수·전류)
# - 앞서 본 압축기 로그와 별개로, 온도·진동·회전수·전류를 기록한 또 다른 설비 센서 로그를 사용
# - 이 데이터에는 실제로 이상값이 섞여 있어 describe로 이상 신호를 감지하는 연습에 알맞음
equip_path = os.path.join("data", "12_equipment_sensor.csv")
equip = pd.read_csv(equip_path)
print(equip.head())

# [개념] .describe() - 기초 통계 요약, 숫자 열들의 평균·최대·최소를 한 번에 자동 계산
print(equip.describe())
# 수만 줄을 안 봐도 전체 모습 파악 - 글자 열(설비ID·측정시각·가동상태)은 빼고 숫자 열만 자동 계산

# [정리] describe 8개 통계량 - 개수·중심
# - COUNT: 빈 칸 아닌 값의 개수 (info의 Non-Null과 같음 - 결측 확인 가능)
# - MEAN: 평균, 데이터의 대표값
# - STD: 표준편차, 값들이 흩어진 정도 (작으면 안정적, 크면 넓게 퍼져 불안정)

# [정리] describe 8개 통계량 - 위치
# - MIN/MAX: 가장 작은 값과 가장 큰 값 - 데이터의 양 끝을 한눈에 파악
# - 25%/50%/75%: 작은 값부터 줄 세운 위치값 - 50%는 한가운데 값(중앙값), 25%·75%는 아래위 4분의 1 지점


# [개념] 평균·표준편차로 센서값 폭 읽기 - 평균과 표준편차는 짝으로 봐야 의미를 알 수 있음
# - Q1. 평균이 같으면 같은 데이터? A. 아니오, 표준편차가 다르면 전혀 다름
# - Q2. 표준편차가 크면? A. 값이 들쭉날쭉, 설비가 불안정하다는 신호

# [정리] 평균·표준편차 - 핵심
# - 평균은 중심, 표준편차는 흔들림
# - 설비 안정성을 보려면 표준편차를 꼭 함께 확인 (평소값의 흔들림이 갑자기 커지면 주의)


# [개념] 분위수·min·max로 분포 보기 - 가운데 절반(25~75%)이 어디 모였고 어디까지 퍼지는지 확인
temp_stats = equip["온도"].describe()
print(temp_stats)
# 75%와 max 사이 거리가 유독 멀면 그 사이 어딘가에 멀리 떨어진 이상값이 있다는 뜻

# [정리] 분위수·min·max - 읽는 법
# - POINT 01: 중앙값(50%)과 평균이 비슷하면 고른 분포
# - POINT 02: max만 유독 크면 한쪽으로 튄 이상값 신호 (75%와 max 사이가 멀수록 강한 신호)

# [강사님께 질문하기] 75%랑 max 사이 거리가 멀면 이상값을 의심한다고 했는데, 그럼
# 반대로 25%랑 min 사이가 먼 경우는 왜 안 다루나요? 낮은 쪽에서 튀는 값은 이상치가
# 아닌가요?
# -> 답변: 다룸, 다만 오늘 예시가 "과열(값이 비정상적으로 큼)"이라는 상황을 다루다 보니
#    위쪽(75%~max) 이야기가 먼저 나온 것뿐임. 원리는 완전히 대칭적이라서, 25%와 min
#    사이가 유독 멀면 그건 "평소보다 비정상적으로 낮은 값"이 섞여 있다는 신호가 됨 -
#    예를 들어 압력이 정상 범위보다 뚝 떨어진 경우처럼. 그러니까 실제로 데이터를 볼
#    때는 위쪽(75%~max)과 아래쪽(min~25%) 양쪽을 다 확인해야 하고, 오늘은 그중 위쪽
#    사례로 설명한 것일 뿐 아래쪽도 똑같은 논리로 봐야 함


# [정리] 이상 신호 - 의심일 뿐 확정 아님
# - 75%와 max가 가까우면 고른 분포, 멀면 이상 의심
# - describe는 수상한 곳을 찾는 출발점 (확정은 추가 확인 필요) - 최댓값이 크다고 무조건 오류는 아님


print("\n===================== 실습 6. describe로 이상 신호 찾기 =====================")
# 목표: 평균·분위수·최대를 읽어 이상 신호 있는 열 찾기
# 단계: ① 설비 센서 데이터에 describe 적용 -> ② 75%와 max 차이가 큰 열 찾기
# 예상 결과: 온도와 진동에서 75%와 max 차이가 크게 나타나 이상값이 있다고 의심됨
equip_describe = equip.describe()
print(equip_describe)
for col in ["온도", "진동", "회전수", "전류"]:
    gap = round(equip_describe.loc["max", col] - equip_describe.loc["75%", col], 2)
    print(col, gap)


print("\n===================== 실습 7. 통계량 문장으로 묘사 =====================")
# 목표: describe 통계를 자기 말로 풀어 설명
# 단계: ① 온도·진동·전류 중 하나를 골라 평균·min·max·중앙값을 문장으로 묘사
# 예상 결과: 숫자를 그대로 옮기지 않고 의미로 풀어 쓴 한 문장 요약
vib_stats = equip["진동"].describe()
print(
    f"진동은 보통 {vib_stats['mean']:.2f} 정도이고, "
    f"가장 낮을 때 {vib_stats['min']:.2f}, 가장 높을 때 {vib_stats['max']:.2f}까지 올라간다. "
    f"표준편차가 {vib_stats['std']:.2f}로 크지 않아 대체로 안정적이지만, "
    f"최댓값이 75% 지점보다 훨씬 커서 이상값이 섞여 있을 가능성이 있다."
)


# [정리] 데이터 첫 탐색 체크리스트 - head -> shape -> info -> describe, 네 단계의 흐름
# - STEP 1 head: 실제 값 확인 - 무엇에 관한 데이터인가
# - STEP 2 shape: 크기 확인 - 얼마나 큰 작업인가
# - STEP 3 info: 구조와 결측 점검
# - STEP 4 describe: 통계와 이상 신호 - 첫 탐색의 마침표
# 이 네 단계만 거치면 어떤 데이터를 받아도 막막하지 않음

# [정리] 압축기 vs 디지털 신호 구조 비교 관점 - 성격이 정반대인 두 데이터
# - Q1. 압축압력 로그는 어떤 데이터? A. 결측이 거의 없이 깔끔한 편 - 대부분 바로 분석 가능
# - Q2. 디지털 신호 표본은 어떤 데이터? A. 결측이 여러 열에 흩어져 있어 정리가 먼저 필요
# 현실 데이터는 대부분 후자에 가까움 - 그래서 첫 탐색으로 먼저 판단해야 함


print("\n===================== 실습 8. 압축기와 디지털 신호 구조 비교 =====================")
# 목표: 같은 체크리스트로 깔끔한 데이터와 지저분한 데이터 비교
# 단계: ① 두 데이터를 각각 다른 변수에 담기 -> ② shape·info로 크기·결측 비교
# 예상 결과: 압축기는 결측이 거의 없고, 디지털 신호는 결측이 여러 열에 걸쳐 많이 나타남
df_metro_compressor = pd.read_csv(comma_path)
df_metro_digital = pd.read_csv(digital_sample_path)

print(df_metro_compressor.shape, df_metro_compressor.isna().sum().sum())  # (200, 7) 1
print(df_metro_digital.shape, df_metro_digital.isna().sum().sum())  # (300, 25) 결측 총합


print("\n===================== 실습 9. 첫 탐색 종합 리포트 =====================")
# 목표: 불러오기부터 구조 파악, 통계 확인까지 이어서 리포트로 정리
# 단계: ① 디지털 신호 데이터를 head·shape·info로 훑기
#      -> ② 개요·열구성·결측·통계·이상신호·종합의견 6개 항목으로 리포트 문자열 작성
# 예상 결과: 탐색 결과를 요약한 리포트가 출력됨
report_target = pd.read_csv(digital_sample_path)
missing_by_col = report_target.isna().sum()
missing_cols = missing_by_col[missing_by_col > 0]
worst_col = missing_by_col.idxmax()
worst_count = missing_by_col.max()

report_lines = []
report_lines.append("=== 첫 탐색 리포트: 디지털 신호 표본 ===")
report_lines.append(f"개요: 행 {report_target.shape[0]}개, 열 {report_target.shape[1]}개")
report_lines.append(f"열 구성: 글자 열 2개(lot_id, timestamp), 숫자 열 {report_target.shape[1] - 2}개")
report_lines.append(f"결측: 결측이 있는 열 {len(missing_cols)}개, 가장 심한 열은 {worst_col}({worst_count}개)")
report_lines.append("통계: 숫자 열은 모두 0 또는 1로만 채워진 디지털 신호라 평균이 곧 켜짐 비율을 뜻함")
report_lines.append(f"이상 신호: {worst_col}는 결측 비율이 유독 높아 센서 점검이 필요해 보임")
report_lines.append("종합 의견: 바로 분석하기보다 결측 처리가 먼저 필요한 데이터")

for line in report_lines:
    print(line)


# =====================================================================
# [흔한 질문 진단] 구조 파악과 통계 미리보기에서 헷갈리기 쉬운 것들
# =====================================================================

# Q3. shape는 괄호가 없는데 head·tail·info·describe는 왜 괄호가 있나요?
# -> A. 괄호가 있고 없고는 "동작을 실행하는 함수인가, 이미 있는 정보를 보여주는
#       속성인가"의 차이임. shape·columns·index·dtypes는 데이터가 만들어질 때 이미
#       정해져 있는 값을 그대로 보여주기만 하는 속성이라 괄호가 없고, head·tail·info·
#       describe는 "몇 줄을 보여줄지, 어떻게 계산할지"를 그때그때 실행해야 하는
#       동작이라 괄호가 필요함

# Q4. describe를 실행했는데 글자 열(측정시각·가동상태)이 결과에 안 보이는 이유는
#     무엇인가요? 그 열들은 아예 무시되나요?
# -> A. 무시되는 게 아니라 애초에 계산 대상이 아님. describe는 평균·표준편차·분위수처럼
#       숫자에만 의미가 있는 계산을 하기 때문에, 계산할 수 없는 글자 열은 기본적으로
#       결과에서 자동으로 빠짐. 열 자체가 사라진 게 아니라 원본 데이터에는 그대로 남아
#       있고, describe의 요약표에만 나타나지 않는 것

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# s = pd.Series([10, 20, 30, 40, 50])
# stats = s.describe()
# print(stats["count"])
# print(stats["mean"])
# print(stats["max"] - stats["75%"])
# 정답: 5.0 / 30.0 / 12.5
# (다섯 개 값의 평균은 30, 75% 지점은 37.5이므로 max(50)과의 차이는 12.5)

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# df = pd.read_csv("data/12_metro_compressor.csv")
# print(df.shape)
# small = df.head(3)
# print(small.shape)
# print(df.shape)
# 정답: (200, 7) / (3, 7) / (200, 7)
# (head도 astype·reshape처럼 새 결과를 만들 뿐이라 원본 df의 shape는 그대로 유지됨)
