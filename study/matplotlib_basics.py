import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


# =====================================================================
# Matplotlib 기초 - 선 그래프와 그래프 완성
# =====================================================================

# [문제 상황] 숫자표로는 안 보이던 변화가 그래프 한 장에 드러남
# - 사람 눈은 숫자 비교엔 약하지만 모양·색 차이엔 강함 - 잘하는 일로 바꿔주는 도구가 시각화
# - 이 단원의 실데이터: 열처리 공정(17_열처리.csv, 44행) - 로트A/B/C 세 배치의 소입로 온도를
#   10분 간격으로 기록, 뒤에서는 120행짜리 공정 로그(17_열처리_공정.csv)로 이어감

# [개념] matplotlib과 pyplot - 큰 도구 상자 안의 자주 쓰는 공구함
# - matplotlib: 파이썬 그래프 도구 전체를 담은 큰 상자
# - pyplot(별명 plt): 선 그리기·제목 붙이기·화면 표시처럼 자주 쓰는 명령만 모은 공구함
# - import matplotlib.pyplot as plt - numpy를 np로, pandas를 pd로 부르는 것과 같은 전 세계 공통 약속

# [개념] 그래프 그리는 기본 4단계 - 준비 -> 그리기 -> 꾸미기 -> 보여주기
# - 준비: 도구 불러오고 데이터 담기 / 그리기: plot 등으로 데이터를 선으로 바꾸기(화면엔 아직 없음)
# - 꾸미기: 제목·축·범례 붙이기 / 보여주기: show()를 만나야 비로소 화면에 나타남
# - show를 중간에 쓰면 그 뒤에 꾸민 내용이 반영되지 않은 채로 한 장이 먼저 뜸

# [개념] 한글 폰트 설정 - 코드 오류가 아니라 글꼴에 한글 모양이 없어서 생기는 문제
# - 기본 글꼴엔 한글 자형이 없어 네모로 깨짐 - 윈도우는 'Malgun Gothic', 맥은 'AppleGothic'
# - axes.unicode_minus를 False로 꺼야 "-3도" 같은 음수 기호까지 정상 표시 (이 파일 맨 위에서 설정 완료)


print("\n===================== 실습 1. 환경 준비와 첫 그래프 =====================")
# 목표: 실데이터로 첫 선 그래프를 그려 4단계 흐름(준비-그리기-꾸미기-보여주기) 체감
# 단계: ① 로트A 데이터를 불러와 온도 리스트 준비 -> ② plot으로 그리기 -> ③ show 직전까지 마무리
# 예상 결과: 로트A 15개 측정값이 850~865 사이에서 오르내리는 선
heat = pd.read_csv("data/17_열처리.csv")
print(heat.shape)  # (44, 6)
lot_a = heat[heat["배치"] == "로트A"].reset_index(drop=True)
print(len(lot_a))  # 15
plt.plot(lot_a["측정시각"], lot_a["온도"])
plt.savefig(os.path.join("data", "_tmp_mpl_practice1.png"))
plt.close()


# [개념] plt.plot() - 점을 선으로 잇기
# - x와 y를 같은 순서끼리 짝지어 점으로 만들고, 그 점들을 순서대로 선으로 이음
# - x를 생략하면 y 개수만큼 0,1,2... 자동 번호가 x로 쓰임 - 파이썬이 순서를 0부터 세기 때문
# - x·y는 반드시 개수가 같아야 함 - 다르면 짝이 안 맞아 오류

print("\n===================== 실습 2. 선 그래프 색·스타일 직접 지정 =====================")
# 목표: color·linestyle·marker 옵션으로 선을 꾸며보기
# 단계: ① 로트A 온도를 빨간 점선+동그라미 마커로 그리기 -> ② 저장
# 예상 결과: 온도 15개가 빨간 점선과 동그라미 마커로 표시됨
plt.plot(lot_a["측정시각"], lot_a["온도"], color="red", linestyle="--", marker="o")
plt.title("로트A 온도 변화")
plt.savefig(os.path.join("data", "_tmp_mpl_practice2.png"))
plt.close()
print(os.path.exists(os.path.join("data", "_tmp_mpl_practice2.png")))  # True

