# Real-Time Big Data Analytics for IoT Environmental Monitoring

A Lambda Architecture-based environmental monitoring system that processes IoT sensor data through batch and speed layers, computes a Sensor/Smart Health Environmental Index (SHEI), and identifies locations with elevated environmental stress.

## Overview

Internet of Things (IoT) devices continuously generate environmental measurements such as temperature, humidity, air quality, and device battery levels. Processing these measurements efficiently can help identify potentially concerning environmental conditions across multiple locations.

This project demonstrates a simplified **Lambda Architecture** for processing IoT sensor data. It combines batch processing for aggregated historical analysis with speed-layer processing for recent sensor readings. A serving layer filters locations with elevated SHEI values, while a Streamlit dashboard visualizes environmental measurements.

The project uses Python and Pandas for data processing and Streamlit for visualization.

## Objectives

- Explore the Lambda Architecture pattern for IoT data processing.
- Process environmental sensor readings using batch and speed layers.
- Compute an SHEI score from environmental and device measurements.
- Aggregate sensor readings by location.
- Identify locations that exceed configurable SHEI thresholds.
- Visualize temperature and air quality measurements through a dashboard.

## Architecture

The implementation separates processing into four components.

```text
           IoT Sensor Dataset
                    |
          +---------+---------+
          |                   |
          v                   v
     Batch Layer          Speed Layer
   Full Dataset          Recent 20 Rows
          |                   |
          v                   v
   Location-Level       SHEI Calculation
    Aggregation         and Risk Alerts
          |
          v
    batch_output.csv
          |
          v
     Serving Layer
          |
          v
  High-Risk Locations

   Streamlit Dashboard
          |
          v
  Temperature and Air
     Quality Charts
```

*This diagram represents the current scripts. The dashboard reads the sensor CSV directly, and the speed layer and serving layer are standalone scripts rather than a continuously connected streaming service.*

## Key Features

### 1. Batch Processing

The batch layer reads the complete `iot_sensor_data.csv` dataset and calculates the SHEI score for each record.

It then groups the data by location and computes mean values for:

- Temperature
- Humidity
- Air Quality Index
- SHEI

The aggregated output is written to `batch_output.csv`.

### 2. Speed-Layer Processing

The speed layer reads the most recent 20 rows of the dataset and calculates SHEI for those records.

It identifies environmental risk alerts using an SHEI threshold greater than 42 and displays the corresponding sensor IDs, locations, and scores.

### 3. Serving Layer

The serving layer loads the batch output and filters locations with an aggregated SHEI score greater than 39.

It prints the locations classified as having high environmental stress based on this threshold.

### 4. Interactive Dashboard

The Streamlit dashboard provides two basic visualizations:

- A line chart of temperature measurements.
- A bar chart of Air Quality Index measurements.

The dashboard reads the source CSV directly.

## SHEI Calculation

The project calculates SHEI using the following weighted expression:

\[
\begin{aligned}
\mathrm{SHEI} ={}& 0.4A + 0.3T \\
&+ 0.2H - 0.1B
\end{aligned}
\]

Where:

- \(A\) = Air Quality Index (`air_quality_index`)
- \(T\) = Temperature in Celsius (`temperature_c`)
- \(H\) = Relative humidity percentage (`humidity_percent`)
- \(B\) = Device battery level (`battery_level`)

The current implementation uses this same expression in both the batch and speed layers.

**Important:** This is a project-specific weighted score, not a validated environmental or public-health index. Its thresholds and interpretation should be validated before using it for real-world environmental risk assessment.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| Pandas | Data loading, transformation, aggregation, and filtering |
| Streamlit | Interactive dashboard |
| CSV | Input sensor dataset and batch output |
| Lambda Architecture | Conceptual separation of batch and speed processing |

## Dataset

The repository includes `iot_sensor_data.csv`, containing 500 data rows and the following columns:

| Column | Description |
|---|---|
| `sensor_id` | Sensor identifier |
| `device_id` | Device identifier |
| `location` | Sensor location |
| `timestamp` | Measurement timestamp |
| `temperature_c` | Temperature in Celsius |
| `humidity_percent` | Humidity percentage |
| `pressure_hpa` | Atmospheric pressure in hectopascals |
| `air_quality_index` | Air quality measurement |
| `battery_level` | Sensor battery measurement |
| `status` | Sensor status |

The current SHEI formula uses temperature, humidity, air quality, and battery level. Atmospheric pressure and sensor status are present in the dataset but are not used in the formula.

## Project Structure

```text
rtbda/
├── .gitignore
├── batch_layer.py
├── batch_output.csv
├── dashboard.py
├── iot_sensor_data.csv
├── serving_layer.py
└── speed_layer.py
```

| File | Responsibility |
|---|---|
| `batch_layer.py` | Calculates SHEI and generates location-level aggregates |
| `speed_layer.py` | Processes the latest 20 rows and prints risk alerts |
| `serving_layer.py` | Filters aggregated locations using the SHEI threshold |
| `dashboard.py` | Visualizes temperature and air quality |
| `iot_sensor_data.csv` | Source IoT dataset |
| `batch_output.csv` | Generated batch-processing results |

## Getting Started

### Prerequisites

- Python 3.9 or later
- pip
- Git

### 1. Clone the repository

```bash
git clone https://github.com/meeksha/rtbda.git
cd rtbda
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install pandas streamlit
```

### 4. Run the batch layer

```bash
python batch_layer.py
```

This reads the sensor dataset, calculates SHEI, aggregates measurements by location, and creates or overwrites `batch_output.csv`.

### 5. Run the speed layer

```bash
python speed_layer.py
```

This processes the latest 20 rows and prints records whose SHEI score exceeds 42.

### 6. Run the serving layer

Run the batch layer first, then execute:

```bash
python serving_layer.py
```

This reads `batch_output.csv` and prints locations whose aggregated SHEI exceeds 39.

### 7. Launch the dashboard

```bash
streamlit run dashboard.py
```

Streamlit will provide a local URL, typically `http://localhost:8501`.

## Current Thresholds

| Component | Condition | Purpose |
|---|---|---|
| Speed layer | `SHEI > 42` | Flags recent sensor records |
| Serving layer | `SHEI > 39` | Filters aggregated location-level results |

These thresholds are hardcoded in the current scripts. They are demonstration parameters, not clinically or scientifically validated risk boundaries.

## Limitations

- The speed layer processes the latest 20 rows of a static CSV file rather than consuming a live IoT stream.
- Batch and speed processing are executed manually as separate scripts.
- The dashboard does not currently consume the batch output or speed-layer alerts.
- The SHEI formula combines measurements with different units without normalization.
- No predictive machine learning model or automated alert delivery is implemented in the current scripts.
- No automated tests or formal validation of the SHEI thresholds are included.

## Future Enhancements

- Integrate live sensor ingestion using MQTT, Kafka, or another streaming platform.
- Schedule and automate batch and speed processing.
- Connect the dashboard to batch aggregates and real-time alerts.
- Normalize sensor measurements before computing a composite score.
- Validate SHEI weights and thresholds against domain-specific reference data.
- Add time-series trend analysis and historical comparisons.
- Introduce missing-value handling, data validation, and automated tests.
- Store historical measurements and aggregated results in a suitable database.

## Learning Outcomes

This project demonstrates:

- Practical implementation of batch and speed processing patterns.
- Data manipulation and aggregation using Pandas.
- Processing of environmental IoT sensor measurements.
- Threshold-based detection of potentially concerning readings.
- Dashboard creation using Streamlit.
- Separation of data processing and visualization into modular scripts.

