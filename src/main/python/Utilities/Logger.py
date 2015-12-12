# Copyright (C) 2015 Siavoosh Payandeh Azad 
import sys
import os
import time
from ConfigAndPackages import PackageFile

class Logger(object):
    """
    This Class is for redirecting the console messages to a log file...
    """
    def __init__(self):
        LoGDirectory = PackageFile.LoGDirectory
        if not os.path.isdir(LoGDirectory):
           os.makedirs(LoGDirectory)
        self.terminal = sys.stdout
        self.log = open( os.path.join(os.path.join(os.path.curdir ,LoGDirectory),
                                      'Console_log_'+str(time.time())+'.log'), "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)