# Copyright (C) 2015 Siavoosh Payandeh Azad

import Config,Scheduler,Mapping_Functions
from Clusterer import Clustering_Functions,Clustering
from Mapping_Heuristics import SimpleGreedy,Local_Search
from Scheduler import Scheduling_Functions,Scheduler,Scheduling_Reports
import copy

def Mapping (TG,AG,NoCRG,SHM,logging):
    # to run the following heuristics (Min_Min,Max_Min), one needs to use independent
    # tasks... Please use: GenerateRandomIndependentTG
    if Config.Mapping_Function=='MinMin':
        if Config.TG_Type=='RandomIndependent':
            return SimpleGreedy.Min_Min_Mapping (TG,AG,NoCRG,SHM,logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function=='MaxMin':
        if Config.TG_Type=='RandomIndependent':
            return SimpleGreedy.Max_Min_Mapping (TG,AG,NoCRG,SHM,logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function=='MinExecutionTime':
        if Config.TG_Type=='RandomIndependent':
            return SimpleGreedy.MinExecutionTime(TG,AG,SHM)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function=='MinimumCompletionTime':
        if Config.TG_Type=='RandomIndependent':
            return SimpleGreedy.MinimumCompletionTime(TG,AG,SHM)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function=='LocalSearch' or Config.Mapping_Function=='IterativeLocalSearch':
        if Config.TG_Type =='RandomDependent' or Config.TG_Type =='Manual':
            None
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomDependent')
    # clustered task graph
        CTG=copy.deepcopy(Clustering.TaskClusterGeneration(len(AG.nodes())))
        if Clustering.InitialClustering(TG, CTG):
            # Clustered Task Graph Optimization
            (BestClustering,BestTaskGraph)= Clustering.ClusteringOptimization_LocalSearch(TG, CTG, 1000)
            TG= copy.deepcopy(BestTaskGraph)
            CTG= copy.deepcopy(BestClustering)
            del BestClustering, BestTaskGraph
            Clustering_Functions.DoubleCheckCTG(TG,CTG)
            Clustering_Functions.ReportCTG(CTG,"CTG_PostOpt.png")
            # Mapping CTG on AG
            if Mapping_Functions.MakeInitialMapping(TG,CTG,AG,SHM,NoCRG,True,logging):
                Mapping_Functions.ReportMapping(AG)
                # Schedule all tasks
                Scheduler.ScheduleAll(TG,AG,SHM,Config.DebugInfo,Config.DebugDetails)
                Scheduling_Reports.ReportMappedTasks(AG)
                Mapping_Functions.CostFunction(TG,AG,SHM,Config.DebugInfo)
                if Config.Mapping_Function=='LocalSearch':
                    (BestTG,BestCTG,BestAG)=Local_Search.OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,SHM,
                                                                                Config.LocalSearchIteration,
                                                                                Config.DebugInfo,Config.DebugDetails,
                                                                                logging)
                    TG= copy.deepcopy(BestTG)
                    AG= copy.deepcopy(BestAG)
                    del BestTG,BestCTG,BestAG
                elif Config.Mapping_Function=='IterativeLocalSearch':
                    (BestTG,BestCTG,BestAG)=Local_Search.OptimizeMappingIterativeLocalSearch(TG,CTG,AG,NoCRG,SHM,
                                                                                        Config.IterativeLocalSearchIterations,
                                                                                        Config.LocalSearchIteration,
                                                                                        Config.DebugInfo,
                                                                                        Config.DebugDetails,
                                                                                        logging)
                    TG= copy.deepcopy(BestTG)
                    AG= copy.deepcopy(BestAG)
                    del BestTG,BestCTG,BestAG
                Scheduling_Reports.ReportMappedTasks(AG)
                Mapping_Functions.CostFunction(TG,AG,SHM,True)
                return TG,AG
            else:
                Mapping_Functions.ReportMapping(AG)
                print "==========================================="
                return None, None
        else :
            print "Initial Clustering Failed...."
            return None, None
    elif Config.Mapping_Function=='SimulatedAnnealing':
        None