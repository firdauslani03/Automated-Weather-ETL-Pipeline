import os
import requests
import sqlite3
import pandas as pd
from datetime import datetime
from custom_logger import get_pipeline_logger

logger = get_pipeline_logger()
DB_FILE = r"C:\Users\firdaus\Documents\Automated-Weather-ETL-Pipeline\weather_data.db"

logger.info("=== Starting ETL Pipeline Execution ===")

try:
    # ---------------------------------------------------------
    # EXTRACT
    # ---------------------------------------------------------
    # Define your location metadata here so it is easy to change later
    CITY_NAME = "London"
    COUNTRY = "UK"
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 51.5085,
        "longitude": -0.1257,
        "current_weather": True
    }
    
    logger.info(f"Fetching data for {CITY_NAME}...")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()  
    raw_data = response.json()
    
    logger.info("Extraction successful: API returned 200 OK.")

    # ---------------------------------------------------------
    # TRANSFORM
    # ---------------------------------------------------------
    weather_record = {
        # Inject the new city columns right at the top
        "city": CITY_NAME,
        "country": COUNTRY,
        
        "latitude": raw_data["latitude"],
        "longitude": raw_data["longitude"],
        "temperature_c": raw_data["current_weather"]["temperature"],
        "wind_speed_kmh": raw_data["current_weather"]["windspeed"],
        "observation_time": raw_data["current_weather"]["time"],
        "etl_processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    df = pd.DataFrame([weather_record])
    logger.info(f"Transformation successful: Added {CITY_NAME} to record.")

    # ---------------------------------------------------------
    # LOAD
    # ---------------------------------------------------------
    logger.info("Connecting to the database...")
    conn = sqlite3.connect(DB_FILE)
    
    df.to_sql(
        name="daily_weather", 
        con=conn, 
        if_exists="append",
        index=False 
    )
    
    conn.close()
    logger.info("Load successful: Saved 1 record to SQLite.")

except Exception as e:
    logger.exception("CRITICAL: Pipeline failed during execution!")

finally:
    logger.info("=== Pipeline Execution Finished ===\n")