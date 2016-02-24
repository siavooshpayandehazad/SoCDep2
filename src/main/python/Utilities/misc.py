# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import Config, PackageFile
import os
import ConfigParser
import ast


def draw_logo():
    print ("================================================================================================" +
           "===================")
    print ("  _________      .__               .___    .__             ____    ________                     " +
           "              .___")
    print (" /   _____/ ____ |  |__   ____   __| _/_ __|  |   ____    /  _ \   \______ \   ____ ______   ___" +
           "_   ____    __| _/")
    print (" \_____  \_/ ___\|  |  \_/ __ \ / __ |  |  \  | _/ __ \   >  _ </\  |    |  \_/ __ \\\\____ \_/ " +
           "__ \ /    \  / __ | ")
    print (" _____/   \  \___|   Y  \  ___// /_/ |  |  /  |_\  ___/  /  <_\ \/  |    `   \  ___/|  |_> >  __" +
           "_/|   |  \/ /_/ | ")
    print ("/_______  /\___  >___|  /\___  >____ |____/|____/\___  > \_____\ \ /_______  /\___  >   __/ \___" +
           "  >___|  /\____ | ")
    print ("        \/     \/     \/     \/     \/               \/         \/         \/     \/|__|        " +
           "\/     \/      \/ ")
    print ("================================================================================================" +
           "===================")
    print ("AUTHORS:")
    print ("          SIAVOOSH PAYANDEH AZAD")
    print ("          RENE PIHLAK")
    print ("          BEHRAD NIAZMAND")
    print ("DATE:    MAY 2015")
    print ("THE GOAL OF THIS PROGRAM IS TO MAKE A PLATFORM FOR TESTING SOME ")
    print ("DEPENDABILITY MECHANISMS ON DIFFERENT ARCHITECTURES....")
    print ("Copyright (C) 2015-2016 as collective work done by Siavoosh Payandeh Azad, Rene Pihlak and Behrad Niazmand")
    print ("================================================================================")
    print ("DEBUG DETAILS: "+str(Config.DebugDetails))
    print ("DEBUG INFO: "+str(Config.DebugInfo))
    print ("===========================================")
    return None


def generate_file_directories():
    graph_directory = "GraphDrawings"
    if not os.path.isdir(graph_directory):
        os.makedirs(graph_directory)

    file_list = [png_file for png_file in os.listdir(graph_directory) if png_file.endswith(".png")]
    for png_file in file_list:
        os.remove(graph_directory+'/'+png_file)

    animation_directory = "GraphDrawings/Mapping_Animation_Material"
    if not os.path.isdir(animation_directory):
        os.makedirs(animation_directory)

    file_list = [png_file for png_file in os.listdir(animation_directory) if png_file.endswith(".png")]
    for png_file in file_list:
        os.remove(animation_directory+'/'+png_file)

    generated_files_directory = "Generated_Files"
    if not os.path.isdir(generated_files_directory):
        os.makedirs(generated_files_directory)

    file_list = [text_file for text_file in os.listdir(generated_files_directory) if text_file.endswith(".txt")]
    for text_file in file_list:
        os.remove(generated_files_directory+'/'+text_file)

    internal_files_directory = "Generated_Files/Internal"
    if not os.path.isdir(internal_files_directory):
        os.makedirs(internal_files_directory)
    file_list = [text_file for text_file in os.listdir(internal_files_directory) if text_file.endswith(".txt")]
    for text_file in file_list:
        os.remove(internal_files_directory+'/'+text_file)
    return None


def check_for_dependencies():
    for module in PackageFile.ImportModules:
        try:
            __import__(module)
        except ImportError:
            raise ImportError("MODULE "+str(module)+" DOES NOT EXIST...")
    print "ALL REQUIRED MODULES AVAILABLE..."
    return True


