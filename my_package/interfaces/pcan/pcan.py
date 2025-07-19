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

logger = logging.getLogger(__name__)



"""PCAN Hardware class. 
   provide information about the PCAN Hardware like status of the deivce, provide API to read or write to hardware.
"""
TPCANStatus = int  # Represents a PCAN status/error code
TPCANDevice = c_ubyte  # Represents a PCAN device
TPCANBaudrate = c_ushort  # Represents a PCAN Baud rate register value
TPCANType = c_ubyte  # Represents the type of PCAN hardware to be initialized

# PCAN devices
#
TPCANHandle = c_ushort  # Represents a PCAN hardware channel handle
PCAN_NONE = TPCANDevice(0x00)  # Undefined, unknown or not selected PCAN device value
PCAN_PEAKCAN = TPCANDevice(0x01)  # PCAN Non-PnP devices. NOT USED WITHIN PCAN-Basic API
PCAN_ISA = TPCANDevice(0x02)  # PCAN-ISA, PCAN-PC/104, and PCAN-PC/104-Plus
PCAN_DNG = TPCANDevice(0x03)  # PCAN-Dongle
PCAN_PCI = TPCANDevice(0x04)  # PCAN-PCI, PCAN-cPCI, PCAN-miniPCI, and PCAN-PCI Express
PCAN_USB = TPCANDevice(0x05)  # PCAN-USB and PCAN-USB Pro
PCAN_PCC = TPCANDevice(0x06)  # PCAN-PC Card

#PCAN Channel
PCAN_USBBUS1 = TPCANHandle(0x51)  # PCAN-USB interface, channel 1

#Baud rate codes = BTR0/BTR1 register values for the CAN controller.
PCAN_BAUD_500K = TPCANBaudrate(0x001C)  # 500 kBit/s
PCAN_BAUD_250K = TPCANBaudrate(0x011C)  # 250 kBit/s

#PCAN Error code
PCAN_ERROR_OK = TPCANStatus(0x00000)  # No error

PCAN_BITRATES = {
    500000 : PCAN_BAUD_500K,
    250000 : PCAN_BAUD_250K,
}

PCAN_CHANNEL_NAMES = {
    "PCAN_USBBUS1" : PCAN_USBBUS1
}

class PCANHardware():
    def __init__(self):
    
        """Initialize with type of platform"""
        
        #get the platform type
        PLATFORM = platform.system()
        IS_WINDOWS = PLATFORM == "Windows"

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

    def Initialize(self,
                   Channel,
                   Btr0Btr1,
                   hWType=TPCANType(0),
                   IOPort=c_uint(0),
                   Interrupt=c_ushort(0)
                   ):
        """
           Initializes PCAN device

           Parameters:

           
                Channel     : PCAN Channel like "PCANUSB1,2,3.."
                Btr0Btr1    : The speed for the communication
                HwType      : The type of the hardware
                IOPort      : The I/O address for parreller port
                Interrupt   : The interrupt number

           Returns:
            A TPCANStatus error code
        
        """
        try:
            ret = self._m_ddlbasic.CAN_Initialize(Channel,Btr0Btr1,hWType,IOPort,Interrupt)
            return TPCANStatus(ret)
        except:
            print("Failed to Initialize the PCAN Driver..")
            raise
    
    def GetErrorText(self, Error, Langauge = 0x09):

        try:
            mybuffer = create_string_buffer(256)
            ret      = self._m_ddlbasic.CAN_GetErrorText(Error, Langauge, byref(mybuffer))
            return TPCANStatus(ret), mybuffer.value
        except:
            print("Exception on PCANBasic.GetErrorText")
            raise


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
       self.__mHardwareObject = PCANHardware()
         
       self.__mChannel = PCAN_CHANNEL_NAMES.get(Channel)
       
       if self.__mChannel is None:
           err_msg = f"Cannot find a '{Channel}' Channel from supported Channel.."
           raise ValueError(err_msg)
       
       self.__pcan_bitrate = PCAN_BITRATES.get(bitrate, PCAN_BAUD_500K)

       logger.info(f"PCAN Channel : '{self.__mChannel}' PCAN bitrate: '{self.__pcan_bitrate}' ")

       result = self.__mHardwareObject.Initialize(self.__mChannel, self.__pcan_bitrate)
       
       if result != PCAN_ERROR_OK:
           logger.error(f"'{self._get_formatted_error(result)}'")
       
       super().__init__(channel=Channel, **kwargs)

    def open_connection(self, port, baudrate):
        logger.info("open connection")

    def close_connection(self):
        logger.info("closing serial connection")
    
    def status(self):
        logger.info("status")
    
    def _get_formatted_error(self, Error):
        """
        Help Function used to get error in text

        """
        strReturn = self.__mHardwareObject.GetErrorText(Error, 0x09)
        if strReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(Error)
        else:
            message = str(strReturn[1])
            return message.replace("'","",2).replace("b","",1)

        
