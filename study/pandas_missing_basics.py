import os
import pandas as pd


# =====================================================================
# 결측치 처리 - 결측치 이해와 확인
# =====================================================================

# [문제 상황] 데이터 전처리란 - 분석 시간의 70~80%가 전처리에 들어감
# - 현장 데이터는 센서 고장·입력 실수로 비거나 잘못된 값이 많음 - Garbage In, Garbage Out
# - 멋진 모델 이전에 데이터를 손질하는 게 먼저 - 전처리의 첫 단추가 바로 결측치 다루기
# - 이 단원의 실데이터: 사출성형 공정 - 배럴온도·사출압력·스크루속도 등 20여 개 공정값을
#   17초 간격으로 기록, 최종적으로 그 샷이 불량인지(불량여부) 함께 남김

# [개념] 결측치(Missing Value)란 - 데이터 표에서 값이 비어 있는 칸
# - 사람은 빈 칸을 그냥 넘어가지만, 컴퓨터는 평균을 내다가도 멈추거나 에러를 냄
# - 설비에는 센서가 수십~수백 개씩 붙어 있어 결측이 특히 흔하게 발생

# [개념] NaN의 정체 - Not a Number, 판다스가 빈 칸에 자동으로 붙이는 "값 없음" 푯말
# - 빈 칸을 0으로 채우면 "측정을 못 했다"와 "측정했더니 0이었다"를 컴퓨터가 구분 못 하게 됨
# - NaN은 전염성이 있음 - 계산에 NaN이 하나라도 섞이면 그 계산 결과 전체가 NaN이 되기 쉬움
# - None(순수 파이썬의 빈 값)과 NaN(데이터 표 속 빈 숫자값)은 이름은 다르지만 판다스에서는
#   똘같이 결측으로 처리됨 - 실무에서 자주 보는 건 NaN


print("\n===================== 실습 1. 눈으로 결측 찾기 =====================")
# 목표: 진짜 결측(NaN)과 위장 결측을 코드로 세어 확인
# 단계: ① 사출성형 로그(16행)를 불러와 눈으로 직접 빈 칸 확인 -> ② isna로 컬럼별 NaN 개수 세기
#      -> ③ 조건 필터링으로 사출압력 0, 스크루속도 -999 같은 위장 결측 개수 세기
# 예상 결과: 진짜 NaN 5개(사출기1·배럴온도2·사출압력1·스크루속도1), 위장 결측 5개
#   (사출압력 0이 2건, 스크루속도 -999가 2건, 배럴온도 999가 1건)
log_path = os.path.join("data", "15_사출성형_로그.csv")
mlog = pd.read_csv(log_path)
print(mlog.shape)  # (16, 7)
print(mlog)  # CSV를 메모장으로 보면 빈 칸, 판다스로 불러오면 그 자리가 NaN으로 표시됨

print(mlog.isna().sum())  # 사출기 1, 배럴온도 2, 사출압력 1, 스크루속도 1 - 진짜 결측 합 5개
suspect_pressure = (mlog["사출압력"] == 0).sum()
suspect_screw = (mlog["스크루속도"] == -999).sum()
suspect_temp = (mlog["배럴온도"] == 999).sum()
print(suspect_pressure, suspect_screw, suspect_temp)  # 2, 2, 1 - 위장 결측 합 5개


# [개념] 결측치가 표에 보이는 모습 - 도구마다 옷만 다를 뿐 속은 같음
# - CSV를 메모장으로 열면 결측 자리는 그냥 빈 칸으로 보임
# - 그 파일을 판다스로 불러오는 순간 빈 칸이 NaN으로 바뀜
# - 실전에서는 앞부분 몇 줄만 훑어 빠르게 살피지만, 앞쪽에 NaN이 없다고 결측이 없다고
#   단정하면 안 됨 - 눈으로 보는 확인과 숫자로 세는 확인을 늘 함께

# [강사님께 질문하기] mlog를 눈으로 보면 배럴온도가 NaN인 행(2·12번)과 999인 행(8번)이
# 겉보기엔 둘 다 "이상한 온도"인데, 왜 하나는 판다스가 자동으로 NaN이라고 알려주고
# 다른 하나는 그냥 평범한 숫자 999로 읽어버리나요?
# -> 답변: 판다스가 결측이라고 자동으로 인식하는 기준은 딱 하나 - "그 자리에 아무것도
#    안 적혀 있었는가"임. CSV 파일을 열어 보면 진짜 결측인 자리는 값 자체가 비어 있는
#    반면, 999는 누군가 실제로 "999"라는 글자를 그 칸에 적어 넣은 것이라서 판다스
#    입장에서는 다른 숫자 201.2나 200.2와 전혀 구분할 이유가 없는 정상적인 값임. 즉
#    판다스는 "빈 칸인지 아닌지"만 기계적으로 판단할 뿐, 그 숫자가 현실적으로 말이
#    되는 온도인지는 전혀 모름 - 그래서 999처럼 값이 버젓이 채워진 위장 결측은 사람이
#    직접 최솟값·최댓값을 보고 "이건 말이 안 되는 값이다"라고 눈치채야 함


# [개념] 결측이 생기는 이유 - 이유를 알아야 채울지 지울지 판단이 섬
# - 센서 고장: 설비 부품인 만큼 언제든 고장 날 수 있어 그 순간 값이 빔
# - 점검·교체: 센서를 잠깐 떼면 그 구간만 기록이 끊김 - 앞뒤 값으로 채우기 자연스러움
# - 환경(먼지·고온): 일시적 측정 실패 - 통째로 고장 난 컬럼은 아예 빼는 선택지도 합리적
# - 통신·합치기: 센서가 멀쩡해도 통신이 끊기거나, 주기가 다른 표를 합칠 때 시점이 안 맞아 빔
# - 결측은 데이터가 잘못된 게 아니라 현실 데이터의 일상 - 발견하고 처리하는 능력이 관건


# [개념] 위장된 결측치 - 숫자 0, 멀쩡한 숫자인 척 숨어 있는 결측
# - 사출 중인데 사출압력이 정확히 0일 수는 없음 - 센서가 못 읽은 신호일 가능성이 큼
# - 반대로 멈춘 설비의 속도가 0인 것은 진짜 정상값 - 같은 0이라도 맥락에 따라 다름
# - 0의 의미를 가려내는 건 컴퓨터가 못 하는 일 - 데이터 의미를 아는 사람의 몫

# [개념] 위장된 결측치 - 센티넬 값(Sentinel Value), -999·999처럼 약속된 결측 표시
# - 옛날 시스템은 빈 칸을 저장할 방법이 없어 "현실에 없는 값"을 결측 표시로 약속해 씀
# - 그대로 두면 평균이 크게 망가짐 - 컴퓨터는 -999를 진짜 숫자로 받아들이기 때문
# - 데이터의 최솟값·최댓값을 보면 발견할 수 있는 단서

