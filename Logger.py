__author__ = 'siavoosh'

import sys
import os
import time
class Logger(object):
    def __init__(self):
        LoGDirectory = "LOGS"
        if not os.path.isdir(LoGDirectory):
           os.makedirs(LoGDirectory)
        self.terminal = sys.stdout
        self.log = open( os.path.join(os.path.join(os.path.curdir,LoGDirectory),'Console_log_'+str(time.time())+'.log') , "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)