import numpy as np
import os
# 실습 7
file_path = os.path.join("data", "10_mct_tool.csv")

# np.loadtxt로 회전수 배열을 파일에서 불러오기
rpm = np.loadtxt(file_path, encoding='utf-8', delimiter=",", skiprows=1, usecols=4)
rpm_avg = np.mean(rpm)
rpm_std = np.std(rpm)
rpm_min = np.min(rpm)
rpm_max = np.max(rpm)

print(f"값의 범위 확인 : {rpm_max - rpm_min:.2f}")

print(f"회전수 평균: {rpm_avg:.2f}, 표준편차: {rpm_std:.2f}, 최소값: {rpm_min:.2f}, 최대값: {rpm_max:.2f}")
