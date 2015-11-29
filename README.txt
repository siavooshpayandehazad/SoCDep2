==============================================================================
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
	 |    |  \_/ __ \____ \_/ __ \ /    \  / __ | 
	 |    `   \  ___/|  |_> >  ___/|   |  \/ /_/ | 
	/_______  /\___  >   __/ \___  >___|  /\____ | 
	        \/     \/|__|        \/     \/      \/  
==============================================================================
AUTHORS:
 	  SIAVOOSH PAYANDEH AZAD
DATE: MAY 2015
LICENSE: GNU GENERAL PUBLIC LICENSE Version 2
PYTHON VER: 2.7.6
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

../../../src
├── main
│   ├── python
│   │   ├── ArchGraphUtilities
│   │   │   ├── AG_Functions.py
│   │   │   ├── AG_Test.py
│   │   │   ├── Arch_Graph_Reports.py
│   │   │   └── Optimize_3D_AG.py
│   │   ├── Benchmarks
│   │   ├── Clusterer
│   │   │   ├── Clustering.py
│   │   │   ├── Clustering_Functions.py
│   │   │   ├── Clustering_Reports.py
│   │   │   └── Clustering_Test.py
│   │   ├── ConfigAndPackages
│   │   │   ├── Config.py
│   │   │   └── PackageFile.py
│   │   ├── GUI_Util
│   │   │   ├── Disclaimer
│   │   │   └── GUI.py
│   │   ├── Generated_Files
│   │   │   ├── GSNoCTrafficTable.txt
│   │   │   ├── GSNoC_RectangleFile.txt
│   │   │   ├── Internal
│   │   │   │   ├── ClusteringCost.txt
│   │   │   │   ├── LocalSearchMappingCost.txt
│   │   │   │   └── MappingProcess.txt
│   │   │   ├── NoximTrafficTable.txt
│   │   │   └── ReachAbilityNodeReport.txt
│   │   ├── GraphDrawings
│   │   │   └── Mapping_Animation_Material
│   │   ├── LOGS
│   │   ├── Main.py
│   │   ├── Mapper
│   │   │   ├── Mapping.py
│   │   │   ├── Mapping_Animation.py
│   │   │   ├── Mapping_Functions.py
│   │   │   ├── Mapping_Heuristics
│   │   │   │   ├── GeneticsAlgorithm.py
│   │   │   │   ├── Local_Search.py
│   │   │   │   ├── NMap.py
│   │   │   │   ├── SimpleGreedy.py
│   │   │   │   └── SimulatedAnnealing.py
│   │   │   ├── Mapping_Reports.py
│   │   │   └── Mapping_Test.py
│   │   ├── RoutingAlgorithms
│   │   │   ├── Calculate_Reachability.py
│   │   │   ├── ReachabilityReports.py
│   │   │   ├── Reachability_Test.py
│   │   │   ├── Routing.py
│   │   │   └── RoutingGraph_Reports.py
│   │   ├── Scheduler
│   │   │   ├── Scheduler.py
│   │   │   ├── Scheduling_Functions.py
│   │   │   ├── Scheduling_Reports.py
│   │   │   └── TrafficTableGenerator.py
│   │   ├── Simulator
│   │   │   ├── FaultInjector.py
│   │   │   └── Simulator.py
│   │   ├── SystemHealthMonitoring
│   │   │   ├── SHMU_Functions.py
│   │   │   ├── SHMU_Reports.py
│   │   │   ├── SHMU_Test.py
│   │   │   ├── SystemHealthMonitoringUnit.py
│   │   │   └── TestSchedulingUnit.py
│   │   ├── SystemInitialization.py
│   │   ├── TaskGraphUtilities
│   │   │   ├── TG_File_Parser.py
│   │   │   ├── TG_Functions.py
│   │   │   ├── TG_Test.py
│   │   │   └── Task_Graph_Reports.py
│   │   └── Utilities
│   │       ├── Benchmark_Alg_Downloader.py
│   │       ├── Logger.py
│   │       └── misc.py
│   └── scripts
│       ├── GUI
│       └── GenerateReadMe
└── unittest
    └── Python
        └── Unit_tests.py

23 directories, 57 files
===============================================================================
