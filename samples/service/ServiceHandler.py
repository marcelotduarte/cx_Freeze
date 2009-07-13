"""
Implements a simple service using cx_Freeze.

This sample makes use of cx_PyGenLib (http://cx-pygenlib.sourceforge.net) and
cx_Logging (http://cx-logging.sourceforge.net).

See below for more information on what methods must be implemented and how they
are called.
"""

import cx_Logging
import cx_Threads
import sys

class Handler(object):

    # no parameters are permitted; all configuration should be placed in the
    # configuration file and handled in the Initialize() method
    def __init__(self):
        cx_Logging.Info("creating handler instance")
        self.stopEvent = cx_Threads.Event()

    # called when the service is starting
    def Initialize(self, configFileName):
        cx_Logging.Info("initializing: config file name is %r", configFileName)

    # called when the service is starting immediately after Initialize()
    # use this to perform the work of the service; don't forget to set or check
    # for the stop event or the service GUI will not respond to requests to
    # stop the service
    def Run(self):
        cx_Logging.Info("running service....")
        self.stopEvent.Wait()

    # called when the service is being stopped by the service manager GUI
    def Stop(self):
        cx_Logging.Info("stopping service...")
        self.stopEvent.Set()