# [강사님께 질문하기] color·linestyle·marker처럼 옵션이 여러 개면 순서를 꼭 지켜서 써야 하나요?
# -> 답변: 아님. plt.plot(x, y, color=..., linestyle=..., marker=...)처럼 이름=값 형태로 쓰는
#    "키워드 인자"라서, 이름표가 붙어 있는 한 순서를 바꿔 써도 똑같이 동작함. 다만 맨 앞의
#    x, y처럼 이름 없이 값만 넣는 자리(위치 인자)는 순서가 고정돼 있어야 함 - 옵션들은
#    자유, 데이터 두 개는 순서 고정이라고 기억하면 됨


print("\n===================== 실습 3. 두 로트 비교하며 추세 보기 =====================")
# 목표: 로트A·로트C를 한 그래프에 겹쳐 그리고 legend로 구분
# 단계: ① 로트C 데이터 불러오기 -> ② 두 로트를 각각 plot(label=...)로 그리기 -> ③ legend 호출
# 예상 결과: 로트A(평균 858.42) 아래, 로트C(평균 860.42) 위쪽에서 움직이는 두 선
lot_c = heat[heat["배치"] == "로트C"].reset_index(drop=True)
print(round(lot_a["온도"].mean(), 2), round(lot_c["온도"].mean(), 2))  # 858.42 860.42
plt.plot(range(len(lot_a)), lot_a["온도"], label="로트A")
plt.plot(range(len(lot_c)), lot_c["온도"], label="로트C")
plt.legend()
plt.savefig(os.path.join("data", "_tmp_mpl_practice3.png"))
plt.close()


# [개념] 제목·축 이름 달기 - plt.title() · plt.xlabel() · plt.ylabel()
# - 제목 없는 그래프는 그린 사람도 며칠 뒤엔 무슨 그래프인지 헷갈림
# - 축 이름엔 단위까지 적어야 함 - 70이 70도인지 70%인지는 단위 없이 알 수 없음
# - 제목·가로축·세로축 이름은 항상 한 세트로 함께 붙이는 습관

# [개념] xticks로 눈금 글자 바꾸기, legend(loc=...)로 범례 위치 정하기
# - xticks(위치, 글자)는 데이터는 그대로 두고 화면에 보이는 표시만 글자로 바꿈
# - legend(loc='upper left') 등으로 데이터가 비어 있는 쪽에 범례를 보내 겹침 방지
# - label은 plot 안에 이름을 "적어두는" 역할, legend()는 그 이름을 실제로 "보여주는" 역할 -
#   둘 다 있어야 범례가 뜸(label만 쓰고 legend를 빠뜨리는 게 가장 흔한 실수)

# [퀴즈] 아래 코드를 실행하면 범례가 화면에 나타날지 먼저 예상해보기
# plt.plot(lot_a["측정시각"], lot_a["온도"], label="로트A")
# plt.show()
# 정답: 나타나지 않음
# (label은 이름표를 "적어두기"만 할 뿐, legend()를 호출해야 그 이름표가 실제로 화면에
#  "보여지기" 때문 - 이 둘은 항상 짝으로 붙어 다녀야 함)


print("\n===================== 실습 4. 제목·축·범례 갖춘 완성형 그래프 =====================")
# 목표: figsize로 도화지 크기를 먼저 잡고, 로트A·로트B를 제목·축·범례까지 갖춰 비교
# 단계: ① figure(figsize=...)를 plot보다 먼저 호출 -> ② 두 로트를 색·마커 다르게 그리기
#      -> ③ title·xlabel·ylabel·legend(loc=...)로 완성
# 예상 결과: 가로로 긴 도화지에 로트A·로트B 온도 선이 제목·축·범례와 함께 표시
lot_b = heat[heat["배치"] == "로트B"].reset_index(drop=True)
plt.figure(figsize=(10, 4))
plt.plot(range(len(lot_a)), lot_a["온도"], color="blue", marker="o", label="로트A")
plt.plot(range(len(lot_b)), lot_b["온도"], color="red", marker="s", label="로트B")
plt.title("로트A·로트B 온도 비교")
plt.xlabel("측정 순서")
plt.ylabel("온도(℃)")
plt.legend(loc="lower right")
plt.savefig(os.path.join("data", "_tmp_mpl_practice4.png"))
plt.close()
# figure는 반드시 plot보다 먼저 - plot 다음에 쓰면 크기가 적용되지 않음


print("\n===================== 실습 5. 세 로트 비교와 이미지 저장 =====================")
# 목표: 반복문으로 로트A/B/C 세 선을 겹쳐 그리고 savefig로 저장(show보다 먼저 저장)
# 단계: ① 배치 이름·색 목록을 반복하며 각 로트 온도를 그리기 -> ② 제목·축·범례 -> ③ savefig
# 예상 결과: 세 로트 온도 비교 그래프가 파일로 저장됨(파일 존재 여부로 확인)
plt.figure(figsize=(10, 4))
lot_names = ["로트A", "로트B", "로트C"]
lot_colors = ["blue", "green", "red"]
for name, color in zip(lot_names, lot_colors):
    lot = heat[heat["배치"] == name].reset_index(drop=True)
    plt.plot(range(len(lot)), lot["온도"], color=color, label=name)
plt.title("로트별 온도 비교")
plt.xlabel("측정 순서")
plt.ylabel("온도(℃)")
plt.legend()
save_path = os.path.join("data", "_tmp_mpl_practice5.png")
plt.savefig(save_path, dpi=100)
plt.close()
print(os.path.exists(save_path))  # True
os.remove(save_path)


print("\n===================== 실습 6. 한 로트의 여러 값 종합 그리기 =====================")
# 목표: 로트A의 온도·CP값을 한 그래프에 겹쳐 그리며 단위 차이 문제를 체감
# 단계: ① 온도(850~865대)와 CP값(대부분 0.44~0.46대)을 그대로 겹쳐 그려 CP값이 바닥에 깔리는 것 확인
#      -> ② CP값에 1000을 곱해 눈에 보이는 크기로 보정
# 예상 결과: 보정 전엔 CP값 선이 바닥에 눌려 안 보이고, 1000배 후엔 온도와 나란히 보임
print(round(lot_a["온도"].min(), 1), round(lot_a["온도"].max(), 1))  # 852.1 861.9
print(round(lot_a["CP값"].min(), 3), round(lot_a["CP값"].max(), 3))
# CP값 최댓값 0.607은 10:40에 찍힌 단 한 번의 스파이크 - 나머지 14개는 0.444~0.463 사이로
# CP값 자체에도 온도와는 별개로 짚어볼 만한 이상치가 하나 섞여 있음
plt.figure(figsize=(10, 4))
plt.plot(range(len(lot_a)), lot_a["온도"], label="온도")
plt.plot(range(len(lot_a)), lot_a["CP값"] * 1000, label="CP값 x1000(보정)")
plt.title("로트A 온도·CP값 종합(단위 보정)")
plt.xlabel("측정 순서")
plt.legend()
plt.savefig(os.path.join("data", "_tmp_mpl_practice6.png"))
plt.close()
# 단위가 비슷한 값끼리 묶어야 함 - 그대로 겹치면 스케일이 작은 쪽 선이 바닥에 깔려 사라짐


# =====================================================================
# Matplotlib 기초 - 분포·범주·관계 시각화
# =====================================================================

# [문제 상황] 막대·히스토그램·산점도로 데이터의 세 얼굴을 봄
# - 이 단원부터는 120행짜리 열처리 공정 로그(17_열처리_공정.csv)를 사용 - 소입로온도1존·2존,
#   CP값·OP값·세정기 다섯 숫자 컬럼과 라인(주간/야간), result(정상/이상) 두 범주 컬럼을 가짐

proc = pd.read_csv("data/17_열처리_공정.csv")
print(proc.shape)  # (120, 8)


# [개념] 막대그래프 vs 히스토그램 vs 산점도 - 무엇을 보고 싶은가로 결정
# - 막대(bar): 서로 떨어진 항목(라인 A·B·C 등)의 크기를 비교 - 가로축은 독립된 범주
# - 히스토그램(hist): 숫자 하나가 어떤 구간에 얼마나 몰려 있는지 분포를 봄 - 가로축은 연속 구간
# - 산점도(scatter): 두 숫자 값이 함께 어떻게 움직이는지 관계를 봄

print("\n===================== 실습 1. 막대 그래프 직접 그리기 =====================")
# 목표: 라인별 평균 온도1존을 막대로 비교하고 색으로 강조
# 단계: ① groupby로 라인별 평균 계산 -> ② plt.bar로 막대 그리기 -> ③ 더 높은 라인만 색 강조
# 예상 결과: 야간 858.89, 주간 859.47 - 주간이 근소하게 더 높음
line_mean = proc.groupby("라인")["소입로온도1존"].mean().round(2)
print(line_mean)  # 야간 858.89, 주간 859.47
bar_colors = ["red" if v == line_mean.max() else "blue" for v in line_mean]
plt.bar(line_mean.index, line_mean.values, color=bar_colors, width=0.5)
plt.title("라인별 평균 소입로온도1존")
plt.ylabel("온도(℃)")
plt.savefig(os.path.join("data", "_tmp_mpl_bar1.png"))
plt.close()

# [강사님께 질문하기] 막대그래프는 세로축이 반드시 0부터 시작해야 한다고 하셨는데, 지금처럼
# 858~860 사이 좁은 범위 값을 0부터 그리면 막대 높이 차이가 거의 안 보이지 않나요?
# -> 답변: 맞음. 실제로 858.89와 859.47은 0부터 그리면 육안으로 거의 구분이 안 될 만큼
#    가까움. "0부터 시작" 규칙은 막대 높이의 비율을 왜곡하지 말라는 원칙이라서 반드시
#    지켜야 하지만, 그 결과 "두 라인 차이가 거의 없다"는 사실을 있는 그대로 보여주는
#    것도 정직한 그래프의 역할임. 차이를 더 크게 보고 싶다면 막대그래프 대신 boxplot이나
#    두 그룹의 평균 차이를 직접 숫자로 표로 보여주는 방식이 더 적절함


print("\n===================== 실습 2. 범주별 집계 막대 그래프 =====================")
# 목표: result(정상/이상) 개수와 라인별 평균 세정기 값을 막대로 비교
# 단계: ① value_counts로 result 개수 세기 -> ② groupby로 라인별 평균 세정기 계산 -> ③ 막대로 표현
# 예상 결과: 정상 109·이상 11, 라인별 평균 세정기 값 비교
result_count = proc["result"].value_counts()
print(result_count["정상"], result_count["이상"])  # 109 11
plt.bar(result_count.index, result_count.values, color=["blue", "red"])
plt.title("result 개수")
plt.savefig(os.path.join("data", "_tmp_mpl_bar2.png"))
plt.close()

line_cleaner = proc.groupby("라인")["세정기"].mean().round(2)
print(line_cleaner)
plt.bar(line_cleaner.index, line_cleaner.values)
plt.title("라인별 평균 세정기 값")
plt.savefig(os.path.join("data", "_tmp_mpl_bar3.png"))
plt.close()


# [개념] plt.hist()로 히스토그램 그리기, bins로 구간 수 조절
# - 숫자 목록 하나만 넣으면 값 범위를 구간(bins)으로 쪼개 구간별 개수를 막대로 보여줌
# - bins가 작으면 뭉뚱그려지고 크면 자세해짐 - 정답은 없고, 데이터 개수의 제곱근이 출발점
#   (120개면 약 11개)

print("\n===================== 실습 3. 히스토그램 직접 그리기 =====================")
# 목표: 소입로온도1존 분포를 히스토그램으로 그리고 bins를 바꿔가며 비교
# 단계: ① 결측 제외 후 hist(bins=11) 기본 그리기 -> ② bins=5·30으로 바꿔 모양 변화 확인
# 예상 결과: 858~860 사이에 값이 몰린 분포, bins가 작을수록 뭉뚱그려짐
temp1 = proc["소입로온도1존"].dropna()
print(round(temp1.mean(), 2), round(temp1.std(), 2))  # 859.18 2.75
plt.hist(temp1, bins=11)
plt.xlabel("소입로온도1존(℃)")
plt.ylabel("개수")
plt.title("소입로온도1존 분포(bins=11)")
plt.savefig(os.path.join("data", "_tmp_mpl_hist1.png"))
plt.close()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(temp1, bins=5)
axes[0].set_title("bins=5(뭉뚱그려짐)")
axes[1].hist(temp1, bins=30)
axes[1].set_title("bins=30(잘게 쪼개짐)")
plt.savefig(os.path.join("data", "_tmp_mpl_hist2.png"))
plt.close()


