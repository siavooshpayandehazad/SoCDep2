# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import Config, PackageFile
import os
import ConfigParser
import ast


def draw_logo():
    print ("================================================================================================")
    print ("                                                         ___   ")
    print ("                                                       /'___`\  ")
    print ("                                                      /\_\ /\ \ ")
    print ("     ____            ____     ____                    \/_/// /__     ")
    print ("    /\  _`\         /\  _`\  /\  _`\                     // /_\ \	 ")
    print ("    \ \,\L\_\    ___\ \ \/\_\\\\ \ \/\ \     __   _____  /\______/   	")
    print ("     \/_\__ \   / __`\ \ \/_/_\ \ \ \ \  /'__`\/\ '__`\\\\/_____/	 ")
    print ("       /\ \L\ \/\ \L\ \ \ \L\ \\\\ \ \_\ \/\  __/\ \ \L\ \  	 			")
    print ("       \ `\____\ \____/\ \____/ \ \____/\ \____\\\\ \ ,__/")
    print ("        \/_____/\/___/  \/___/   \/___/  \/____/ \ \ \/ ")
    print ("                                                  \ \_\ ")
    print ("                                                   \/_/ ")
    print ("================================================================================================")
    print ("AUTHORS:")
    print ("          SIAVOOSH PAYANDEH AZAD")
    print ("          RENE PIHLAK")
    print ("          BEHRAD NIAZMAND")
    print ("          NEVIN GEORGE")
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

    latex_directory = "Generated_Files/Latex"
    if not os.path.isdir(latex_directory):
        os.makedirs(latex_directory)
    file_list = [tex_file for tex_file in os.listdir(latex_directory) if tex_file.endswith(".tex")]
    for tex_file in file_list:
        os.remove(latex_directory+'/'+tex_file)

    turn_model_directory = "Generated_Files/Turn_Model_Lists"
    if not os.path.isdir(turn_model_directory):
        os.makedirs(turn_model_directory)
    file_list = [txt_file for txt_file in os.listdir(turn_model_directory) if txt_file.endswith(".txt")]
    for txt_file in file_list:
        os.remove(turn_model_directory+'/'+txt_file)

    turn_model_eval_directory = "Generated_Files/Turn_Model_Eval"
    if not os.path.isdir(turn_model_eval_directory):
        os.makedirs(turn_model_eval_directory)
    file_list = [txt_file for txt_file in os.listdir(turn_model_eval_directory) if txt_file.endswith(".txt")]
    for txt_file in file_list:
        os.remove(turn_model_eval_directory+'/'+txt_file)

    if Config.EventDrivenFaultInjection:
        fault_drawing_directory = "GraphDrawings/Components_Fault_Drawings"
        if not os.path.isdir(fault_drawing_directory):
            os.makedirs(fault_drawing_directory)
        file_list = [png_file for png_file in os.listdir(fault_drawing_directory) if png_file.endswith(".png")]
        for png_file in file_list:
            os.remove(fault_drawing_directory+'/'+png_file)
    return None


