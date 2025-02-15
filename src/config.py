import yaml
from logger import logger

def load_config(filepath="config.yaml"):
    logger.debug(f'Loading configuration from {filepath}')
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)  # Use safe_load to prevent arbitrary code execution
    except FileNotFoundError:
        logger.error(f'Configuration file not found at {filepath}')
        return None
