# Copyright (C) 2015 Siavoosh Payandeh Azad

import copy, time

from ConfigAndPackages import Config
import Scheduler
import Mapping_Functions, Mapping_Reports, Mapping_Animation
from Clusterer import Clustering, ClusteringReports, Clustering_Functions
from Mapping_Heuristics import SimpleGreedy,Local_Search,SimulatedAnnealing,NMap
from Scheduler import Scheduler,Scheduling_Reports, Scheduling_Functions


def Mapping(TG, AG, NoCRG, CriticalRG, NonCriticalRG, SHM, logging):
    # to run the following heuristics (Min_Min,Max_Min), one needs to use independent
    # tasks... Please use: GenerateRandomIndependentTG
    if Config.Mapping_Function == 'MinMin':
        if Config.TG_Type == 'RandomIndependent':
            return SimpleGreedy.Min_Min_Mapping(TG, AG, NoCRG, SHM, logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function == 'MaxMin':
        if Config.TG_Type == 'RandomIndependent':
            return SimpleGreedy.Max_Min_Mapping (TG, AG, NoCRG, SHM, logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function == 'MinExecutionTime':
        if Config.TG_Type == 'RandomIndependent':
            return SimpleGreedy.MinExecutionTime(TG, AG, SHM, logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function == 'MinimumCompletionTime':
        if Config.TG_Type == 'RandomIndependent':
            return SimpleGreedy.MinimumCompletionTime(TG, AG, SHM, logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function == 'NMap':
        return NMap.NMap(TG, AG, NoCRG, CriticalRG, NonCriticalRG, SHM, logging)

    elif Config.Mapping_Function in ['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing']:
        if Config.TG_Type == 'RandomDependent' or Config.TG_Type == 'Manual':
            pass
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomDependent')
        ClusteringStartTime = time.time()
        # clustered task graph
        CTG = copy.deepcopy(Clustering.TaskClusterGeneration(len(AG.nodes())))
        if Clustering.InitialClustering(TG, CTG):
            # Clustered Task Graph Optimization
            if Config.Clustering_Optimization:
                (BestClustering, BestTaskGraph) = Clustering.ClusteringOptimization_LocalSearch(TG, CTG,
                                                                                                Config.ClusteringIteration)
                TG = copy.deepcopy(BestTaskGraph)
                CTG = copy.deepcopy(BestClustering)
                del BestClustering, BestTaskGraph
                # Clustering_Test.DoubleCheckCTG(TG, CTG)
                ClusteringReports.ReportCTG(CTG, "CTG_PostOpt.png")
                ClusteringReports.VizClusteringOpt()
            else:
                print ("CLUSTERING OPTIMIZATION TURNED OFF...")
                print ("REMOVING EMPTY CLUSTERS...")
                Clustering_Functions.DeleteEmptyClusters(CTG)
                ClusteringReports.ReportCTG(CTG, "CTG_PostCleaning.png")

            print ("\033[92mTIME::\033[0m CLUSTERING AND OPTIMIZATION TOOK: "
                   +str(round(time.time()-ClusteringStartTime))+" SECONDS")
            MappingStartTime = time.time()
            # Mapping CTG on AG
            if Mapping_Functions.MakeInitialMapping(TG, CTG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, True, logging):

                if Config.DistanceBetweenMapping:
                    initmpSr = Mapping_Functions.MappingIntoString(TG)
                    # print (initmpSr)
                else:
                    initmpSr = None

                Mapping_Reports.ReportMapping(AG, logging)
                # Schedule all tasks
                Scheduling_Functions.ClearScheduling(AG, TG)
                Scheduler.ScheduleAll(TG, AG, SHM, Config.DebugInfo, Config.DebugDetails, logging)
                Scheduling_Reports.ReportMappedTasks(AG, logging)
                Mapping_Functions.CostFunction(TG, AG, SHM, Config.DebugInfo)
                if Config.Mapping_Function == 'LocalSearch':
                    MappingCostFile = open('Generated_Files/Internal/LocalSearchMappingCost.txt','w')
                    CurrentCost = Mapping_Functions.CostFunction(TG,AG,SHM,False)
                    MappingCostFile.write(str(CurrentCost)+"\n")
                    MappingCostFile.close()

                    MappingProcessFile = open('Generated_Files/Internal/MappingProcess.txt','w')
                    MappingProcessFile.write(Mapping_Functions.MappingIntoString(TG)+"\n")
                    MappingProcessFile.close()

                    (BestTG, BestCTG, BestAG) = Local_Search.OptimizeMappingLocalSearch(TG, CTG, AG, NoCRG, CriticalRG,
                                                                                        NonCriticalRG, SHM,
                                                                                        Config.LocalSearchIteration,
                                                                                        Config.DebugInfo,
                                                                                        Config.DebugDetails, logging,
                                                                                        "LocalSearchMappingCost",
                                                                                        "MappingProcess")
                    TG = copy.deepcopy(BestTG)
                    AG = copy.deepcopy(BestAG)
                    del BestTG,BestCTG,BestAG
                    Mapping_Reports.VizMappingOpt('LocalSearchMappingCost')
                elif Config.Mapping_Function == 'IterativeLocalSearch':
                    (BestTG, BestCTG, BestAG) = Local_Search.OptimizeMappingIterativeLocalSearch(TG, CTG, AG, NoCRG,
                                                                                                 CriticalRG,
                                                                                                 NonCriticalRG, SHM,
                                                                                                 Config.IterativeLocalSearchIterations,
                                                                                                 Config.LocalSearchIteration,
                                                                                                 Config.DebugInfo,
                                                                                                 Config.DebugDetails,
                                                                                                 logging)
                    TG = copy.deepcopy(BestTG)
                    AG = copy.deepcopy(BestAG)
                    del BestTG, BestCTG, BestAG
                    Mapping_Reports.VizMappingOpt('LocalSearchMappingCost')
                elif Config.Mapping_Function == 'SimulatedAnnealing':
                    (BestTG, BestCTG, BestAG) = SimulatedAnnealing.OptimizeMapping_SA(TG, CTG, AG, NoCRG, CriticalRG,
                                                                                      NonCriticalRG, SHM,
                                                                                      'SA_MappingCost', logging)
                    Mapping_Reports.VizMappingOpt('SA_MappingCost')
                    if Config.SA_AnnealingSchedule == 'Adaptive':
                        Mapping_Reports.VizCostSlope()
                    elif Config.SA_AnnealingSchedule == 'Huang':
                        Mapping_Reports.VizHuangRace()
                    TG = copy.deepcopy(BestTG)
                    AG = copy.deepcopy(BestAG)
                    del BestTG, BestCTG, BestAG
                # print (Mapping_Functions.MappingIntoString(TG))
                print ("\033[92mTIME::\033[0m MAPPING AND OPTIMIZATION TOOK: "
                       +str(round(time.time()-MappingStartTime))+" SECONDS")

                Scheduling_Functions.ClearScheduling(AG, TG)
                Scheduler.ScheduleAll(TG, AG, SHM, False, False, logging)
                Scheduling_Reports.ReportMappedTasks(AG, logging)
                Mapping_Functions.CostFunction(TG, AG, SHM, True,  InitialMappingString = initmpSr)
                return TG, AG
            else:
                Mapping_Reports.ReportMapping(AG, logging)
                print ("===========================================")
                raise ValueError("INITIAL MAPPING FAILED...")
        else :
            print ("Initial Clustering Failed....")
            raise ValueError("INITIAL CLUSTERING FAILED...")
    return None, None