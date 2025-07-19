#common init for all the module listed on the interfaces directory.
"""this BACKENDS used for the searching the module as per the interface request"""
__all__ = [
    "BACKENDS"
    "pcan"
    "serialcan"
]

#intercace name = (module, classname)
BACKENDS: dict[str, tuple[str, str]] = {
    "pcan":("my_package.interfaces.pcan", "PcanBus"),
    "serialcan":("my_package.interfaces.serialcan.serial_can", "SerialBus"),
}