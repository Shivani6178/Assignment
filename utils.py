import logging
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load configuration
def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

# Logging setup
def setup_logging(log_file="logs/app.log", level=logging.INFO):
    logging.basicConfig(
        filename=log_file,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=level
    )
    return logging.getLogger("app")

config = load_config()
logger = setup_logging(level=config.get("logging_level", logging.INFO))

# Function to get API keys from environment
def get_api_key(key_name):
    return os.getenv(key_name)