print("\n===================== 실습 4. 센서값 분포와 이상 범위 확인 =====================")
# 목표: 분포를 평균·표준편차로 요약하고, 정상 범위를 벗어난 값 개수 확인
# 단계: ① 평균±표준편차 범위 계산 -> ② 그 범위를 벗어난 값 개수 세기
# 예상 결과: 평균 859.18, 표준편차 2.75 근처 범위를 벗어난 값이 소수 존재
mean_t, std_t = temp1.mean(), temp1.std()
out_mask = (temp1 < mean_t - 2 * std_t) | (temp1 > mean_t + 2 * std_t)
print(out_mask.sum())  # 평균±2표준편차 밖 값 개수
plt.hist(temp1, bins=11)
plt.axvline(mean_t - 2 * std_t, color="red", linestyle="--")
plt.axvline(mean_t + 2 * std_t, color="red", linestyle="--")
plt.title("소입로온도1존 분포와 ±2표준편차 경계")
plt.savefig(os.path.join("data", "_tmp_mpl_hist3.png"))
plt.close()


# [개념] plt.scatter()로 산점도 그리기 - 두 숫자 값의 관계를 점으로
# - 점만 찍고 잇지 않음(선 그래프와 차이) - 순서 없이 흩어진 전체 모양을 봄
# - 오른쪽 위로 줄지으면 양의 관계, 오른쪽 아래로 줄지으면 음의 관계, 둥글게 흩어지면 관계 없음
# - alpha로 겹친 점을 반투명 처리하면 밀도까지 함께 드러남

print("\n===================== 실습 5. 산점도로 두 온도존의 관계 확인 =====================")
# 목표: 소입로온도1존·2존의 관계를 산점도로 확인하고 상관계수로 검증
# 단계: ① 두 컬럼의 결측 없는 행만 골라 scatter 그리기 -> ② corr()로 상관계수 계산
# 예상 결과: 거의 -0.01로, 둥글게 흩어진 관계 없음 패턴
both = proc.dropna(subset=["소입로온도1존", "소입로온도2존"])
corr_12 = both["소입로온도1존"].corr(both["소입로온도2존"])
print(round(corr_12, 3))  # -0.007
plt.scatter(both["소입로온도1존"], both["소입로온도2존"], alpha=0.5)
plt.xlabel("소입로온도1존(℃)")
plt.ylabel("소입로온도2존(℃)")
plt.title("온도1존-2존 관계(상관 거의 없음)")
plt.savefig(os.path.join("data", "_tmp_mpl_scatter1.png"))
plt.close()

# [정리] 같은 소입로인데 왜 두 존의 온도가 서로 무관하게 보이는가
# - 1존·2존은 같은 로 안에서도 서로 다른 히터가 독립적으로 온도를 제어하는 별도 구간일
#   가능성이 큼 - 무관하다는 결과 자체가 "두 존이 독립 제어되고 있다"는 실질적인 정보


print("\n===================== 실습 6. 자유롭게 고른 두 값의 관계 분석 =====================")
# 목표: CP값과 OP값의 관계를 스스로 골라 산점도로 분석
# 단계: ① 두 컬럼 결측 제외 -> ② scatter로 관계 확인 -> ③ 기준선(axhline)으로 정상 CP값 표시
# 예상 결과: 뚜렷한 방향 없이 흩어진 모양, CP값 0.45 근처에 기준선 표시
cp_op = proc.dropna(subset=["CP값", "OP값"])
print(round(cp_op["CP값"].corr(cp_op["OP값"]), 3))
plt.scatter(cp_op["OP값"], cp_op["CP값"], alpha=0.5)
plt.axhline(y=0.45, color="red", linestyle="--")
plt.xlabel("OP값")
plt.ylabel("CP값")
plt.title("OP값-CP값 관계와 기준선(CP값 0.45)")
plt.savefig(os.path.join("data", "_tmp_mpl_scatter2.png"))
plt.close()