def check_for_dependencies():
    for module in PackageFile.ImportModules:
        try:
            __import__(module)
        except ImportError:
            raise ImportError("MODULE "+str(module)+" DOES NOT EXIST...")
    print "\033[33m* INFO::\033[0m ALL REQUIRED MODULES AVAILABLE..."
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
    Config.fault_injection_method = config.get("Program_Config", "fault_injection_method")
    Config.fault_injection_file = config.get("Program_Config", "fault_injection_file")
    # ------------------------------------------------
    #               TG_Config
    # ------------------------------------------------
    Config.tg.type = config.get("TG_Config", "TG_Type")

    Config.tg.num_of_tasks = config.getint("TG_Config", "NumberOfTasks")
    Config.tg.num_of_critical_tasks = config.getint("TG_Config", "NumberOfCriticalTasks")
    Config.tg.num_of_edges = config.getint("TG_Config", "NumberOfEdges")
    Config.tg.wcet_range = config.getint("TG_Config", "WCET_Range")
    Config.tg.edge_weight_range = config.getint("TG_Config", "EdgeWeightRange")
    Config.tg.release_range = config.getint("TG_Config", "Release_Range")      # task release time range
    Config.tg.random_seed = config.getint("TG_Config", "tg_random_seed")

    # Config.Task_List = map(int, config.get("TG_Config", "Task_List").split(","))
    # Config.Task_WCET_List = map(int, config.get("TG_Config", "Task_WCET_List").split(","))
    # Config.Task_Criticality_List = config.get("TG_Config", "Task_Criticality_List").split(",")
    # TG_Edge_List
    # TG_Edge_Weight
    # TG_DOT_Path

    # ------------------------------------------------
    #               AG_Config
    # ------------------------------------------------
    Config.ag.type = config.get("AG_Config", "AG_Type")
    # VirtualChannelNum
    Config.ag.topology = config.get("AG_Config", "NetworkTopology")
    Config.ag.x_size = config.getint("AG_Config", "Network_X_Size")
    Config.ag.y_size = config.getint("AG_Config", "Network_Y_Size")
    Config.ag.z_size = config.getint("AG_Config", "Network_Z_Size")
    # Config.PE_List = map(int, config.get("AG_Config", "PE_List").split(","))
    # AG_Edge_List
    # AG_Edge_Port_List

    # ------------------------------------------------
    #               VL_Config
    # ------------------------------------------------
    Config.FindOptimumAG = config.getboolean("VL_Config", "FindOptimumAG")
    Config.vl_opt.vl_opt_alg = config.get("VL_Config", "VL_OptAlg")
    Config.vl_opt.ils_iteration = config.getint("VL_Config", "AG_Opt_Iterations_ILS")
    Config.vl_opt.ls_iteration = config.getint("VL_Config", "AG_Opt_Iterations_LS")
    Config.vl_opt.vl_num = config.getint("VL_Config", "VerticalLinksNum")

    Config.vl_opt.random_seed = config.getint("VL_Config", "random_seed")
    Config.vl_opt.sa_annealing_schedule = config.get("VL_Config", "sa_annealing_schedule")
    Config.vl_opt.termination_criteria = config.get("VL_Config", "termination_criteria")
    Config.vl_opt.sa_initial_temp = config.getint("VL_Config", "sa_initial_temp")
    Config.vl_opt.sa_stop_temp = config.getint("VL_Config", "sa_stop_temp")
    Config.vl_opt.sa_iteration = config.getint("VL_Config", "sa_iteration")
    Config.vl_opt.sa_report_solutions = config.getboolean("VL_Config", "sa_report_solutions")
    Config.vl_opt.sa_alpha = config.getfloat("VL_Config", "sa_alpha")
    Config.vl_opt.sa_log_cooling_constant = config.getfloat("VL_Config", "sa_log_cooling_constant")
    # ------------------------------------------------
    #               Routing_Config
    # ------------------------------------------------
    if config.get("Routing_Config", "UsedTurnModel") == "XY_TurnModel":
        Config.UsedTurnModel = PackageFile.XY_TurnModel
    elif config.get("Routing_Config", "UsedTurnModel") == "YX_TurnModel":
        Config.UsedTurnModel = PackageFile.YX_TurnModel
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
    Config.TurnsHealth = Config.setup_turns_health()
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
    Config.task_clustering = config.getboolean("CTG_Config", "task_clustering")
    Config.Clustering_Optimization = config.getboolean("CTG_Config", "Clustering_Optimization")
    Config.clustering.iterations = config.getint("CTG_Config", "ClusteringIteration")
    Config.clustering.random_seed = config.getint("CTG_Config", "ctg_random_seed")
    Config.clustering.report = config.getboolean("CTG_Config", "Clustering_Report")
    Config.clustering.detailed_report = config.getboolean("CTG_Config", "Clustering_DetailedReport")
    Config.clustering.cost_function = config.get("CTG_Config", "Clustering_CostFunctionType")
    Config.clustering.opt_move = config.get("CTG_Config", "ClusteringOptMove")
    Config.clustering.circulation_length = config.getint("CTG_Config", "CTG_CirculationLength")

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
    Config.viz.rg = config.getboolean("Viz_Config", "RG_Draw")
    Config.viz.pmcg = config.getboolean("Viz_Config", "PMCG_Drawing")
    Config.viz.ttg = config.getboolean("Viz_Config", "TTG_Drawing")
    Config.viz.mapping_distribution = config.getboolean("Viz_Config", "Mapping_Dstr_Drawing")
    Config.viz.mapping = config.getboolean("Viz_Config", "Mapping_Drawing")
    Config.viz.scheduling = config.getboolean("Viz_Config", "Scheduling_Drawing")
    Config.viz.shm = config.getboolean("Viz_Config", "SHM_Drawing")
    Config.viz.mapping_frames = config.getboolean("Viz_Config", "GenMappingFrames")
    Config.viz.frame_resolution = config.getint("Viz_Config", "FrameResolution")
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
    cnfgpars.set('Program_Config', 'fault_injection_method', Config.fault_injection_method)
    cnfgpars.set('Program_Config', 'fault_injection_file', Config.fault_injection_file)
    # ------------------------------------------------
    #               TG_Config
    # ------------------------------------------------
    cnfgpars.add_section('TG_Config')
    cnfgpars.set('TG_Config', 'TG_Type', Config.tg.type)
    cnfgpars.set('TG_Config', 'NumberOfTasks', Config.tg.num_of_tasks)
    cnfgpars.set('TG_Config', 'NumberOfCriticalTasks', Config.tg.num_of_critical_tasks)
    cnfgpars.set('TG_Config', 'NumberOfEdges', Config.tg.num_of_edges)
    cnfgpars.set('TG_Config', 'WCET_Range', Config.tg.wcet_range)
    cnfgpars.set('TG_Config', 'EdgeWeightRange', Config.tg.edge_weight_range)
    cnfgpars.set('TG_Config', 'Release_Range', Config.tg.release_range)
    cnfgpars.set('TG_Config', 'tg_random_seed', Config.tg.random_seed)

    # ------------------------------------------------
    #               AG_Config
    # ------------------------------------------------
    cnfgpars.add_section('AG_Config')

    cnfgpars.set('AG_Config', 'AG_Type', Config.ag.type)
    cnfgpars.set('AG_Config', 'NetworkTopology', Config.ag.topology)
    cnfgpars.set('AG_Config', 'Network_X_Size', Config.ag.x_size)
    cnfgpars.set('AG_Config', 'Network_Y_Size', Config.ag.y_size)
    cnfgpars.set('AG_Config', 'Network_Z_Size', Config.ag.z_size)
    # VirtualChannelNum
    # Config.PE_List = map(int, config.get("AG_Config", "PE_List").split(","))
    # AG_Edge_List
    # AG_Edge_Port_List

    # ------------------------------------------------
    #               VL_Config
    # ------------------------------------------------
    cnfgpars.add_section('VL_Config')
    cnfgpars.set('VL_Config', 'FindOptimumAG', Config.FindOptimumAG)
    cnfgpars.set('VL_Config', 'VL_OptAlg', Config.vl_opt.vl_opt_alg)
    cnfgpars.set('VL_Config', 'AG_Opt_Iterations_ILS', Config.vl_opt.ils_iteration)
    cnfgpars.set('VL_Config', 'AG_Opt_Iterations_LS', Config.vl_opt.ls_iteration)
    cnfgpars.set('VL_Config', 'VerticalLinksNum', Config.vl_opt.vl_num)

    cnfgpars.set('VL_Config', 'random_seed', Config.vl_opt.random_seed)
    cnfgpars.set('VL_Config', 'sa_annealing_schedule', Config.vl_opt.sa_annealing_schedule)
    cnfgpars.set('VL_Config', 'termination_criteria', Config.vl_opt.termination_criteria)
    cnfgpars.set('VL_Config', 'sa_initial_temp', Config.vl_opt.sa_initial_temp)
    cnfgpars.set('VL_Config', 'sa_stop_temp', Config.vl_opt.sa_stop_temp)
    cnfgpars.set('VL_Config', 'sa_iteration', Config.vl_opt.sa_iteration)
    cnfgpars.set('VL_Config', 'sa_report_solutions', Config.vl_opt.sa_report_solutions)
    cnfgpars.set('VL_Config', 'sa_alpha', Config.vl_opt.sa_alpha)
    cnfgpars.set('VL_Config', 'sa_log_cooling_constant', Config.vl_opt.sa_log_cooling_constant)

    # ------------------------------------------------
    #               Routing_Config
    # ------------------------------------------------
    cnfgpars.add_section('Routing_Config')
    cnfgpars.set('Routing_Config', 'UsedTurnModel', Config.UsedTurnModel)

    if Config.UsedTurnModel == PackageFile.XY_TurnModel:
        cnfgpars.set('Routing_Config', 'UsedTurnModel', "XY_TurnModel")
    elif Config.UsedTurnModel == PackageFile.YX_TurnModel:
        cnfgpars.set('Routing_Config', 'UsedTurnModel', "YX_TurnModel")
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
    cnfgpars.set('CTG_Config', 'task_clustering', Config.task_clustering)
    cnfgpars.set('CTG_Config', 'Clustering_Optimization', Config.Clustering_Optimization)
    cnfgpars.set('CTG_Config', 'ClusteringIteration', Config.clustering.iterations)
    cnfgpars.set('CTG_Config', 'ctg_random_seed', Config.clustering.random_seed)
    cnfgpars.set('CTG_Config', 'Clustering_Report', Config.clustering.report)
    cnfgpars.set('CTG_Config', 'Clustering_DetailedReport', Config.clustering.detailed_report)
    cnfgpars.set('CTG_Config', 'Clustering_CostFunctionType', Config.clustering.cost_function)
    cnfgpars.set('CTG_Config', 'ClusteringOptMove', Config.clustering.opt_move)
    cnfgpars.set('CTG_Config', 'CTG_CirculationLength', Config.clustering.circulation_length)
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
    cnfgpars.set('Viz_Config', 'RG_Draw', Config.viz.rg)
    cnfgpars.set('Viz_Config', 'PMCG_Drawing', Config.viz.pmcg)
    cnfgpars.set('Viz_Config', 'TTG_Drawing', Config.viz.ttg)
    cnfgpars.set('Viz_Config', 'Mapping_Dstr_Drawing', Config.viz.mapping_distribution)
    cnfgpars.set('Viz_Config', 'Mapping_Drawing', Config.viz.mapping)
    cnfgpars.set('Viz_Config', 'Scheduling_Drawing', Config.viz.scheduling)
    cnfgpars.set('Viz_Config', 'SHM_Drawing', Config.viz.shm)
    cnfgpars.set('Viz_Config', 'GenMappingFrames', Config.viz.mapping_frames)
    cnfgpars.set('Viz_Config', 'FrameResolution', Config.viz.frame_resolution)

    cnfgpars.write(cfg_file)
    cfg_file.close()

    return None


