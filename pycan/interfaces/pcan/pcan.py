"""PCAN Hardware class
   PCAN Class will provide the API to intract with the Hardware of PCAN.
"""

from typing import Any, Optional
from ctypes import *
from ctypes.util import find_library
import logging

#import module
from pycan import(
    BusABC,
    InitializationError,
    ValueErrorHandler,
)

from .pbasic import(
    PCAN_ERROR_OK,
    PCAN_BITRATES,
    PCAN_CHANNEL_NAMES,
    PCANHardware
)

logger = logging.getLogger(__name__)

class PcanBus(BusABC):
    def __init__(self,
                 Channel: str = "PCAN_USBBUS1",
                 bitrate: int = 5000000,
                 device_id: Optional[int] = None,
                 **kwargs: Any):
       
       """
          A PCAN USB Interface to CAN

          A top level class.

          parameters:
                Channel         : The can interface name. An example would be "PCAN_USBBUS1"
                bitrate         : The speed of the communication. Example. 250Kbps, 1Mbps etc.
                                  default is 500 bit/s.
                                
       """
       
       logger.info("__init__ of PcanBus class initialize..")
       
       #Initialize the PCAN Hardware instance
       self.m_objPCANHardware = PCANHardware()
       self.m_PCANHandler = PCAN_CHANNEL_NAMES.get(Channel)
       
       if self.m_PCANHandler is None:
           err_msg = f"Cannot find a '{Channel}' Channel from supported Channel.."
           raise ValueErrorHandler(err_msg)
       
       #get bit-rate 
       self._pcan_bitrate = PCAN_BITRATES.get(bitrate)

       result = self.m_objPCANHardware.Initialize(self.m_PCANHandler, self._pcan_bitrate)
       
       if result != PCAN_ERROR_OK:
           raise InitializationError(self._get_formatted_error(result), result)
       
       #get channel status
       result = self.m_objPCANHardware.GetStatus(self.m_PCANHandler)
       if result != PCAN_ERROR_OK:
           raise InitializationError(self._get_formatted_error(result), result)
       
       result = self.m_objPCANHardware.Uninitialize(self.m_PCANHandler)
       if result != PCAN_ERROR_OK:
           raise InitializationError(self._get_formatted_error(result), result)
       
       self.m_objPCANHardware.Read(self.m_PCANHandler)
       
       super().__init__(channel=Channel, **kwargs)

    def send(self, port, baudrate):
        logger.info("open connection")

    def recv(self, timeout: Optional[float] = None):
        logger.info("closing serial connection")
    
    def status(self):
        """Query of PCAN Status
        
        returns:
            PCAN Device status
        """
        return self.m_objPCANHardware.GetStatus(self.m_PCANHandler)
    
    def _get_formatted_error(self, Error):
        """
        Help Function used to get error in text

        """
        strReturn = self.m_objPCANHardware.GetErrorText(Error, 0x09)
        if strReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(Error)
        else:
            message = str(strReturn[1])
            return message.replace("'","",2).replace("b","",1)

        
