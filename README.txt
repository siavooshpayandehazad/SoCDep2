============================================================================
	  _________      .__               .___    .__
	 /   _____/ ____ |  |__   ____   __| _/_ __|  |   ____
	 \_____  \_/ ___\|  |  \_/ __ \ / __ |  |  \  | _/ __ \
	 /        \  \___|   Y  \  ___// /_/ |  |  /  |_\  ___/
	/_______  /\___  >___|  /\___  >____ |____/|____/\___  >
	        \/     \/     \/     \/     \/               \/
	                   .___
	_____    ____    __| _/
	\__  \  /    \  / __ |
	 / __ \|   |  \/ /_/ |
	(____  /___|  /\____ |
	     \/     \/      \/
	________                                   .___
	\______ \   ____ ______   ____   ____    __| _/
	 |    |  \_/ __ \\____ \_/ __ \ /    \  / __ | 
	 |    `   \  ___/|  |_> >  ___/|   |  \/ /_/ | 
	/_______  /\___  >   __/ \___  >___|  /\____ | 
	        \/     \/|__|        \/     \/      \/  
==============================================================================
AUTHOR:  SIAVOOSH PAYANDEH AZAD
DATE:    MAY 2015
LICENSE: GNU GENERAL PUBLIC LICENSE Version 2
PYTHON VER: 2.6.9
THE GOAL OF THIS PROGRAM IS TO MAKE A PLATFORM FOR TESTING SOME DEPENDABILITY 
MECHANISMS ON DIFFERENT ARCHITECTURES....
Copyright (C) 2015 Siavoosh Payandeh Azad
===============================================================================
Libraries needed:
    * networkx:     https://networkx.github.io/
    * matplotlib:   http://matplotlib.org/
===============================================================================
Project Directory Map:

ScheduleAndDepend
 |
 |------ArchGraphUtilities
 |          |
 |          |------- AG_Functions
 |          |------- Arch_Graph_Reports
 |          |------- AG_Test
 |
 |------Clusterer
 |          |
 |          |------- Clustering
 |          |------- Clustering_Functions
 |          |------- Clustering_Test
 |
 |------ConfigAndPackages
 |          |
 |          |------- Config
 |          |------- PackageFile
 |
 |------Generated_Files
 |------GraphDrawings
 |------LOGS
 |------Mapper
 |          |
 |          |------------------- Mapping_Heuristics
 |          |                           |
 |          |                           |------- GeneticsAlgorithm
 |          |                           |------- Local_Search
 |          |----- Mapping              |------- SimpleGreedy
 |          |----- Mapping_Functions    |------- SimulatedAnnealing
 |          |----- Mapping_Reports
 |
 |------RoutingAlgorithms
 |          |
 |          |----- Calculate_Reachability
 |          |----- ReachabilityReports
 |          |----- Routing
 |          |----- Reachability_Test
 |
 |------Scheduler
 |          |
 |          |----- Scheduler
 |          |----- Scheduling_Functions
 |          |----- Scheduling_Reports
 |          |----- TrafficTableGenerator
 |
 |------SystmHealthMonitoring
 |          |
 |          |----- SystemHealthMonitor
 |          |----- SHM_Reports
 |          |----- SHM_Functions
 |
 |------TaskGraphUtilities
 |          |
 |          |----- Task_Graph_Reports
 |          |----- TG_Functions
 |
 |------UserInputs
 |          |
 |          |----- RoutingFile
 |
 |------Utilities
 |          |
 |          |----- Logger
 |          |----- misc
 |
 |-- Main
 |-- SystemInitialization

===============================================================================

ToDo:

    - At the moment thinking about a better name and a better logo for
      the project

    - I want to run a reliability Analysis of the system... so we can have
      a sense about the system state...

    - can we generate some file based on scheduling to feed in Noxim?

    - can we get TG specifications automatically from some benchmark alg??

    - Generate multiple levels of priority levels for Non/Mid-critical tasks

    - going 3D

    - Simulated annealing and Genetics Algorithm for Mapping

    - Support for adaptive routing! but have to solve some scheduling issues... 
      have no idea how to schedule on multiple paths... should be stochastic... 
      needs more reading...

    - Support for virtual channels!

    - Some 8-bit background music during execution of the program would be
      really cool. Something like this maybe:
      https://soundcloud.com/eric-skiff/hhavok-intro

    - Implement Memory Usage Profiler (want to make sure if we have memory leak)

    - Can we exploit the idea of repetition in TG during scheduling?

    - Checking if a re-mapping/scheduling is necessary considering the
      fault that has occurred...

    - Adding color bar for mapping graphs

    - Automatic Generation of fault configuration for partitioning, specially
      the case of covering actual faults in virtually broken links... this is very
      serious...