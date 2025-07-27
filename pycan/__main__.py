"""Test Python sample"""

import pycan

def main():
    print("Testing the ABC class and method..")
        
    # Get a CAN bus instance (assuming a CAN bus implementation exists)
    can_bus = pycan.Bus(interface="pcan", channel="PCAN_USBBUS1", bitrate=500000)

    if can_bus:
        can_bus.status()
        can_bus.shutdown()
    else:
        print("Failed to get bus instance.")

if __name__ == "__main__":
    main()