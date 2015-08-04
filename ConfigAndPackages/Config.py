# Copyright (C) 2015 Siavoosh Payandeh Azad
import PackageFile

################################################
#          Program  Config
################################################
ProgramRunTime = 9      # in seconds
DebugInfo = True
DebugDetails = False
LoGDirectory = "LOGS"
TestMode = True
EventDrivenFaultInjection = False
################################################
#          TG  Config
################################################
# TG_Type can be: 'RandomDependent','RandomIndependent','Manual'
TG_Type = 'RandomDependent'
# For Random TG_Type:
NumberOfTasks = 25
NumberOfCriticalTasks = 0
NumberOfEdges = 20
WCET_Range = 15
EdgeWeightRange = 7
Release_Range = 5      # task release time range
# The following is only for Manual TG_Type:
# Note::    if you have High-critical tasks in your TG, make sure that you have checked partitioning options for the
#           network.
Task_List = [0, 1, 2, 3, 4, 5, 6, 7]
Task_WCET_List = [30, 30, 20, 40, 10, 5, 15, 20]
Task_Criticality_List = ['H', 'L', 'H', 'L', 'L', 'H', 'L', 'L']
TG_Edge_List = [(1, 2), (1, 3), (2, 5), (0, 5), (4, 7), (4, 3), (1, 6), (0, 6)]
TG_Edge_Weight = [5, 9, 4, 7, 5, 3, 5, 1]
################################################
#          AG  Config
################################################
# AG_Type can be : 'Generic','Manual'
AG_Type = 'Generic'
# Todo: virtual channel
VirtualChannelNum = 0
# in case of Generic AG_type
# available topologies: 2DTorus, 2DMesh, 2DLine, 2DRing, 3DMesh
NetworkTopology = '3DMesh'
Network_X_Size = 3
Network_Y_Size = 3
Network_Z_Size = 3
# Only for Manual AG_Type:
PE_List = [0, 1, 2, 3]
AG_Edge_List = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 2), (3, 1)]
# AG_Edge_Port_List shows which port of each router is connected to which port of the other on every link
AG_Edge_Port_List = [('E', 'W'), ('S', 'N'), ('W', 'E'), ('S', 'N'), ('N', 'S'), ('E', 'W'), ('W', 'E'), ('N', 'S')]
################################################
#          Routing  Config
################################################
# Todo: introduce more turn models
# Available Turn Models : 'FULL_TurnModel', 'XY_TurnModel', 'WestFirst_TurnModel',
#                         'NorthLast_TurnModel', 'XYZ_TurnModel'
UsedTurnModel = PackageFile.XYZ_TurnModel
RoutingFilePath = "User_Inputs/RoutingFile.txt"
SetRoutingFromFile = False
################################################
#          SHM  Config
################################################
# Do not change if you have conventional 2D NoC
TurnsHealth = PackageFile.TurnsHealth_3DNetwork
if not SetRoutingFromFile:
    for Turn in PackageFile.FULL_TurnModel_3D:
        if Turn not in UsedTurnModel:
            if Turn in TurnsHealth.keys():
                TurnsHealth[Turn] = False
# ==========================
# Number of Unreachable-Rectangles
NumberOfRects = 5
# ==========================
# Here you can break things as initial defects...
# ==========================
# Sample for 2X2 network:
# ListOfBrokenLinks = [(0, 1), (0, 2)]
# Sample for 4X4 network:
# ListOfBrokenLinks = [(0, 1), (0, 4)]
# For those who don't need broken links
ListOfBrokenLinks = []
# Some random broken link
# ListOfBrokenLinks = [(0, 1), (22, 21)]
# ==========================
# List of broken PE
ListOfBrokenPEs = [1]
# ListOfBrokenPEs = []
# ==========================
# List of broken Turns
ListOfBrokenTurns = {}
# sample for broken turns
# ListOfBrokenTurns = {1: 'W2S', 2: 'W2S'}
# And I know its a dictionary
# ==========================
# For aging, we need to give the tool a dictionary of nodes and their speed down...
# so {1: 0.3} means that node 1's speed has decreased by 30% from its current state.
# I know its a dictionary too
ListOfAgedPEs = {3: 0.3, 2: 0.1}
################################################
#          Clustering Function  Config
################################################
Clustering_Optimization = True     # If false, Turns the clustering off. Each Cluster would have only one Task in it.
ClusteringIteration = 1000
Clustering_Report = False
Clustering_DetailedReport = False
# here you can change the type of cost function used for Clustering the available cost functions are:
# 'SD' = Com_Weight_SD + Node_Util_SD
# 'SD+MAX' = Com_Weight_SD + MaxComWeight + Node_Util_SD + MaxNodeUtil
Clustering_CostFunctionType = 'SD+MAX'
################################################
#          Mapping Function  Config
################################################
# Mapping_Function can be : 'MinMin','MaxMin','MinExecutionTime','MinimumCompletionTime'
#                           'LocalSearch','IterativeLocalSearch','SimulatedAnnealing', 'NMap'
Mapping_Function = 'SimulatedAnnealing'
LocalSearchIteration = 100
IterativeLocalSearchIterations = 20
#######################
SimulatedAnnealingIteration = 50000
SA_InitialTemp = 100
SA_StopTemp = 5             # Stops annealing earlier if reaches this temp
SA_ReportSolutions = False   # if True, it prints every accepted move to console
# Available Annealing Schedule: 'Linear', 'Exponential', 'Adaptive', 'Markov', 'Logarithmic', 'Aart', 'Huang'
SA_AnnealingSchedule = 'Huang'
# Termination Criteria Could be either 'StopTemp' or 'IterationNum'
TerminationCriteria = 'StopTemp'
# --------------------------
# only usable under Exponential and Adaptive and Aart and Huang's Schedule
SA_Alpha = 0.999
# --------------------------
# only for Markov Cooling
MarkovNum = 2000
MarkovTempStep = 1        # this is the amount of Temp decrease that the system would have after MarkovNum Steps
# --------------------------
# only for Aart's cooling schedule
# The number K in Aart's cooling schedule is determined by CostMonitorQueSize
Delta = 0.05     # smaller Delta would result in slower annealing

