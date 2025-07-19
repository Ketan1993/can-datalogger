"""PCAN Hardware class
   PCAN Class will provide the API to intract with the Hardware of PCAN.
"""

from typing import Any, Optional
from ctypes import *
from ctypes.util import find_library
import logging
import platform

#import module
from my_package import(
    BusABC
)

#get the platform type
PLATFORM = platform.system()
IS_WINDOWS = PLATFORM == "Windows"

logger = logging.getLogger(__name__)

"""PCAN Hardware class. 
   provide information about the PCAN Hardware like status of the deivce, provide API to read or write to hardware.
"""
class PCANHardware():
    def __init__(self):
    
        """Initialize with type of platform"""
    
        if IS_WINDOWS:
            load_libray_func = windll.LoadLibrary 
            lib_name         = "PCANBasic"      

        """let's find the PCANBasic dll library on system, which is provided by the PCAN hardware maker.
        """
        lib_path = find_library(lib_name)
        
        if not lib_path:
            raise OSError(f"'{lib_name}' not found in system")
        
        #load the PCANBasic.dll library from the system
        try:
            #this approch is equivalent to windll.LoadLibrary("PCANBasic") method
            self._m_ddlbasic = load_libray_func(lib_path)
        except OSError:
            raise OSError(f"PCAN Basic Library could not loaded. '{lib_path}'")



class PcanBus(BusABC):
    def __init__(self,
                 channel: str = "PCAN",
                 device_id: Optional[int] = None,
                 **kwargs: Any):
       
       logger.info("__init__ of PcanBus class initialize..")
       self.__mHardwareObject = PCANHardware()

       self._device_id = device_id
       logger.info(f"channel name: '{channel}'")

       super().__init__(channel=channel, **kwargs)

    def open_connection(self, port, baudrate):
        logger.info("open connection")

    def close_connection(self):
        logger.info("closing serial connection")
    
    def status(self):
        logger.info("status")
        
