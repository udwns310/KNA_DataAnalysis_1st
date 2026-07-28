# =====================================================================
# 텍스트 정리 실무 사례 모음 (이메일 / 전화번호 / 이름 / 목록 / 컬럼명 / 라벨)
# =====================================================================

# [정리] 텍스트 정리 도구 모으기 - 네 묶음으로 정리
# 목적          | 도구
# --------------|------------------------------------------------
# 만들기·출력  | 따옴표, print, f-string, 형변환(str, int, float)
# 꺼내기       | 인덱싱, 슬라이싱, split
# 확인·다듬기  | len, in, count, find / strip, lower, replace, join

# [정리] 텍스트 정리 순서 (5단계 흐름) - 필요한 단계만 골라 쓰면 됨
# 공백 제거(strip) -> 통일·치환(lower, replace) -> 나누기(split)
#   -> 조각 정리(strip) -> 합치기(join) -> 출력


print("===================== 이메일 정리 사례 =====================")
# 이메일은 공백 제거 후 소문자 통일이 기본
# strip으로 앞뒤 공백, lower로 소문자
raw_email = " Hong@Company.com "
clean_email = raw_email.strip().lower()
print(clean_email)  # hong@company.com

# 아이디는 find로 @ 위치를 찾아 슬라이싱
at_pos = clean_email.find("@")
user_id = clean_email[:at_pos]
domain = clean_email[at_pos + 1:]
print(f"아이디: {user_id}, 도메인: {domain}")  # 아이디: hong, 도메인: company.com


print("\n===================== 전화번호 정리 사례 =====================")
# 전화번호는 하이픈·공백을 replace로 제거해 숫자만 남김
# replace 체이닝으로 어떤 형태든 통일
raw_phone1 = "010-1234-5678"
raw_phone2 = "010 1234 5678"
digits1 = raw_phone1.replace("-", "").replace(" ", "")
digits2 = raw_phone2.replace("-", "").replace(" ", "")
print(digits1, digits2)  # 01012345678 01012345678

# len으로 11자리인지 점검
print(len(digits1) == 11)  # True

# 다시 형식을 넣을 땐 슬라이싱 + f-string
formatted = f"{digits1[:3]}-{digits1[3:7]}-{digits1[7:]}"
print(formatted)  # 010-1234-5678


print("\n===================== 이름 정리 사례 =====================")
# 이름은 공백 제거 후 title()로 형식 통일
raw_name = " hong gil dong "
clean_name = raw_name.strip().title()
print(clean_name)  # Hong Gil Dong

# 공백이 들쭉날쭉하면 split 후 한 칸으로 join
messy_name = "  hong   gil    dong "
fixed_name = " ".join(messy_name.split()).title()
print(fixed_name)  # Hong Gil Dong


print("\n===================== 쉼표 구분 목록 정리 사례 =====================")
# 쉼표 목록은 split -> 각 항목 strip -> join
raw_list = "사과, 배 , 감"
items = [item.strip() for item in raw_list.split(",")]  # 각 항목 공백 제거
print(items)  # ['사과', '배', '감']
print(", ".join(items))  # 사과, 배, 감


print("\n===================== 컬럼명 정리 사례 - 데이터 분석 연결 =====================")
# 컬럼명은 공백 제거·소문자·기호 정리로 다듬기
raw_col = " Sensor Measurement 3 "
clean_col = raw_col.strip().lower().replace(" ", "_")
print(clean_col)  # sensor_measurement_3


print("\n===================== 범주형 라벨 통일 사례 =====================")
# 정해진 몇 종류로 나뉘는 라벨은 표기 통일이 핵심
# 'NORMAL' 'Normal' 'normal' 이 같은 상태가 되도록 strip·lower로 통일
labels = ["NORMAL", "Normal", " normal ", "WARNING"]
clean_labels = [label.strip().lower() for label in labels]
print(clean_labels)  # ['normal', 'normal', 'normal', 'warning']
# 통일하지 않으면 같은 상태가 서로 다른 값으로 따로 집계됨


print("\n===================== 여러 항목 한 줄 요약 출력 =====================")
# 정리한 값들을 f-string 한 줄로 모아 요약
code = "EQP-001"
status = "normal"
value = 25.34567
print(f"[{code}] 상태: {status} / 측정값: {value:.1f}")


# =====================================================================
# [추가 학습] 더 복잡한 패턴은 정규표현식(re 모듈)으로
# =====================================================================
# - strip/replace/split 조합만으로 해결하기 어려운 복잡한 패턴
#   (예: 전화번호 형식이 뒤죽박죽 섞여 있는 경우, 숫자만 뽑아내기 등)
#   은 정규표현식(re 모듈)을 사용하면 훨씬 간결해짐
# - 지금 단계에서는 strip/lower/replace/split/join 조합으로 충분하지만
#   나중에 "패턴이 너무 다양해서 하나하나 처리하기 힘들다"는 느낌이 들 때
#   정규표현식을 학습하면 됨 (추후 학습 예정)
import re
phone_mixed = "010.1234.5678"
digits_only = re.sub(r"\D", "", phone_mixed)  # 숫자가 아닌 문자를 전부 제거
print(digits_only)  # 01012345678
