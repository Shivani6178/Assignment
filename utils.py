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
# import os
# import json
# import logging
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure logging
# def configure_logging():
#     log_dir = "logs"
#     log_file = os.path.join(log_dir, "app.log")

#     # Ensure the logs directory exists
#     os.makedirs(log_dir, exist_ok=True)

#     # Configure logging
#     logging.basicConfig(
#         filename=log_file,
#         level=logging.INFO,
#         format="%(asctime)s - %(levelname)s - %(message)s"
#     )

# # Load brand guidelines from the config.json file
# def load_config():
#     config_path = os.path.join(os.path.dirname(__file__), "../config.json")
#     with open(config_path, "r") as f:
#         return json.load(f)

# Function to get API keys from environment
def get_api_key(key_name):
    return os.getenv(key_name)