# [정리] mlog에서 발견한 위장 결측 - 우연이 아닌 패턴
print(mlog[mlog["불량여부"] == 1])
# 불량여부가 1인 세 행(3·8·11번)이 각각 사출압력 0, 배럴온도 999, 사출압력 0을 하나씩 안고
# 있음 - 불량으로 표시된 샷마다 위장 결측이 함께 나타나는 실제 패턴

# [강사님께 질문하기] 불량여부가 1인 행마다 매번 위장 결측이 하나씩 같이 나온다는 게
# 우연이 아니라면, 이 정보 자체를 불량 예측에 활용해도 되는 건가요?
# -> 답변: 조심해서 접근해야 함. 두 가지 가능성이 있는데, ① 센서가 흔들리는 순간
#    실제로 성형 품질도 함께 나빠져서 "센서 이상 = 진짜 불량 신호"인 경우와, ② 센서
#    오류 자체가 불량 판정 로직에 잘못 끼어들어 "센서가 이상하게 찍히면 시스템이
#    자동으로 불량 처리"해버린 경우가 있을 수 있음. 앞의 경우라면 유용한 신호지만,
#    뒤의 경우라면 그건 진짜 품질 정보가 아니라 데이터 수집 과정의 결함일 뿐이라서
#    그대로 모델에 넣으면 "센서가 잠깐 흔들린 것"과 "진짜 불량"을 혼동하게 됨. 그래서
#    이런 패턴을 발견하면 바로 활용하기보다, 왜 그런 패턴이 생기는지 공정 담당자에게
#    확인하는 절차가 먼저 필요함


# [개념] 빈 문자열과 공백도 결측 - 글자 컬럼에서도 결측은 일어남
# - 설비명·작업자 이름 같은 텍스트 컬럼에서 빈 문자열이나 공백만 들어간 칸이 생길 수 있음
# - 공백만 있으면 판다스가 정상값으로 취급해 결측으로 못 잡는 함정이 있음
# - 원칙: 비어 보이는 모든 것을 의심 - NaN·빈 칸·0·-999·공백, 결측은 여러 얼굴로 나타남


# [개념] 결측치와 데이터 타입 - 정수가 갑자기 소수로 보이면 결측이 끼었다는 신호
mixed = pd.Series([1, 2, 3, None])
print(mixed.dtype)  # float64 - 정수 넣었는데 실수형으로 바뀜
print(mixed)  # 1.0, 2.0, 3.0, NaN - NaN이 기술적으로 실수형이라 컬럼 전체가 실수형으로 변환
# 오류가 아닌 정상 동작 - 처리 후에는 astype("int")로 다시 정수형으로 되돌릴 수 있음

# [개념] NaN의 비교 연산 함정 - NaN은 자기 자신과 비교해도 "다르다"고 나옴
print((mlog["배럴온도"] == float("nan")).sum())  # 0 - 결측이 분명 2개인데 0으로 나옴
print(mlog["배럴온도"].isna().sum())  # 2 - isna를 써야 정확히 잡힘
# 값 없는 것과 값 없는 것이 같다고 단정하기 어색해서, NaN은 등호(==)로 비교할 수 없음
# 초보가 가장 자주 당하는 함정 - 결측은 반드시 isna 같은 전용 도구로 확인

# [강사님께 질문하기] 다른 모든 값은 자기 자신과 비교하면 항상 같다고 나오는데, 왜
# NaN만 유독 자기 자신과 비교해도 "다르다"고 나오도록 만들어졌나요?
# -> 답변: NaN이 원래 표현하려는 의미가 "알 수 없는 값"이기 때문. 두 칸이 모두
#    NaN이라고 해서 그 두 자리가 "같은 값"이라고 보장할 수는 없음 - 하나는 센서
#    고장으로 빈 것이고 다른 하나는 통신 오류로 빈 것일 수도 있어서, "둘 다 모른다"는
#    것이지 "둘이 같다"는 뜻이 전혀 아님. 그래서 NaN끼리 비교하면 "같다"고 거짓으로
#    답하는 대신, 아예 "비교 자체가 의미 없다"는 뜻으로 항상 거짓을 돌려주도록 설계된
#    것 - 이 규칙은 파이썬만의 특별한 약속이 아니라 여러 프로그래밍 언어가 공유하는
#    부동소수점 표준(NaN 정의)에서 온 것이기도 함


# [개념] 결측 방치 시 통계 왜곡 - "결측 빼고 계산"이 만드는 침묵의 오차
clean_speed = mlog["스크루속도"].replace(-999, pd.NA).dropna()
print(round(mlog["스크루속도"].mean(), 2))  # 위장 결측(-999)이 낀 채 계산한 평균 - 크게 왜곡
print(round(pd.to_numeric(clean_speed).mean(), 2))  # 위장 결측을 걷어낸 뒤의 진짜 평균
# 16개 중 2개가 -999로 위장돼 있으면 평균이 크게 낮은 쪽으로 쏠려 설비 상태를 오판하게 됨

# [개념] 결측 방치 시 그래프·모델 문제
# - 그래프: 시간에 따른 값 변화선이 결측을 만나면 중간이 뚝 끊기거나 점이 듬성듬성해짐
# - 모델: 대부분의 머신러닝 도구는 빈 칸을 아예 거부해 학습이 시작조차 안 됨
# - 엉성하게 채우면 모델이 가짜 값을 진짜인 것처럼 학습해버림 - 결측 처리는 모든 분석의 기초


# [개념] 결측이 타깃(정답) 컬럼에 있을 때 - 입력값 결측과는 처리 방식이 다름
# - 입력값(배럴온도·사출압력 등) 결측: 평균·앞뒤값으로 채워 활용 가능
# - 정답(불량여부) 결측: 추측으로 채우면 모델이 가짜 정답을 외워 버림
# - 원칙: 정답이 빈 행은 채우지 말고 제거 - 센서값 결측과 정답 결측은 처리 방식을 분리

# [정리] 결측치 처리의 큰 그림 - 확인 -> 판단 -> 처리 -> 재확인의 고리
# - 확인: 결측이 어디에 얼마나 있는지 파악 (어디가 아픈지도 모르고 약부터 먹지 않기)
# - 판단: 제거할지 대체할지 결정 - 컬럼이 너무 많이 비었으면 빼고, 조금이면 채워 살림
# - 처리: 실제로 제거·대체 실행
# - 재확인: 결측이 정말 0이 됐는지 다시 검증 - 초보가 가장 자주 건너뛰는 단계
# 이번 단원은 첫 단계 "확인"을 집중적으로 연습, 다음 단원에서 "처리"를 본격적으로 다룸


# [문제 상황] 이제부터는 250행짜리 진짜 사출성형 공정 로그로 확인 방법을 익힌다
injection_path = os.path.join("data", "15_01_사출성형_공정.csv")
inj = pd.read_csv(injection_path)
print(inj.shape)  # (250, 22)
print(inj.head())


# [개념] na_values로 위장 결측 인식 - 불러올 때부터 지정한 값을 NaN으로 자동 변환
try:
    naive = pd.read_csv(log_path, na_values=[0, -999, 999])
    print(naive["불량여부"].isna().sum())  # 무턱대고 0을 넣으면 불량여부의 정상적인 0까지 결측 처리됨
