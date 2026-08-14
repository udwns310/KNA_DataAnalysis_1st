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


# =====================================================================
# Pandas 데이터 선택·필터링 - 행·열 선택
# =====================================================================

# [문제 상황] 이 단원의 실데이터 - 다이캐스팅 주조 공정
# - 공정: 용융 금속을 금형에 고압으로 밀어 넣어 부품을 찍어내는 다이캐스팅(die-casting) 공정
# - 매 샷(shot)마다 실린더압력·주조압력·사이클타임·비스킷두께·형체력 다섯 개 공정값을 기록하고,
#   그 샷에서 나온 제품을 양품·주의·불량 셋 중 하나로 품질등급을 매김
# - 왜 행·열 선택인가: 수백 개 샷 로그 전체를 매번 다 보는 게 아니라, 필요한 열만 뽑거나
#   특정 구간의 샷만 골라보는 것이 실무 분석의 시작
diecasting_small_path = os.path.join("data", "13_diecasting_small.csv")
diecasting_shot_path = os.path.join("data", "13_diecasting_shot.csv")

cast = pd.read_csv(diecasting_small_path)
print(cast.shape)  # (30, 7)
print(cast.columns.tolist())  # ['샷', '실린더압력', '주조압력', '사이클타임', '비스킷두께', '형체력', '품질등급']
print(cast.head())


# [개념] 열 선택 - 대괄호 1겹은 Series, 대괄호 2겹은 DataFrame
col_series = cast["비스킷두께"]
print(type(col_series))  # <class 'pandas.core.series.Series'>
print(col_series.shape)  # (30,) - 1차원

col_df = cast[["비스킷두께"]]
print(type(col_df))  # <class 'pandas.core.frame.DataFrame'>
print(col_df.shape)  # (30, 1) - 2차원, 열이 하나뿐인 표
# 대괄호 1겹 = 열 이름 하나만 그대로 -> Series / 대괄호 2겹 = 열 이름을 리스트로 감쌈 -> DataFrame

multi_cols = cast[["비스킷두께", "형체력"]]
print(type(multi_cols))  # <class 'pandas.core.frame.DataFrame'>
print(multi_cols.head())
# 열이 몇 개든 리스트로 감싸면 항상 DataFrame - 리스트에 적은 순서대로 열 순서가 정해짐

# [정리] Series vs DataFrame 선택 - 겉보기엔 비슷해도 완전히 다른 자료형
# - df["열"]: 대괄호 1겹, 결과는 Series (1차원, 값이 한 줄로 늘어섬)
# - df[["열"]]: 대괄호 2겹, 결과는 DataFrame (2차원, 열이 하나뿐인 표)
# - df[["열1", "열2"]]: 대괄호 안 리스트 순서 그대로 DataFrame의 열 순서가 정해짐

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# cast = pd.read_csv("data/13_diecasting_small.csv")
# a = cast["형체력"]
# b = cast[["형체력"]]
# print(type(a) == type(b))
# print(a.shape)
# print(b.shape)
# 정답: False / (30,) / (30, 1)
# (화면에 찍히는 값은 똑같아 보여도 a는 1차원 Series, b는 2차원 DataFrame이라 shape의
#  생김새 자체가 다름 - 대괄호 개수 하나 차이가 자료형을 통째로 가름)

# [강사님께 질문하기] 대괄호를 1겹 쓰면 Series, 2겹 쓰면 DataFrame이 된다고 했는데, 왜
# pandas는 그냥 df["열"]도 항상 DataFrame으로 통일해서 반환하지 않고 굳이 두 가지 형태를
# 다 만들어서 헷갈리게 만들었나요?
# -> 답변: 통일하지 않은 이유는 Series와 DataFrame이 애초에 "차원이 다른" 별개의
#    자료형이기 때문. 열 하나만 뽑을 때는 값이 한 줄로 늘어선 1차원으로 다루는 게 자연스러운
#    경우가 많음 - 그 열의 평균을 구하거나 조건을 걸 때 Series 쪽이 다루기 더 간단함.
#    반면 df[["열"]]처럼 대괄호로 한 번 더 감싸면 "여러 열 중 일부를 표 형태로 고르겠다"는
#    의도를 분명히 밝힌 것이라서 결과도 표(DataFrame) 형태를 그대로 유지함. 즉 대괄호
#    개수는 단순한 문법 차이가 아니라 "1차원 값 자체가 필요한가, 표 형태를 유지해야
#    하는가"라는 의도를 코드로 표현하는 방법인 것

# [개념] df.columns로 정확한 열 이름 먼저 확인 - 오타 하나로 KeyError가 남
print(cast.columns)
try:
    cast["비스킷 두께"]  # 띄어쓰기 하나 다름
