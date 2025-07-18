"""Test Python sample"""

from my_package.interface import Bus

def main():
    print("Testing the ABC class and method..")
        
    # Get a CAN bus instance (assuming a CAN bus implementation exists)
    can_bus = Bus(interface="pcan", channel="PCANUSB1", bitrate=500000)

    if can_bus:
        can_bus.status()
    else:
        print("Failed to get bus instance.")
    
if __name__ == "__main__":
    main()