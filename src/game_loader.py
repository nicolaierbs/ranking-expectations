from logger import logger
from config import load_config

logger.debug("Loading game configuration")
config = load_config()
logger.info(f"Game configuration loaded: {config}")