def update_config(config_file_path):
    try:
        config_file = open(config_file_path, 'r')
        config_file.close()
    except IOError:
        print ('CAN NOT OPEN config_file')

    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.read(config_file_path)
    # ------------------------------------------------
    #               Program_Config
    # ------------------------------------------------
    Config.enable_simulator = config.getboolean("Program_Config", "enable_simulator")
    Config.ProgramRunTime = config.getint("Program_Config", "ProgramRunTime")
    Config.DebugInfo = config.getboolean("Program_Config", "DebugInfo")
    Config.DebugDetails = config.getboolean("Program_Config", "DebugDetails")

    Config.TestMode = config.getboolean("Program_Config", "TestMode")
    Config.MemoryProfiler = config.getboolean("Program_Config", "MemoryProfiler")
    Config.EventDrivenFaultInjection = config.getboolean("Program_Config", "EventDrivenFaultInjection")
    # ------------------------------------------------
    #               TG_Config
    # ------------------------------------------------
    Config.TG_Type = config.get("TG_Config", "TG_Type")

    Config.NumberOfTasks = config.getint("TG_Config", "NumberOfTasks")
    Config.NumberOfCriticalTasks = config.getint("TG_Config", "NumberOfCriticalTasks")
    Config.NumberOfEdges = config.getint("TG_Config", "NumberOfEdges")
    Config.WCET_Range = config.getint("TG_Config", "WCET_Range")
    Config.EdgeWeightRange = config.getint("TG_Config", "EdgeWeightRange")
    Config.Release_Range = config.getint("TG_Config", "Release_Range")      # task release time range
    Config.tg_random_seed = config.getint("TG_Config", "tg_random_seed")

    # Config.Task_List = map(int, config.get("TG_Config", "Task_List").split(","))
    # Config.Task_WCET_List = map(int, config.get("TG_Config", "Task_WCET_List").split(","))
    # Config.Task_Criticality_List = config.get("TG_Config", "Task_Criticality_List").split(",")
    # TG_Edge_List
    # TG_Edge_Weight
    # TG_DOT_Path

    # ------------------------------------------------
    #               AG_Config
    # ------------------------------------------------
    Config.AG_Type = config.get("AG_Config", "AG_Type")
    # VirtualChannelNum
    Config.NetworkTopology = config.get("AG_Config", "NetworkTopology")
    Config.Network_X_Size = config.getint("AG_Config", "Network_X_Size")
    Config.Network_Y_Size = config.getint("AG_Config", "Network_Y_Size")
    Config.Network_Z_Size = config.getint("AG_Config", "Network_Z_Size")
    # Config.PE_List = map(int, config.get("AG_Config", "PE_List").split(","))
    # AG_Edge_List
    # AG_Edge_Port_List

    # ------------------------------------------------
    #               VL_Config
    # ------------------------------------------------
    Config.FindOptimumAG = config.getboolean("VL_Config", "FindOptimumAG")
    Config.VL_OptAlg = config.get("VL_Config", "VL_OptAlg")
    Config.AG_Opt_Iterations_ILS = config.getint("VL_Config", "AG_Opt_Iterations_ILS")
    Config.AG_Opt_Iterations_LS = config.getint("VL_Config", "AG_Opt_Iterations_LS")
    Config.VerticalLinksNum = config.getint("VL_Config", "VerticalLinksNum")

    # ------------------------------------------------
    #               Routing_Config
    # ------------------------------------------------
    if config.get("Routing_Config", "UsedTurnModel") == "XY_TurnModel":
        Config.UsedTurnModel = PackageFile.XY_TurnModel
    elif config.get("Routing_Config", "UsedTurnModel") == "WestFirst_TurnModel":
        Config.UsedTurnModel = PackageFile.WestFirst_TurnModel
    elif config.get("Routing_Config", "UsedTurnModel") == "NorthLast_TurnModel":
        Config.UsedTurnModel = PackageFile.NorthLast_TurnModel
    elif config.get("Routing_Config", "UsedTurnModel") == "NegativeFirst2D_TurnModel":
        Config.UsedTurnModel = PackageFile.NegativeFirst2D_TurnModel
    elif config.get("Routing_Config", "UsedTurnModel") == "XYZ_TurnModel":
        Config.UsedTurnModel = PackageFile.XYZ_TurnModel
    elif config.get("Routing_Config", "UsedTurnModel") == "NegativeFirst3D_TurnModel":
        Config.UsedTurnModel = PackageFile.NegativeFirst3D_TurnModel
    else:
        raise ValueError("Turn Model not Available")

    Config.RotingType = config.get("Routing_Config", "RotingType")
    Config.RoutingFilePath = config.get("Routing_Config", "RoutingFilePath")
    Config.SetRoutingFromFile = config.getboolean("Routing_Config", "SetRoutingFromFile")
    Config.FlowControl = config.get("Routing_Config", "FlowControl")

    # ------------------------------------------------
    #               Dark_Sil_Config
    # ------------------------------------------------
    Config.DarkSiliconPercentage = config.getint("Dark_Sil_Config", "DarkSiliconPercentage")

    # ------------------------------------------------
    #               SHM_Config
    # ------------------------------------------------
    Config.NumberOfRects = config.getint("SHM_Config", "NumberOfRects")
    # ListOfBrokenLinks:
    Config.ListOfBrokenTurns = ast.literal_eval(config.get("SHM_Config", "ListOfBrokenTurns"))
    Config.MaxTemp = config.getint("SHM_Config", "MaxTemp")

    # ------------------------------------------------
    #               CTG_Config
    # ------------------------------------------------
    Config.Clustering_Optimization = config.getboolean("CTG_Config", "Clustering_Optimization")
    Config.ClusteringIteration = config.getint("CTG_Config", "ClusteringIteration")
    Config.ctg_random_seed = config.getint("CTG_Config", "ctg_random_seed")
    Config.Clustering_Report = config.getboolean("CTG_Config", "Clustering_Report")
    Config.Clustering_DetailedReport = config.getboolean("CTG_Config", "Clustering_DetailedReport")
    Config.Clustering_CostFunctionType = config.get("CTG_Config", "Clustering_CostFunctionType")
    Config.ClusteringOptMove = config.get("CTG_Config", "ClusteringOptMove")
    Config.CTG_CirculationLength = config.getint("CTG_Config", "CTG_CirculationLength")

    # ------------------------------------------------
    #               Mapping_Config
    # ------------------------------------------------
    Config.read_mapping_from_file = config.getboolean("Mapping_Config", "read_mapping_from_file")
    Config.mapping_file_path = config.get("Mapping_Config", "mapping_file_path")

    Config.Mapping_Function = config.get("Mapping_Config", "Mapping_Function")
    Config.LocalSearchIteration = config.getint("Mapping_Config", "LocalSearchIteration")
    Config.IterativeLocalSearchIterations = config.getint("Mapping_Config", "IterativeLocalSearchIterations")
    Config.mapping_random_seed = config.getint("Mapping_Config", "mapping_random_seed")

    Config.SimulatedAnnealingIteration = config.getint("Mapping_Config", "SimulatedAnnealingIteration")
    Config.SA_InitialTemp = config.getint("Mapping_Config", "SA_InitialTemp")
    Config.SA_StopTemp = config.getint("Mapping_Config", "SA_StopTemp")
    Config.SA_ReportSolutions = config.getboolean("Mapping_Config", "SA_ReportSolutions")

    Config.SA_AnnealingSchedule = config.get("Mapping_Config", "SA_AnnealingSchedule")
    Config.TerminationCriteria = config.get("Mapping_Config", "TerminationCriteria")
    Config.SA_Alpha = config.getfloat("Mapping_Config", "SA_Alpha")

    Config.LogCoolingConstant = config.getint("Mapping_Config", "LogCoolingConstant")
    Config.CostMonitorQueSize = config.getint("Mapping_Config", "CostMonitorQueSize")
    Config.SlopeRangeForCooling = config.getfloat("Mapping_Config", "SlopeRangeForCooling")
    Config.MaxSteadyState = config.getint("Mapping_Config", "MaxSteadyState")
    Config.MarkovNum = config.getfloat("Mapping_Config", "MarkovNum")
    Config.MarkovTempStep = config.getfloat("Mapping_Config", "MarkovTempStep")
    Config.Delta = config.getfloat("Mapping_Config", "Delta")
    Config.HuangAlpha = config.getfloat("Mapping_Config", "HuangAlpha")

    Config.HuangN = config.getint("Mapping_Config", "HuangN")
    Config.HuangTargetValue1 = config.getint("Mapping_Config", "HuangTargetValue1")
    Config.HuangTargetValue2 = config.getint("Mapping_Config", "HuangTargetValue2")

    Config.Mapping_CostFunctionType = config.get("Mapping_Config", "Mapping_CostFunctionType")
    Config.DistanceBetweenMapping = config.getboolean("Mapping_Config", "DistanceBetweenMapping")
    # ------------------------------------------------
    #               Scheduling_Config
    # ------------------------------------------------
    Config.Communication_SlackCount = config.getint("Scheduling_Config", "Communication_SlackCount")
    Config.Task_SlackCount = config.getint("Scheduling_Config", "Task_SlackCount")

    # ------------------------------------------------
    #               Fault_Config
    # ------------------------------------------------
    Config.MTBF = config.getfloat("Fault_Config", "MTBF")
    # Config.SD4MTBF = 0.2
    Config.classification_method = config.get("Fault_Config", "classification_method")
    Config.health_counter_threshold = config.getint("Fault_Config", "health_counter_threshold")
    Config.fault_counter_threshold = config.getint("Fault_Config", "fault_counter_threshold")
    Config.intermittent_counter_threshold = config.getint("Fault_Config", "intermittent_counter_threshold")
    Config.enable_link_counters = config.getboolean("Fault_Config", "enable_link_counters")
    Config.enable_router_counters = config.getboolean("Fault_Config", "enable_router_counters")
    Config.enable_pe_counters = config.getboolean("Fault_Config", "enable_pe_counters")
    Config.error_correction_rate = config.getfloat("Fault_Config", "error_correction_rate")

    # ------------------------------------------------
    #           Network_Partitioning
    # ------------------------------------------------
    Config.EnablePartitioning = config.getboolean("Network_Partitioning", "EnablePartitioning")

    # ------------------------------------------------
    #               PMCG_Config
    # ------------------------------------------------
    Config.GeneratePMCG = config.getboolean("PMCG_Config", "GeneratePMCG")
    Config.OneStepDiagnosable = config.getboolean("PMCG_Config", "OneStepDiagnosable")
    Config.TFaultDiagnosable = config.get("PMCG_Config", "TFaultDiagnosable")
    Config.NodeTestExeTime = config.getint("PMCG_Config", "NodeTestExeTime")
    Config.NodeTestComWeight = config.getint("PMCG_Config", "NodeTestComWeight")

    # ------------------------------------------------
    #               Viz_Config
    # ------------------------------------------------
    Config.RG_Draw = config.getboolean("Viz_Config", "RG_Draw")
    Config.PMCG_Drawing = config.getboolean("Viz_Config", "PMCG_Drawing")
    Config.TTG_Drawing = config.getboolean("Viz_Config", "TTG_Drawing")
    Config.Mapping_Dstr_Drawing = config.getboolean("Viz_Config", "Mapping_Dstr_Drawing")
    Config.Mapping_Drawing = config.getboolean("Viz_Config", "Mapping_Drawing")
    Config.Scheduling_Drawing = config.getboolean("Viz_Config", "Scheduling_Drawing")
    Config.SHM_Drawing = config.getboolean("Viz_Config", "SHM_Drawing")
    Config.GenMappingFrames = config.getboolean("Viz_Config", "GenMappingFrames")
    Config.FrameResolution = config.getint("Viz_Config", "FrameResolution")
    return None


