import logging
import os
import sys  # Required for terminal output

def get_pipeline_logger():
    # 1. Define paths
    BASE_DIR = r"C:\Users\firdaus\Documents\Automated-Weather-ETL-Pipeline"
    LOG_FILE = os.path.join(BASE_DIR, "pipeline.log")

    # 2. Create a custom logger object
    logger = logging.getLogger("WeatherETL")
    logger.setLevel(logging.INFO)

    # 3. Prevent duplicate log entries
    if not logger.handlers:
        # Create the formatter we want to use for both handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", 
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Handler 1: Writes to pipeline.log
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler 2: Prints to the VS Code Terminal
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger