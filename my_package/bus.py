"""Abstract class"""

from abc import ABC, abstractmethod
from typing import Any
import logging

#get current logger name
logger = logging.getLogger(__name__)

"""Abstract class for the interface device."""

class BusABC(ABC):

    #channel info
    channel_info = "unknown"
    def __init__(self, 
                 channel: Any,
                 **kwargs: object
                ):
        
        self.channel_info = channel
        logger.info("__init__ of BusABC class initialize..")
        logger.info(f"channel name: '{self.channel_info}'")

    @abstractmethod
    def open_connection(self, port, baudrate):
        """Abstract method for the open driver instance"""
        pass

    @abstractmethod
    def close_connection(self):
        """Abstract method for the close driver instance"""
        pass

    
