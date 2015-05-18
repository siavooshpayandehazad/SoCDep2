
__author__ = 'siavoosh'
import matplotlib.pyplot as plt
import networkx
import copy
from Scheduler import Clustering
from Scheduler import Scheduler
from Scheduler import Mapping
from SystemHealthMonitoring import SystemHealthMonitor
from TaskGraphUtilities import Task_Graph_Reports
from TaskGraphUtilities import TG_Functions
from RoutingAlgorithms import Routing
#from SystemHealthMonitoring import SystemHealthMonitor
# here im going to tryout my initial idea about scheduling stuff...
# probably should import the files from the previous project...

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

DebugDetails=False
MaXBandWidth=10

print "DEBUG DETAILS:", DebugDetails
print "MAXIMUM LINK BAND WIDTH:", MaXBandWidth
print "==========================================="

print("PREPARING A TASK GRAPH (TG)...")
TG=networkx.DiGraph()
Task_List = [0, 1, 2, 3, 4, 5, 6, 7]
Task_WCET_List=[30, 30, 20, 40, 10, 5, 15, 20]
Task_Criticality_List=['H', 'L', 'H', 'L', 'L', 'H', 'L', 'L']
TG_Edge_List=[(1,2), (1,3), (2,5), (0,5), (4,7), (4,3), (1,6), (0,6)]
TG_Edge_Weight=[5, 9, 4, 7, 5, 3, 5, 1]
Edge_Criticality_List=['L', 'L', 'H', 'H', 'L', 'L', 'L', 'L']

for i in range(0,len(Task_List)):
    TG.add_node(Task_List[i],WCET=Task_WCET_List[i],Criticality=Task_Criticality_List[i],Cluster=None,Node=None,Priority=None)

for i in range(0,len(TG_Edge_List)):
    TG.add_edge(TG_Edge_List[i][0],TG_Edge_List[i][1],Criticality=Edge_Criticality_List[i],Link=[],ComWeight=TG_Edge_Weight[i])  # Communication weight
TG_Functions.AssignPriorities(TG)
print("TASK GRAPH (TG) IS READY...")
Task_Graph_Reports.ReportTaskGraph(TG)
Task_Graph_Reports.DrawTaskGraph(TG,TG_Edge_List,TG_Edge_Weight)

################################################
print "PREPARING AN ARCHITECTURE GRAPH (AG)..."
AG=networkx.DiGraph()
PE_List = [0, 1, 2, 3]
AG_Edge_List=[(0,1), (0,2), (1,0), (1,3), (2,0), (2,3), (3,2), (3,1)]
AG_Edge_Port_List=[('W','E'), ('S','N'), ('E','W'), ('S','N'), ('N','S'), ('W','E'), ('E','W'), ('N','S')]
for PE in PE_List:
    AG.add_node(PE,MappedTasks = [],Scheduling={},Utilization=0)

for i in range(0,len(AG_Edge_List)):
    EDGE = AG_Edge_List[i]
    AG.add_edge(EDGE[0],EDGE[1],Port=AG_Edge_Port_List[i],MappedTasks = [],Scheduling={})  # UsedBandWidth
print "\tNODES: ",AG.nodes(data=DebugDetails)
print "\tEDGES: ",AG.edges(data=DebugDetails)
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
TurnModel=['E2N','E2S','W2N','W2S']
SHM.SHM.edge[0][1]['LinkHealth']=False
NoCRG=Routing.GenerateNoCRouteGraph(AG,SHM,TurnModel)
print Routing.FindRouteInRouteGraph(NoCRG,0,3)
print "==========================================="
################################################
CTG=networkx.DiGraph()   # clustered task graph
Clustering.TaskClusterGeneration(TG, CTG, len(PE_List), DebugDetails)
if Clustering.InitialClustering(TG, CTG, MaXBandWidth):
    print "==========================================="
    (BestSolution,BestTaskGraph)=Clustering.ClusteringOptimization_LocalSearch(TG, CTG, 1000, MaXBandWidth)
    TG= copy.deepcopy(BestTaskGraph)
    CTG= copy.deepcopy(BestSolution)
    Clustering.DoubleCheckCTG(TG,CTG)
    Clustering.ReportCTG(CTG,"CTG_PostOpt.png")
    print "==========================================="
    if Mapping.MakeInitialMapping(TG,CTG,AG,NoCRG):
        Mapping.ReportMapping(AG)
        print "==========================================="
        Task_Graph_Reports.ReportTaskGraph(TG)
        Scheduler.ScheduleAll(TG,AG,True)
        Scheduler.ReportMappedTasks(AG)
        print "==========================================="
        Mapping.CostFunction(TG,AG,True)
        Mapping.OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,100,False)
    else:
        Mapping.ReportMapping(AG)
        print "==========================================="
else :
    print "Initial Clustering Failed...."



