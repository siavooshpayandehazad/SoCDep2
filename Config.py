__author__ = 'siavoosh'

################################################
#          Debug  Config
################################################
DebugInfo = True
DebugDetails = False

################################################
#          TG  Config
################################################
# TG_Type can be: 'RandomDependent','RandomIndependent','Manual'
TG_Type='RandomIndependent'
#For Random TG_Type:
NumberOfTasks= 10
NumberOfEdges= 15
WCET_Range= 30
EdgeWeightRange= 7

#Only for Manual TG_Type:
Task_List = [0, 1, 2, 3, 4, 5, 6, 7]
Task_WCET_List=[30, 30, 20, 40, 10, 5, 15, 20]
Task_Criticality_List=['H', 'L', 'H', 'L', 'L', 'H', 'L', 'L']
TG_Edge_List=[(1,2), (1,3), (2,5), (0,5), (4,7), (4,3), (1,6), (0,6)]
TG_Edge_Weight=[5, 9, 4, 7, 5, 3, 5, 1]
################################################
#          AG  Config
################################################
# AG_Type can be : 'Generic','Manual'
AG_Type='Generic'

VirtualChannelNum = 0
# in case of Generic AG_type
# available topologies: 2DTorus, 2DMesh, 2DLine, 2DRing
NetworkTopology='2DMesh'
Network_X_Size=2
Network_Y_Size=2
Network_Z_Size=0
# Only for Manual AG_Type:
PE_List = [0, 1, 2, 3]
AG_Edge_List=[(0,1), (0,2), (1,0), (1,3), (2,0), (2,3), (3,2), (3,1)]
#AG_Edge_Port_List shows which port of each router is connected to which port of the other on every link
AG_Edge_Port_List=[('E','W'), ('S','N'), ('W','E'), ('S','N'), ('N','S'), ('E','W'), ('W','E'), ('N','S')]
################################################
#          Mapping Function  Config
################################################
# AG_Type can be : 'MinMin','MaxMin','LocalSearch','IterativeLocalSearch'
Mapping_Function='MinMin'

################################################
#          Routing  Config
################################################
# Todo: introduce more turn models
FULL_TurnModel=['E2N','E2S','W2N','W2S','S2W','S2E','N2W','N2E']
XY_TurnModel=['E2N','E2S','W2N','W2S']
# at the moment there is no support adaptive routing algorithm
WestFirst_TurnModel=[]
EastFirst_TurnModel=[]

################################################
#          SHM  Config
################################################
TurnsHealth={"N2W":True,"N2E":True,"S2W":True,"S2E":True,
            "W2N":True,"W2S":True,"E2N":True,"E2S":True}

ListOfBrokenLinks=[(0,1),(0,2)]