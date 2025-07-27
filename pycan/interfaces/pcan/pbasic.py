"""PCAN Hardware level class.
This class provide access to PCAN device to read and write the messages.
This is basically provided by the PCAN device maker. 
"""

from ctypes import *
from ctypes.util import find_library
import platform

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

#BIT-RATE Mapping
PCAN_BITRATES = {
    500000 : PCAN_BAUD_500K,
    250000 : PCAN_BAUD_250K,
}

#PCAN Channel Mapping
PCAN_CHANNEL_NAMES = {
    "PCAN_USBBUS1" : PCAN_USBBUS1
}

class TPCANMsg(Structure):
    """Represents a CAN Message"""
    _fields_ = [("ID", c_uint)]

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
            print("Exception on pbasic.CAN_Initialize")
            raise

    def Uninitialize(self, Channel):
        """Uninitialize PCAN Channel, Initialized by CAN_Initialize

        Parameters:
            Channel         : PCAN Handler
        
        Return:
            A TPCANStatus error code
        """
        try:
            ret = self._m_ddlbasic.CAN_Uninitialize(Channel)
            return TPCANStatus(ret)
        except:
            print("Exception on pbasic.CAN_Uninitialize")
            raise
        
    def Read(self, Channel):
        """Read A CAN Message
        
        Parameters:
            Channel         : PCAN Handler

        Returns:
            PCAN Read API return 3 tuple value
            [0]: A TPCANStatus error code
            [1]: A TPCANMsg structure with CAN Message
            [2]: A TPCANTimestamp structure with time-stamp

        """
        try:
            msg = TPCANMsg()
            ret = self._m_ddlbasic.CAN_Read(Channel, byref(msg))
            return TPCANStatus(ret), msg
        except:
            print("Exception on pbasic.CAN_Read")
            raise

    def Write(self, Channel, MessageBuffer):
        """Transmits a CAN Message
        
        Parameters:
            Channel         : PCAN Handler
            MessageBuffer   : A Message representing the CAN Message
        
        Returns:
            A TPCANStatus Error Code
        """
        try:
            ret = self._m_ddlbasic.CAN_Write(Channel,byref(MessageBuffer))
            return TPCANStatus(ret)
        except:
            print("Exception on pbasic.CAN_Write")
            raise

    def GetStatus(self, Channel):
        """Get current status of the PCAN Device

        Parameters:
            Channel     :A PCAN Channel Handler
        
        Returns:
            A TPCANStatus Error code
        """
        try:
            ret = self._m_ddlbasic.CAN_GetStatus(Channel)
            return TPCANStatus(ret)
        except:
            print("Exception on pbasic.CAN_GetStatus")
            raise

    def GetErrorText(self, Error, Language = 0x09):
        """Get Error in text format.
        
        Parameters:
            Error       : A TPCANStatus Error code
            Language    : Indicate the Language Id. default (English : 0x09)
        
        Returns: 
            A touple value with 2
            [0]:    A TPCANStatus Error code
            [1]:    Error in Text format
        
        """

        try:
            mybuffer = create_string_buffer(256)
            ret      = self._m_ddlbasic.CAN_GetErrorText(Error, Language, byref(mybuffer))
            return TPCANStatus(ret), mybuffer.value
        except:
            print("Exception on pbasic.GetErrorText")
            raise