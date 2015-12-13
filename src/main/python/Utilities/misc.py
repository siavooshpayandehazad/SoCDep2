# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import Config, PackageFile
import os
import ConfigParser


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
    print ("AUTHOR:  SIAVOOSH PAYANDEH AZAD")
    print ("DATE:    MAY 2015")
    print ("THE GOAL OF THIS PROGRAM IS TO MAKE A PLATFORM FOR TESTING SOME ")
    print ("DEPENDABILITY STUFF ON DIFFERENT ARCHITECTURES....")
    print ("================================================================================")
    print ("DEBUG DETAILS:"+str(Config.DebugDetails))
    print ("DEBUG INFO:"+str(Config.DebugInfo))
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
    Config.TG_Type = config.get("TG_Config", "TG_Type")

    Config.NumberOfTasks = config.getint("TG_Config", "NumberOfTasks")
    Config.NumberOfCriticalTasks = config.getint("TG_Config", "NumberOfCriticalTasks")
    Config.NumberOfEdges = config.getint("TG_Config", "NumberOfEdges")
    Config.WCET_Range = config.getint("TG_Config", "WCET_Range")
    Config.EdgeWeightRange = config.getint("TG_Config", "EdgeWeightRange")
    Config.Release_Range = config.getint("TG_Config", "Release_Range")      # task release time range

    Config.Task_List = map(int, config.get("TG_Config", "Task_List").split(","))
    Config.Task_WCET_List = map(int, config.get("TG_Config", "Task_WCET_List").split(","))
    Config.Task_Criticality_List = config.get("TG_Config", "Task_Criticality_List").split(",")

    Config.AG_Type = config.get("AG_Config", "AG_Type")
    Config.NetworkTopology = config.get("AG_Config", "NetworkTopology")
    Config.Network_X_Size = config.getint("AG_Config", "Network_X_Size")
    Config.Network_Y_Size = config.getint("AG_Config", "Network_Y_Size")
    Config.Network_Z_Size = config.getint("AG_Config", "Network_Z_Size")
    Config.PE_List = map(int, config.get("AG_Config", "PE_List").split(","))

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

    Config.FindOptimumAG = config.getboolean("VL_Config", "FindOptimumAG")
    Config.VL_OptAlg = config.get("VL_Config", "VL_OptAlg")
    Config.AG_Opt_Iterations_ILS = config.getint("VL_Config", "AG_Opt_Iterations_ILS")
    Config.AG_Opt_Iterations_LS = config.getint("VL_Config", "AG_Opt_Iterations_LS")
    Config.VerticalLinksNum = config.getint("VL_Config", "VerticalLinksNum")

    Config.DarkSiliconPercentage = config.getint("Dark_Sil_Config", "DarkSiliconPercentage")

    Config.Clustering_Optimization = config.getboolean("CTG_Config", "Clustering_Optimization")
    Config.ClusteringIteration = config.getint("CTG_Config", "ClusteringIteration")
    Config.ctg_random_seed = config.getint("CTG_Config", "ctg_random_seed")
    Config.Clustering_Report = config.getboolean("CTG_Config", "Clustering_Report")
    Config.Clustering_DetailedReport = config.getboolean("CTG_Config", "Clustering_DetailedReport")
    Config.Clustering_CostFunctionType = config.get("CTG_Config", "Clustering_CostFunctionType")
    Config.ClusteringOptMove = config.get("CTG_Config", "ClusteringOptMove")
    Config.CTG_CirculationLength = config.getint("CTG_Config", "CTG_CirculationLength")

    Config.GeneratePMCG = config.getboolean("PMCG_Config", "GeneratePMCG")
    Config.OneStepDiagnosable = config.getboolean("PMCG_Config", "OneStepDiagnosable")
    Config.TFaultDiagnosable = config.get("PMCG_Config", "TFaultDiagnosable")
    Config.NodeTestExeTime = config.getint("PMCG_Config", "NodeTestExeTime")
    Config.NodeTestComWeight = config.getint("PMCG_Config", "NodeTestComWeight")