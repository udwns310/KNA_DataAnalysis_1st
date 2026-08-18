# 실습 1
import pandas as pd
import os 

equipment_path = os.path.join("data", "14_equipment_sensor.csv")
eqsensor = pd.read_csv(equipment_path)
print(eqsensor.shape)  # (120, 7)
print(eqsensor.head())

print(eqsensor["machine"].value_counts())  # M04 42, M01 29, M02 25, M03 24
print(eqsensor["shift"].value_counts())  # 야간 61, 주간 59