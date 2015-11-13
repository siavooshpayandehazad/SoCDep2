# Copyright (C) 2015 Siavoosh Payandeh Azad
from Utilities import misc
misc.CheckForDependencies()


import sys, os, time
import logging
from ConfigAndPackages import Config
from Utilities import Logger, Benchmark_Alg_Downloader
import SystemInitialization
from GUI_Util import GUI
from pympler import tracker
from Simulator import Simulator, FaultInjector



tr = tracker.SummaryTracker()

if '--help' in sys.argv[1:] or '-help' in sys.argv[1:]:
    print("Usage:    python Main.py [option1]")
    print("Options and arguments:")
    print("-GUI\t:Graphical User Interface for Configuration")
    print("-UTEST\t:Runs Unit Tests")
    print("")
    sys.exit()
elif '-GUI' in sys.argv[1:]:
    app = GUI.ConfigAppp(None)
    app.title('Schedule And Depend')
    app.mainloop()
    if not app.Apply_Button:
        sys.exit()
elif '-UTEST' in sys.argv[1:]:
    os.system('python UnitTest/UnitTests.py')
    sys.exit()
elif '-BENCHMARK' in sys.argv[1:]:
    Benchmark = sys.argv[sys.argv.index('-BENCHMARK') + 1]
    if Benchmark_Alg_Downloader.Download_Benchmark_Algorithms(str(Benchmark)):
        pass
    else:
        sys.exit()


ProgramStartTime = time.time()
##############################
# Just for getting a copy of the current console
sys.stdout = Logger.Logger()

# preparing to setup Logging
logging.basicConfig(filename=os.path.join(os.path.join(os.path.curdir, Config.LoGDirectory),
                    'Logging_Log_'+str(time.time())+'.log'), level=logging.DEBUG)
logging.info('Starting logging...')
####################################################################
misc.GenerateFileDirectories()
misc.DrawLogo()
####################################################################
# Initialization of the system
TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, PMCG = SystemInitialization.InitializeSystem(logging)


# just to have a sense of how much time we are spending in each section
print ("===========================================")
SystemStartingTime = time.time()
print ("\033[92mTIME::\033[0m SYSTEM STARTS AT:"+str(round(SystemStartingTime-ProgramStartTime))+
       " SECONDS AFTER PROGRAM START...")
Simulator.RunSimualtor(100, AG, SHM, NoCRG)
# FaultInjector.FaultInjector(SystemStartingTime, AG, SHM, NoCRG)
logging.info('Logging finished...')

print("===========================================")
print("         Reporting Memory Usage")
print("===========================================")
tr.print_diff()
print("===========================================")