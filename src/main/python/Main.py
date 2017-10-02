# Copyright (C) 2015 Siavoosh Payandeh Azad
import sys
import os
from Utilities import misc

if '--help' in sys.argv[1:] or '-help' in sys.argv[1:]:
    pass
else:
    misc.check_for_dependencies()

import time
import logging
from ConfigAndPackages import Config, PackageFile, Check_Config
from Utilities import Logger, Benchmark_Alg_Downloader, misc
import SystemInitialization
from GUI_Util import GUI
from pympler import tracker
from Simulator import Simulator
from RoutingAlgorithms.turn_model_evaluation import list_all_turn_models, turn_model_viz, turn_mode_classifier
from RoutingAlgorithms.turn_model_evaluation import odd_even_evaluation
from multiprocessing import Pool


tr = None
if Config.MemoryProfiler:
    tr = tracker.SummaryTracker()

if '--help' in sys.argv[1:] or '-help' in sys.argv[1:]:
    misc.print_help_man()
    sys.exit()
elif '-GUI' in sys.argv[1:]:
    main_window = GUI.MainView(None)
    main_window.title("Schedule and Depend Configuration GUI")
    main_window.mainloop()
    if not main_window.apply_button:
        sys.exit()
elif '-EvTM_odd_even' in sys.argv[1:]:
    #misc.generate_file_directories()

    """
    for size in range(3, 4):
        for routing_type in ["MinimalPath", "NonMinimalPath"]:
            odd_even_evaluation.odd_even_fault_tolerance_metric(size, routing_type)
    sys.exit()
    """
    ##################################
    # 2X2 NoC
    #  DoA
    # selected_turn_models = [807, 816, 819]
    #  DoA_ex
    # selected_turn_models = [807, 787, 816, 796, 819]
    #  new metric minimal
    # selected_turn_models = [0, 1, 58]
    #  new metric non minimal
    # selected_turn_models = [2, 0, 33, 1, 58]

    ##################################
    # 3X3 NoC
    #  DoA
    # selected_turn_models = [32, 0, 33, 1, 249, 93, 669, 255, 254, 679, 677]
    #  DoA_ex
    # selected_turn_models = [8, 284, 52, 680, 287, 264, 256, 244, 685, 682, 660, 37, 245, 121, 273, 56, 288, 257, 247, 76,
    #                         662, 32, 0 , 55, 260, 265, 274, 286, 38, 39, 53, 40, 684, 278, 79, 275, 33, 259, 277, 267,
    #                         248, 290, 258, 1 , 4 , 34, 663, 54, 35, 246, 41, 270, 664, 269, 281, 57, 250, 289, 282, 249,
    #                         693, 263, 670, 5 , 669, 36, 93, 122, 58, 295, 251, 271, 252, 673, 698, 672, 294, 697, 254, 677,
    #                         126, 255, 679]
    #  new metric minimal
    # selected_turn_models = [32, 256, 0,  33, 35, 258, 1,  250, 36, 670, 93, 255, 679]
    #  new metric non minimal
    selected_turn_models = [284, 88, 52, 680, 244, 264, 287, 256, 285, 32, 121, 245, 37, 685, 265, 272, 247, 33, 56,
                            0,  55, 40, 4,  38, 34, 35, 53, 39, 89, 262, 269, 293, 250, 290, 261, 122, 1,  292, 253,
                            252, 5,  57, 58, 93, 126]

    odd_even_evaluation.evaluate_turn_model_fault_tolerance(selected_turn_models, 3, "nonminimal", 3)
    #odd_even_evaluation.viz_all_turn_models_against_each_other()
    #odd_even_evaluation.evaluate_doa_for_all_odd_even_turn_model_list()
    #odd_even_evaluation.enumerate_all_odd_even_turn_models()
    sys.exit()
elif '-odd_even_viz' in sys.argv[1:]:
    turn_model_viz.viz_2d_odd_even_turn_model()
    sys.exit()

elif '-ETM' in sys.argv[1:]:     # Enumerate turn model
    misc.generate_file_directories()
    if __name__ == '__main__':
        p = Pool(6)
        if sys.argv[sys.argv.index('-ETM') + 1] == '3D':
            args = list(range(0, len(PackageFile.FULL_TurnModel_3D)+1))
            p.map(list_all_turn_models.enumerate_all_3d_turn_models, args)
            p.terminate()
        if sys.argv[sys.argv.index('-ETM') + 1] == '2D':
            args = list(range(0, len(PackageFile.FULL_TurnModel_2D)+1))
            p.map(list_all_turn_models.enumerate_all_2d_turn_models, args)
            p.terminate()
        del p
    sys.exit()
