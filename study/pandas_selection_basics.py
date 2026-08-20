import os
import pandas as pd


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