except Exception as e:
    print(e)

safe = pd.read_csv(
    log_path,
    na_values={"사출압력": [0], "스크루속도": [-999], "배럴온도": [999]},
)
print(safe.isna().sum())  # 사출기1, 배럴온도3, 사출압력3, 스크루속도3 - 컬럼별로 정확히 지정
# 컬럼별로 na_values를 딕셔너리로 지정하면, 다른 컬럼의 정상적인 0·-999·999는 건드리지 않음

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# mlog = pd.read_csv("data/15_사출성형_로그.csv")
# a = mlog["불량여부"].isna().sum()
# naive = pd.read_csv("data/15_사출성형_로그.csv", na_values=[0])
# b = naive["불량여부"].isna().sum()
# print(a, b)
# 정답: 0 13
# (원본에는 불량여부에 결측이 전혀 없지만, na_values=[0]을 전체 컬럼에 걸어버리면
#  "불량 아님"을 뜻하던 멀쩡한 0이 13개나 결측으로 둔갑함 - 컬럼을 안 가리고 값을
#  지정하는 na_values의 위험성을 보여주는 실제 사례)


# [개념] info()로 결측 한눈에 보기 - 데이터를 받으면 가장 먼저 실행하는 도구
inj.info()
# Non-Null Count가 250보다 작은 컬럼이 결측 있는 컬럼 - 정수인데 float64로 보이면 결측 의심 신호

# [개념] describe()의 count로 결측 추정 - 숫자 컬럼의 count가 곧 결측 아닌 값의 개수
print(inj[["사출압력", "스크루속도", "계량종료점"]].describe())
# count가 250보다 작을수록 결측이 많은 컬럼 - min·max로 위장 결측(비현실적인 값)도 함께 확인


# [개념] isna()의 동작 원리 - "is na, 결측이니?"를 묻는 전용 도구
print(inj.isna().head(3))  # 원본과 같은 크기의 참(True)·거짓(False) 표
# isna는 NaN·None을 모두 정확히 True로 잡음 - 등호(==) 비교의 함정을 피해가는 정확한 방법

# [정리] isnull과 notna
# - isnull: isna와 완전히 같음 - 판다스 역사적 이유로 이름만 두 개
# - notna: isna의 반대, 값이 있으면 참 (notnull도 동일)
# - 결측 셀 때는 isna, 값 있는 행만 골라낼 때는 notna

# [개념] True는 1, sum으로 세기 - isna().sum()은 한 단어처럼 외우는 결측 확인 공식
print(inj.isna().sum())
# 컴퓨터는 True를 1, False를 0으로 취급 - isna가 위치를 표시하고 sum이 그 개수를 합산


# [개념] 전체 결측 개수와 비율 - 개수만 보면 안 되고 전체 대비 비율로 봐야 처리 방향이 보임
total_na = inj.isna().sum().sum()
print(total_na)  # 475

na_ratio = (inj.isna().sum() / len(inj) * 100).round(1)
print(na_ratio.sort_values(ascending=False).head(5))
# 계량종료점·감압시간이 각 109개(43.6%)로 최다 - 절반 가까이 빈 컬럼은 채워봤자 절반이 추측


# [개념] 결측 비율 정렬과 순위 - sort_values(ascending=False)로 가장 심각한 컬럼을 맨 위로
na_counts = inj.isna().sum()
na_table = pd.DataFrame({"결측수": na_counts, "비율(%)": na_ratio})
na_table = na_table[na_table["결측수"] > 0].sort_values("결측수", ascending=False)
print(na_table)
# 위쪽은 제거를 고민할 컬럼, 아래쪽은 채워 살릴 컬럼 - 정렬 한 번이면 처리 우선순위가 보임


# [개념] 행별 결측 개수 - 방향을 가로(axis=1)로 돌려 "어느 측정 기록이 많이 비었나" 확인
row_na = inj.isna().sum(axis=1)
print((row_na == 0).sum())  # 76 - 결측이 하나도 없는 행
print((row_na > 0).sum())  # 174 - 결측이 하나라도 있는 행
print(row_na.max())  # 8 - 가장 많이 빠진 행은 8개 컬럼이 통째로 빔
# 컬럼과 행 양쪽을 모두 봐야 결측의 전체 그림이 보임


# [개념] 결측 많은 행·컬럼 추출 - 문제 부분만 확대경으로 들여다보기
heavy_cols = na_table[na_table["비율(%)"] > 20].index.tolist()
print(heavy_cols)  # 결측 20% 넘는 컬럼만 골라 확인 - 제거 후보 목록

heavy_rows = inj[row_na >= 5]
print(heavy_rows.shape)  # (27, 22) - 결측 5개 이상인 부실한 행만 추출


print("\n===================== 실습 2. SECOM 첫 탐색 =====================")
# 목표: 처음 받은 데이터의 구조와 결측 분위기 파악
# 단계: ① read_csv로 불러와 head와 shape로 크기 확인 -> ② info로 컬럼별 채워진 값 개수 훑기
#      -> ③ describe의 count로 결측 있는 컬럼 짐작
# 예상 결과: 250행 22열, 뒤쪽 공정값 컬럼일수록 채워진 수가 감소
inj_intro = pd.read_csv(injection_path)
print(inj_intro.head())
print(inj_intro.shape)
inj_intro.info()
print(inj_intro.describe())


print("\n===================== 실습 3. 위장 결측 사냥 =====================")
# 목표: 위장 결측을 조건과 na_values로 진짜 결측으로 전환
# 단계: ① 위장 결측이 있는 로그 파일을 조건 필터링으로 추출해 확인 -> ② na_values로 위장값을
#      결측으로 인식해 다시 불러오기 -> ③ 변환 전후 결측 개수를 비교
# 예상 결과: 변환 전 진짜 NaN 5개 -> 컬럼별 na_values 지정 후 10개(위장 5개 추가 인식)
before_na = mlog.isna().sum().sum()
print(before_na)  # 5

after = pd.read_csv(
    log_path,
    na_values={"사출압력": [0], "스크루속도": [-999], "배럴온도": [999]},
)
after_na = after.isna().sum().sum()
print(after_na)  # 10


print("\n===================== 실습 4. 컬럼별 결측 개수와 비율 =====================")
# 목표: 컬럼별 결측 개수와 비율을 한 표로 정리
# 단계: ① isna와 sum으로 컬럼별 결측 개수를 변수에 담기 -> ② 전체 행 수로 나누고 백분율로
#      바꿔 비율 계산 -> ③ 결측이 있는 컬럼만 골라 개수와 비율을 나란히 정리
# 예상 결과: 결측 12개 컬럼, 계량종료점·감압시간이 각 109개(43.6%)로 최다
summary_counts = inj.isna().sum()
summary_ratio = (summary_counts / len(inj) * 100).round(1)
summary_table = pd.DataFrame({"결측수": summary_counts, "비율(%)": summary_ratio})
summary_table = summary_table[summary_table["결측수"] > 0].sort_values("결측수", ascending=False)
print(len(summary_table))  # 12
print(summary_table)


