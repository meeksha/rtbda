import streamlit as st
import pandas as pd

df = pd.read_csv("iot_sensor_data.csv")

st.title("IoT Environmental Monitoring Dashboard")

st.line_chart(df["temperature_c"])

st.bar_chart(df["air_quality_index"])