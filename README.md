can-datalogger
==============

The Controller Area Network is a bus standard designed to allow microcontrollers and device to communicated each other.

Features
--------

- common abstraction for CAN Communication
- receiving, sending and periodically sending messages


Setup
-----

Example Uses
------------

``pip install pycan``

.. code:: python

    #import pycan module
    import pycan

    #create a bus instance using 'with' statement.

    with pycan.Bus(interface="pcan", channel="PCAN_USBBUS1", bitrate=500000) as bus:

        bus.status()
    

Discussion
----------

Contributing
------------