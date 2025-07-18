from typing import Any
import logging

from my_package import(
    BusABC
)

logger = logging.getLogger(__name__)

class SerialBus(BusABC):
    def __init__(self,
                 channel: Any,
                 **kwargs: object):
        
        logger.info("__init__ of SerialBus class initialize..")
    
    def open_connection(self, port, baudrate):
        logger.info("connection open")

    def close_connection(self):
        logger.info("closing serial connection")

    def status(self):
        logger.info("status")
        
