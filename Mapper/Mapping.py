# Copyright (C) 2015 Siavoosh Payandeh Azad

import copy

from ConfigAndPackages import Config
import Scheduler
import Mapping_Functions, Mapping_Reports, Mapping_Animation
from Clusterer import Clustering, ClusteringReports
from Mapping_Heuristics import SimpleGreedy,Local_Search,SimulatedAnnealing,NMap
from Scheduler import Scheduler,Scheduling_Reports


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

    elif Config.Mapping_Function == 'LocalSearch' or Config.Mapping_Function == 'IterativeLocalSearch'\
         or Config.Mapping_Function == 'SimulatedAnnealing':
        if Config.TG_Type == 'RandomDependent' or Config.TG_Type == 'Manual':
            pass
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomDependent')
    # clustered task graph
        CTG = copy.deepcopy(Clustering.TaskClusterGeneration(len(AG.nodes())))
        if Clustering.InitialClustering(TG, CTG):
            # Clustered Task Graph Optimization
            (BestClustering, BestTaskGraph) = Clustering.ClusteringOptimization_LocalSearch(TG, CTG, Config.ClusteringIteration)
            TG = copy.deepcopy(BestTaskGraph)
            CTG = copy.deepcopy(BestClustering)
            del BestClustering, BestTaskGraph
            #Clustering_Test.DoubleCheckCTG(TG, CTG)
            ClusteringReports.ReportCTG(CTG, "CTG_PostOpt.png")
            ClusteringReports.VizClusteringOpt()
            # Mapping CTG on AG
            if Mapping_Functions.MakeInitialMapping(TG, CTG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, True, logging):

                if Config.DistanceBetweenMapping:
                    initmpSr = Mapping_Functions.MappingIntoString(TG)
                    #print initmpSr
                else:
                    initmpSr = None

                Mapping_Reports.ReportMapping(AG, logging)
                # Schedule all tasks
                Scheduler.ScheduleAll(TG, AG, SHM, Config.DebugInfo, Config.DebugDetails)
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
                                                                                        Config.DebugDetails,logging,
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
                                                                                      Config.SimulatedAnnealingIteration,
                                                                                      'SA_MappingCost', logging)
                    Mapping_Reports.VizMappingOpt('SA_MappingCost')
                    if Config.CoolingMethod == 'Adaptive':
                        Mapping_Reports.VizCostSlope()
                    TG = copy.deepcopy(BestTG)
                    AG = copy.deepcopy(BestAG)
                    del BestTG, BestCTG, BestAG
                #print Mapping_Functions.MappingIntoString(TG)
                Scheduling_Reports.ReportMappedTasks(AG, logging)
                Mapping_Functions.CostFunction(TG, AG, SHM, True,  InitialMappingString = initmpSr)
                # Mapping_Animation.AnimateMapping()
                return TG, AG
            else:
                Mapping_Reports.ReportMapping(AG, logging)
                print "==========================================="
                return None, None
        else :
            print "Initial Clustering Failed...."
            return None, None
    return None, None