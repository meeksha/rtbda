import pandas as pd

batch = pd.read_csv("batch_output.csv")

risk = batch[batch["SHEI"] > 39]

print("High Environmental Stress Locations")
print(risk)