elif '-ETMD' in sys.argv[1:]:     # Enumerate turn model based on deadlock
    misc.generate_file_directories()
    if __name__ == '__main__':
        routing_type = sys.argv[sys.argv.index('-ETMD') + 2]
        if routing_type == "M":
            Config.RotingType = 'MinimalPath'
        elif routing_type == "NM":
            Config.RotingType = 'NonMinimalPath'
        else:
            print "ARGUMENT ERROR:: Routing type should be either M or NM..."
        number_of_multi_threads = int(sys.argv[sys.argv.index('-ETMD') + 3])
        p = Pool(number_of_multi_threads)
        if sys.argv[sys.argv.index('-ETMD') + 1] == '3D':
            args = list(range(0, len(PackageFile.FULL_TurnModel_3D)+1))
            p.map(list_all_turn_models.enumerate_all_3d_turn_models_based_on_df, args)
            p.terminate()
        elif sys.argv[sys.argv.index('-ETMD') + 1] == '2D':
            args = list(range(0, len(PackageFile.FULL_TurnModel_2D)+1))
            p.map(list_all_turn_models.enumerate_all_2d_turn_models_based_on_df, args)
            p.terminate()
        else:
            print "ARGUMENT ERROR:: Dimension should be specified as 2D or 3D..."
    sys.exit()
elif '-TMFT' in sys.argv[1:]:     # check All turn model's fault tolerance
    misc.generate_file_directories()
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    routing_type = sys.argv[sys.argv.index('-TMFT') + 2]
    if routing_type == "M":
        Config.RotingType = 'MinimalPath'
    elif routing_type == "NM":
        Config.RotingType = 'NonMinimalPath'
    else:
        print "ARGUMENT ERROR:: Routing type should be either M or NM..."

    number_of_multi_threads = int(sys.argv[sys.argv.index('-TMFT') + 3])
    if "2D" in sys.argv[1:] or "3D" in sys.argv[1:]:
        pass
    else:
        print "MISSING ARGUMENT:: A dimension value is required for this command"
        sys.exit()
    dimension = sys.argv[sys.argv.index('-TMFT') + 1]
    if "-V" in sys.argv[1:]:
        viz = True
    else:
        viz = False
    list_all_turn_models.check_fault_tolerance_of_routing_algs(dimension, number_of_multi_threads, viz)
    sys.exit()
elif '-VIZTM' in sys.argv[1:]:     # visualizes the turn models in 2D or 3D
    misc.generate_file_directories()
    if "2D" in sys.argv[1:] or "3D" in sys.argv[1:]:
        pass
    else:
        print "MISSING ARGUMENT:: A dimension value is required for this command"
        sys.exit()
    dimension = sys.argv[sys.argv.index('-VIZTM') + 1]
    routing_type = sys.argv[sys.argv.index('-VIZTM') + 2]
    turn_model_viz.viz_all_turn_models(dimension, routing_type)
    sys.exit()
elif '-TMC' in sys.argv[1:]:
    turn_mode_classifier.classify_3d_turn_models()
    sys.exit()
elif '-CONF' in sys.argv[1:]:
    if len(sys.argv) == 2:
        misc.update_config("ConfigAndPackages/ConfigFile.txt")
    else:
        path_to_config_file = sys.argv[sys.argv.index('-CONF') + 1]
        misc.update_config(path_to_config_file)
elif '-BENCHMARK' in sys.argv[1:]:
    benchmark = sys.argv[sys.argv.index('-BENCHMARK') + 1]
    print benchmark
    if Benchmark_Alg_Downloader.download_benchmark_algorithms(str(benchmark)):
        pass
    else:
        sys.exit()

Check_Config.check_config_file()
program_start_time = time.time()
##############################
# Just for getting a copy of the current console
sys.stdout = Logger.Logger()

# preparing to setup Logging
logging.basicConfig(filename=os.path.join(os.path.join(os.path.curdir, PackageFile.LoGDirectory),
                    'Logging_Log_'+str(time.time())+'.log'), level=logging.DEBUG)
logging.info('Starting logging...')
####################################################################
misc.generate_file_directories()
misc.draw_logo()
misc.generate_configfile()
####################################################################
# Initialization of the system

tg, ag, shmu, noc_rg, CriticalRG, NonCriticalRG, pmcg = SystemInitialization.initialize_system(logging)

# just to have a sense of how much time we are spending in each section
print ("===========================================")
system_starting_time = time.time()
print ("\033[92mTIME::\033[0m SYSTEM STARTS AT:"+str(round(system_starting_time-program_start_time)) +
       " SECONDS AFTER PROGRAM START...")

if Config.enable_simulator:
    Simulator.run_simulator(Config.ProgramRunTime, tg, ag, shmu, noc_rg, CriticalRG, NonCriticalRG, logging)
logging.info('Logging finished...')

if Config.MemoryProfiler:
    print("===========================================")
    print("         Reporting Memory Usage")
    print("===========================================")
    tr.print_diff()
    print("===========================================")