except KeyError as e:
    print(e)  # '비스킷 두께' - 존재하지 않는 이름을 그대로 알려줌
# 열을 선택하기 전에 columns로 정확한 이름을 확인하는 습관이 KeyError를 줄임


print("\n===================== 실습 1. 다이캐스팅 로그 불러오기·구조확인 =====================")
# 목표: 새 실데이터를 불러와 shape·columns·head로 첫인상 잡기
# 단계: ① 다이캐스팅 소규모 로그를 read_csv로 불러오기 -> ② shape·columns·head로 구조 확인
# 예상 결과: 30행 7열, 샷·실린더압력·주조압력·사이클타임·비스킷두께·형체력·품질등급 7개 열
cast_intro = pd.read_csv(diecasting_small_path)
print(cast_intro.shape)  # (30, 7)
print(cast_intro.columns.tolist())
print(cast_intro.head())


print("\n===================== 실습 2. 열선택하기 =====================")
# 목표: 대괄호 1겹·2겹으로 Series와 DataFrame을 구분해 선택
# 단계: ① 품질등급 열을 Series로 ② 품질등급 열을 DataFrame으로 ③ 타입과 shape로 차이 확인
# 예상 결과: 같은 열이어도 대괄호 개수에 따라 타입과 shape가 달라짐
quality_series = cast["품질등급"]
quality_df = cast[["품질등급"]]
print(type(quality_series), quality_series.shape)  # Series (30,)
print(type(quality_df), quality_df.shape)  # DataFrame (30, 1)


print("\n===================== 실습 3. 공정센서열골라내기 =====================")
# 목표: 품질등급·샷 번호를 뺀 순수 공정 센서값 열만 골라내기
# 단계: ① 실린더압력·주조압력·사이클타임·비스킷두께·형체력 5개 열만 DataFrame으로 선택
# 예상 결과: (30, 5) - 샷 번호와 품질등급을 뺀 숫자형 공정값 열만 남음
process_cols = cast[["실린더압력", "주조압력", "사이클타임", "비스킷두께", "형체력"]]
print(process_cols.shape)  # (30, 5)
print(process_cols.head())


# [개념] loc - 라벨(label) 기반 선택, 슬라이싱이 끝 번호까지 포함
print(cast.loc[0:2])  # 라벨 0부터 2까지 - 3행 (끝 번호 2도 포함)
print(cast.loc[0:2].shape)  # (3, 7)
# loc의 슬라이싱은 "적힌 이름표까지 포함" - 파이썬 리스트 슬라이싱과는 다른 규칙

# [개념] iloc - 위치(position) 기반 선택, 슬라이싱이 끝 번호를 제외 (파이썬 기본 규칙과 동일)
print(cast.iloc[0:2])  # 위치 0부터 2 전까지 - 2행 (끝 번호 2는 제외)
print(cast.iloc[0:2].shape)  # (2, 7)
# iloc의 슬라이싱은 리스트·문자열 슬라이싱과 똑같이 끝은 제외

# [정리] loc vs iloc - 가장 헷갈리는 차이 두 가지
# - 기준: loc는 라벨(이름표) 기준, iloc는 위치(순서) 기준
# - 슬라이싱: loc[0:2]는 라벨 2까지 포함해 3행, iloc[0:2]는 위치 2 전까지라 2행

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# cast = pd.read_csv("data/13_diecasting_small.csv")
# a = cast.loc[0:2]
# b = cast.iloc[0:2]
# print(len(a), len(b))
# 정답: 3 2
# (loc는 라벨 2까지 포함해서 0·1·2 세 줄, iloc는 파이썬 규칙대로 위치 2 앞에서 끊겨
#  0·1 두 줄 - 같은 숫자 0:2를 썼는데도 결과 줄 수가 다름)

# [강사님께 질문하기] iloc는 파이썬 리스트처럼 끝을 제외하는데, loc는 왜 굳이 규칙을
# 다르게 만들어서 끝 라벨까지 포함하게 했나요? 둘 다 그냥 파이썬 방식으로 통일하는 게
# 더 헷갈리지 않았을 것 같은데요.
# -> 답변: 라벨은 애초에 "순서가 있는 위치 번호"라는 보장이 없기 때문. iloc는 0, 1, 2, ...
#    처럼 항상 정수 위치라서 파이썬 슬라이싱 규칙을 그대로 따라도 자연스럽지만, loc의
#    라벨은 정수일 수도, 문자열일 수도, 정렬 뒤에 뒤죽박죽 섞인 순서일 수도 있음. 만약
#    loc도 "끝은 제외"로 만들었다면, 예를 들어 라벨이 ["가", "나", "다"]처럼 문자로 되어
#    있을 때 "나"부터 "다" 전까지라는 표현이 "나"만 포함하는 건지 어색해짐. 반대로 "이
#    라벨부터 저 라벨까지, 둘 다 포함"이라고 하면 사람이 라벨 두 개를 손으로 짚어 범위를
#    지정하는 감각과 훨씬 자연스럽게 맞아떨어짐. 즉 iloc는 컴퓨터의 순번 세는 방식을,
#    loc는 사람이 이름표 두 개로 구간을 지정하는 방식을 따르도록 일부러 다르게 설계된 것

