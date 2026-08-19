# 실습 2
import pandas as pd
import os

hydraulic_qc_path = os.path.join("data", "14_hydraulic_qc.csv")
qc = pd.read_csv(hydraulic_qc_path)
qc_counts = qc["검사결과"].value_counts()
qc_ratio = qc["검사결과"].value_counts(normalize=True).round(3)
print(qc_counts)
print(qc_ratio)