# only for Adaptive, Aart's and Huang's Cooling
CostMonitorQueSize = 2000
# --------------------------
# only for Huang Annealing Schedule
HuangAlpha = 0.5
HuangN = 30
HuangTargetValue1 = 45          # should be equal to 3*erf(alpha)*N
HuangTargetValue2 = 45          # should be equal to 3*(1-erf(alpha))*N
# --------------------------
# only for Adaptive Cooling
SlopeRangeForCooling = 0.02     # If the slope falls between SlopeRangeForCooling and 0, the SA
#                                 starts cooling with rate of alpha.
# A counter would count number of steps moved with slope = 0. when the counter reaches MaxSteadyState,
# the process terminates
MaxSteadyState = 30000          # 5-10% of the iteration numbers would makes sense
# --------------------------
# Only for Logarithmic cooling
LogCoolingConstant = 1000       # c should be greater than or equal to the largest energy barrier in the problem
######################
if Mapping_Function == 'LocalSearch':
    MaxNumberOfIterations = LocalSearchIteration
elif Mapping_Function == 'IterativeLocalSearch':
    MaxNumberOfIterations = LocalSearchIteration * IterativeLocalSearchIterations
elif Mapping_Function == 'SimulatedAnnealing':
    MaxNumberOfIterations = SimulatedAnnealingIteration

# here you can change the type of cost function used for mapping the available cost functions are:
# 'SD' = Com_MakeSpan_SD + Node_MakeSpan_SD
# 'SD+MAX' = Link_MakeSpan_SD + MaxLinkMakeSpan + Node_MakeSpan_SD + MaxNodeMakeSpan
# 'CONSTANT' = 1   ---> can be used if user needs only distance
Mapping_CostFunctionType = 'SD+MAX'
# if 'DistanceBetweenMapping' is true => Cost += Hamming distance between the current
# solution and the neighbour solution
DistanceBetweenMapping = False
################################################
#          Scheduling  Config
################################################
SlackCount = 1      # this is used for number of repetitions of the critical tasks
################################################
#          System's Fault  Config
################################################
MTTF = None     # Mean time to failure in seconds have not used MTTF yet...
MTBF = 2        # Mean time between failures in seconds
SD4MTBF = 0.1   # Standard deviation for Distribution of faults in a normal distribution
################################################
#           Network Partitioning
################################################
EnablePartitioning = False
if EnablePartitioning:
    # Critical Region Nodes:
    # for 6X6 network example no 2 of ReCoSoc Paper
    CriticalRegionNodes = [16, 17, 21, 22, 23, 28, 29]
    GateToNonCritical = [15, 27]
    GateToCritical = [20]
    # For 6X6 network: (This is the Example scenario no. 2 in ReCoSoC paper)
    ListOfBrokenLinks += [(35, 29), (29, 35), (34, 28), (28, 34), (33, 27), (11, 17), (17, 11), (10, 16), (16, 10),
                          (9, 15), (14, 15), (20, 26), (20, 19), (20, 14), (26, 27)]
    # The virtual broken links for Non critical is not quite right in the ReCoSoC paper for the case of gateways
    # To automatic generation of rectangles for the gateways can be fixed with the following workaround
    # we have to break the links between Gateways and the nodes on the region that gateway should not send
    # data to.
    VirtualBrokenLinksForNonCritical = [(20, 21), (27, 28), (27, 21), (15, 21), (15, 16)]
    VirtualBrokenLinksForCritical = [(27, 33), (27, 26), (15, 14), (15, 9)]
else:
    # No regions:
    CriticalRegionNodes = []
    GateToNonCritical = []
    GateToCritical = []
    # We don't need additional broken links
    ListOfBrokenLinks += []
    VirtualBrokenLinksForNonCritical = []
    VirtualBrokenLinksForCritical = []
###############################################
#           PMCG Config
###############################################
OneStepDiagonosable = False     # set to False if you need Sequentially diagnosable PMCG
TFaultDiagnosable = None        # one-step t-fault diagnosable system, if set to none, default value would be
#                                 (n-1)/2
NodeTestExeTime = 2
NodeTestComWeight = 2
###############################################
#           VISUALIZATION Config
###############################################
GenMappingFrames = False    # If True, generates the frames for animation
FrameResolution = 20        # Resolution in dpi. for resolutions above 50, text is added to the tasks