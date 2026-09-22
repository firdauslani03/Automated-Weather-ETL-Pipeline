import logging
import os

def get_pipeline_logger():
    # 1. Define paths
    BASE_DIR = r"C:\Users\firdaus\Documents\Automated-Weather-ETL-Pipeline"
    LOG_FILE = os.path.join(BASE_DIR, "pipeline.log")

    # 2. Create a custom logger object
    logger = logging.getLogger("WeatherETL")
    logger.setLevel(logging.INFO)

    # 3. Prevent duplicate log entries if the function is called multiple times
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", 
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger