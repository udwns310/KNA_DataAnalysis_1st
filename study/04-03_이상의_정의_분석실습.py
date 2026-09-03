"""
04-03 이상의 정의와 판정 기준 - 데이터 분석 실습 1
진동 데이터의 이상 감시 기준 설계

실행 방법:
1) 이 파일을 04-03_이상의_정의_진동데이터.csv 와 같은 폴더에 두고 실행
2) 필요 라이브러리: pandas, matplotlib
   (없다면: pip install pandas matplotlib)

산출물:
- 그래프1_시간에따른진동변화.png
- 그래프2_부하율과진동RMS관계.png
- 콘솔에 [4] 정상 기준 통계값 출력
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# 한글 폰트 설정 (그래프에 한글이 깨지지 않도록)
mpl.rcParams["font.family"] = "Malgun Gothic"
mpl.rcParams["axes.unicode_minus"] = False

CSV_PATH = "data/04-03_이상의_정의_진동데이터.csv"

# ── 데이터 불러오기 ───────────────────────────────────────
df = pd.read_csv(CSV_PATH)
print("전체 행 수:", len(df))
print(df.head())
print(df["가동여부"].value_counts())


# ════════════════════════════════════════════════════════
# [2] 그래프 1 — 시간에 따른 진동 변화
#     조건: 가동여부 == 1 만 사용, x=일자, y=진동RMS, 선 그래프
#          4.5 mm/s 위치에 수평 임계선
# ════════════════════════════════════════════════════════
running = df[df["가동여부"] == 1]

plt.figure(figsize=(10, 5))
plt.plot(running["일자"], running["진동RMS"], marker="o", markersize=3,
         linewidth=1, color="#2E5EAA", label="진동RMS")
plt.axhline(y=4.5, color="red", linestyle="--", linewidth=1.5,
            label="고정 임계치 4.5 mm/s")
plt.xlabel("일자")
plt.ylabel("진동RMS (mm/s)")
plt.title("시간에 따른 진동RMS 변화 (가동 중 데이터만)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("그래프1_시간에따른진동변화.png", dpi=150)
plt.close()
print("\n[그래프1] 저장 완료 -> 그래프1_시간에따른진동변화.png")


# ════════════════════════════════════════════════════════
# [3] 그래프 2 — 부하율과 진동RMS의 관계
#     조건: 80일 미만의 가동 데이터만 사용, 선 그래프
#          (부하율 순으로 정렬 후 연결)
# ════════════════════════════════════════════════════════
subset = df[(df["가동여부"] == 1) & (df["일자"] < 80)].sort_values("부하율")

plt.figure(figsize=(6, 6))
plt.plot(subset["부하율"], subset["진동RMS"], marker="o", markersize=3,
         linewidth=1, color="#2E5EAA")
plt.xlabel("부하율 (%)")
plt.ylabel("진동RMS (mm/s)")
plt.title("부하율과 진동RMS의 관계 (80일 미만, 가동 중)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("그래프2_부하율과진동RMS관계.png", dpi=150)
plt.close()
print("[그래프2] 저장 완료 -> 그래프2_부하율과진동RMS관계.png")


# ════════════════════════════════════════════════════════
# [4] 정상 기준 숫자로 확인하기
#     조건: 가동여부 == 1, 일자 < 80
# ════════════════════════════════════════════════════════
normal = df[(df["가동여부"] == 1) & (df["일자"] < 80)]

count = len(normal)
mean = normal["진동RMS"].mean()
std = normal["진동RMS"].std()
stat_threshold = mean + 3 * std

print("\n[4] 정상 기준 통계")
print(f"정상 후보 데이터 수 : {count} 행")
print(f"진동RMS 평균        : {mean:.3f} mm/s")
print(f"진동RMS 표준편차    : {std:.3f}")
print(f"통계 임계치(평균+3*표준편차) : {stat_threshold:.3f} mm/s")

# 참고: 고정 임계치(4.5)와 통계 임계치를 정상 구간에 적용했을 때
# 오탐(정상인데 임계치를 넘는 경우) 비교
fixed_false = normal[normal["진동RMS"] >= 4.5]
stat_false = normal[normal["진동RMS"] >= stat_threshold]
print("\n[참고] 정상 구간(가동==1, 일자<80) 내 임계치 초과 사례")
print("고정 임계치(4.5) 초과 행:")
print(fixed_false[["일자", "진동RMS", "부하율"]])
print("통계 임계치 초과 행:")
print(stat_false[["일자", "진동RMS", "부하율"]] if len(stat_false) else "(없음)")