# [주의] loc에 괄호를 쓰면 에러 없이 조용히 엉뚱한 결과가 나옴 - 대괄호와 헷갈리면 안 됨
loc_call_result = cast.loc(0)  # 괄호로 호출 - 에러는 안 나지만 원하는 행이 아님
print(type(loc_call_result))  # <class 'pandas.core.indexing._LocIndexer'> - 그냥 선택 도구 객체
print(cast.loc[0])  # 대괄호로 써야 진짜 0번 라벨 행이 나옴

# [정리] loc·iloc는 무조건 대괄호 - 함수가 아니라 "선택 도구" 자체이기 때문
# - 틀린 예: cast.loc(0) - 에러조차 안 나고 쓸모없는 도구 객체만 돌려줌 (조용한 함정)
# - 맞는 예: cast.loc[0] - 대괄호 안에 라벨을 적어야 실제 행이 나옴


print("\n===================== 실습 4. loc·iloc 행선택 =====================")
# 목표: 정렬로 라벨 순서가 뒤섞인 뒤에도 loc·iloc 차이를 행 선택으로 확인
# 단계: ① 비스킷두께 기준 내림차순 정렬 -> ② 같은 자리(0)를 loc와 iloc로 각각 선택해 비교
# 예상 결과: 정렬 후에는 loc[0]과 iloc[0]이 서로 다른 행을 가리킴
cast_sorted = cast.sort_values("비스킷두께", ascending=False)
print(cast_sorted.head())  # 정렬되면서 원래 라벨(인덱스)이 뒤섞인 채로 붙어 있음

print(cast_sorted.loc[0])  # 라벨이 0인 행 - 정렬 전 원래 0번째 행 그대로
print(cast_sorted.iloc[0])  # 정렬된 표에서 위치가 0번째인 행 - 비스킷두께가 가장 큰 행
# 정렬 전에는 라벨과 위치가 우연히 같아 구분이 안 됐지만, 정렬 뒤에는 완전히 다른 행을 가리킴


print("\n===================== 실습 5. loc·iloc 행열동시선택 =====================")
# 목표: 행과 열을 한 번에 골라내는 loc[행, 열] · iloc[행, 열] 문법 연습
# 단계: ① loc로 라벨 0~2행의 비스킷두께·형체력 열만 ② iloc로 위치 0~1행의 두 번째·세 번째 열만
# 예상 결과: loc는 라벨 기준 3행 2열, iloc는 위치 기준 2행 2열
loc_selected = cast.loc[0:2, ["비스킷두께", "형체력"]]
print(loc_selected)  # (3, 2) - 라벨 0·1·2 세 행, 지정한 두 열만

iloc_selected = cast.iloc[0:2, 1:3]
print(iloc_selected)  # (2, 2) - 위치 0·1 두 행, 위치 1·2(실린더압력·주조압력) 두 열


print("\n===================== 실습 6. 특정구간추출종합 =====================")
# 목표: 음수 인덱스와 loc 구간 지정을 함께 써서 원하는 구간만 뽑아내기
# 단계: ① iloc[-5:]로 마지막 5개 샷 ② loc로 라벨 10~15 구간의 품질등급·형체력만
# 예상 결과: 마지막 5행, 그리고 지정 구간의 품질등급·형체력 6행 2열
last_five = cast.iloc[-5:]
print(last_five)  # 뒤에서 5개 샷 - iloc 음수 인덱스로 "끝에서부터" 표현

mid_section = cast.loc[10:15, ["품질등급", "형체력"]]
print(mid_section)  # 라벨 10부터 15까지(포함) 6행, 품질등급·형체력 2열


# =====================================================================
# [흔한 질문 진단] 행·열 선택에서 헷갈리기 쉬운 것들
# =====================================================================

# Q5. df["열"]과 df.열 (점 표기법)처럼 점으로도 열을 꺼낼 수 있다고 들었는데, 대괄호 대신
#     점을 써도 되나요?
# -> A. 열 이름이 공백·특수문자 없이 파이썬 변수 이름 규칙을 만족하면 점 표기법도 되긴
#       함. 하지만 "품질등급"처럼 한글이어도 규칙만 맞으면 되는 것과 별개로, shape·mean처럼
#       pandas가 이미 쓰는 이름과 열 이름이 겹치면 점 표기법은 원래 기능을 가려버려서
#       예상과 다르게 동작할 수 있음. 그래서 실무에서는 항상 안전한 대괄호 df["열"] 방식을
#       기본으로 씀

