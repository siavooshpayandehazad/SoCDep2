# Copyright (C) 2015 Siavoosh Payandeh Azad
import PackageFile

################################################
#          Program  Config
################################################
ProgramRunTime = 900      # in cycles
DebugInfo = False
DebugDetails = False

TestMode = False
MemoryProfiler = False
EventDrivenFaultInjection = True
################################################
#          TG Config
################################################
# TG_Type can be: 'RandomDependent','RandomIndependent','Manual', 'FromDOTFile', 'GenericTraffic'
TG_Type = 'RandomDependent'
# For Generic Traffic:
generic_traffic = 'random_uniform'
injection_rate = 1
# For Random TG_Type:
NumberOfTasks = 25
NumberOfCriticalTasks = 0
NumberOfEdges = 35
WCET_Range = 25
EdgeWeightRange = 5
Release_Range = 5      # task release time range
tg_random_seed = 1000
# The following is only for Manual TG_Type:
# Note::    if you have High-critical tasks in your TG, make sure that you have checked partitioning options for the
#           network.
Task_List = [0, 1, 2, 3, 4, 5, 6, 7]
Task_WCET_List = [30, 30, 20, 40, 10, 5, 15, 20]
Task_Criticality_List = ['L', 'L', 'L', 'L', 'L', 'L', 'L', 'L']
TG_Edge_List = [(1, 2), (1, 3), (2, 5), (0, 5), (4, 7), (4, 3), (1, 6), (0, 6)]
TG_Edge_Weight = [5, 9, 4, 7, 5, 3, 5, 1]

# TG DOT FILE PATH
# you can use this one: http://express.ece.ucsb.edu/benchmark/jpeg/h2v2_smooth_downsample.html
# as example...
TG_DOT_Path = 'Something.dot'
################################################
#          AG Config
################################################
# AG_Type can be : 'Generic','Manual'
AG_Type = 'Generic'
# Todo: virtual channel
VirtualChannelNum = 0
# in case of Generic AG_type
# available topologies: 2DTorus, 2DMesh, 2DLine, 2DRing, 3DMesh
NetworkTopology = '2DMesh'
Network_X_Size = 3
Network_Y_Size = 3
Network_Z_Size = 1

# this is just for double check...
if '2D' in NetworkTopology:
    Network_Z_Size = 1

# Only for Manual AG_Type:
PE_List = [0, 1, 2, 3]
AG_Edge_List = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 2), (3, 1)]
# AG_Edge_Port_List shows which port of each router is connected to which port of the other on every link
AG_Edge_Port_List = [('E', 'W'), ('S', 'N'), ('W', 'E'), ('S', 'N'), ('N', 'S'), ('E', 'W'), ('W', 'E'), ('N', 'S')]

################################################
#          VL Config
################################################
FindOptimumAG = False
# Available Choices: 'LocalSearch', 'IterativeLocalSearch'
VL_OptAlg = "LocalSearch"
AG_Opt_Iterations_ILS = 10
AG_Opt_Iterations_LS = 10
# Number of Vertical Links
VerticalLinksNum = 20
################################################
#          Routing Config
################################################
# Todo: introduce more turn models
# Available Turn Models :
#         2D Turn Models: XY_TurnModel, WestFirst_TurnModel, NorthLast_TurnModel, NegativeFirst2D_TurnModel
#         3D Turn Models: XYZ_TurnModel, NegativeFirst3D_TurnModel
UsedTurnModel = PackageFile.XY_TurnModel
# Available choices: 'MinimalPath', 'NonMinimalPath'
RotingType = 'MinimalPath'
RoutingFilePath = "User_Inputs/RoutingFile.txt"
SetRoutingFromFile = False
# Flow control switch can be: "StoreAndForward" or "Wormhole"
FlowControl = "Wormhole"
################################################
#          Dark Silicon  Config
################################################
DarkSiliconPercentage = 0
################################################
#          SHM  Config
################################################
# Do not change if you have conventional 2D NoC


def setup_turns_health():
    global TurnsHealth
    if '2D' in NetworkTopology:
        TurnsHealth = PackageFile.TurnsHealth_2DNetwork
        if not SetRoutingFromFile:
            for Turn in PackageFile.FULL_TurnModel_2D:
                if Turn not in UsedTurnModel:
                    if Turn in TurnsHealth.keys():
                        TurnsHealth[Turn] = False
    elif '3D' in NetworkTopology:
        TurnsHealth = PackageFile.TurnsHealth_3DNetwork
        if not SetRoutingFromFile:
            for Turn in PackageFile.FULL_TurnModel_3D:
                if Turn not in UsedTurnModel:
                    if Turn in TurnsHealth.keys():
                        TurnsHealth[Turn] = False
    return None

