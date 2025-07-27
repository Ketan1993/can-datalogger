import logging
from typing import Optional #  Optional for type hinting

# Set up module-specific logging
logger = logging.getLogger(__name__) # Use module-level logger
logger.setLevel(logging.INFO) # Set default logging level for this logger
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Define the public interface of this module
__all__ = ["BusABC", "Bus" "interfaces" "interface", "exeptions"] # Only expose the abstract base class and the factory function

from .bus import BusABC

from .exceptions import(
    ErrorHanler,
    InitializationError,
    ValueErrorHandler,
)