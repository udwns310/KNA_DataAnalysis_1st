# 실습 3
import pandas as pd
import os

equipment_path = os.path.join("data", "14_equipment_sensor.csv")
eqsensor = pd.read_csv(equipment_path)
print(eqsensor["vibration"].min(), eqsensor["vibration"].max())  # 0.45 5.63

vib_band = pd.cut(eqsensor["vibration"], bins=[0, 2, 3.5, 10], labels=["약함", "보통", "강함"])
print(vib_band.value_counts())  # 약함 15, 보통 64, 강함 41