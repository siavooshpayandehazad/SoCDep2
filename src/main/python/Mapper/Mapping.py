# Copyright (C) 2015 Siavoosh Payandeh Azad

import copy
import time
from ConfigAndPackages import Config
import Mapping_Functions
import Mapping_Reports
from Clusterer import Clustering, Clustering_Reports, Clustering_Functions
from Mapping_Heuristics import SimpleGreedy, Local_Search, SimulatedAnnealing, NMap
from Scheduler import Scheduler, Scheduling_Reports, Scheduling_Functions


def mapping(tg, ag, noc_rg, critical_rg, non_critical_rg, shm, logging, iteration=None
            , initial_mapping_string = None):
    """
    Calculate different mapping algorithms
    Returns tg And ag after Mapping in case of success
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param noc_rg: NoC Routing Graph
    :param critical_rg: NoC Routing Graph for Critical Region
    :param non_critical_rg: NoC Routing Graph for non-Critical Region
    :param shm: System Health Map! (Please note that mapper should not even have access to ful SHMU info)
    :param logging: logging file
    :return: (tg, ag) in case of failing returns (None, None)
    """
    # to run the following heuristics (Min_Min,Max_Min), one needs to use independent
    # tasks... Please use: generate_random_independent_tg
    if Config.Mapping_Function == 'MinMin':
        if Config.tg.type == 'RandomIndependent':
            return SimpleGreedy.min_min_mapping(tg, ag, shm, logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function == 'MaxMin':
        if Config.tg.type == 'RandomIndependent':
            return SimpleGreedy.max_min_mapping(tg, ag, shm, logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function == 'MinExecutionTime':
        if Config.tg.type == 'RandomIndependent':
            return SimpleGreedy.min_execution_time(tg, ag, shm, logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function == 'MinimumCompletionTime':
        if Config.tg.type == 'RandomIndependent':
            return SimpleGreedy.minimum_completion_time(tg, ag, shm, logging)
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomIndependent')

    elif Config.Mapping_Function == 'NMap':
        return NMap.n_map(tg, ag, noc_rg, critical_rg, non_critical_rg, shm, logging)

    elif Config.Mapping_Function in ['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing']:
        if Config.tg.type in ['RandomDependent', 'Manual', 'FromDOTFile']:
            pass
        else:
            raise ValueError('WRONG TG TYPE FOR THIS MAPPING FUNCTION. SHOULD USE::RandomDependent')
        clustering_start_time = time.time()
        # clustered task graph
        if Config.task_clustering:
            ctg = copy.deepcopy(Clustering.generate_ctg(len(ag.nodes())))
            if Clustering.initial_clustering(tg, ctg):
                # Clustered Task Graph Optimization
                if Config.Clustering_Optimization:
                    (best_clustering, best_task_graph) = \
                        Clustering.ctg_opt_local_search(tg, ctg, Config.clustering.iterations, logging)
                    tg = copy.deepcopy(best_task_graph)
                    ctg = copy.deepcopy(best_clustering)
                    del best_clustering, best_task_graph
                    # Clustering_Test.double_check_ctg(tg, ctg)
                    Clustering_Reports.report_ctg(ctg, "CTG_PostOpt.png")
                    Clustering_Reports.viz_clustering_opt()
                else:
                    print ("CLUSTERING OPTIMIZATION TURNED OFF...")
                    print ("REMOVING EMPTY CLUSTERS...")
                    Clustering_Functions.remove_empty_clusters(ctg)
                    Clustering_Reports.report_ctg(ctg, "CTG_PostCleaning.png")

                print ("\033[92mTIME::\033[0m CLUSTERING AND OPTIMIZATION TOOK: "
                       + str(round(time.time()-clustering_start_time))+" SECONDS")
            else:
                print ("Initial Clustering Failed....")
                raise ValueError("INITIAL CLUSTERING FAILED...")
        else:
            ctg = copy.deepcopy(Clustering.gen_transparent_clusters(tg))
        mapping_start_time = time.time()
        # Mapping CTG on AG
        random_seed = Config.mapping_random_seed
        if Mapping_Functions.make_initial_mapping(tg, ctg, ag, shm, noc_rg, critical_rg, non_critical_rg,
                                                  True, logging, random_seed, iteration):
            #if Config.DistanceBetweenMapping:
            #    init_mapping_string = Mapping_Functions.mapping_into_string(tg)
                # print (init_mapping_string)
            #else:
            #    init_mapping_string = None

            Mapping_Reports.report_mapping(ag, logging)
            # Schedule all tasks
            Scheduling_Functions.clear_scheduling(ag)
            Scheduler.schedule_all(tg, ag, shm, Config.DebugDetails, logging)
            Scheduling_Reports.report_mapped_tasks(ag, logging)
            Mapping_Functions.mapping_cost_function(tg, ag, shm, Config.DebugInfo)
            if Config.Mapping_Function == 'LocalSearch':
                mapping_cost_file = open('Generated_Files/Internal/LocalSearchMappingCost.txt', 'w')
                current_cost = Mapping_Functions.mapping_cost_function(tg, ag, shm, False, initial_mapping_string=initial_mapping_string)
                mapping_cost_file.write(str(current_cost)+"\n")
                mapping_cost_file.close()

                mapping_process_file = open('Generated_Files/Internal/MappingProcess.txt', 'w')
                mapping_process_file.write(Mapping_Functions.mapping_into_string(tg)+"\n")
                mapping_process_file.close()

                (best_tg, best_ctg, best_ag) = \
                    Local_Search.mapping_opt_local_search(tg, ctg, ag, noc_rg, critical_rg,
                                                          non_critical_rg, shm,
                                                          Config.LocalSearchIteration,
                                                          Config.DebugInfo, Config.DebugDetails, logging,
                                                          "LocalSearchMappingCost", "MappingProcess",
                                                          Config.mapping_random_seed, initial_mapping_string=initial_mapping_string)
                tg = copy.deepcopy(best_tg)
                ag = copy.deepcopy(best_ag)
                del best_tg, best_ctg, best_ag
                Mapping_Reports.viz_mapping_opt('LocalSearchMappingCost', iteration)
            elif Config.Mapping_Function == 'IterativeLocalSearch':
                (best_tg, best_ctg, best_ag) = \
                    Local_Search.mapping_opt_iterative_local_search(tg, ctg, ag, noc_rg, critical_rg,
                                                                    non_critical_rg, shm,
                                                                    Config.IterativeLocalSearchIterations,
                                                                    Config.LocalSearchIteration,
                                                                    Config.DebugInfo, Config.DebugDetails,
                                                                    logging)
                tg = copy.deepcopy(best_tg)
                ag = copy.deepcopy(best_ag)
                del best_tg, best_ctg, best_ag
                Mapping_Reports.viz_mapping_opt('LocalSearchMappingCost', iteration)
            elif Config.Mapping_Function == 'SimulatedAnnealing':
                (best_tg, best_ctg, best_ag) = SimulatedAnnealing.optimize_mapping_sa(tg, ctg, ag, noc_rg,
                                                                                      critical_rg, non_critical_rg,
                                                                                      shm, 'SA_MappingCost',
                                                                                      logging)
                Mapping_Reports.viz_mapping_opt('SA_MappingCost', iteration=None)
                if Config.SA_AnnealingSchedule == 'Adaptive':
                    Mapping_Reports.viz_cost_slope()
                elif Config.SA_AnnealingSchedule == 'Huang':
                    Mapping_Reports.viz_huang_race()
                tg = copy.deepcopy(best_tg)
                ag = copy.deepcopy(best_ag)
                del best_tg, best_ctg, best_ag
            # print (Mapping_Functions.mapping_into_string(TG))
            print ("\033[92mTIME::\033[0m MAPPING AND OPTIMIZATION TOOK: "
                   + str(round(time.time()-mapping_start_time))+" SECONDS")

            Mapping_Reports.report_mapping(ag, logging)
            Scheduling_Functions.clear_scheduling(ag)
            Scheduler.schedule_all(tg, ag, shm, False, logging)
            Scheduling_Reports.report_mapped_tasks(ag, logging)
            if not Scheduling_Functions.check_if_all_deadlines_are_met(tg,ag):
                raise ValueError("not all critical tasks have met their deadline!")
            Mapping_Functions.mapping_cost_function(tg, ag, shm, True,  initial_mapping_string=initial_mapping_string)
            return tg, ag
        else:
            Mapping_Reports.report_mapping(ag, logging)
            print ("===========================================")
            raise ValueError("INITIAL MAPPING FAILED...")

    return None, None
