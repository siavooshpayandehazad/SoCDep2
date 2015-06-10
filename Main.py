__author__ = 'siavoosh'
import os,sys
import copy
import logging
import time
import networkx
from Mapper import Mapping
from SystemHealthMonitoring import SystemHealthMonitor
from TaskGraphUtilities import Task_Graph_Reports,TG_Functions
from RoutingAlgorithms import Routing
from ArchGraphUtilities import Arch_Graph_Reports,AG_Functions
import Logger
import Config

####################################################################
#
#                       Logging Material
#
####################################################################
# Just for getting a copy of the current console
sys.stdout = Logger.Logger()
LoGDirectory = "LOGS"
if not os.path.isdir(LoGDirectory):
    os.makedirs(LoGDirectory)
####################################################################
# preparing to setup Logging
logging.basicConfig(filename=os.path.join(os.path.join(os.path.curdir,LoGDirectory),'Logging_Log_'+str(time.time())+'.log'),level=logging.DEBUG)
logging.info('Starting logging...')
####################################################################
print("===================================================================================================================")
print("  _________      .__               .___    .__             ____    ________                                   .___")
print(" /   _____/ ____ |  |__   ____   __| _/_ __|  |   ____    /  _ \   \______ \   ____ ______   ____   ____    __| _/")
print(" \_____  \_/ ___\|  |  \_/ __ \ / __ |  |  \  | _/ __ \   >  _ </\  |    |  \_/ __ \\\\____ \_/ __ \ /    \  / __ | ")
print(" _____/   \  \___|   Y  \  ___// /_/ |  |  /  |_\  ___/  /  <_\ \/  |    `   \  ___/|  |_> >  ___/|   |  \/ /_/ | ")
print("/_______  /\___  >___|  /\___  >____ |____/|____/\___  > \_____\ \ /_______  /\___  >   __/ \___  >___|  /\____ | ")
print("        \/     \/     \/     \/     \/               \/         \/         \/     \/|__|        \/     \/      \/ ")
print("===================================================================================================================")
print("AUTHOR:  SIAVOOSH PAYANDEH AZAD")
print("DATE:    MAY 2015")
print("THE GOAL OF THIS PROGRAM IS TO MAKE A PLATFORM FOR TESTING SOME ")
print("DEPENDABILITY STUFF ON DIFFERENT ARCHITECTURES....")
print("================================================================================")

GraphDirectory = "GraphDrawings"
if not os.path.isdir(GraphDirectory):
   os.makedirs(GraphDirectory)

print "DEBUG DETAILS:", Config.DebugDetails
print "DEBUG INFO:", Config.DebugInfo
print "==========================================="
####################################################################
# TODO: can we get TG specifications automatically from some benchmark alg??
TG = copy.deepcopy(TG_Functions.GenerateTG())
Task_Graph_Reports.ReportTaskGraph(TG,logging)
Task_Graph_Reports.DrawTaskGraph(TG)
if not networkx.is_directed_acyclic_graph(TG):
    raise ValueError('TASK GRAPH HAS CYCLES..!!!')
else:
    logging.info("TG IS AN ACYCLIC DIRECTED GRAPH... ALL IS GOOD...")
####################################################################
AG = copy.deepcopy(AG_Functions.GenerateAG(logging))
Arch_Graph_Reports.DrawArchGraph(AG)
####################################################################
SHM = SystemHealthMonitor.SystemHealthMonitor()
SHM.SetUp_NoC_SystemHealthMap(AG,Config.TurnsHealth)
SHM.Report_NoC_SystemHealthMap()
print "==========================================="
print "SYSTEM IS UP..."
# Here we are applying initial faults of the system
SHM.ApplyInitialFaults()
NoCRG=Routing.GenerateNoCRouteGraph(AG,SHM,Config.XY_TurnModel,Config.DebugInfo,Config.DebugDetails)
# print Routing.FindRouteInRouteGraph(NoCRG,0,3,True,True)

####################################################################
BestTG,BestAG = Mapping.Mapping(TG,AG,NoCRG,SHM,logging)
if BestAG is not None:
    TG = copy.deepcopy(BestTG)
    AG = copy.deepcopy(BestAG)
    del BestTG, BestAG
    SHM.AddCurrentMappingToMPM(TG)
    SHM.ReportMPM()

logging.info('Logging finished...')