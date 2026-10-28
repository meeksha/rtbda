import pandas as pd

df = pd.read_csv("iot_sensor_data.csv")

df["SHEI"] = 0.4*df["air_quality_index"] + 0.3*df["temperature_c"] + 0.2*df["humidity_percent"] - 0.1*df["battery_level"]

batch = df.groupby("location")[["temperature_c","humidity_percent","air_quality_index","SHEI"]].mean()

batch.to_csv("batch_output.csv")

print(batch)