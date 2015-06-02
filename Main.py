

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


import Config
print "==================================================================================================================="
print "  _________      .__               .___    .__             ____    ________                                   .___"
print " /   _____/ ____ |  |__   ____   __| _/_ __|  |   ____    /  _ \   \______ \   ____ ______   ____   ____    __| _/"
print " \_____  \_/ ___\|  |  \_/ __ \ / __ |  |  \  | _/ __ \   >  _ </\  |    |  \_/ __ \\\\____ \_/ __ \ /    \  / __ | "
print " _____/   \  \___|   Y  \  ___// /_/ |  |  /  |_\  ___/  /  <_\ \/  |    `   \  ___/|  |_> >  ___/|   |  \/ /_/ | "
print "/_______  /\___  >___|  /\___  >____ |____/|____/\___  > \_____\ \ /_______  /\___  >   __/ \___  >___|  /\____ | "
print "        \/     \/     \/     \/     \/               \/         \/         \/     \/|__|        \/     \/      \/ "
print "==================================================================================================================="
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
print "MAXIMUM LINK BAND WIDTH:", Config.MaXBandWidth
print "==========================================="

Task_List = [0, 1, 2, 3, 4, 5, 6, 7]
Task_WCET_List=[30, 30, 20, 40, 10, 5, 15, 20]
Task_Criticality_List=['H', 'L', 'H', 'L', 'L', 'H', 'L', 'L']
TG_Edge_List=[(1,2), (1,3), (2,5), (0,5), (4,7), (4,3), (1,6), (0,6)]
TG_Edge_Weight=[5, 9, 4, 7, 5, 3, 5, 1]
#TG = copy.deepcopy(TG_Functions.GenerateTG(Task_List,TG_Edge_List,Task_Criticality_List,Task_WCET_List,TG_Edge_Weight))
TG = copy.deepcopy(TG_Functions.GenerateRandomTG(10,15,30,7))
#TG = copy.deepcopy(TG_Functions.GenerateRandomIndependentTG(10,15))
Task_Graph_Reports.ReportTaskGraph(TG)
Task_Graph_Reports.DrawTaskGraph(TG)
################################################
PE_List = [0, 1, 2, 3]
AG_Edge_List=[(0,1), (0,2), (1,0), (1,3), (2,0), (2,3), (3,2), (3,1)]
AG_Edge_Port_List=[('W','E'), ('S','N'), ('E','W'), ('S','N'), ('N','S'), ('W','E'), ('E','W'), ('N','S')]
AG = copy.deepcopy(AG_Functions.GenerateAG(PE_List,AG_Edge_List,AG_Edge_Port_List))
Arch_Graph_Reports.DrawArchGraph(AG)
################################################
SHM = SystemHealthMonitor.SystemHealthMap()
SHM.SetUp_NoC_SystemHealthMap(AG)
SHM.Report_NoC_SystemHealthMap()
print "SYSTEM IS UP..."
print "==========================================="
 # here we use XY routing
 # the turns should be named with port 2 port naming convention...
 # E2N is a turn that connects input of East port of the router to
 # output of north
TurnModel=['E2N','E2S','W2N','W2S']
SHM.SHM.edge[0][1]['LinkHealth']=False
NoCRG=Routing.GenerateNoCRouteGraph(AG,SHM,TurnModel,Config.DebugInfo,Config.DebugDetails)
if NoCRG is not False:
    #Mapping_Heuristics.Min_Min_Mapping (TG,AG,NoCRG,True)
    #Mapping_Heuristics.Max_Min_Mapping (TG,AG,NoCRG,True)
    ################################################
    # clustered task graph

    CTG=copy.deepcopy(Clustering.TaskClusterGeneration(len(PE_List), Config.DebugInfo))
    if Clustering.InitialClustering(TG, CTG, Config.MaXBandWidth):
        (BestClustering,BestTaskGraph)= Clustering.ClusteringOptimization_LocalSearch(TG, CTG, 1000, Config.MaXBandWidth)
        TG= copy.deepcopy(BestTaskGraph)
        CTG= copy.deepcopy(BestClustering)
        del BestClustering
        del BestTaskGraph
        Clustering_Functions.DoubleCheckCTG(TG,CTG)
        Clustering_Functions.ReportCTG(CTG,"CTG_PostOpt.png")

        if Mapping.MakeInitialMapping(TG,CTG,AG,NoCRG,Config.DebugInfo):
            Scheduler.ScheduleAll(TG,AG,Config.DebugInfo,Config.DebugDetails)
            Scheduling_Functions.ReportMappedTasks(AG)
            Mapping_Functions.CostFunction(TG,AG,Config.DebugInfo)
            #(BestTG,BestCTG,BestAG)=Mapping.OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,1000,Config.DebugInfo,Config.DebugDetails)
            (BestTG,BestCTG,BestAG)=Mapping.OptimizeMappingIterativeLocalSearch(TG,CTG,AG,NoCRG,20,100,Config.DebugInfo,Config.DebugDetails)
            TG= copy.deepcopy(BestTG)
            CTG= copy.deepcopy(BestCTG)
            AG= copy.deepcopy(BestAG)
            del BestTG
            del BestCTG
            del BestAG
            Scheduling_Functions.ReportMappedTasks(AG)
        else:
            Mapping_Functions.ReportMapping(AG)
            print "==========================================="
    else :
        print "Initial Clustering Failed...."