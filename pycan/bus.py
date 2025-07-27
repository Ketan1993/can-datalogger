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

    #private
    channel_info = "unknown"
    _is_shutdown: bool = True

    @abstractmethod
    def __init__(self, 
                 channel: Any,
                 **kwargs: object
                ):
        
        self.channel_info = channel
        self._is_shutdown = False

    @abstractmethod
    def send(self, port, baudrate):
        """Abstract method for the open driver instance"""
        pass

    def recv(self, timeout: Optional[float] = None):
        self._recv_internal(timeout)
        logger.info("closing serial connection in bus")

    def _recv_internal(self, timeout:Optional[float]):
        raise NotImplementedFunc("This is not implemented")

    
    def shutdown(self) -> None:

        """Call shut-down process when bus instance exit from the block mode or clean-up request made
        """
        if self._is_shutdown:
            logger.info("%s is already shut down", self.__class__)
            return

        self._is_shutdown = True

    #To support the onject creation with `with statement`
    def __enter__(self):
        return self
    
    #To support the object creation with `with` statement    
    def __exit__(self, exc_type,
                 exc_val, exc_tb
                ) -> None:
        self.shutdown()
        
    #To support destructor clean up method
    def __del__(self) -> None:
        if not self._is_shutdown:
            self.shutdown()


