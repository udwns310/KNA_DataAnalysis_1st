# 실습 2
import numpy as np

mct_table = np.array(
    [
        [1200, 45.2],
        [1250, 44.8],
        [980, 52.3],
    ]
)  # 열: [회전수, 토크], 행: 설비별
print(mct_table[1])  # [1250.   44.8] - 특정 설비(1번) 행 전체
print(mct_table[:, 0])  # [1200. 1250.  980.] - 회전수 열 전체
print(mct_table[:, 1])  # [45.2 44.8 52.3] - 토크 열 전체
