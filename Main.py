# Copyright (C) 2015 Siavoosh Payandeh Azad

import threading
import sys, os, time
import numpy
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
TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG = SystemInitialization.InitializeSystem(logging)

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

def FaultEvent():
    global timer
    TimeAfterSystemStart = round(time.time() - SystemStartingTime)
    # Should we reset the timer or the next fault falls out of the program run time?
    # Todo: We need to make this occurrence of faults random... while keeping MTBF as mean value
    # Todo: still should think about standard deviation for fault distribution
    # print numpy.random.normal(Config.MTBF,0.1*Config.MTBF)
    if TimeAfterSystemStart + Config.MTBF <= Config.ProgramRunTime:
        # reset the timer
        timer = threading.Timer(Config.MTBF, FaultEvent)
        timer.start()
    print "\033[92mTIME::\033[0m", TimeAfterSystemStart, " AFTER SYSTEM START..."
    # we generate some random fault to be inserted in the system
    FaultLocation, FaultType = SHM_Functions.RandomFaultGeneration(SHM)
    # here we actually insert the fault in the system
    SHM_Functions.ApplyFaultEvent(SHM,FaultLocation, FaultType)

timer = threading.Timer(Config.MTBF, FaultEvent)
timer.start()

while True:
    if time.time() - SystemStartingTime > Config.ProgramRunTime:
        break

timer.cancel()
timer.join()
logging.info('Logging finished...')