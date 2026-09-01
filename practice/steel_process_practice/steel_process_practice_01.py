# 실습1 - 설비 태그에서 공정 위치 추론
# 목표: 24개 설비 태그를 읽어 공정과 상하공정 구분을 판정한 표 작성
import pandas as pd

# STEP 1. 파일 구조 확인
df = pd.read_csv("data/01-01_철강_공정_개관_설비태그.csv")
# print(df.shape)         # 확인용 - 필요하면 주석 해제
# print(df.head())

# STEP 2. 태그 분해 - tag 컬럼을 하이픈 기준으로 다섯 컬럼 생성
parts = df["tag"].str.split("-", expand=True)
parts.columns = ["plant", "proc", "equip", "no", "meas"]
df = pd.concat([df, parts], axis=1)
# print(df.head())

# STEP 3. 공정명 매핑 - 공정 코드를 한글 이름으로 변환
proc_name = {
    "SNT": "소결",
    "CKO": "코크스로",
    "BF": "고로",
    "BOF": "전로",
    "CCM": "연주",
    "HSM": "열간압연",
    "CRM": "냉간압연",
    "UTL": "유틸리티",
}
df["proc_name"] = df["proc"].map(proc_name)

# STEP 4. 상하공정 분류 - stage 컬럼에 상공정 · 하공정 · 유틸리티 구분
# 경계는 연주(CCM) - 액체(용강)를 다뤄 온 흐름이 연주에서 굳은 반제품으로 넘어가므로
# 연주까지는 상공정, 그 뒤 압연(HSM·CRM)부터 하공정으로 분류함
upstream = {"SNT", "CKO", "BF", "BOF", "CCM"}
downstream = {"HSM", "CRM"}


def classify_stage(proc):
    if proc in upstream:
        return "상공정"
    if proc in downstream:
        return "하공정"
    return "유틸리티"


df["stage"] = df["proc"].apply(classify_stage)

# 체크포인트 (필요하면 주석 해제해서 검증)
# ① 분해 확인 - 다섯 마디로 나눈 결과에 빈 값이나 어긋난 행이 없는지
# print(parts.isna().sum().sum())
# ② 예외 처리 - 딕셔너리에 없는 코드가 미등록으로 표시되는지 (map은 없는 키를 NaN으로 반환)
# print(df["proc_name"].isna().sum())
# ③ 분류 확인 - UTL 태그가 상하공정 어디에도 들어가지 않았는지
# print(df.loc[df["proc"] == "UTL", "stage"].unique())

# 결과 - 설비 태그별 공정/상하공정 판정표
result = df[["tag", "proc_name", "stage"]].reset_index(drop=True)
print(result.to_string(index=False))

# STEP 5. 상공정 · 하공정 · 유틸리티 개수
stage_count = df.groupby("stage").size()
print(stage_count)

# STEP 6. 공정별 태그개수 + 가장 많이 등장하는 공정
proc_count = df.groupby("proc_name").size().sort_values(ascending=False)
print(proc_count)
print("가장 많이 등장하는 공정:", proc_count.idxmax())

# STEP 7. 계측항목별 태그개수 + 가장 많이 등장하는 물리량
meas_count = df.groupby("meas").size().sort_values(ascending=False)
print(meas_count)
print("가장 많이 등장하는 계측항목:", meas_count.idxmax())