def generate_configfile():
    cfg_file = open('Generated_Files/ConfigFile.txt', 'w')
    cnfgpars = ConfigParser.ConfigParser(allow_no_value=True)
    # ------------------------------------------------
    #               Program_Config
    # ------------------------------------------------
    cnfgpars.add_section('Program_Config')
    cnfgpars.set('Program_Config', 'enable_simulator', Config.enable_simulator)
    cnfgpars.set('Program_Config', 'ProgramRunTime', Config.ProgramRunTime)
    cnfgpars.set('Program_Config', 'DebugInfo', Config.DebugInfo)
    cnfgpars.set('Program_Config', 'DebugDetails', Config.DebugDetails)

    cnfgpars.set('Program_Config', 'TestMode', Config.TestMode)
    cnfgpars.set('Program_Config', 'MemoryProfiler', Config.MemoryProfiler)
    cnfgpars.set('Program_Config', 'EventDrivenFaultInjection', Config.EventDrivenFaultInjection)
    # ------------------------------------------------
    #               TG_Config
    # ------------------------------------------------
    cnfgpars.add_section('TG_Config')
    cnfgpars.set('TG_Config', 'TG_Type', Config.TG_Type)
    cnfgpars.set('TG_Config', 'NumberOfTasks', Config.NumberOfTasks)
    cnfgpars.set('TG_Config', 'NumberOfCriticalTasks', Config.NumberOfCriticalTasks)
    cnfgpars.set('TG_Config', 'NumberOfEdges', Config.NumberOfEdges)
    cnfgpars.set('TG_Config', 'WCET_Range', Config.WCET_Range)
    cnfgpars.set('TG_Config', 'EdgeWeightRange', Config.EdgeWeightRange)
    cnfgpars.set('TG_Config', 'Release_Range', Config.Release_Range)
    cnfgpars.set('TG_Config', 'tg_random_seed', Config.tg_random_seed)

    # ------------------------------------------------
    #               AG_Config
    # ------------------------------------------------
    cnfgpars.add_section('AG_Config')

    cnfgpars.set('AG_Config', 'AG_Type', Config.AG_Type)
    cnfgpars.set('AG_Config', 'NetworkTopology', Config.NetworkTopology)
    cnfgpars.set('AG_Config', 'Network_X_Size', Config.Network_X_Size)
    cnfgpars.set('AG_Config', 'Network_Y_Size', Config.Network_Y_Size)
    cnfgpars.set('AG_Config', 'Network_Z_Size', Config.Network_Z_Size)
    # VirtualChannelNum
    # Config.PE_List = map(int, config.get("AG_Config", "PE_List").split(","))
    # AG_Edge_List
    # AG_Edge_Port_List

    # ------------------------------------------------
    #               VL_Config
    # ------------------------------------------------
    cnfgpars.add_section('VL_Config')
    cnfgpars.set('VL_Config', 'FindOptimumAG', Config.FindOptimumAG)
    cnfgpars.set('VL_Config', 'VL_OptAlg', Config.VL_OptAlg)
    cnfgpars.set('VL_Config', 'AG_Opt_Iterations_ILS', Config.AG_Opt_Iterations_ILS)
    cnfgpars.set('VL_Config', 'AG_Opt_Iterations_LS', Config.AG_Opt_Iterations_LS)
    cnfgpars.set('VL_Config', 'VerticalLinksNum', Config.VerticalLinksNum)
    # ------------------------------------------------
    #               Routing_Config
    # ------------------------------------------------
    cnfgpars.add_section('Routing_Config')
    cnfgpars.set('Routing_Config', 'UsedTurnModel', Config.UsedTurnModel)

    if Config.UsedTurnModel == PackageFile.XY_TurnModel:
        cnfgpars.set('Routing_Config', 'UsedTurnModel', "XY_TurnModel")
    elif Config.UsedTurnModel == PackageFile.WestFirst_TurnModel:
        cnfgpars.set('Routing_Config', 'UsedTurnModel', "WestFirst_TurnModel")
    elif Config.UsedTurnModel == PackageFile.NorthLast_TurnModel:
        cnfgpars.set('Routing_Config', 'UsedTurnModel', "NorthLast_TurnModel")
    elif Config.UsedTurnModel == PackageFile.NorthLast_TurnModel:
        cnfgpars.set('Routing_Config', 'UsedTurnModel', "NorthLast_TurnModel")
    elif Config.UsedTurnModel == PackageFile.NegativeFirst2D_TurnModel:
        cnfgpars.set('Routing_Config', 'UsedTurnModel', "NegativeFirst2D_TurnModel")
    elif Config.UsedTurnModel == PackageFile.XYZ_TurnModel:
        cnfgpars.set('Routing_Config', 'UsedTurnModel', "XYZ_TurnModel")
    elif Config.UsedTurnModel == PackageFile.NegativeFirst3D_TurnModel:
        cnfgpars.set('Routing_Config', 'UsedTurnModel', "NegativeFirst3D_TurnModel")
    else:
        raise ValueError("Turn Model not Available")

    cnfgpars.set('Routing_Config', 'RotingType', Config.RotingType)
    cnfgpars.set('Routing_Config', 'RoutingFilePath', Config.RoutingFilePath)
    cnfgpars.set('Routing_Config', 'SetRoutingFromFile', Config.SetRoutingFromFile)
    cnfgpars.set('Routing_Config', 'FlowControl', Config.FlowControl)
    # ------------------------------------------------
    #               Dark_Sil_Config
    # ------------------------------------------------
    cnfgpars.add_section('Dark_Sil_Config')
    cnfgpars.set('Dark_Sil_Config', 'DarkSiliconPercentage', Config.DarkSiliconPercentage)
    # ------------------------------------------------
    #               SHM_Config
    # ------------------------------------------------
    cnfgpars.add_section('SHM_Config')
    cnfgpars.set('SHM_Config', 'NumberOfRects', Config.NumberOfRects)
    # ListOfBrokenLinks
    cnfgpars.set('SHM_Config', 'ListOfBrokenTurns', Config.ListOfBrokenTurns)
    cnfgpars.set('SHM_Config', 'MaxTemp', Config.MaxTemp)
    # ------------------------------------------------
    #               CTG_Config
    # ------------------------------------------------
    cnfgpars.add_section('CTG_Config')
    cnfgpars.set('CTG_Config', 'Clustering_Optimization', Config.Clustering_Optimization)
    cnfgpars.set('CTG_Config', 'ClusteringIteration', Config.ClusteringIteration)
    cnfgpars.set('CTG_Config', 'ctg_random_seed', Config.ctg_random_seed)
    cnfgpars.set('CTG_Config', 'Clustering_Report', Config.Clustering_Report)
    cnfgpars.set('CTG_Config', 'Clustering_DetailedReport', Config.Clustering_DetailedReport)
    cnfgpars.set('CTG_Config', 'Clustering_CostFunctionType', Config.Clustering_CostFunctionType)
    cnfgpars.set('CTG_Config', 'ClusteringOptMove', Config.ClusteringOptMove)
    cnfgpars.set('CTG_Config', 'CTG_CirculationLength', Config.CTG_CirculationLength)
    # ------------------------------------------------
    #               Mapping_Config
    # ------------------------------------------------
    cnfgpars.add_section('Mapping_Config')
    cnfgpars.set('Mapping_Config', 'read_mapping_from_file', Config.read_mapping_from_file)
    cnfgpars.set('Mapping_Config', 'mapping_file_path', Config.mapping_file_path)
    cnfgpars.set('Mapping_Config', 'Mapping_Function', Config.Mapping_Function)
    cnfgpars.set('Mapping_Config', 'LocalSearchIteration', Config.LocalSearchIteration)
    cnfgpars.set('Mapping_Config', 'iterativelocalsearchiterations', Config.IterativeLocalSearchIterations)
    cnfgpars.set('Mapping_Config', 'mapping_random_seed', Config.mapping_random_seed)
    cnfgpars.set('Mapping_Config', 'SimulatedAnnealingIteration', Config.SimulatedAnnealingIteration)
    cnfgpars.set('Mapping_Config', 'SA_InitialTemp', Config.SA_InitialTemp)
    cnfgpars.set('Mapping_Config', 'SA_StopTemp', Config.SA_StopTemp)
    cnfgpars.set('Mapping_Config', 'SA_ReportSolutions', Config.SA_ReportSolutions)
    cnfgpars.set('Mapping_Config', 'SA_AnnealingSchedule', Config.SA_AnnealingSchedule)
    cnfgpars.set('Mapping_Config', 'TerminationCriteria', Config.TerminationCriteria)
    cnfgpars.set('Mapping_Config', 'LogCoolingConstant',
                 Config.LogCoolingConstant if hasattr(Config, 'LogCoolingConstant') else 0)
    cnfgpars.set('Mapping_Config', 'CostMonitorQueSize',
                 Config.CostMonitorQueSize if hasattr(Config, 'CostMonitorQueSize') else 0)
    cnfgpars.set('Mapping_Config', 'MaxSteadyState',
                 Config.MaxSteadyState if hasattr(Config, 'MaxSteadyState') else 0)
    cnfgpars.set('Mapping_Config', 'MarkovNum',
                 Config.MarkovNum if hasattr(Config, 'MarkovNum') else 0)
    cnfgpars.set('Mapping_Config', 'HuangN',
                 Config.HuangN if hasattr(Config, 'HuangN') else 0)
    cnfgpars.set('Mapping_Config', 'HuangTargetValue1',
                 Config.HuangTargetValue1 if hasattr(Config, 'HuangTargetValue1') else 0)
    cnfgpars.set('Mapping_Config', 'HuangTargetValue2',
                 Config.HuangTargetValue2 if hasattr(Config, 'HuangTargetValue2') else 0)
    cnfgpars.set('Mapping_Config', 'SA_Alpha',
                 Config.SA_Alpha if hasattr(Config, 'SA_Alpha') else 0)
    cnfgpars.set('Mapping_Config', 'SlopeRangeForCooling',
                 Config.SlopeRangeForCooling if hasattr(Config, 'SlopeRangeForCooling') else 0)
    cnfgpars.set('Mapping_Config', 'MarkovTempStep',
                 Config.MarkovTempStep if hasattr(Config, 'MarkovTempStep') else 0)
    cnfgpars.set('Mapping_Config', 'Delta',
                 Config.Delta if hasattr(Config, 'Delta') else 0)
    cnfgpars.set('Mapping_Config', 'HuangAlpha',
                 Config.HuangAlpha if hasattr(Config, 'HuangAlpha') else 0)
    cnfgpars.set('Mapping_Config', 'Mapping_CostFunctionType', Config.Mapping_CostFunctionType)
    cnfgpars.set('Mapping_Config', 'DistanceBetweenMapping', Config.DistanceBetweenMapping)
    # ------------------------------------------------
    #               Scheduling_Config
    # ------------------------------------------------
    cnfgpars.add_section('Scheduling_Config')
    cnfgpars.set('Scheduling_Config', 'Communication_SlackCount', Config.Communication_SlackCount)
    cnfgpars.set('Scheduling_Config', 'Task_SlackCount', Config.Task_SlackCount)
    # ------------------------------------------------
    #               Fault_Config
    # ------------------------------------------------
    cnfgpars.add_section('Fault_Config')
    cnfgpars.set('Fault_Config', 'MTBF', Config.MTBF)
    cnfgpars.set('Fault_Config', 'classification_method', Config.classification_method)
    cnfgpars.set('Fault_Config', 'health_counter_threshold', Config.health_counter_threshold)
    cnfgpars.set('Fault_Config', 'fault_counter_threshold', Config.fault_counter_threshold)
    cnfgpars.set('Fault_Config', 'intermittent_counter_threshold', Config.intermittent_counter_threshold)
    cnfgpars.set('Fault_Config', 'enable_link_counters', Config.enable_link_counters)
    cnfgpars.set('Fault_Config', 'enable_router_counters', Config.enable_router_counters)
    cnfgpars.set('Fault_Config', 'enable_pe_counters', Config.enable_pe_counters)
    cnfgpars.set('Fault_Config', 'error_correction_rate', Config.error_correction_rate)

    # ------------------------------------------------
    #           Network_Partitioning
    # ------------------------------------------------
    cnfgpars.add_section('Network_Partitioning')
    cnfgpars.set('Network_Partitioning', 'EnablePartitioning', Config.EnablePartitioning)
    # ------------------------------------------------
    #               PMCG_Config
    # ------------------------------------------------
    cnfgpars.add_section('PMCG_Config')
    cnfgpars.set('PMCG_Config', 'GeneratePMCG', Config.GeneratePMCG)
    cnfgpars.set('PMCG_Config', 'OneStepDiagnosable', Config.OneStepDiagnosable)
    cnfgpars.set('PMCG_Config', 'TFaultDiagnosable', Config.TFaultDiagnosable)
    cnfgpars.set('PMCG_Config', 'NodeTestExeTime', Config.NodeTestExeTime)
    cnfgpars.set('PMCG_Config', 'NodeTestComWeight', Config.NodeTestComWeight)
    # ------------------------------------------------
    #               Viz_Config
    # ------------------------------------------------
    cnfgpars.add_section('Viz_Config')
    cnfgpars.set('Viz_Config', 'RG_Draw', Config.RG_Draw)
    cnfgpars.set('Viz_Config', 'PMCG_Drawing', Config.PMCG_Drawing)
    cnfgpars.set('Viz_Config', 'TTG_Drawing', Config.TTG_Drawing)
    cnfgpars.set('Viz_Config', 'Mapping_Dstr_Drawing', Config.Mapping_Dstr_Drawing)
    cnfgpars.set('Viz_Config', 'Mapping_Drawing', Config.Mapping_Drawing)
    cnfgpars.set('Viz_Config', 'Scheduling_Drawing', Config.Scheduling_Drawing)
    cnfgpars.set('Viz_Config', 'SHM_Drawing', Config.SHM_Drawing)
    cnfgpars.set('Viz_Config', 'GenMappingFrames', Config.GenMappingFrames)
    cnfgpars.set('Viz_Config', 'FrameResolution', Config.FrameResolution)

    cnfgpars.write(cfg_file)
    cfg_file.close()

    return None
