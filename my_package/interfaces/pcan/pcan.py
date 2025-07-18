"""PCAN Hardware class"""

from typing import Any, Optional
import logging

#import module
from my_package import(
    BusABC
)
logger = logging.getLogger(__name__)

class PcanBus(BusABC):
    def __init__(self,
                 channel: str = "PCAN",
                 device_id: Optional[int] = None,
                 **kwargs: Any):
       
       logger.info("__init__ of PcanBus class initialize..")
       
       self._device_id = device_id
       logger.info(f"channel name: '{channel}'")

       super().__init__(channel=channel, **kwargs)

    def open_connection(self, port, baudrate):
        logger.info("open connection")

    def close_connection(self):
        logger.info("closing serial connection")
    
    def status(self):
        logger.info("status")
        
