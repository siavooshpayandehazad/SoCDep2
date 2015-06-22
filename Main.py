# Copyright (C) 2015 Siavoosh Payandeh Azad 

import os
import sys
import logging
import time
from ConfigAndPackages import Config
from Utilities import misc
from Utilities import Logger
import SystemInitialization
from notify.all import *

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
misc.GenerateFileDirectories()
####################################################################
misc.DrawLogo()
####################################################################
TG, AG, NoCRG, SHM, CriticalRG, NonCriticalRG = SystemInitialization.InitializeSystem(logging)


# Im trying to write some sort of Event driven system...

EventHandler = Signal()
EventHandler.connect(SHM.ReportTheEvent)
EventHandler.connect(SHM.ApplyFaultEvent)

EventHandler((2,1), 'T')
EventHandler(1, 'T')
EventHandler({1: 'N2E'}, 'P')
EventHandler.disconnect(SHM.ReportTheEvent)
EventHandler.disconnect(SHM.ApplyFaultEvent)

logging.info('Logging finished...')