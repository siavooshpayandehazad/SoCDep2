# Copyright (C) 2015 Siavoosh Payandeh Azad 

import os
import sys
import logging
import time
from ConfigAndPackages import Config
from Utilities import GenerateFileDirectories
from Utilities import misc
from Utilities import Logger
import SystemInitialization

####################################################################
#
#                       Logging Material
#
####################################################################
# Just for getting a copy of the current console
sys.stdout = Logger.Logger()
##############################
# preparing to setup Logging
logging.basicConfig(filename=os.path.join(os.path.join(os.path.curdir, Config.LoGDirectory),
                                          'Logging_Log_'+str(time.time())+'.log'), level=logging.DEBUG)
logging.info('Starting logging...')
####################################################################
GenerateFileDirectories.GenerateFileDirectories()
####################################################################
misc.DrawLogo()
####################################################################
TG, AG, NoCRG, SHM, CriticalRG, NonCriticalRG = SystemInitialization.InitializeSystem(logging)

"""
# Im trying to write some sort of Event driven system...
def ReportTheEvent(Event):
    print "Event:",Event,"Happened"

EventHandler = Signal()
EventHandler.connect(ReportTheEvent)

EventHandler("Dead chip")
EventHandler.disconnect(ReportTheEvent)
"""

logging.info('Logging finished...')