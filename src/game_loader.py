from logger import logger
from config import load_config
import pandas as pd

def read_game_data(path):
    logger.debug("Reading game data")
    try:
        return pd.read_csv(path, encoding="windows-1252", sep=";")
    except FileNotFoundError:
        logger.error(f"Data file not found at {path}")
        return pd.DataFrame()
