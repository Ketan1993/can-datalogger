"""Test Python sample"""

import pycan

def main():
    print("Testing the ABC class and method..")
        
    # Get a CAN bus instance (assuming a CAN bus implementation exists)
    with pycan.Bus(interface="pcan", channel="PCAN_USBBUS1", bitrate=500000) as bus:
        bus.status()

if __name__ == "__main__":
    main()