"""Abstract class"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import logging

from .exceptions import(
    NotImplementedFunc,
)

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
    def send(self, port, baudrate):
        """Abstract method for the open driver instance"""
        pass

    def recv(self, timeout: Optional[float] = None):
        self._recv_internal(timeout)
        logger.info("closing serial connection in bus")

    def _recv_internal(self, timeout:Optional[float]):
        raise NotImplementedFunc("This is not implemented")

    
