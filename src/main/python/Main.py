# Copyright (C) 2015 Siavoosh Payandeh Azad

from Utilities import misc
misc.check_for_dependencies()

import sys
import os
import time
import logging
from ConfigAndPackages import Config, PackageFile, Check_Config
from Utilities import Logger, Benchmark_Alg_Downloader
import SystemInitialization
from GUI_Util import GUI
from pympler import tracker
from Simulator import Simulator
from ArchGraphUtilities import list_all_turn_models
from multiprocessing import Pool


tr = None
if Config.MemoryProfiler:
    tr = tracker.SummaryTracker()

if '--help' in sys.argv[1:] or '-help' in sys.argv[1:]:
    print("Usage:    python Main.py [option1]")
    print("Options and arguments:")
    print("-GUI\t\t:Graphical User Interface for Configuration")
    print("-UTEST\t\t:Runs Unit Tests")
    print("-BENCHMARK [Benchmark Name] \t: Runs Benchmark Algorithms:")
    print("\t\t\t * idct: Inverse Discrete Cosine Transform")
    print("\t\t\t * fdct: Forward Discrete Cosine Transform")
    print("\t\t\t * mi: Matrix Inverse")
    print("-ETM\t: Enumerates turn models")
    print("-ETMD\t [Dimension] [number of threads]: Enumerates turn models based on deadlock-free-ness")
    print("\t\t\t Dimension: 2D or 3D")
    print("\t\t\t number of threads: number of threads in integer")
    print("-TMFT  [Dimension] [number of threads] [-V]\t: Checks the fault tolerant of implemented routing algorithms")
    print("\t\t\t Dimension: 2D or 3D")
    print("\t\t\t number of threads: number of threads in integer")
    print("\t\t\t -V: Enables visualization of every step of routing algorithm checks ")
    print("")
    sys.exit()
elif '-GUI' in sys.argv[1:]:
    main_window = GUI.MainView(None)
    main_window.title("Schedule and Depend Configuration GUI")
    main_window.mainloop()
    if not main_window.apply_button:
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
        number_of_multi_threads = int(sys.argv[sys.argv.index('-ETMD') + 2])
        p = Pool(number_of_multi_threads)
        if sys.argv[sys.argv.index('-ETMD') + 1] == '3D':
            args = list(range(0, len(PackageFile.FULL_TurnModel_3D)+1))
            p.map(list_all_turn_models.enumerate_all_3d_turn_models_based_on_df, args)
            p.terminate()
        if sys.argv[sys.argv.index('-ETMD') + 1] == '2D':
            args = list(range(0, len(PackageFile.FULL_TurnModel_2D)+1))
            p.map(list_all_turn_models.enumerate_all_2d_turn_models_based_on_df, args)
            p.terminate()
    sys.exit()
elif '-TMFT' in sys.argv[1:]:     # check All 2D turn model's fault tolerance
    misc.generate_file_directories()
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    number_of_multi_threads = int(sys.argv[sys.argv.index('-TMFT') + 2])
    dimension = sys.argv[sys.argv.index('-TMFT') + 1]
    if "-V" in sys.argv[1:]:
        viz = True
    else:
        viz = False
    list_all_turn_models.check_fault_tolerance_of_routing_algs(dimension, number_of_multi_threads, viz)
    sys.exit()

elif '-UTEST' in sys.argv[1:]:
    os.system('python ../../unittest/Python/Unit_tests.py')
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