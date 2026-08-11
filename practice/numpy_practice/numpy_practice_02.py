import numpy as np

# 0부터 30까지 6간격으로 배열 채워만들기
# 0부터 숫자 6씩 증가시켜가면서 30보다 작은 값들일 때 배열에 붙여나감
gab_six = np.arange(0, 30, 6)
print(gab_six)  # [ 0  6 12 18 24]

# 0부터 30까지 6등분 나누어 배열 내용 채우기
div_six = np.linspace(0, 30, 6)
print(div_six)  # [ 0.  6. 12. 18. 24. 30.]