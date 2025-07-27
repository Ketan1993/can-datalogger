"""
This module provides a unified interface for interacting with different bus types.
It uses a factory function to retrieve the appropriate bus implementation.
"""
import logging
import importlib
from typing import Any, Optional, cast
from .bus import BusABC
from .interfaces import BACKENDS

logger = logging.getLogger(__name__)

def _get_class_from_instance(interface: str) ->type[BusABC]:
    """Return Main class for the given instance.
    """
    #let's find the correct module name from BACKEND
    logger.info(f"Finding interface '{interface}' in BACKENDS list..")
    try:
        module_name, class_name = BACKENDS[interface]
    except Exception as e:
        raise NotImplementedError(f"Interface '{interface}' is not supported.."
                                  f"'{interface}':{e}") from None
    
    #import correct interface module
    try:
        logger.info(f"importing module '{module_name}'....")
        module = importlib.import_module(module_name)
    except Exception as e:
        raise NotImplementedError(f"Module '{module_name}' is not supported.."
                                  f"'{interface}':{e}") from None
    
    #import correct interface class 
    try:
        logger.info(f"importing class '{class_name}' ....")
        bus_class = getattr(module, class_name)
    except Exception as e:
        raise NotImplementedError(f"Cannot import class '{class_name}' from '{module_name}' is not supported.."
                                  f"'{interface}':{e}") from None

    #return retrive class from the module.    
    return cast("type[BusABC]", bus_class)

def Bus(interface: Optional[str] = None, 
        channel: Optional[str] = None, 
        **kwargs: Any,
        ) -> BusABC:
    """
    Factory function to get a particular device class (BusABC implementation).

    Args:
        interface (str, optional): The type of bus interface (e.g., 'CAN', 'USB', 'Serial'). 
                                   Defaults to None, allowing for automatic resolution or default configuration.
        channel (str, optional): The specific channel or port for the bus. 
                                  Expected type is backend dependent. Defaults to None.
        **kwargs: Additional backend-dependent configurations.

    Returns:
        BusABC: An instance of a concrete BusABC subclass representing the requested bus interface.
    """
    logger.info(f"Attempting to get bus interface: {interface}, channel: {channel}") #
    
    if interface is not None:
        kwargs["interface"] = interface
    
    #resolve the bus class to use for the instance.
    cls = _get_class_from_instance(kwargs["interface"])
    bus = cls(channel, **kwargs)
    return bus