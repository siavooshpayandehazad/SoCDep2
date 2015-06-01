__author__ = 'siavoosh'
import os
import copy
import matplotlib.pyplot as plt
import networkx
from ScheduleAndDepend.Clusterer import Clustering, Clustering_Functions
from Scheduler import Scheduler
from ScheduleAndDepend.Mapper import Mapping_Functions, Mapping
from Scheduler import Scheduling_Functions
from SystemHealthMonitoring import SystemHealthMonitor
from TaskGraphUtilities import Task_Graph_Reports
from TaskGraphUtilities import TG_Functions
from RoutingAlgorithms import Routing

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

DebugDetails=False
MaXBandWidth=10

print "DEBUG DETAILS:", DebugDetails
print "MAXIMUM LINK BAND WIDTH:", MaXBandWidth
print "==========================================="

print("PREPARING A TASK GRAPH (TG)...")
Task_List = [0, 1, 2, 3, 4, 5, 6, 7]
Task_WCET_List=[30, 30, 20, 40, 10, 5, 15, 20]
Task_Criticality_List=['H', 'L', 'H', 'L', 'L', 'H', 'L', 'L']
TG_Edge_List=[(1,2), (1,3), (2,5), (0,5), (4,7), (4,3), (1,6), (0,6)]
TG_Edge_Weight=[5, 9, 4, 7, 5, 3, 5, 1]
TG = copy.deepcopy(TG_Functions.GenerateTG(Task_List,TG_Edge_List,Task_Criticality_List,Task_WCET_List,TG_Edge_Weight))
TG_Functions.AssignPriorities(TG)
print("TASK GRAPH (TG) IS READY...")
Task_Graph_Reports.ReportTaskGraph(TG)
Task_Graph_Reports.DrawTaskGraph(TG,TG_Edge_List,TG_Edge_Weight)

################################################
print "PREPARING AN ARCHITECTURE GRAPH (AG)..."
#todo: add virtual channel support AG...
AG=networkx.DiGraph()
PE_List = [0, 1, 2, 3]
AG_Edge_List=[(0,1), (0,2), (1,0), (1,3), (2,0), (2,3), (3,2), (3,1)]
AG_Edge_Port_List=[('W','E'), ('S','N'), ('E','W'), ('S','N'), ('N','S'), ('W','E'), ('E','W'), ('N','S')]
for PE in PE_List:
    AG.add_node(PE,MappedTasks = [],Scheduling={},Utilization=0)

for i in range(0,len(AG_Edge_List)):
    EDGE = AG_Edge_List[i]
    AG.add_edge(EDGE[0],EDGE[1],Port=AG_Edge_Port_List[i],MappedTasks = [],Scheduling={})  # UsedBandWidth
print "\tNODES: ",AG.nodes(data=False)
print "\tEDGES: ",AG.edges(data=False)
print("ARCHITECTURE GRAPH (AG) IS READY...")
pos=networkx.spring_layout(AG)
networkx.draw(AG,pos,with_labels=True,node_size=1200)
plt.savefig("GraphDrawings/AG.png")
plt.clf()
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
NoCRG=Routing.GenerateNoCRouteGraph(AG,SHM,TurnModel,DebugDetails)
if NoCRG is not False:
    ################################################
    # clustered task graph
    CTG=copy.deepcopy(Clustering.TaskClusterGeneration(len(PE_List), DebugDetails))
    if Clustering.InitialClustering(TG, CTG, MaXBandWidth):
        (BestClustering,BestTaskGraph)= Clustering.ClusteringOptimization_LocalSearch(TG, CTG, 1000, MaXBandWidth)
        TG= copy.deepcopy(BestTaskGraph)
        CTG= copy.deepcopy(BestClustering)
        del BestClustering
        del BestTaskGraph
        Clustering_Functions.DoubleCheckCTG(TG,CTG)
        Clustering_Functions.ReportCTG(CTG,"CTG_PostOpt.png")
        if Mapping.MakeInitialMapping(TG,CTG,AG,NoCRG,True):
            Scheduler.ScheduleAll(TG,AG,True,DebugDetails)
            Scheduling_Functions.ReportMappedTasks(AG)
            Mapping_Functions.CostFunction(TG,AG,True)
            #(BestTG,BestCTG,BestAG)=Mapping.OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,1000,True,False)
            (BestTG,BestCTG,BestAG)=Mapping.OptimizeMappingIterativeLocalSearch(TG,CTG,AG,NoCRG,10,100,True,False)
            TG= copy.deepcopy(BestTG)
            CTG= copy.deepcopy(BestCTG)
            AG= copy.deepcopy(BestAG)
            del BestTG
            del BestCTG
            del BestAG
        else:
            Mapping_Functions.ReportMapping(AG)
            print "==========================================="

    else :
        print "Initial Clustering Failed...."