# Copyright (C) 2015 Siavoosh Payandeh Azad

from notify.all import *
import threading
import sys, os, time
import logging
from ConfigAndPackages import Config
from Utilities import misc
from Utilities import Logger
from SystemHealthMonitoring import SHM_Functions
import SystemInitialization

ProgramStartTime = time.time()
##############################
# Just for getting a copy of the current console
sys.stdout = Logger.Logger()

# preparing to setup Logging
logging.basicConfig(filename=os.path.join(os.path.join(os.path.curdir, Config.LoGDirectory),
                                          'Logging_Log_'+str(time.time())+'.log'), level=logging.DEBUG)
logging.info('Starting logging...')
####################################################################
misc.GenerateFileDirectories()
misc.DrawLogo()
####################################################################
# Initialization of the system
TG, AG, NoCRG, SHM, CriticalRG, NonCriticalRG = SystemInitialization.InitializeSystem(logging)

# just to have a sense of how much time we are spending in each section
print "==========================================="
SystemStartingTime = time.time()
print "\033[92mTIME::\033[0m SYSTEM STARTS AT:", round(SystemStartingTime - ProgramStartTime), \
      "SECONDS AFTER PROGRAM START..."

####################################################################
#
#                   Fault event handler
#
####################################################################
EventHandler = Signal()
EventHandler.connect(SHM.ApplyFaultEvent)

def FaultEvent():
    TimeAfterSystemStart = round(time.time() - SystemStartingTime)
    print "\033[92mTIME::\033[0m", TimeAfterSystemStart, " AFTER SYSTEM START..."
    # we generate some random fault to be inserted in the system
    FaultLocation, FaultType = SHM_Functions.RandomFaultGeneration(SHM)
    # here we actually insert the fault in the system
    EventHandler(FaultLocation, FaultType)
    # Should we reset the timer or the next fault falls out of the program run time?
    if TimeAfterSystemStart + Config.MTBF <= Config.ProgramRunTime:
        # reset the timer
        timer = threading.Timer(Config.MTBF, FaultEvent)
        timer.start()

timer = threading.Timer(Config.MTBF, FaultEvent)
timer.start()

while True:
    if time.time() - SystemStartingTime > Config.ProgramRunTime:
        break

timer.cancel()
timer.join()
EventHandler.disconnect(SHM.ApplyFaultEvent)
logging.info('Logging finished...')