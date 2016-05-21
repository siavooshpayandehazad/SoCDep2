# Copyright (C) Siavoosh Payandeh Azad

import copy
import time

from ArchGraphUtilities import Arch_Graph_Reports, AG_Functions
from ArchGraphUtilities.vl_optimization import vl_opt, vl_opt_functions
from ConfigAndPackages import Config
from Mapper import Mapping, Mapping_Reports, Mapping_Animation
from Mapper import Mapping_Functions
from RoutingAlgorithms import Routing, Calculate_Reachability, ReachabilityReports, \
    RoutingGraph_Reports, Routing_Functions
from Scheduler import Scheduling_Reports, TrafficTableGenerator, Scheduler
from SystemHealthMonitoring import SystemHealthMonitoringUnit, SHMU_Reports, \
    SHMU_Functions, TestSchedulingUnit
from TaskGraphUtilities import Task_Graph_Reports, TG_Functions, TG_Test


def initialize_system(logging):
    """
    Generates the Task graph, Architecture Graph, System Health Monitoring Unit, NoC routing graph(s) and
    Test Task Graphs and does the mapping and scheduling and returns to the user the initial system
    :param logging: logging file
    :return:  tg, ag, shmu, noc_rg, critical_rg, noncritical_rg, pmcg
    """
    tg = copy.deepcopy(TG_Functions.generate_tg())
    if Config.DebugInfo:
        Task_Graph_Reports.report_task_graph(tg, logging)
    Task_Graph_Reports.draw_task_graph(tg)
    if Config.TestMode:
        TG_Test.check_acyclic(tg, logging)
    ####################################################################
    ag = copy.deepcopy(AG_Functions.generate_ag(logging))
    AG_Functions.update_ag_regions(ag)
    AG_Functions.random_darkness(ag)
    if Config.EnablePartitioning:
        AG_Functions.setup_network_partitioning(ag)
    if Config.FindOptimumAG:
        Arch_Graph_Reports.draw_ag(ag, "AG_Full")
    else:
        Arch_Graph_Reports.draw_ag(ag, "AG")
    ####################################################################
    Config.setup_turns_health()

    shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
    shmu.setup_noc_shm(ag, Config.TurnsHealth, True)
    # Here we are injecting initial faults of the system: we assume these fault
    # information is obtained by post manufacturing system diagnosis
    if Config.FindOptimumAG:
        vl_opt.optimize_ag_vertical_links(ag, shmu, logging)
        vl_opt_functions.cleanup_ag(ag, shmu)
        Arch_Graph_Reports.draw_ag(ag, "AG_VLOpt")
    SHMU_Functions.apply_initial_faults(shmu)
    if Config.viz.shm:
        SHMU_Reports.draw_shm(shmu.SHM)
        SHMU_Reports.draw_temp_distribution(shmu.SHM)
    # SHM_Reports.report_noc_shm()
    ####################################################################
    routing_graph_start_time = time.time()
    if Config.SetRoutingFromFile:
        noc_rg = copy.deepcopy(Routing.gen_noc_route_graph_from_file(ag, shmu, Config.RoutingFilePath,
                                                                     Config.DebugInfo, Config.DebugDetails))
    else:
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                Config.DebugInfo, Config.DebugDetails))
    Routing_Functions.check_deadlock_freeness(noc_rg)
    print ("\033[92mTIME::\033[0m ROUTING GRAPH GENERATION TOOK: " +
           str(round(time.time()-routing_graph_start_time))+" SECONDS")
    # this is for double checking...
    if Config.FindOptimumAG:
        Calculate_Reachability.reachability_metric(ag, noc_rg, True)
    # Some visualization...
    if Config.viz.rg:
        RoutingGraph_Reports.draw_rg(noc_rg)
    ####################################################################
    # in case of partitioning, we have to route based on different Route-graphs
    if Config.EnablePartitioning:
        critical_rg, noncritical_rg = Calculate_Reachability.calculate_reachability_with_regions(ag, shmu)
        ReachabilityReports.report_gsnoc_friendly_reachability_in_file(ag)
    else:
        critical_rg, noncritical_rg = None, None
        Calculate_Reachability.calculate_reachability(ag, noc_rg)
        Calculate_Reachability.optimize_reachability_rectangles(ag, Config.NumberOfRects)
        # ReachabilityReports.report_reachability(ag)
        ReachabilityReports.report_reachability_in_file(ag, "ReachAbilityNodeReport")
        ReachabilityReports.report_gsnoc_friendly_reachability_in_file(ag)
    ####################################################################
    if Config.read_mapping_from_file:
        Mapping_Functions.read_mapping_from_file(tg, ag, shmu.SHM, noc_rg, critical_rg, noncritical_rg,
                                                 Config.mapping_file_path, logging)
        Scheduler.schedule_all(tg, ag, shmu.SHM, False, logging)
    else:
        best_tg, best_ag = Mapping.mapping(tg, ag, noc_rg, critical_rg, noncritical_rg, shmu.SHM, logging)
        if best_ag is not None and best_tg is not None:
            tg = copy.deepcopy(best_tg)
            ag = copy.deepcopy(best_ag)
            del best_tg, best_ag
            # SHM.add_current_mapping_to_mpm(tg)
            Mapping_Functions.write_mapping_to_file(ag, "mapping_report")
    if Config.viz.mapping_distribution:
        Mapping_Reports.draw_mapping_distribution(ag, shmu)
    if Config.viz.mapping:
        Mapping_Reports.draw_mapping(tg, ag, shmu.SHM, "Mapping_post_opt")
    if Config.viz.scheduling:
        Scheduling_Reports.generate_gantt_charts(tg, ag, "SchedulingTG")
    ####################################################################
    # PMC-Graph
    # at this point we assume that the system health map knows about the initial faults from
    # the diagnosis process
    if Config.GeneratePMCG:
        pmcg_start_time = time.time()
        if Config.OneStepDiagnosable:
            pmcg = TestSchedulingUnit.gen_one_step_diagnosable_pmcg(ag, shmu.SHM)
        else:
            pmcg = TestSchedulingUnit.gen_sequentially_diagnosable_pmcg(ag, shmu.SHM)
        test_tg = TestSchedulingUnit.generate_test_tg_from_pmcg(pmcg)
        print ("\033[92mTIME::\033[0m PMCG AND TTG GENERATION TOOK: " +
               str(round(time.time()-pmcg_start_time)) + " SECONDS")
        if Config.viz.pmcg:
            TestSchedulingUnit.draw_pmcg(pmcg)
        if Config.viz.ttg:
            TestSchedulingUnit.draw_ttg(test_tg)
        TestSchedulingUnit.insert_test_tasks_in_tg(pmcg, tg)
        Task_Graph_Reports.draw_task_graph(tg, ttg=test_tg)
        TestSchedulingUnit.map_test_tasks(tg, ag, shmu.SHM, noc_rg, logging)
        Scheduler.schedule_test_in_tg(tg, ag, shmu.SHM, False, logging)
        Scheduling_Reports.report_mapped_tasks(ag, logging)
        # TestSchedulingUnit.remove_test_tasks_from_tg(test_tg, tg)
        # Task_Graph_Reports.draw_task_graph(tg, TTG=test_tg)
        Scheduling_Reports.generate_gantt_charts(tg, ag, "SchedulingWithTTG")
    else:
        pmcg = None
    Arch_Graph_Reports.gen_latex_ag(ag, shmu.SHM)
    print ("===========================================")
    print ("SYSTEM IS UP...")

    TrafficTableGenerator.generate_noxim_traffic_table(ag, tg)
    if Config.viz.mapping_frames:
        Mapping_Animation.generate_frames(ag, shmu.SHM)
    return tg, ag, shmu, noc_rg, critical_rg, noncritical_rg, pmcg