print("\n===================== 실습 5. 결측 순위와 행별 분석 =====================")
# 목표: 컬럼 순위와 행별 결측을 함께 봐 처리 근거 모으기
# 단계: ① 결측 비율을 내림차순 정렬해 가장 심한 컬럼 확인 -> ② 방향을 가로(행)로 바꿔
#      행마다 결측 개수 세기 -> ③ 결측이 많은 부실 행만 조건으로 골라내기
# 예상 결과: 계량종료점·감압시간 최상위, 결측 없는 행 76·있는 행 174
print(summary_table.head(2))
row_na_5 = inj.isna().sum(axis=1)
print((row_na_5 == 0).sum(), (row_na_5 > 0).sum())
print(inj[row_na_5 >= 5].shape)


print("\n===================== 실습 6. 결측 시각화 =====================")
# 목표: 막대그래프와 히트맵으로 결측의 양과 위치 보기
# 단계: ① 컬럼별 결측 개수를 내림차순 정렬해 막대그래프로 그리기 -> ② 결측 여부를 히트맵으로
#      그려 몰린 영역 확인 -> ③ 그림에서 결측이 집중된 컬럼 확인
# 예상 결과: 계량종료점·감압시간 막대 최고, 뒤쪽 공정값 영역에 결측 집중
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"  # 한글 라벨이 네모(tofu)로 안 깨지도록 지정
plt.rcParams["axes.unicode_minus"] = False  # 한글 폰트 사용 시 마이너스 기호 깨짐 방지

na_sorted = inj.isna().sum().sort_values(ascending=False)
na_sorted = na_sorted[na_sorted > 0]

fig, ax = plt.subplots(figsize=(8, 4))
colors = ["tab:red" if v > 50 else "tab:blue" for v in na_sorted.values]
ax.bar(na_sorted.index, na_sorted.values, color=colors)
ax.set_title("컬럼별 결측 개수")
ax.set_ylabel("결측 개수")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
bar_path = os.path.join("data", "15_missing_bar_temp.png")
plt.savefig(bar_path)
plt.close(fig)
print(os.path.exists(bar_path))  # True - 막대가 높을수록 먼저 손볼 대상

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.imshow(inj.isna().to_numpy().T, aspect="auto", cmap="cividis", interpolation="nearest")
ax2.set_title("결측 위치 히트맵 (밝을수록 결측)")
ax2.set_yticks(range(len(inj.columns)))
ax2.set_yticklabels(inj.columns, fontsize=6)
plt.tight_layout()
heatmap_path = os.path.join("data", "15_missing_heatmap_temp.png")
plt.savefig(heatmap_path)
plt.close(fig2)
print(os.path.exists(heatmap_path))  # True

os.remove(bar_path)
os.remove(heatmap_path)
# 그림 파일은 확인용으로만 잠깐 저장하고 바로 정리 - 실제로는 결과를 파일로 계속 보관해도 됨


print("\n===================== 실습 7. 결측 확인 요약표 =====================")
# 목표: 개수·비율·처리방향을 담은 요약표를 만들어 저장
# 단계: ① 컬럼별 개수와 비율을 하나의 표로 합치기 -> ② 비율 기준으로 대체·검토·제거 처리
#      방향 열 추가 -> ③ 요약표를 파일로 저장해 다음 단계 지시서로 남기기
# 예상 결과: 결측 12개 컬럼 요약표 + 처리방향, csv 저장


def decide_direction(pct):
    if pct < 5:
        return "대체로 살리기"
    if pct < 40:
        return "중요도 보고 결정"
    return "제거 고민"


report_table = summary_table.copy()
report_table["처리방향"] = report_table["비율(%)"].apply(decide_direction)
print(report_table)

report_path = os.path.join("data", "15_missing_summary_temp.csv")
report_table.to_csv(report_path, encoding="utf-8-sig")
print(os.path.exists(report_path))
os.remove(report_path)


# =====================================================================
# [흔한 질문 진단] 결측치 이해와 확인에서 헷갈리기 쉬운 것들
# =====================================================================

# Q1. 위장 결측(0, -999 같은 값)은 read_csv 단계에서 무조건 na_values로 처리하는 게
#     맞나요?
# -> A. 그 컬럼에서 0이나 -999가 절대 정상값일 수 없다는 확신이 있을 때만 안전함.
#       불량여부처럼 0 자체가 "정상"이라는 뜻으로 쓰이는 컬럼에 무턱대고 na_values=[0]을
#       걸면 멀쩡한 값이 통째로 사라짐 - 그래서 컬럼 이름을 지정하는 딕셔너리 형태
#       (na_values={"컬럼명": [값]})로 좁혀 쓰는 습관이 안전함

# Q2. isna().sum()과 info()의 Non-Null Count는 같은 정보를 다른 방식으로 보여주는
#     건가요?
# -> A. 맞음. info()의 Non-Null Count는 "결측이 아닌 값의 개수"이고, isna().sum()은
#       "결측인 값의 개수"라서 서로 (전체 행 수 - Non-Null Count)만큼 차이가 남 - 방향만
#       반대일 뿐 같은 결측 정보를 담고 있음

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# inj = pd.read_csv("data/15_01_사출성형_공정.csv")
# a = inj["사출압력"].isna().sum()
# b = (inj["사출압력"] == 0).sum()
# print(a, b)
# 정답: 1 0
# (실제 250행 데이터에는 사출압력이 진짜 NaN으로 1개 비어 있을 뿐, 위장 결측처럼
#  0으로 찍힌 값은 없음 - 위장 결측은 이 큰 파일이 아니라 앞서 본 16행짜리 로그에서
#  발견됐던 것)

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# inj = pd.read_csv("data/15_01_사출성형_공정.csv")
# row_na = inj.isna().sum(axis=1)
# print(row_na.sum() == inj.isna().sum().sum())
# 정답: True
# (행 방향으로 센 결측을 모두 더한 값과 열 방향으로 센 결측을 모두 더한 값은 결국
#  데이터 전체의 결측 개수를 두 가지 방향에서 센 것뿐이라 항상 같음)


# =====================================================================
# 결측치 처리 - 결측치 제거와 대체
# =====================================================================

# [개념] 결측치 제거란 - 결측이 있는 행·열을 통째로 지우는 단순하고 정직한 방법
# - 장점: 없는 값을 지어내지 않는 왜곡 없는 처리 - 남은 데이터는 모두 진짜 측정값
# - 단점: 센서 하나만 비어도 그 행 전체가 함께 버려짐
# - 제거는 되돌릴 수 없으므로, 원본은 반드시 따로 보관

# [개념] dropna() - 옵션 없이 쓰면 결측이 하나라도 있는 행을 모두 삭제
clean_any = inj.dropna()
print(clean_any.shape)  # (76, 22) - 250행 중 174행이 통째로 사라짐
# dropna는 원본을 바꾸지 않고 결과를 돌려주므로, 반드시 새 변수에 담아야 반영됨

