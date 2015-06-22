# Copyright (C) 2015 Siavoosh Payandeh Azad 

import os
import sys
import logging
import time
import misc
import Logger
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
LoGDirectory = "LOGS"
logging.basicConfig(filename=os.path.join(os.path.join(os.path.curdir, LoGDirectory),
                                          'Logging_Log_'+str(time.time())+'.log'), level=logging.DEBUG)
logging.info('Starting logging...')
####################################################################
GraphDirectory = "GraphDrawings"
if not os.path.isdir(GraphDirectory):
    os.makedirs(GraphDirectory)

GeneratedFilesDirectory = "Generated_Files"
if not os.path.isdir(GeneratedFilesDirectory):
    os.makedirs(GeneratedFilesDirectory)
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