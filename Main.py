# Copyright (C) 2015 Siavoosh Payandeh Azad

from notify.all import *
import sys, os, time
import logging
from ConfigAndPackages import Config
from Utilities import misc
from Utilities import Logger
from SystemHealthMonitoring import SHM_Functions
import SystemInitialization

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

# Im trying to write some sort of Event driven system...

EventHandler = Signal()
EventHandler.connect(SHM.ApplyFaultEvent)

FaultLocation, FaultType = SHM_Functions.RandomFaultGeneration(SHM)
EventHandler(FaultLocation, FaultType)

EventHandler.disconnect(SHM.ApplyFaultEvent)
logging.info('Logging finished...')