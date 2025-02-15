from logger import logger
from config import load_config
import pandas as pd

logger.debug("Loading game configuration")
config = load_config()
logger.debug(f"Configuration loaded: {config}")


def read_game_data_from_file():
    logger.debug("Reading game data")
    data_file = config["game_file"]
    try:
        return pd.read_csv(data_file, encoding="windows-1252", sep=";")
    except FileNotFoundError:
        logger.error(f"Data file not found at {data_file}")
        return None
