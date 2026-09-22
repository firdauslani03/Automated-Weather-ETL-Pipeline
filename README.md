# Automated Weather ETL Pipeline & Dashboard 🌦️

## Objective
An end-to-end Data Engineering pipeline that extracts daily weather data for multiple global cities, transforms it into a structured format, loads it into a local SQLite database, and visualizes the results in an interactive web dashboard.

This project demonstrates core ETL concepts, batch processing, automated scheduling, robust error logging, and data visualization.

## Architecture & Data Flow
1. **Extract:** Fetches real-time weather data (temperature, wind speed) for 5 major cities via the [Open-Meteo API](https://open-meteo.com/). Implements rate-limiting to respect API constraints.
2. **Transform:** Uses `pandas` to flatten nested JSON data, filter required fields, and inject critical ETL metadata (processing timestamps).
3. **Load:** Appends the cleaned, batched data into a local `SQLite` database without duplicating historical records.
4. **Automate:** Scheduled via Windows Task Scheduler to run silently in the background every day.
5. **Consume:** An interactive `Streamlit` web application reads directly from the SQLite database to display temperature trends and raw data using `plotly`.

## Tech Stack
* **Language:** Python 3
* **Data Processing:** `pandas`, `requests`
* **Database:** SQLite (`sqlite3`)
* **Visualization:** `streamlit`, `plotly`
* **Orchestration:** Windows Task Scheduler

## Data Engineering Skills Demonstrated
* **Batch Processing & Rate Limiting:** Looping through multiple API endpoints efficiently while using `time.sleep()` to prevent server bans.
* **Data Transformation:** Structuring raw, nested API responses into tabular formats suitable for a relational database.
* **Metadata Tracking:** Adding `etl_processed_at` timestamps to track when rows were ingested, a standard industry practice for auditing.
* **Robust Error Handling:** Utilizing `raise_for_status()` for API failures and a custom logging module (`custom_logger.py`) to track execution history and capture stack traces in a local `.log` file.
* **Data Visualization:** Building an interactive, front-end dashboard to make the raw database accessible to business users.

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/Automated-Weather-ETL-Pipeline.git](https://github.com/YourUsername/Automated-Weather-ETL-Pipeline.git)