# [개념] axis로 결측 열 삭제 - axis=1은 결측 있는 열을 삭제
clean_cols = inj.dropna(axis=1)
print(clean_cols.shape)  # (250, 10) - 결측 없는 컬럼만 남음

dropped = inj.drop(columns=["계량종료점", "감압시간"])
print(dropped.shape)  # (250, 20) - 특정 컬럼만 콕 집어 빼기
# axis=0은 세로 방향 행, axis=1은 가로 방향 열 - 실무에서는 drop으로 콕 집어 빼는 방식이 더 흔함

# [개념] how로 삭제 기준 정하기 - 같은 dropna여도 how 하나로 결과가 극과 극
print(inj.dropna(how="any").shape)  # (76, 22) - 결측 1개라도 있으면 삭제(기본값)
print(inj.dropna(how="all").shape)  # (250, 22) - 모든 값이 결측일 때만 삭제, 거의 그대로 유지
# df.dropna(how="all")은 완전히 빈 행만 정리하는 가장 안전한 첫 단계

# [강사님께 질문하기] how="any"가 기본값이라는 게 조금 위험하게 느껴져요. 왜 판다스는
# 더 안전해 보이는 how="all"이 아니라 more 공격적인 any를 기본으로 정해뒀나요?
# -> 답변: "안전하다"의 기준을 어디에 두느냐의 문제. any가 기본인 이유는 dropna()의
#    설계 철학이 "결측이 조금이라도 섞인 행은 통계 계산에 그대로 넣기엔 찜찜하니
#    일단 걸러내라"는 보수적인 태도이기 때문임 - 즉 "데이터 손실을 줄이는 안전"보다
#    "결측이 섞인 채로 계산되는 걸 막는 안전"을 우선한 것. 실제로 결측 처리에서
#    진짜 위험한 건 손실 자체가 아니라 결측이 섞인 걸 모르고 계산해서 틀린 결론을
#    내리는 것이라서, "일단 눈에 보이게 걸러주는" any를 기본값으로 삼고, 데이터를
#    더 살리고 싶으면 how="all"이나 thresh를 사람이 직접 선택하도록 설계한 것

# [개념] thresh로 임계값 삭제 - "결측 N개 이상이면 삭제"가 아니라 "값 N개 이상이면 유지"
clean_thresh = inj.dropna(thresh=20)
print(clean_thresh.shape)  # (162, 22) - 22개 컬럼 중 20개 이상 값이 있는 행만 유지
# 기본 dropna(76행)보다 두 배 넘게 살림 - any와 all의 중간, 너무 부실한 행만 거르는 균형점

# [개념] subset으로 특정 컬럼 기준 삭제 - 지정한 컬럼만 보고 결측 판단
protected = inj.dropna(subset=["불량여부"])
print(protected.shape)  # (250, 22) - 불량여부(정답 컬럼)엔 애초에 결측이 없어 그대로 유지

pressure_only = inj.dropna(subset=["사출압력"])
print(pressure_only.shape)  # (249, 22) - 사출압력이 빈 행 1개만 정확히 삭제
# 여러 컬럼을 리스트로 지정하면 그중 하나라도 빈 행이 삭제 대상 - 정답처럼 함부로 채우면
# 안 되는 컬럼을 보호하는 데 특히 유용

# [정리] 제거의 장단점
# - 장점: 간단하고 정직, 코드 한 줄로 처리, 남은 데이터는 모두 진짜 측정값
# - 단점: 멀쩡한 값까지 함께 손실 (250행 -> 76행, 70% 손실)
# - 주의: 결측이 특정 상황에 몰리면 그 상황의 데이터가 통째로 사라지는 편향 위험
# 제거 후 데이터가 절반 아래로 줄면 멈춰서 다시 생각 - 제거 대신 대체를 고려

# [개념] 삭제 전후 shape 검증 - 확인으로 시작해 확인으로 끝나는 처리의 마무리
before_shape = inj.shape
after_drop = inj.dropna()
after_shape = after_drop.shape
print(before_shape, after_shape, after_drop.isna().sum().sum())  # 마지막 0이면 결측 완전 제거 확인

# [정리] 행 삭제 vs 열 삭제 판단 - 결측이 어디에 몰려 있는가가 핵심 기준
# - 일부 행에 집중: 행 삭제 (측정 실패한 몇몇 행만 빼면 나머지는 거의 살림)
# - 특정 컬럼에 집중: 열 삭제 (절반 넘게 빈 컬럼 하나만 빼면 모든 행을 살릴 수 있음)
# - 실무 권장 순서: 열 -> 행 (결측 심한 컬럼 먼저 정리한 뒤 부실 행 정리, 순서를 바꾸면 손실이 커짐)


print("\n===================== 실습 1. dropna로 행·열 삭제 =====================")
# 목표: 결측 있는 행과 열을 삭제하고 크기 변화 확인
# 단계: ① 원본 크기를 shape로 확인 -> ② dropna로 결측 있는 행을 모두 삭제
#      -> ③ 방향을 열로 바꿔 결측 있는 열을 삭제
# 예상 결과: 250x22 -> 행삭제 76x22, 열삭제 250x10
print(inj.shape)
print(inj.dropna().shape)
print(inj.dropna(axis=1).shape)


print("\n===================== 실습 2. dropna 옵션 조절 =====================")
# 목표: how·thresh·subset으로 삭제 기준을 세밀하게 조절
# 단계: ① how로 완전히 빈 행만 삭제하는 기준 적용 -> ② thresh로 값이 일정 개수 이상인
#      행만 남기기 -> ③ subset으로 특정 컬럼이 빈 행만 삭제
# 예상 결과: 완전 결측 행만 삭제는 거의 유지(250), 임계값 20은 162행
print(inj.dropna(how="all").shape)
print(inj.dropna(thresh=20).shape)
print(inj.dropna(subset=["사출압력"]).shape)


print("\n============   ========= 실습 3. 결측 비율 기준 컬럼 제거 =====================")
# 목표: 결측 비율이 높은 컬럼만 골라 제거
# 단계: ① 컬럼별 결측 비율을 계산 -> ② 비율이 기준을 넘는 컬럼 이름만 목록으로 뽑기
#      -> ③ 그 컬럼들을 drop으로 제거하고 크기 확인
# 예상 결과: 40% 초과 계량종료점·감압시간 제거 -> 250x20
ratio = (inj.isna().sum() / len(inj) * 100)
over_40 = ratio[ratio > 40].index.tolist()
print(over_40)  # ['계량종료점', '감압시간']

trimmed = inj.drop(columns=over_40)
print(trimmed.shape)  # (250, 20)


print("\n===================== 실습 4. 삭제 손실 비교 =====================")
# 목표: 삭제 방식별 남는 행 수와 손실률을 표로 비교
# 단계: ① 원본·행삭제·thresh 각 방식의 남는 행 수 구하기 -> ② 방식과 행 수를 하나의
#      표로 모으기 -> ③ 원본 대비 손실률을 백분율로 계산해 나란히 보기
# 예상 결과: 행삭제 손실 약 70%, thresh 손실 약 35%
n_original = len(inj)
n_any = len(inj.dropna())
n_thresh = len(inj.dropna(thresh=20))