# Q6. loc[0:2]가 라벨 2까지 포함한다고 했는데, 만약 정렬 뒤에 라벨 2가 아예 없으면 어떻게
#     되나요?
# -> A. 에러가 나지 않고, 있는 라벨까지만 조용히 걸러서 보여줌. loc의 슬라이싱은 "이
#       라벨부터 저 라벨까지"라는 뜻이라서, 중간에 빠진 라벨이 있어도 실제로 존재하는
#       라벨들 중 그 구간에 속하는 것만 골라줌 - KeyError처럼 딱 떨어지게 막아주는 안전장치가
#       아니므로, 정렬이나 필터링 뒤에 loc 슬라이싱을 쓸 때는 결과 행 개수를 한 번 눈으로
#       확인하는 습관이 필요함

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# cast = pd.read_csv("data/13_diecasting_small.csv")
# a = cast.loc(3)
# print(type(a))
# b = cast.loc[3]
# print(type(b))
# 정답: <class 'pandas.core.indexing._LocIndexer'> / <class 'pandas.core.series.Series'>
# (괄호로 호출하면 에러 없이 선택 도구 객체 자체가 돌아올 뿐 원하는 행이 아니고, 대괄호를
#  써야 실제로 3번 라벨의 행 하나가 Series로 나옴)


# =====================================================================
# Pandas 데이터 선택·필터링 - 조건 필터링과 정렬
# =====================================================================

# [문제 상황] 이 단원에서 쓸 실데이터 - 200개 샷짜리 다이캐스팅 로그
# - 앞서 본 30개 샷 소규모 로그와 같은 구조(실린더압력·주조압력·사이클타임·비스킷두께·형체력·
#   품질등급)를 가진, 훨씬 더 큰 200개 샷 로그를 사용
# - 이 로그에는 결측치도 일부 섞여 있어(공정값 5개 열에 각각 14개씩) 조건 필터링을 결측과
#   함께 다루는 연습도 겸함
cast_shot = pd.read_csv(diecasting_shot_path)
print(cast_shot.shape)  # (200, 7)
print(cast_shot.isna().sum())  # 실린더압력·주조압력·사이클타임·비스킷두께·형체력 각 14개 결측


# [개념] 비교 연산 복습 - 조건을 걸면 True·False로 이루어진 Boolean Series가 나옴
pressure_mask = cast_shot["실린더압력"] >= 230
print(type(pressure_mask))  # <class 'pandas.core.series.Series'>
print(pressure_mask.head())  # 행마다 조건을 만족하면 True, 아니면 False

# [개념] .sum()으로 True 개수 세기 - True는 1, False는 0으로 취급되는 성질을 이용
print(pressure_mask.sum())  # 91 - 실린더압력이 230 이상인 샷 개수

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# s = pd.Series([True, False, True, True, False])
# print(s.sum())
# print(s.sum() / len(s))
# 정답: 3 / 0.6
# (True 세 개가 각각 1로 더해져 합이 3, 전체 5개 중 3개이므로 비율은 0.6 - True 비율을
#  구할 때 이 성질을 자주 사용함)

# [개념] df[조건] - 조건을 만족하는 행만 걸러내는 필터링의 기본 패턴
filtered_pressure = cast_shot[cast_shot["실린더압력"] >= 230]
print(filtered_pressure.shape)  # (91, 7)
print(filtered_pressure.head())
# "df[조건]"이 필터링의 전부 - 대괄호 안에 Boolean Series를 넣으면 True인 행만 남음

# [정리] 필터링 패턴 - df[조건]
# - 조건을 먼저 Boolean Series로 만들고, 그 Series를 df[ ] 안에 넣으면 True인 행만 남음
# - 앞서 loc·iloc가 "위치·라벨로" 골랐다면, 필터링은 "조건으로" 고르는 방식


print("\n===================== 실습 1. 단일조건행추출 =====================")
# 목표: 하나의 비교 조건으로 원하는 행만 골라내기
# 단계: ① 실린더압력이 230 이상인 샷만 필터링 -> ② 몇 건인지 shape로 확인
# 예상 결과: 200개 샷 중 91개가 조건을 만족
high_cyl = cast_shot[cast_shot["실린더압력"] >= 230]
print(high_cyl.shape)  # (91, 7)


