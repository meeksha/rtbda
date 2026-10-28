import pandas as pd

stream = pd.read_csv("iot_sensor_data.csv").tail(20)

stream["SHEI"] = 0.4*stream["air_quality_index"] + 0.3*stream["temperature_c"] + 0.2*stream["humidity_percent"] - 0.1*stream["battery_level"]

alerts = stream[stream["SHEI"] > 42]

print("Environmental Risk Alerts")
print(alerts[["sensor_id","location","SHEI"]])