loss_table = pd.DataFrame({
    "방식": ["원본", "dropna()", "dropna(thresh=20)"],
    "남는 행 수": [n_original, n_any, n_thresh],
})
loss_table["손실률(%)"] = ((n_original - loss_table["남는 행 수"]) / n_original * 100).round(1)
print(loss_table)


# [개념] 결측치 대체(imputation)란 - 빈 칸만 콕 집어 그럴듯한 값으로 채워 크기를 유지
# - 제거와 정반대 접근: 데이터를 하나도 안 버리고 원래 크기 그대로 유지
# - 쓰는 이유: 제거하면 70%가 날아가는 데이터에서 빈 값 하나만 채우면 나머지를 다 살림
# - 주의점: 채운 값은 결국 추측 - 너무 많이 채우면 진짜 데이터 모습에서 멀어질 수 있음

# [개념] fillna로 상수 채우기 - 결측이 특정 의미를 가질 때만 사용
sample = mlog.copy()
sample["누적샷"] = sample["누적샷"].fillna(0)  # 숫자 결측이 "기록 없음=0"을 의미할 때
sample["사출기"] = sample["사출기"].fillna("미상")  # 글자 결측은 "미상" 같은 표시값
print(sample.loc[7, "사출기"])  # 미상
# 주의: 사출압력 같은 측정값에 0을 채우면 "압력이 진짜 0이었다"는 틀린 정보가 되어 평균이 왜곡됨


# [개념] 평균으로 채우기 - 그 컬럼의 평소 대표값으로 채우는 측정값 결측의 표준
pressure_mean = inj["사출압력"].mean()
inj_mean_filled = inj["사출압력"].fillna(pressure_mean)
print(round(pressure_mean, 3), inj_mean_filled.isna().sum())  # 1.338, 0

# [개념] 중앙값으로 채우기 - 크기순 한가운데 값, 이상치가 있어도 흔들리지 않는 안전한 대체
pressure_median = inj["사출압력"].median()
inj_median_filled = inj["사출압력"].fillna(pressure_median)
print(round(pressure_median, 3), inj_median_filled.isna().sum())  # 1.34, 0

# [정리] 평균 vs 중앙값 - 이상치가 있으면 둘이 크게 벌어짐
# - 예시(이상치 있는 경우): 1, 2, 3, 4, 100 -> 평균 22, 중앙값 3 - 평균이 100 하나에 크게 끌려감
# - 실제 사출압력 컬럼: 평균 1.338, 중앙값 1.34 - 둘이 거의 같음
# - 이 공정 데이터는 배럴온도·사이클시간처럼 대부분 표준편차가 아주 작게 관리되고
#   있어서(설비가 정밀하게 통제되는 공정), 극단적인 이상치가 드물어 평균과 중앙값이
#   자연스럽게 가까움 - 평균이 나쁜 게 아니라, 이상치가 없고 고르게 퍼졌으면 평균이
#   가장 자연스러운 대표값이라는 원칙 그대로

# [정리] 평균 vs 중앙값, 무엇을 쓸까
# - 대체 전 평균과 중앙값을 둘 다 구해 비교 - 두 값이 비슷하면 분포가 고르다는 뜻(평균 선택)
# - 두 값이 눈에 띄게 다르면 이상치 신호 - 안전한 중앙값 선택
# - 헷갈릴 때는 중앙값 - 미처 못 걸러낸 이상치가 남아 있어도 영향을 거의 안 받는 보험

# [강사님께 질문하기] 사출압력은 평균과 중앙값이 거의 똑같이 나왔는데, 그럼 이런
# 경우엔 평균으로 채우나 중앙값으로 채우나 결과가 똑같으니 아무거나 써도 상관없는
# 건가요?
# -> 답변: 이번처럼 두 값이 가까운 경우라면 채워지는 숫자 자체는 거의 같아서 실용적인
#    차이는 크지 않음. 다만 "결과가 같으니 아무 이유 없이 골라도 된다"는 뜻은 아님 -
#    지금 데이터에 이상치가 없다는 걸 우리가 평균·중앙값을 비교해서 확인했기 때문에
#    안심하고 평균을 쓸 수 있는 것이지, 그 비교 과정 자체를 건너뛰면 나중에 다른
#    컬럼(예: 이상치가 섞인 컬럼)에도 습관적으로 평균을 썼다가 낭패를 볼 수 있음. 즉
#    "이번엔 뭘 써도 되는 상황"이라는 판단 자체가 미리 평균·중앙값을 비교해봤기
#    때문에 나온 결론이라는 게 핵심


# [개념] 최빈값으로 채우기 - 범주형(글자·분류) 데이터는 평균이 없어 가장 흔한 값으로 채움
print(mlog["사출기"].value_counts())  # 1호기 4, 2호기 4, A호기 4, B호기 3 - 세 값이 동률 최다
top_machine = mlog["사출기"].mode()
print(top_machine.tolist())  # ['1호기', '2호기', 'A호기'] - 동률이면 mode()가 여러 개를 모두 돌려줌

filled_machine = mlog["사출기"].fillna(top_machine[0])
print(filled_machine.isna().sum())  # 0 - 동률일 때는 관례상 mode()[0](첫 번째 후보)을 사용

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# mlog = pd.read_csv("data/15_사출성형_로그.csv")
# m = mlog["사출기"].mode()
# print(len(m))
# print(type(m))
# 정답: 3 / <class 'pandas.core.series.Series'>
# (최빈값이 하나로 딱 정해지는 경우가 더 흔하지만, 이번처럼 여러 값이 동률로 가장
#  많이 나오면 mode()는 그 후보를 모두 담은 Series를 돌려줌 - 값 하나만 나올 거라고
#  단정하면 안 되는 이유)


# [개념] 앞 값으로 채우기 - ffill, 설비 상태는 짧은 시간에 급변하지 않는다는 가정
mlog_sorted = mlog.sort_values("측정시각")
temp_ffilled = mlog_sorted["배럴온도"].ffill()
print(temp_ffilled.tolist()[:4])  # [201.2, 201.5, 201.5, 202.0] - 2번 행 NaN이 직전 값 201.5로 채워짐

# [주의] ffill은 진짜 NaN만 채움 - 위장 결측(999 같은 값)은 애초에 NaN이 아니라서 그대로 남음
print(temp_ffilled.tolist()[8])  # 999.0 - ffill을 해도 위장 결측은 손대지 못함
# 그래서 순서는 항상 "위장 결측을 먼저 NaN으로 변환 -> 그다음 ffill/bfill"이어야 함

# [개념] 뒤 값으로 채우기 - bfill, 맨 앞이 비어 ffill로 못 채울 때의 보완
machine_col_fixed = safe.sort_values("측정시각")["사출기"]
print(machine_col_fixed.ffill().bfill().tolist())  # ffill 후 남은 맨 앞 결측을 bfill로 마무리

