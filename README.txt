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
               IN CASE YOU WANT SOMETHING TO BE IMPLEMENTED,
              PLEASE CONTACT: siavoosh[AT]ati[DOT]ttu[DOT]ee
===============================================================================
                FOR DOCUMENTATIONS PLEASE REFER TO WIKI!
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
 |          |                           |------- NMAP
 |          |----- Mapping              |------- SimpleGreedy
 |          |----- Mapping_Animation    |------- SimulatedAnnealing
 |          |----- Mapping_Functions
 |          |----- Mapping_Reports
 |          |----- Mapping_Test
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
 |------SystemHealthMonitoring
 |          |
 |          |----- SystemHealthMonitor
 |          |----- SHM_Reports
 |          |----- SHM_Test
 |          |----- SHM_Functions
 |          |----- TestSchedulingUnit
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

    - We need to implement some test routine where we can schedule Test-Tasks where
      one PE tests another. we can use TTG made based on PMC model for this.

    - can we generate some file based on scheduling to feed in Noxim?

    - can we get TG specifications automatically from some benchmark alg??

    - Generate multiple levels of priority levels for Non/Mid-critical tasks

    - Genetics Algorithm for Mapping

    - Add logarithmic and Boltzmann cooling for SA

    - Support for adaptive routing! but have to solve some scheduling issues... 
      have no idea how to schedule on multiple paths... should be stochastic... 
      needs more reading...

    - Support for virtual channels!

    - Some 8-bit background music during execution of the program would be
      really cool. Something like this maybe:
      https://soundcloud.com/eric-skiff/hhavok-intro

    - Implement Memory Usage Profiler (want to make sure if we have
      memory leak)

    - Can we exploit the idea of repetition in TG during scheduling?

    - Checking if a re-mapping/scheduling is necessary considering the
      fault that has occurred... (with Karl)

    - Adding color bar for mapping graphs

    - Visualizing transient faults in scheduling gantt charts

    - Adding support for preemption: if we have T1 and T2 then with preemption
      T2 can interrupt T1 and execution would maybe T11->T2->T12
        - we need to write a function that breaks tasks into parts...
        - we would not have preemption in communication tasks

    - we need to have a deadline for the whole task graph

    - Can we implement something like Core-Cannibalization method for Router's control unit etc.?

    - Can we have some sort of local repair?

    - for later time we need to schedule flits in the critical domain with a model of the router with
      latency etc considered (low priority- thesis of Mihkel Tagel)

    - we need to add 0 weight communication between the tasks just to stablish
      precedence without data dependence. (we can have this in the data dependence assumptions)

    - can we identify two cores that we can just swap their mapped tasks and it doesnt change any
      other traffic on the network?
    --------------------------------------------------
    List of functions without DocString:

    ArchGraphUtilities/AG_Functions: GenerateManualAG
    ArchGraphUtilities/AG_Functions: UpdateAGRegions
    ArchGraphUtilities/AG_Functions: ReturnNodeNumber
    Clusterer/Clustering_Functions: RemoveTaskFromCTG

    --------------------------------------------------
    List of functions without Test:

    --------------------------------------------------
    To be Read:
    - GigaNoC architecture (Self-optimization of MPSoCs Targeting Resource Efficiency and Fault Tolerance-2009)
    - Core Salvaging