# Automated Weather ETL Pipeline 🌦️

## Objective
A lightweight, automated Data Engineering pipeline that extracts daily weather data from a public API, transforms it into a structured format, and loads it into a local SQLite database for historical analysis. 

This project demonstrates core ETL concepts, automated scheduling, and robust error logging.

## Architecture & Data Flow
1. **Extract:** Fetches real-time weather data (temperature, wind speed) for London via the [Open-Meteo API](https://open-meteo.com/).
2. **Transform:** Uses `pandas` to flatten nested JSON data, filter required fields, and inject critical ETL metadata (processing timestamps).
3. **Load:** Appends the cleaned data into a local `SQLite` database without duplicating historical records.
4. **Automate:** Scheduled via Windows Task Scheduler to run silently in the background every day at 8:00 AM.

## Tech Stack
* **Language:** Python 3
* **Libraries:** `pandas`, `requests`, `sqlite3`, `logging`
* **Database:** SQLite
* **Orchestration:** Windows Task Scheduler

## Data Engineering Skills Demonstrated
* **API Integration:** Handling HTTP requests, parameters, and JSON parsing.
* **Data Transformation:** Structuring raw API responses into tabular formats suitable for a relational database.
* **Metadata Tracking:** Adding `etl_processed_at` timestamps to track when rows were ingested, a standard industry practice for auditing.
* **Robust Error Handling:** Utilizing `raise_for_status()` for API failures and a custom logging module to track execution history and capture stack traces without stopping the pipeline silently.
* **Separation of Concerns:** Decoupling the logging configuration (`custom_logger.py`) from the main execution script (`test.py`).

## How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/YourUsername/Automated-Weather-ETL-Pipeline.git](https://github.com/YourUsername/Automated-Weather-ETL-Pipeline.git)