# [정리] ffill·bfill 사용 시 주의점
# - 정렬 필수: 쓰기 전 반드시 시간 컬럼으로 정렬 - 뒤죽박죽 상태면 엉뚱한 값을 끌어옴
# - 긴 결측 주의: 결측이 연달아 있으면 같은 값이 여러 칸 반복 - 잠깐 빠진 한두 칸에만 적합
# - 그룹 분리: 여러 설비가 섞인 데이터는 설비별로 묶은 뒤 그룹 안에서만 ffill해야
#   A 설비의 빈칸을 B 설비 값으로 채우는 사고를 막을 수 있음


# [개념] 그룹별로 채우기 - groupby, 같은 종류끼리 값이 비슷할 때 전체 평균보다 정확
injection_grouped_path = os.path.join("data", "15_02_사출성형_공정.csv")
inj_grp = pd.read_csv(injection_grouped_path)
print(inj_grp["사출기"].value_counts())  # 1호기 110, 2호기 85, 3호기 55

print(inj_grp["최대사출속도"].isna().sum())  # 109
group_means = inj_grp.groupby("사출기")["최대사출속도"].mean().round(2)
print(group_means)  # 1호기 78.12, 2호기 78.11, 3호기 78.10 - 사출기 사이 차이는 크지 않음

inj_grp["최대사출속도"] = inj_grp.groupby("사출기")["최대사출속도"].transform(
    lambda x: x.fillna(x.mean())
)
print(inj_grp["최대사출속도"].isna().sum())  # 0
# 이번 데이터는 사출기 간 평균 차이가 크지 않아 전체 평균과 결과가 비슷하지만, 설비별로
# 조건이 다른 공정에서는 그룹별 평균이 전체 평균보다 훨씬 정확한 대체가 됨

# [강사님께 질문하기] 이번 최대사출속도는 사출기별 평균이 78.10~78.12로 거의 똑같이
# 나왔는데, 그러면 그냥 groupby 없이 전체 평균 하나로 채우는 것과 실질적으로 차이가
# 없는 거 아닌가요?
# -> 답변: 맞음, 이번 컬럼 한정으로는 결과 값 자체는 거의 차이가 없음. 다만 groupby로
#    채우는 방식의 값어치는 "우연히 그룹 간 차이가 있을 때 자동으로 그 차이를 반영해
#    준다"는 데 있음 - 미리 그룹마다 평균을 하나하나 확인해서 "차이가 없으니 전체
#    평균 써도 되겠다"고 판단하고 코드를 다르게 짜는 것보다, 처음부터 groupby로
#    채우면 차이가 있든 없든 항상 옳은 결과가 나옴. 즉 지금은 두 방법의 결과가
#    같아서 이득이 안 보이지만, 그건 이 컬럼이 우연히 그런 것일 뿐이고 groupby
#    방식 자체가 항상 더 안전한 선택인 것


# [정리] 대체가 분포에 미치는 영향 - 채운다는 건 없던 값을 만들어 넣는 일
# - 결측 100개를 평균 하나로 채우면 그 값에 100개가 몰려 분포가 인위적으로 뾰족해짐
# - 흩어진 정도(다양성)가 실제보다 줄어드는 부작용이 생김
# - 결측 절반 넘는 컬럼(계량종료점·감압시간처럼)은 무리해서 채우기보다 차라리 제거가 나음

# [개념] inplace 파라미터 주의 - "처리했는데 왜 안 바뀌지"의 십중팔구는 결과 미저장
# - 결과를 변수에 안 담으면 화면엔 처리된 듯 보여도 원본은 그대로
# - inplace=True는 최신 판다스에서 권장하지 않는 흐름(Deprecated) - 아예 안 쓰는 게 안전
# - 우리 원칙은 하나: 처리 결과는 항상 변수에 담는다 (df = df.fillna(0) 또는 clean = df.fillna(0))

# [개념] 처리 후 검증과 저장 - isna 검증 후 새 이름으로 저장
final_check = inj.dropna(thresh=20).copy()
final_check["사출압력"] = final_check["사출압력"].fillna(final_check["사출압력"].median())
print(final_check.isna().sum().sum())  # 남은 결측 확인 (0이 아니면 아직 처리할 컬럼이 남아 있다는 뜻)
# index=False로 행 번호가 안 들어가게, encoding="utf-8-sig"로 한글이 안 깨지게 저장
# 처리가 잘못됐을 때 돌아갈 수 있도록 원본에 덮어쓰지 말고 새 이름으로 저장하는 습관

# [정리] 결측치 처리 흔한 실수 5가지
# - 결과 미반영: 처리했는데 결측이 그대로 -> 결과를 반드시 변수에 담기
# - 위장 결측 방치: 0·-999를 그대로 두고 평균 계산 -> 먼저 NaN으로 변환
# - 과한 대체: 절반 넘는 결측을 다 채움 -> 차라리 컬럼 제거
# - 정답 함부로 채움: 불량여부 같은 정답을 추측으로 채움 -> subset으로 빈 행만 제거
# - 검증 건너뛰기: 처리 후 isna로 재확인 안 함 -> isna().sum().sum() == 0 확인

# [정리] 대체 방법 선택 기준
# - 글자·분류(범주형): 최빈값 - 평균이 없어 가장 자주 나타나는 값으로
# - 숫자 측정값, 고른 분포: 평균 - 이상치 없고 고르면 가장 자연스러운 대표값
# - 숫자 측정값, 치우친 분포: 중앙값 - 이상치에 흔들리지 않는 안전한 보험
# - 시간·순서 있는 데이터: ffill + bfill - 직전 값으로 잇고 맨 앞은 뒤 값으로 보완
# - 의미 있는 결측(없음·0): 상수 - 참여안함=0, 미상="미상" 등 명시적 표시
# - 그룹이 뚜렷한 데이터: 그룹별 평균·중앙값 - 같은 종류끼리 묶어 채우면 더 정확

# [정리] 결측치 처리 전체 워크플로우 - 확인 -> 판단 -> 처리 -> 검증·저장
# ① 확인: 위장 결측을 NaN으로 변환, 비율·순위·분포 파악 (isna·mean·sort_values)
# ② 판단: 컬럼·행별로 제거할지 대체할지 방향 결정
# ③ 처리: 제거로 덜고 대체로 채움, 컬럼별 알맞은 방법 적용 (drop·fillna·ffill)
# ④ 검증·저장: 결측 0 확인, 새 파일로 저장하며 처리 내역 기록 (to_csv)
# 이 흐름은 결측치 전용이 아니라 이상치·정규화 등 모든 전처리에 똑같이 반복되는 기본 리듬


print("\n===================== 실습 5. fillna 평균·중앙값 대체 =====================")
# 목표: 결측을 평균과 중앙값으로 채우고 차이 이해
# 단계: ① 사출압력의 평균과 중앙값을 각각 구해 비교 -> ② fillna로 평균을 채운 결과 만들기
#      -> ③ fillna로 중앙값을 채운 결과 만들기
# 예상 결과: 사출압력 평균 1.338·중앙값 1.34로 대체, 남은 결측 0
mean_v = inj["사출압력"].mean()
median_v = inj["사출압력"].median()
print(round(mean_v, 3), round(median_v, 3))

