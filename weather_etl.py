import os
import time
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from custom_logger import get_pipeline_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_pipeline_logger()
DB_URL = os.getenv("DB_URL")

# Define a list of dictionaries for all the cities you want to track
CITIES = [
    {"name": "London", "country": "UK", "lat": 51.5085, "lon": -0.1257},
    {"name": "New York", "country": "USA", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tokyo", "country": "Japan", "lat": 35.6895, "lon": 139.6917},
    {"name": "Sydney", "country": "Australia", "lat": -33.8688, "lon": 151.2093},
    {"name": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522}
]

logger.info("=== Starting Batch ETL Pipeline Execution ===")

try:
    # ---------------------------------------------------------
    # EXTRACT
    # ---------------------------------------------------------
    all_weather_records = []  # Empty list to hold data for all cities
    url = "https://api.open-meteo.com/v1/forecast"
    
    for city in CITIES:
        params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            "current_weather": True
        }
        
        logger.info(f"Fetching data for {city['name']}...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  
        raw_data = response.json()
        
        # Create a dictionary for this specific city
        weather_record = {
            "city": city["name"],
            "country": city["country"],
            "latitude": raw_data["latitude"],
            "longitude": raw_data["longitude"],
            "temperature_c": raw_data["current_weather"]["temperature"],
            "wind_speed_kmh": raw_data["current_weather"]["windspeed"],
            "observation_time": raw_data["current_weather"]["time"],
            "etl_processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add this city's dictionary to our master list
        all_weather_records.append(weather_record)
        
        # Rate Limiting: Pause for 1 second before asking the API for the next city
        time.sleep(1)

    logger.info("Extraction successful: Downloaded data for all cities.")

    # ---------------------------------------------------------
    # TRANSFORM
    # ---------------------------------------------------------
    # Pandas is smart enough to convert a list of dictionaries into a multi-row table
    df = pd.DataFrame(all_weather_records)
    logger.info(f"Transformation successful: Created DataFrame with {len(df)} rows.")

    # ---------------------------------------------------------
    # LOAD
    # ---------------------------------------------------------
    logger.info("Connecting to the cloud database...")
    
    # NEW: Create a SQLAlchemy engine instead of sqlite3
    engine = create_engine(DB_URL)
    
    # Batch load all 5 rows at once to PostgreSQL
    df.to_sql(
        name="daily_weather", 
        con=engine, 
        if_exists="append",
        index=False 
    )
    
    logger.info("Load successful: Saved batch to Cloud PostgreSQL.")

except Exception as e:
    logger.exception("CRITICAL: Pipeline failed during execution!")

finally:
    logger.info("=== Pipeline Execution Finished ===\n")