print("\n===================== 실습 2. 임계값넘는설비골라내기 =====================")
# 목표: 형체력이 기준치를 넘는 고압 샷만 골라내기
# 단계: ① 형체력이 300을 초과하는 샷 필터링 -> ② 몇 건인지 확인
# 예상 결과: 200개 샷 중 80개가 형체력 300 초과
high_clamp = cast_shot[cast_shot["형체력"] > 300]
print(high_clamp.shape)  # (80, 7)


# [개념] and·or이 Series에서는 왜 안 되나 - 여러 값을 한꺼번에 비교하니 True 하나로 답할 수 없음
try:
    (cast_shot["실린더압력"] >= 230) and (cast_shot["비스킷두께"] >= 16)
except ValueError as e:
    print(e)  # The truth value of a Series is ambiguous ...
# and·or는 "값 하나가 참인가 거짓인가"를 묻는 연산 - Series는 값이 여러 개라 하나로 답을 못함

# [강사님께 질문하기] and·or을 쓰면 왜 하필 "ambiguous(모호하다)"는 에러가 나나요? 그냥
# "Series에는 못 쓴다"고 막아버리면 되지, 굳이 모호하다는 표현을 쓴 이유가 있나요?
# -> 답변: and·or은 원래 "이 값을 참·거짓 딱 하나로 판단해서 다음 동작을 결정하겠다"는
#    연산이라서, 파이썬은 왼쪽 값의 참·거짓을 알아내려고 그 값의 __bool__이라는 내부
#    규칙을 호출함. 숫자 하나나 문자열 하나는 참·거짓이 명확하지만, 값이 200개 들어있는
#    Series를 놓고 "이 전체가 참이냐 거짓이냐"고 물으면 답이 하나로 정해지지 않음 - 191개는
#    참인데 9개는 거짓이면 뭐라고 답해야 할지 알 수 없는 것. 그래서 "안 된다"가 아니라
#    "어느 쪽인지 정할 수 없다(ambiguous)"고 정확하게 표현한 것이고, 그 대신 pandas는
#    &·|처럼 "각 행마다 따로따로 비교해서 행 개수만큼 결과를 돌려주는" 별도의 연산자를
#    마련해 둔 것

# [개념] & · | · ~ - Series 전용 논리 연산자, 각 괄호로 조건을 감싸는 것이 필수
combo_and = cast_shot[(cast_shot["실린더압력"] >= 230) & (cast_shot["비스킷두께"] >= 16)]
print(combo_and.shape)  # (69, 7) - 둘 다 만족

combo_or = cast_shot[(cast_shot["실린더압력"] >= 230) | (cast_shot["비스킷두께"] >= 16)]
print(combo_or.shape)  # (96, 7) - 둘 중 하나만 만족해도 포함

# [주의] 괄호를 생략하면 연산 순서가 꼬여 에러가 남 - &·|는 비교 연산자보다 먼저 계산되기 때문
try:
    cast_shot[cast_shot["실린더압력"] >= 230 & cast_shot["비스킷두께"] >= 16]  # 괄호 생략
except TypeError as e:
    print(e)
# 각 조건을 반드시 괄호로 감싸야 "비교 먼저, & 나중"이라는 원하는 순서로 계산됨

# [정리] &·|·~ 사용 규칙
# - and -> & / or -> | / not -> ~ 로 바꿔 쓰기
# - 각 조건은 반드시 괄호로 감싸기: (조건1) & (조건2)


print("\n===================== 실습 3. 두조건묶기 =====================")
# 목표: &와 |로 두 조건을 하나로 묶어 필터링
# 단계: ① 실린더압력 230 이상 AND 비스킷두께 16 이상 ② 둘 중 하나만 만족(OR)해도 포함
# 예상 결과: AND는 69건, OR는 96건 - OR가 AND보다 항상 같거나 많음
combo_and_only = cast_shot[(cast_shot["실린더압력"] >= 230) & (cast_shot["비스킷두께"] >= 16)]
combo_or_only = cast_shot[(cast_shot["실린더압력"] >= 230) | (cast_shot["비스킷두께"] >= 16)]
print(combo_and_only.shape)  # (69, 7)
print(combo_or_only.shape)  # (96, 7)


# [개념] ~ - not의 Series 버전, 조건을 뒤집어 반대를 뽑음
not_good = cast_shot[~(cast_shot["품질등급"] == "양품")]
print(not_good.shape)  # (38, 7) - 양품이 아닌 샷(주의+불량)

# [개념] .isin([...]) - 여러 값 중 하나라도 일치하면 True, 목록 조건에 유용
not_good_isin = cast_shot[cast_shot["품질등급"].isin(["주의", "불량"])]
print(not_good_isin.shape)  # (38, 7) - ~와 결과가 같음, 표현 방식만 다름