filled_by_mean = inj["사출압력"].fillna(mean_v)
filled_by_median = inj["사출압력"].fillna(median_v)
print(filled_by_mean.isna().sum(), filled_by_median.isna().sum())


print("\n===================== 실습 6. 최빈값·앞뒤 값 대체 =====================")
# 목표: 범주형은 최빈값, 시계열은 앞뒤 값으로 채우기
# 단계: ① 사출기 열의 최빈값을 구해 채우기 -> ② 측정시각 순으로 정렬해 시계열 순서 만들기
#      -> ③ ffill로 앞 값, bfill로 남은 앞쪽 결측까지 채우기
# 예상 결과: 사출기는 최빈값(1호기)으로, 배럴온도는 앞뒤 값으로 대체
mode_value = mlog["사출기"].mode()[0]
machine_filled = mlog["사출기"].fillna(mode_value)
print(machine_filled.isna().sum())

time_sorted = mlog.sort_values("측정시각")
temp_filled = time_sorted["배럴온도"].ffill().bfill()
print(temp_filled.isna().sum())


print("\n===================== 실습 7. 그룹별 대체 =====================")
# 목표: 그룹별 평균으로 채워 집단 특성 반영
# 단계: ① 사출기로 그룹을 나누기 -> ② 각 그룹의 평균으로 그 그룹의 결측을 채우기
#      -> ③ 남은 수치 결측은 전체 중앙값으로 마무리하고 검증
# 예상 결과: 최대사출속도를 사출기별 평균으로 대체, 남은 결측 0
inj_grp2 = pd.read_csv(injection_grouped_path)
inj_grp2["최대사출속도"] = inj_grp2.groupby("사출기")["최대사출속도"].transform(
    lambda x: x.fillna(x.mean())
)
remaining_median = inj_grp2["최대사출속도"].median()
inj_grp2["최대사출속도"] = inj_grp2["최대사출속도"].fillna(remaining_median)
print(inj_grp2["최대사출속도"].isna().sum())


print("\n===================== 실습 8. 제거 vs 대체 비교 =====================")
# 목표: 같은 데이터에 제거와 대체를 적용해 결과 비교
# 단계: ① 결측 심한 컬럼을 먼저 뺀 기준 데이터 만들기 -> ② 기준 데이터에서 결측 행을
#      삭제한 제거 버전 만들기 -> ③ 기준 데이터의 결측을 중앙값으로 채운 대체 버전 만들기
# 예상 결과: 제거 버전은 행이 줄고, 대체 버전은 250행 모두 유지
base = inj.drop(columns=over_40)  # 계량종료점·감압시간처럼 결측 40% 넘는 컬럼 먼저 제거

removed_version = base.dropna()
print(removed_version.shape)  # 남은 결측이 적은 컬럼만으로도 여전히 일부 행은 빠짐

filled_version = base.copy()
for col in filled_version.columns:
    if filled_version[col].isna().sum() > 0 and pd.api.types.is_numeric_dtype(filled_version[col]):
        filled_version[col] = filled_version[col].fillna(filled_version[col].median())
print(filled_version.shape)  # (250, 20) - 제거 없이 모두 유지
print(filled_version.isna().sum().sum())  # 0


print("\n===================== 실습 9. 종합 처리 =====================")
# 목표: 제거와 대체를 조합해 전체 결측을 처리하고 저장
# 단계: ① 결측 비율 높은 컬럼을 제거하고 나머지는 중앙값으로 채우기 -> ② 처리 후 남은
#      결측과 크기를 확인하고 파일로 저장 -> ③ 같은 절차를 사출기 그룹 데이터에도 반복
# 예상 결과: 두 데이터 모두 결측 0, 처리 결과 파일로 저장 후 정리
final_inj = inj.drop(columns=over_40)
for col in final_inj.columns:
    if final_inj[col].isna().sum() > 0 and pd.api.types.is_numeric_dtype(final_inj[col]):
        final_inj[col] = final_inj[col].fillna(final_inj[col].median())
print(final_inj.shape, final_inj.isna().sum().sum())

final_grp = inj_grp.copy()
for col in final_grp.columns:
    if final_grp[col].isna().sum() > 0 and pd.api.types.is_numeric_dtype(final_grp[col]):
        final_grp[col] = final_grp.groupby("사출기")[col].transform(lambda x: x.fillna(x.mean()))
        final_grp[col] = final_grp[col].fillna(final_grp[col].median())
print(final_grp.shape, final_grp.isna().sum().sum())

final_path = os.path.join("data", "15_injection_processed_temp.csv")
final_inj.to_csv(final_path, index=False, encoding="utf-8-sig")
print(os.path.exists(final_path))
os.remove(final_path)


# =====================================================================
# [흔한 질문 진단] 결측치 제거와 대체에서 헷갈리기 쉬운 것들
# =====================================================================

# Q3. dropna(thresh=20)에서 20은 "결측 개수"인가요, "값이 있는 개수"인가요?
# -> A. 값이 있는 개수(살아 있는 값의 최소 개수)임. 22개 컬럼 중 thresh=20이면 "값이
#       20개 이상 있는 행만 남긴다"는 뜻이라서, 거꾸로 말하면 "결측이 2개(=22-20)
#       이하인 행만 남긴다"는 것과 같음 - 방향을 반대로 착각하기 쉬운 옵션이라 항상
#       "N개 이상 살아있어야 유지"로 기억하는 게 안전함

# Q4. groupby로 채운 뒤에도 결측이 남아 있으면 어떻게 되나요?
# -> A. 그 그룹 자체에 값이 하나도 없어서 그룹 평균조차 계산할 수 없는 경우 결측이
#       그대로 남을 수 있음. 그래서 groupby 대체 뒤에는 항상 isna().sum()으로
#       재검증하고, 남은 결측은 전체 중앙값처럼 더 큰 범위의 대표값으로 한 번 더
#       채워 마무리하는 이중 안전장치가 필요함 - 실습7·9에서 그룹별 평균 다음에
#       전체 중앙값을 한 번 더 적용한 이유가 바로 이것

# [퀴즈] 아래 코드의 출력 결과를 먼저 예상해보기
# inj = pd.read_csv("data/15_01_사출성형_공정.csv")
# a = inj.dropna()
# b = inj.fillna(inj.median(numeric_only=True))
# print(a.shape[0], b.shape[0])
# print(a.isna().sum().sum(), b.isna().sum().sum())
# 정답: 76 250 / 0 0
# (제거는 행 개수 자체가 줄어들지만 남은 값은 모두 진짜 측정값이고, 대체는 250행을
#  그대로 유지하지만 채운 자리는 진짜 측정값이 아니라 추정값 - 결측 0이라는 결과는
#  같아도 그 안의 데이터 성격은 완전히 다름)