# [개념] subplot으로 한 화면에 여러 그래프, 그리고 EDA -> 시각화 리포트로 마무리
# - plt.subplot(행, 열, 칸번호)로 격자를 나누고 칸번호는 1부터, 왼쪽 위에서 오른쪽 아래 순서
# - 전체현황(막대) -> 분포(히스토그램) -> 관계(산점도) -> 정리(문장) 순서가 자연스러운 리포트 흐름
# - tight_layout()으로 칸 겹침을 정리하고, savefig는 항상 show보다 먼저

print("\n===================== 실습 7. 결측치 확인과 평균 대체 =====================")
# 목표: 공정 로그의 전체 결측 개수를 확인하고 평균으로 채운 뒤 검증
# 단계: ① 전체 결측 개수 세기 -> ② 숫자 컬럼만 평균으로 채우기 -> ③ 처리 후 결측 0 확인
# 예상 결과: 처리 전 결측 25개(120행 8열 중) -> 처리 후 0개
print(proc.isna().sum().sum())  # 25
proc_filled = proc.copy()
num_cols = proc_filled.select_dtypes("number").columns
proc_filled[num_cols] = proc_filled[num_cols].fillna(proc_filled[num_cols].mean())
print(proc_filled.isna().sum().sum())  # 0
# 슬라이드의 SECOM 예시(120행 23열, 결측 98개)와 컬럼 수는 다르지만, 실제 공정 로그도
# 같은 120행 규모에 결측이 섞여 있다는 점과 처리 절차(확인 -> fillna(평균) -> 재검증)는 동일


print("\n===================== 실습 8. 시각화 리포트 완성과 저장 =====================")
# 목표: 전체현황(막대)·분포(히스토그램)·관계(산점도)·결과(막대)를 2x2 한 화면에 모아 저장
# 단계: ① figure+subplot으로 2x2 격자 만들기 -> ② 네 칸에 각 그래프 배치 -> ③ savefig(show보다 먼저)
# 예상 결과: 라인별 개수·온도분포·온도1존2존관계·result개수를 담은 2x2 리포트 파일 저장
fig = plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
line_count = proc["라인"].value_counts()
plt.bar(line_count.index, line_count.values)
plt.title("라인별 개수")

plt.subplot(2, 2, 2)
plt.hist(temp1, bins=11)
plt.title("소입로온도1존 분포")

plt.subplot(2, 2, 3)
plt.scatter(both["소입로온도1존"], both["소입로온도2존"], alpha=0.5)
plt.title("온도1존-2존 관계")

plt.subplot(2, 2, 4)
plt.bar(result_count.index, result_count.values, color=["blue", "red"])
plt.title("result 개수")

plt.suptitle("열처리 공정 시각화 리포트")
plt.tight_layout()
report_path = os.path.join("data", "_tmp_mpl_report.png")
plt.savefig(report_path, dpi=100)
plt.close()
print(os.path.exists(report_path))  # True
os.remove(report_path)

# [정리] 사실 -> 의미 -> 행동, 그래프만으론 반쪽 리포트
# - 사실: 주간 라인 평균 온도(859.47)가 야간(858.89)보다 근소하게 높고, result는 정상 109·이상 11
# - 의미: 두 라인의 온도 차이는 매우 작아 실질적인 원인으로 보기 어려움 - 다른 변수 추가 확인 필요
# - 행동: 이상(11건)이 몰린 시점의 CP값·세정기 값을 별도로 점검해 원인 후보를 좁히는 것을 제안
# - "온도가 다르니 그게 원인이다"처럼 단정하지 않고, 그래프가 실제로 보여준 것만 사실로 적기

for _f in os.listdir("data"):
    if _f.startswith("_tmp_mpl_"):
        os.remove(os.path.join("data", _f))