def print_help_man():
    print("Usage:    python Main.py [option] [argument 1]... [argument n]")
    print ""
    print("Options and arguments:")
    print("\t-GUI\t\t:Graphical User Interface for Configuration")
    print ""

    print("\t-BENCHMARK [Benchmark Name] \t: Runs Benchmark Algorithms:")
    print("\t\t * idct: Inverse Discrete Cosine Transform")
    print("\t\t * fdct: Forward Discrete Cosine Transform")
    print("\t\t * mi: Matrix Inverse")
    print ""

    print "\t-ETM  [Dimension] : Enumerates turn models regardless of their characteristics."
    print "\t\t Dimension: 2D or 3D"
    print "\t\t *The result will be stored in Generated_Files/Turn_Model_Lists folder."
    print ""

    print "\t-ETMD [Dimension] [Routing Type] [number of threads]: Enumerates turn models based on " \
          "deadlock-free-ness and reports the \n\t\treachability metric (number of connected pairs), doa and doa-ex"
    print "\t\t Dimension: 2D or 3D"
    print "\t\t Routing Type: \"M\" for minimal and \"NM\" for non-minimal"
    print "\t\t number of threads: number of threads in integer"
    print "\t\t *The result will be stored in Generated_Files/Turn_Model_Lists folder."
    print ""

    print("\t-TMFT  [Dimension] [Routing Type] [number of threads] [-V] : Checks the fault tolerance" +
          " of implemented routing algorithms \n\t\tand calculates the average reachability metric (number of" +
          "reachable pairs) for different number of faults in the network.")
    print("\t\t Dimension: 2D or 3D")
    print("\t\t Routing Type: \"M\" for minimal and \"NM\" for non-minimal")
    print("\t\t number of threads: number of threads in integer")
    print("\t\t -V: Enables visualization of every step of routing algorithm checks ")
    print ""

    print("\t-VIZTM [Dimension] [Routing Type]: visualizes the turn models in the given dimension")
    print("\t\t Dimension: 2D or 3D")
    print("\t\t Routing Type: \"M\" for minimal and \"NM\" for non-minimal")
    print ""

    print ("\t-TMC: 3D 18-turn, turn model classification")
    print("")