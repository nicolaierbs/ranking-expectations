import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Create logs directory if it doesn't exist

LOG_FILE = os.path.join(LOG_DIR, "ranking-expectations.log")

logging.basicConfig(
    level=logging.DEBUG,  # Set default logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Include module name
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=LOG_FILE,
    filemode="a"  # Append to log file
)

logger = logging.getLogger(__name__)  # Use __name__ for module-specific logging

# 1. Console handler:
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Console logs at DEBUG level or higher
console_formatter = logging.Formatter("%(levelname)s - %(message)s") # Simpler console format
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


# Example function to configure custom logging levels for specific modules if needed
def setup_module_logging(module_name, level):
    module_logger = logging.getLogger(module_name)
    module_logger.setLevel(level)
    

# Make the logger available to other modules
__all__ = ["logger", "setup_module_logging"]  # Import only these from other modules