# [개념] .between(시작, 끝) - 두 값 사이(양쪽 끝 포함)인지 확인
between_mask = cast_shot["비스킷두께"].between(10, 20)
print(between_mask.sum())  # 179 - 10 이상 20 이하(양쪽 다 포함)인 샷 개수

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# s = pd.Series([9, 10, 15, 20, 21])
# print(s.between(10, 20).tolist())
# 정답: [False, True, True, True, False]
# (between은 양쪽 끝을 모두 포함 - 정확히 10과 20인 값도 True로 잡힘, 9와 21처럼 범위를
#  벗어난 값만 False)

# [정리] ~·isin·between - 상황에 맞는 도구 고르기
# - ~: 어떤 조건이든 반대로 뒤집을 때
# - isin: 목록 안에 있는 값인지 확인할 때 (or를 여러 번 쓰는 것보다 간결)
# - between: 숫자 범위(양쪽 끝 포함) 안에 있는지 확인할 때


print("\n===================== 실습 4. 부정·목록·범위조건 =====================")
# 목표: ~·isin·between 세 가지 조건 도구를 각각 실전에 적용
# 단계: ① ~로 양품이 아닌 샷 ② isin으로 같은 결과를 목록 방식으로 ③ between으로 비스킷두께 범위
# 예상 결과: ~와 isin은 둘 다 38건으로 동일, between은 179건
neg_result = cast_shot[~(cast_shot["품질등급"] == "양품")]
isin_result = cast_shot[cast_shot["품질등급"].isin(["주의", "불량"])]
between_result = cast_shot[cast_shot["비스킷두께"].between(10, 20)]
print(neg_result.shape)  # (38, 7)
print(isin_result.shape)  # (38, 7)
print(between_result.shape)  # (179, 7)


# [개념] .copy() - 필터링 결과를 원본과 완전히 분리된 독립 사본으로 만들기
risky = cast_shot[cast_shot["품질등급"] == "불량"].copy()
risky["점검메모"] = "재검토 필요"  # risky는 독립 사본이라 cast_shot에는 영향 없음
print(risky.shape)  # (20, 8) - 새 열이 추가돼 열이 하나 늘어남
print(cast_shot.shape)  # (200, 7) - 원본은 그대로

# [정리] SettingWithCopyWarning과 .copy()
# - 문제 상황: df[조건] 같은 필터링 결과에 바로 값을 대입하면, 그 결과가 원본의 "일부를
#   보여주는 것"인지 "완전히 새로운 사본"인지 애매해서 경고가 뜨던 시절이 있었음
# - 해결: 필터링 결과를 계속 고쳐 쓸 계획이라면 뒤에 .copy()를 붙여 "이건 원본과 상관없는
#   완전히 새로운 사본"이라고 명확히 선언

# [강사님께 질문하기] 방금 risky를 만들 때 .copy() 없이도 실제로 실행해보면 경고가 안
# 뜨는데, 교재에서는 이게 경고가 뜰 수 있는 위험한 패턴이라고 했잖아요. 왜 그런가요?
# -> 답변: 실제로 실행 중인 pandas 버전을 보면 3.0.3으로, 이 버전부터는 Copy-on-Write(값을
#    실제로 바꿔 쓰는 시점에만 사본을 만드는 방식)가 항상 켜져 있어서, 필터링 결과에 값을
#    대입해도 pandas가 알아서 항상 독립된 사본처럼 안전하게 처리해줌. 예전 버전(2.x 이전)
#    에서는 필터링 결과가 원본을 "들여다보는 창"인지 "새 사본"인지 pandas 내부에서도
#    애매한 경우가 있어서, 애매한 상황에 값을 대입하면 "혹시 원본이 같이 바뀌었을 수도
#    있다"는 뜻으로 SettingWithCopyWarning을 띄웠던 것. 즉 지금은 pandas가 그 애매함
#    자체를 구조적으로 없애버린 상태라서 경고가 안 뜨는 것이고, 그렇다고 .copy()를 안
#    써도 되는 건 아님 - "이 결과는 원본과 분리된 별도의 데이터"라는 의도를 코드로 분명히
#    남겨두는 습관은 여전히 좋은 습관


# [개념] sort_values - 값 기준으로 행 순서를 바꾸는 정렬, 기본은 오름차순
sorted_by_clamp = cast_shot.sort_values("형체력")
print(sorted_by_clamp.head())  # 형체력이 작은 샷부터
print(cast_shot.head())  # 원본 cast_shot은 순서 그대로 - sort_values는 원본을 바꾸지 않음

# [개념] ascending=False - 내림차순, 큰 값부터
sorted_desc = cast_shot.sort_values("형체력", ascending=False)
print(sorted_desc.head())  # 형체력이 가장 큰 샷부터