TurnsHealth = {}
setup_turns_health()
# ==========================
# Number of Unreachable-Rectangles
NumberOfRects = 5
# ==========================
# Here you can break things as initial defects...
# ==========================
# Sample for 2X2 network:
# ListOfBrokenLinks = [(0, 1), (0, 2)]
# Sample for 4X4 network:
# ListOfBrokenLinks = [(0, 1), (2, 5), (4, 7)]
# For those who don't need broken links
ListOfBrokenLinks = []
# Some random broken link
# ListOfBrokenLinks = [(0, 1), (22, 21)]
# ==========================
# List of broken PE
ListOfBrokenPEs = []
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
# I know its a dictionary
# ListOfAgedPEs = {3: 0.3, 2: 0.1}
ListOfAgedPEs = {}
# ==========================
MaxTemp = 100
################################################
#          Clustering Function  Config
################################################
Clustering_Optimization = True     # If false, Turns the clustering off. Each Cluster would have only one Task in it.
ClusteringIteration = 70
ctg_random_seed = 100
Clustering_Report = False
Clustering_DetailedReport = False
# here you can change the type of cost function used for Clustering the available cost functions are:
# 'SD' = Com_Weight_SD + Node_Util_SD
# 'SD+MAX' = Com_Weight_SD + MaxComWeight + Node_Util_SD + MaxNodeUtil
# 'MAX' = MaxComWeight + MaxNodeUtil
# 'MAXCOM' = MaxComWeight
# 'AVGUTIL' = sum(ClusterUtilization)/len(ClusterUtilization)
# 'SUMCOM' = sum(CommunicationWeight)   This one is really funny. one thinks it would converge to a point that
# it puts every task in one cluster. however, it usually gets into local minima. and the result is really interesting
Clustering_CostFunctionType = 'MAX'

# RandomTaskMove: randomly chooses a task from a cluster and moves it to another random cluster
# Swap: randomly chooses a 2 tasks from 2 clusters and Swaps them
# Circulate: randomly chooses a N tasks from N clusters and Circulates them (is not implemented yet)
ClusteringOptMove = 'RandomTaskMove'
CTG_CirculationLength = 3
################################################
#          Mapping Function  Config
################################################
read_mapping_from_file = False
mapping_file_path = "mapping_report.txt"
# Mapping_Function can be : 'MinMin','MaxMin','MinExecutionTime','MinimumCompletionTime'
#                           'LocalSearch','IterativeLocalSearch','SimulatedAnnealing', 'NMap'
Mapping_Function = 'SimulatedAnnealing'
LocalSearchIteration = 150
IterativeLocalSearchIterations = 5
mapping_random_seed = 2000
#######################
SimulatedAnnealingIteration = 1000
SA_InitialTemp = 20
SA_StopTemp = 1             # Stops annealing earlier if reaches this temp
SA_ReportSolutions = False   # if True, it prints every accepted move to console
# Available Annealing Schedule: 'Linear', 'Exponential', 'Adaptive', 'Markov', 'Logarithmic', 'Aart', 'Huang'
SA_AnnealingSchedule = 'Adaptive'
# Termination Criteria Could be either 'StopTemp' or 'IterationNum'
TerminationCriteria = 'StopTemp'
# --------------------------

if SA_AnnealingSchedule == 'Linear':
    pass
elif SA_AnnealingSchedule == 'Exponential':
    SA_Alpha = 0.9995
elif SA_AnnealingSchedule == 'Logarithmic':
    LogCoolingConstant = 10       # c should be greater than or equal to the largest energy barrier in the problem
elif SA_AnnealingSchedule == 'Adaptive':
    CostMonitorQueSize = 2000
    SlopeRangeForCooling = 0.02     # If the slope falls between SlopeRangeForCooling and 0, the SA
    #                                 starts cooling with rate of alpha.
    # A counter would count number of steps moved with slope = 0. when the counter reaches MaxSteadyState,
    # the process terminates
    MaxSteadyState = 30000          # 5-10% of the iteration numbers would makes sense
    SA_Alpha = 0.9999
elif SA_AnnealingSchedule == 'Markov':
    MarkovNum = 2000
    MarkovTempStep = 1.0        # this is the amount of Temp decrease that the system would have after MarkovNum Steps
elif SA_AnnealingSchedule == 'Aart':
    # The number K in Aart's cooling schedule is determined by CostMonitorQueSize
    CostMonitorQueSize = 2000
    Delta = 0.05                # smaller Delta would result in slower annealing
    SA_Alpha = 0.999            # if we have a queue with standard deviation = 0, we cool with this factor
