import cx_Logging
import cx_Threads
import sys

class Handler(object):

    def __init__(self):
        cx_Logging.Info("creating handler instance")
        self.stopEvent = cx_Threads.Event()

    def Initialize(self, configFileName):
        cx_Logging.Info("initializing: config file name is %r", configFileName)

    def Run(self):
        cx_Logging.Info("running service....")
        self.stopEvent.Wait()

    def Stop(self):
        cx_Logging.Info("stopping service...")
        self.stopEvent.Set()