# [정리] sort_values 기본 규칙
# - 기본은 오름차순(작은 값 -> 큰 값), ascending=False로 내림차순
# - 새 DataFrame을 반환할 뿐 원본은 그대로 (head가 원본을 안 바꿨던 것과 같은 원리)
# - 행 전체가 함께 이동 - 정렬 기준 열만 움직이는 게 아니라 그 행의 다른 값도 같이 따라감

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# cast_shot = pd.read_csv("data/13_diecasting_shot.csv")
# before = cast_shot.iloc[0]["형체력"]
# cast_shot.sort_values("형체력", ascending=False)
# after = cast_shot.iloc[0]["형체력"]
# print(before == after)
# 정답: True
# (sort_values는 새 결과를 반환만 할 뿐 변수에 다시 담지 않으면 원본 cast_shot은 전혀
#  안 바뀜 - head·loc·iloc처럼 "원본을 바꾸지 않는" pandas의 일관된 규칙)


print("\n===================== 실습 5. 위험순정렬 =====================")
# 목표: 형체력이 큰(고압) 순서로 정렬해 위험도가 높은 샷부터 확인
# 단계: ① 형체력 기준 내림차순 정렬 -> ② 상위 5개 샷만 확인
# 예상 결과: 형체력이 가장 큰 5개 샷이 순서대로 출력
riskiest = cast_shot.sort_values("형체력", ascending=False).head(5)
print(riskiest)


# [개념] 다중 키 정렬 - 리스트로 여러 열을 넘기면 앞 열이 먼저, 같으면 다음 열로 정렬
multi_sorted = cast_shot.sort_values(["품질등급", "실린더압력"], ascending=[True, False])
print(multi_sorted.head(8))
# 품질등급이 먼저 기준이 되고, 품질등급이 같은 행끼리는 실린더압력 내림차순으로 다시 정렬

# [주의] 문자 열 정렬은 코드값(사전) 순서일 뿐, 심각도 순서를 알아서 알아채지 못함
# - "불량" < "양품" < "주의" 순으로 정렬된 것은 우연히 코드값이 그 순서였을 뿐 -
#   "불량이 제일 심각하니 먼저"라는 의미를 pandas가 이해해서 그런 게 아님
# - 실제로 심각도 순(불량 -> 주의 -> 양품)으로 보고 싶다면, category 자료형에 순서를
#   직접 지정해줘야 함 (오늘 범위를 넘어서는 다음 단계 이야기)

# [강사님께 질문하기] 다중 키 정렬에서 품질등급을 기준으로 정렬했더니 "불량"이 맨 앞에
# 나왔는데, 이게 정말 불량이 제일 심각해서 먼저 나온 건가요, 아니면 우연인가요?
# -> 답변: 우연에 가까움. pandas는 문자열을 정렬할 때 그 글자가 가진 실제 의미(불량이
#    심각하다는 것)를 전혀 모르고, 그냥 컴퓨터 안에서 각 글자에 매겨진 코드값(유니코드
#    번호)의 크기 순서로 줄을 세울 뿐임. "불"이라는 글자의 코드값이 "양"이나 "주"보다
#    작아서 앞에 온 것이지, "불량이 제일 위험하다"는 도메인 지식을 pandas가 이해하고
#    반영한 게 아님. 그래서 지금은 결과가 우리가 원하는 순서와 우연히 비슷해 보였을
#    뿐이고, 만약 정말로 "불량 -> 주의 -> 양품" 같은 의미 있는 순서를 보장하고 싶다면
#    그 순서를 pandas에 직접 알려주는 별도의 설정이 필요함


print("\n===================== 실습 6. 필터링정렬연결 =====================")
# 목표: 필터링과 정렬을 메서드 체이닝으로 한 줄에 이어붙이기
# 단계: ① 품질등급이 양품이 아닌 샷만 필터링 -> ② 실린더압력 내림차순 정렬 -> ③ 상위 5건만
# 예상 결과: 품질등급이 양품이 아닌 샷 중 실린더압력이 가장 높은 5건
suspicious_top5 = (
    cast_shot[cast_shot["품질등급"] != "양품"]
    .sort_values("실린더압력", ascending=False)
    .head(5)
)
print(suspicious_top5)
# 대괄호로 거르고 -> sort_values로 줄 세우고 -> head로 자르기, 점(.)으로 이어 한 문장처럼 작성


