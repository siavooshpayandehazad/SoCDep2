__author__ = 'siavoosh'
import os
import copy
from Clusterer import Clustering, Clustering_Functions
from Scheduler import Scheduler,Scheduling_Functions
from Mapper import Mapping_Functions, Mapping,Mapping_Heuristics
from SystemHealthMonitoring import SystemHealthMonitor
from TaskGraphUtilities import Task_Graph_Reports,TG_Functions
from RoutingAlgorithms import Routing
from ArchGraphUtilities import Arch_Graph_Reports,AG_Functions
import logging
import time
import Logger
import sys
import networkx


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
import Config
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
################################################
# TODO: can we get these specifications automatically from some benchmark alg??
if Config.TG_Type=='RandomDependent':
    TG = copy.deepcopy(TG_Functions.GenerateRandomTG(Config.NumberOfTasks,Config.NumberOfEdges,
                                                     Config.WCET_Range,Config.WCET_Range))
elif Config.TG_Type=='RandomIndependent':
    TG = copy.deepcopy(TG_Functions.GenerateRandomIndependentTG(Config.NumberOfTasks,Config.WCET_Range))
elif Config.TG_Type=='Manual':
    TG = copy.deepcopy(TG_Functions.GenerateManualTG(Config.Task_List,Config.TG_Edge_List,
                                                     Config.Task_Criticality_List,Config.Task_WCET_List,
                                                     Config.TG_Edge_Weight))

Task_Graph_Reports.ReportTaskGraph(TG,logging)
Task_Graph_Reports.DrawTaskGraph(TG)
if  not networkx.is_directed_acyclic_graph(TG):
    raise ValueError('TASK GRAPH HAS CYCLES..!!!')
else:
    logging.info("TG IS AN ACYCLIC DIRECTED GRAPH... ALL IS GOOD...")

################################################
if Config.AG_Type=='Generic':
    AG = copy.deepcopy(AG_Functions.GenerateGenericTopologyAG(Config.NetworkTopology,Config.Network_X_Size,
                                                          Config.Network_Y_Size,Config.Network_Z_Size,logging))
elif Config.AG_Type=='Manual':
    AG = copy.deepcopy(AG_Functions.GenerateAG(Config.PE_List,Config.AG_Edge_List,Config.AG_Edge_Port_List))
Arch_Graph_Reports.DrawArchGraph(AG)
################################################
SHM = SystemHealthMonitor.SystemHealthMonitor()
SHM.SetUp_NoC_SystemHealthMap(AG,Config.TurnsHealth)
SHM.Report_NoC_SystemHealthMap()
print "==========================================="
print "SYSTEM IS UP..."
 # here we use XY routing
 # the turns should be named with port 2 port naming convention...
 # E2N is a turn that connects input of East port of the router to
 # output of north
for BrokenLink in Config.ListOfBrokenLinks:
    SHM.BreakLink(BrokenLink,True)

for NodeWithBrokenTrun in Config.ListOfBrokenTurns:
    SHM.BreakTrun(NodeWithBrokenTrun,Config.ListOfBrokenTurns[NodeWithBrokenTrun],True)

for AgedPE in Config.ListOfAgedPEs:
    SHM.IntroduceAging(AgedPE, Config.ListOfAgedPEs[AgedPE],True)

for BrokenNode in Config.ListOfBrokenPEs:
    SHM.BreakNode(BrokenNode,True)

NoCRG=Routing.GenerateNoCRouteGraph(AG,SHM,Config.XY_TurnModel,Config.DebugInfo,Config.DebugDetails)
# print Routing.FindRouteInRouteGraph(NoCRG,0,3,True,True)

#################################################
# to run the following heuristics (Min_Min,Max_Min), one needs to use independent
# tasks... Please use: GenerateRandomIndependentTG
if Config.Mapping_Function=='MinMin':
    if Config.TG_Type=='RandomIndependent':
        Mapping_Heuristics.Min_Min_Mapping (TG,AG,NoCRG,SHM,logging)
    else:
        raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

elif Config.Mapping_Function=='MaxMin':
    if Config.TG_Type=='RandomIndependent':
        Mapping_Heuristics.Max_Min_Mapping (TG,AG,NoCRG,SHM,logging)
    else:
        raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

elif Config.Mapping_Function=='LocalSearch' or Config.Mapping_Function=='IterativeLocalSearch':
    if Config.TG_Type!='RandomDependent':
        raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomDependent')
# clustered task graph
    CTG=copy.deepcopy(Clustering.TaskClusterGeneration(len(AG.nodes())))
    if Clustering.InitialClustering(TG, CTG):
        # Clustered Task Graph Optimization
        (BestClustering,BestTaskGraph)= Clustering.ClusteringOptimization_LocalSearch(TG, CTG, 1000)
        TG= copy.deepcopy(BestTaskGraph)
        CTG= copy.deepcopy(BestClustering)
        del BestClustering
        del BestTaskGraph
        Clustering_Functions.DoubleCheckCTG(TG,CTG)
        Clustering_Functions.ReportCTG(CTG,"CTG_PostOpt.png")
        # Mapping CTG on AG
        if Mapping.MakeInitialMapping(TG,CTG,AG,SHM,NoCRG,True,logging):
            Mapping_Functions.ReportMapping(AG)
            # Schedule all tasks
            Scheduler.ScheduleAll(TG,AG,SHM,Config.DebugInfo,Config.DebugDetails)
            Scheduling_Functions.ReportMappedTasks(AG)
            Mapping_Functions.CostFunction(TG,AG,Config.DebugInfo)
            if Config.Mapping_Function=='LocalSearch':
                (BestTG,BestCTG,BestAG)=Mapping.OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,SHM,
                                                                            Config.LocalSearchIteration,
                                                                            Config.DebugInfo,Config.DebugDetails,
                                                                            logging)
                TG= copy.deepcopy(BestTG)
                CTG= copy.deepcopy(BestCTG)
                AG= copy.deepcopy(BestAG)
                del BestTG
                del BestCTG
                del BestAG
            elif Config.Mapping_Function=='IterativeLocalSearch':
                (BestTG,BestCTG,BestAG)=Mapping.OptimizeMappingIterativeLocalSearch(TG,CTG,AG,NoCRG,SHM,
                                                                                    Config.IterativeLocalSearchIterations,
                                                                                    Config.LocalSearchIteration,
                                                                                    Config.DebugInfo,
                                                                                    Config.DebugDetails,
                                                                                    logging)
                TG= copy.deepcopy(BestTG)
                CTG= copy.deepcopy(BestCTG)
                AG= copy.deepcopy(BestAG)
                del BestTG
                del BestCTG
                del BestAG
            Scheduling_Functions.ReportMappedTasks(AG)
            Mapping_Functions.CostFunction(TG,AG,True)
        else:
            Mapping_Functions.ReportMapping(AG)
            print "==========================================="
    else :
        print "Initial Clustering Failed...."
elif Config.Mapping_Function=='SimulatedAnnealing':
    None
logging.info('Logging finished...')