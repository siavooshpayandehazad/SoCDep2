# Copyright (C) 2015 Siavoosh Payandeh Azad

from Utilities import misc
misc.check_for_dependencies()

import sys
import os
import time
import logging
from ConfigAndPackages import Config, PackageFile
from Utilities import Logger, Benchmark_Alg_Downloader
import SystemInitialization
from GUI_Util import GUI
from pympler import tracker
from Simulator import Simulator
# from Simulator import FaultInjector

tr = None
if Config.MemoryProfiler:
    tr = tracker.SummaryTracker()

if '--help' in sys.argv[1:] or '-help' in sys.argv[1:]:
    print("Usage:    python Main.py [option1]")
    print("Options and arguments:")
    print("-GUI\t\t:Graphical User Interface for Configuration")
    print("-UTEST\t\t:Runs Unit Tests")
    print("-BENCHMARK\t: Runs Benchmark Algorithms:")
    print("\t\t\t * idct: Inverse Discrete Cosine Transform")
    print("\t\t\t * fdct: Forward Discrete Cosine Transform")
    print("\t\t\t * mi: Matrix Inverse")
    print("")
    sys.exit()
elif '-GUI' in sys.argv[1:]:
    app = GUI.ConfigApp(None)
    app.title('Schedule And Depend')
    app.mainloop()
    if not app.apply_button:
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
    if Benchmark_Alg_Downloader.Download_Benchmark_Algorithms(str(benchmark)):
        pass
    else:
        sys.exit()

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
####################################################################
# Initialization of the system
tg, ag, shmu, noc_rg, CriticalRG, NonCriticalRG, pmcg = SystemInitialization.initialize_system(logging)


# just to have a sense of how much time we are spending in each section
print ("===========================================")
system_starting_time = time.time()
print ("\033[92mTIME::\033[0m SYSTEM STARTS AT:"+str(round(system_starting_time-program_start_time)) +
       " SECONDS AFTER PROGRAM START...")
Simulator.run_simulator(100, ag, shmu, noc_rg, logging)
# FaultInjector.FaultInjector(system_starting_time, ag, shmu, noc_rg)
logging.info('Logging finished...')

if Config.MemoryProfiler:
    print("===========================================")
    print("         Reporting Memory Usage")
    print("===========================================")
    tr.print_diff()
    print("===========================================")