print("\n===================== 실습 7. 이상의심설비리포트 =====================")
# 목표: 여러 조건과 정렬을 종합해 "이상 의심 샷" 리포트 문자열 작성
# 단계: ① 실린더압력 230 이상 AND 비스킷두께 16 이상 AND 품질등급이 양품이 아닌 샷 추출
#      -> ② 형체력 내림차순 정렬 -> ③ 개요·상위 목록·종합의견을 문자열로 정리
# 예상 결과: 세 조건을 모두 만족하는 이상 의심 샷 리포트가 출력됨
suspicious_mask = (
    (cast_shot["실린더압력"] >= 230)
    & (cast_shot["비스킷두께"] >= 16)
    & (cast_shot["품질등급"] != "양품")
)
suspicious = cast_shot[suspicious_mask].sort_values("형체력", ascending=False)

cast_report_lines = []
cast_report_lines.append("=== 다이캐스팅 이상 의심 샷 리포트 ===")
cast_report_lines.append(f"전체 {cast_shot.shape[0]}개 샷 중 이상 의심 {suspicious.shape[0]}개")
cast_report_lines.append(
    f"조건: 실린더압력 230 이상 AND 비스킷두께 16 이상 AND 품질등급 양품 아님"
)
cast_report_lines.append(f"형체력이 가장 큰 상위 3건 샷 번호: {suspicious['샷'].head(3).tolist()}")
cast_report_lines.append("종합 의견: 세 조건이 겹치는 샷은 공정 이상이 겹쳤을 가능성이 높아 우선 점검 대상")

for line in cast_report_lines:
    print(line)


# [정리] 선택·필터링·정렬 5단계 워크플로우 - 실무 분석가가 늘 밟는 순서
# ① 불러오기: read_csv로 DataFrame으로 변환
# ② 확인: head·info·columns로 구조부터 파악
# ③ 필터링: df[조건]으로 필요한 행만 추리기
# ④ 정렬: sort_values로 중요한 순서대로 줄 세우기
# ⑤ 선택: 필요한 열만 골라 head로 최종 확인
# 필터링을 정렬보다 먼저 하는 이유: 필요 없는 행을 먼저 덜어내야 정렬할 대상이 줄어 효율적


# =====================================================================
# [흔한 질문 진단] 조건 필터링과 정렬에서 헷갈리기 쉬운 것들
# =====================================================================

# Q7. isin과 between을 안 쓰고 &·|로 똑같은 결과를 만들 수도 있을 것 같은데, 굳이 따로
#     배워야 하나요?
# -> A. 결과만 보면 &·|로도 만들 수 있음 - 예를 들어 isin(["주의", "불량"])은
#       (조건 == "주의") | (조건 == "불량")과 같은 결과. 하지만 값이 여러 개일수록
#       &·|를 값 개수만큼 이어 붙여야 해서 코드가 빠르게 길어짐. isin·between은 그런
#       반복되는 패턴을 한 번에 표현하는 전용 도구라서, 값 목록이나 범위 조건에서는
#       코드가 훨씬 짧고 읽기도 쉬워짐

# Q8. sort_values로 정렬한 결과를 다시 원본 변수에 안 담으면 정렬이 아예 안 된 건가요?
# -> A. 정렬 계산 자체는 실행됐지만, 그 결과를 담을 곳이 없어서 곧바로 사라진 것.
#       sort_values는 head·loc·iloc와 마찬가지로 원본을 직접 고치지 않고 "정렬된 새
#       DataFrame"을 결과로 돌려주기만 함. 그 결과를 계속 쓰고 싶다면 cast_shot =
#       cast_shot.sort_values(...)처럼 변수에 다시 담아야 하고, 원본을 남겨두고 싶다면
#       cast_shot_sorted = cast_shot.sort_values(...)처럼 새 이름에 담아야 함

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# cast_shot = pd.read_csv("data/13_diecasting_shot.csv")
# a = cast_shot[(cast_shot["형체력"] > 300) & (cast_shot["품질등급"] == "양품")]
# b = cast_shot[(cast_shot["형체력"] > 300)]
# print(len(a) <= len(b))
# 정답: True
# (a는 b의 조건에 품질등급 조건을 하나 더 AND로 얹은 것이므로, a를 만족하는 행은 항상
#  b도 만족함 - 조건을 AND로 추가할수록 결과 행 개수는 줄거나 같을 수밖에 없음)

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# cast_shot = pd.read_csv("data/13_diecasting_shot.csv")
# sorted_df = cast_shot.sort_values("형체력", ascending=False)
# print(sorted_df["형체력"].isna().sum())
# print(sorted_df["형체력"].tail(3).isna().all())
# 정답: 14 / True
# (결측치는 정렬 기준으로 삼을 값 자체가 없어서 오름차순이든 내림차순이든 항상 맨
#  뒤로 밀려남 - 내림차순으로 "큰 값부터" 정렬해도 NaN은 맨 뒤 그대로)