elif SA_AnnealingSchedule == 'Huang':
    Delta = 0.05                # smaller Delta would result in slower annealing
    CostMonitorQueSize = 2000
    HuangAlpha = 0.5
    HuangN = 30
    HuangTargetValue1 = 45      # should be equal to 3*erf(alpha)*N
    HuangTargetValue2 = 45      # should be equal to 3*(1-erf(alpha))*N
    SA_Alpha = 0.999            # if we have a queue with standard deviation = 0, we cool with this factor

######################
# this is used for mapping frame generation. we need some upper bound for knowing how many digits '
# we need in the file name or when arranging by name, doesnt show in a nice manner
if Mapping_Function == 'LocalSearch':
    MaxNumberOfIterations = LocalSearchIteration
elif Mapping_Function == 'IterativeLocalSearch':
    MaxNumberOfIterations = LocalSearchIteration * IterativeLocalSearchIterations
elif Mapping_Function == 'SimulatedAnnealing':
    MaxNumberOfIterations = SimulatedAnnealingIteration
######################
# here you can change the type of cost function used for mapping the available cost functions are:
# 'SD' = Com_MakeSpan_SD + Node_MakeSpan_SD
# 'Node_SD' = Node_MakeSpan_SD
# 'Node_Util_SD' = node_util_sd
# 'Link_SD' = Com_MakeSpan_SD
# 'MAX' = MaxLinkMakeSpan + MaxNodeMakeSpan
# 'SD+MAX' = Link_MakeSpan_SD + MaxLinkMakeSpan + Node_MakeSpan_SD + MaxNodeMakeSpan
# 'CONSTANT' = 1   ---> can be used if user needs only distance
Mapping_CostFunctionType = 'Node_Util_SD'
# if 'DistanceBetweenMapping' is true => Cost += Hamming distance between the current
# solution and the neighbour solution
DistanceBetweenMapping = False
################################################
#          Scheduling  Config
################################################
Communication_SlackCount = 0      # this is used for number of repetitions of the critical packets
Task_SlackCount = 0               # this is used for number of repetitions of the critical tasks
################################################
#          System's Fault  Config
################################################
MTTF = None     # Mean time to failure in seconds have not used MTTF yet...
MTBF = 1       # Mean time between failures in clock cycles
SD4MTBF = 0.1   # Standard deviation for Distribution of faults in a normal distribution
# ------------------------
classification_method = "counter_threshold"     # can be "counter_threshold" or "machine_learning"
health_counter_threshold = 4
fault_counter_threshold = 2
intermittent_counter_threshold = 2
enable_link_counters = True
enable_router_counters = False
enable_pe_counters = False
error_correction_rate = 0.8
################################################
#           Network Partitioning
################################################
EnablePartitioning = False
VirtualBrokenLinksForNonCritical = []
VirtualBrokenLinksForCritical = []
# Critical Region Nodes:
# for 6X6 network example no 2 of ReCoSoc Paper
if EnablePartitioning:
    CriticalRegionNodes = [16, 17, 21, 22, 23, 28, 29]
    GateToNonCritical = [15, 27]
    GateToCritical = [20]
else:
    CriticalRegionNodes = []
    GateToNonCritical = []
    GateToCritical = []
    GateToCritical = []
# For 6X6 network: (This is the Example scenario no. 2 in ReCoSoC paper)
# ListOfBrokenLinks += [(35, 29), (29, 35), (34, 28), (28, 34), (33, 27), (11, 17), (17, 11), (10, 16), (16, 10),
#                      (9, 15), (14, 15), (20, 26), (20, 19), (20, 14), (26, 27)]
# The virtual broken links for Non critical is not quite right in the ReCoSoC paper for the case of gateways
# To automatic generation of rectangles for the gateways can be fixed with the following workaround
# we have to break the links between Gateways and the nodes on the region that gateway should not send
# data to.
# VirtualBrokenLinksForNonCritical = [(20, 21), (27, 28), (27, 21), (15, 21), (15, 16)]
# VirtualBrokenLinksForCritical = [(27, 33), (27, 26), (15, 14), (15, 9)]
###############################################
#           PMCG Config
###############################################
GeneratePMCG = False
# set to False if you need Sequentially diagnosable PMCG
OneStepDiagnosable = False
# one-step t-fault diagnosable system, if set to None, default value would be
#                                 (n-1)/2
TFaultDiagnosable = None
NodeTestExeTime = 2
NodeTestComWeight = 2

###############################################
#           VISUALIZATION Config
###############################################
RG_Draw = False
PMCG_Drawing = False
TTG_Drawing = False
Mapping_Dstr_Drawing = False
Mapping_Drawing = False
Scheduling_Drawing = False
SHM_Drawing = False          # if True generates SHM Drawing
GenMappingFrames = False    # If True, generates the frames for animation
FrameResolution = 20        # Resolution in dpi. for resolutions above 50, text is added to the tasks
