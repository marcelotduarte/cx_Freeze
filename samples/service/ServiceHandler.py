"""Implements a simple service using cx_Freeze.

See below for more information on what methods must be implemented and how they
are called.
"""

from __future__ import annotations

import threading


class Handler:
    # no parameters are permitted; all configuration should be placed in the
    # configuration file and handled in the initialize() method
    def __init__(self) -> None:
        self.stopEvent = threading.Event()
        self.stopRequestedEvent = threading.Event()

    # called when the service is starting
    def initialize(self, configFileName) -> None:
        pass

    # called when the service is starting immediately after initialize()
    # use this to perform the work of the service; don't forget to set or check
    # for the stop event or the service GUI will not respond to requests to
    # stop the service
    def run(self) -> None:
        self.stopRequestedEvent.wait()
        self.stopEvent.set()

    # called when the service is being stopped by the service manager GUI
    def stop(self) -> None:
        self.stopRequestedEvent.set()
        self.stopEvent.wait()
