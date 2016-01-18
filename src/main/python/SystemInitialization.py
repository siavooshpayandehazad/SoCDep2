# Copyright (C) Siavoosh Payandeh Azad

import copy
import time
from ConfigAndPackages import Config
from Mapper import Mapping, Mapping_Reports, Mapping_Animation
from Mapper import Mapping_Functions
from Scheduler import Scheduling_Reports, TrafficTableGenerator, Scheduler
from SystemHealthMonitoring import SystemHealthMonitoringUnit, SHMU_Reports, \
    SHMU_Functions, TestSchedulingUnit, SHMU_Test
from TaskGraphUtilities import Task_Graph_Reports, TG_Functions, TG_Test
from RoutingAlgorithms import Routing, Calculate_Reachability, ReachabilityReports, \
    RoutingGraph_Reports, Reachability_Test
from ArchGraphUtilities import Arch_Graph_Reports, AG_Functions, AG_Test, Optimize_3D_AG


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
        TG_Test.CheckAcyclic(tg, logging)
    ####################################################################
    ag = copy.deepcopy(AG_Functions.generate_ag(logging))
    AG_Functions.update_ag_regions(ag)
    AG_Functions.random_darkness(ag)
    if Config.EnablePartitioning:
        AG_Functions.setup_network_partitioning(ag)
    if Config.TestMode:
        AG_Test.ag_test()
    if Config.FindOptimumAG:
        Arch_Graph_Reports.draw_ag(ag, "AG_Full")
    else:
        Arch_Graph_Reports.draw_ag(ag, "AG")
    ####################################################################
    Config.setup_turns_health()
    if Config.TestMode:
        SHMU_Test.test_shmu(ag)
    shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
    shmu.setup_noc_shm(ag, Config.TurnsHealth)
    # Here we are injecting initial faults of the system: we assume these fault
    # information is obtained by post manufacturing system diagnosis
    if Config.FindOptimumAG:
        Optimize_3D_AG.optimize_ag_vertical_links(ag, shmu, logging)
        Optimize_3D_AG.cleanup_ag(ag, shmu)
        Arch_Graph_Reports.draw_ag(ag, "AG_VLOpt")
    SHMU_Functions.ApplyInitialFaults(shmu)
    if Config.SHM_Drawing:
        SHMU_Reports.DrawSHM(shmu.SHM)
        SHMU_Reports.DrawTempDistribution(shmu.SHM)
    # SHM_Reports.Report_NoC_SystemHealthMap()
    ####################################################################
    routing_graph_start_time = time.time()
    if Config.SetRoutingFromFile:
        noc_rg = copy.deepcopy(Routing.GenerateNoCRouteGraphFromFile(ag, shmu, Config.RoutingFilePath,
                                                                     Config.DebugInfo, Config.DebugDetails))
    else:
        noc_rg = copy.deepcopy(Routing.GenerateNoCRouteGraph(ag, shmu, Config.UsedTurnModel,
                                                             Config.DebugInfo, Config.DebugDetails))
    print ("\033[92mTIME::\033[0m ROUTING GRAPH GENERATION TOOK: "
           + str(round(time.time()-routing_graph_start_time))+" SECONDS")
    # this is for double checking...
    if Config.FindOptimumAG:
        Calculate_Reachability.ReachabilityMetric(ag, noc_rg, True)
    # Some visualization...
    if Config.RG_Draw:
        RoutingGraph_Reports.draw_rg(noc_rg)
    ####################################################################
    # in case of partitioning, we have to route based on different Route-graphs
    if Config.EnablePartitioning:
        critical_rg, noncritical_rg = Calculate_Reachability.calculate_reachability_with_regions(ag, shmu)
        ReachabilityReports.ReportGSNoCFriendlyReachabilityInFile(ag)
    else:
        if Config.TestMode:
            Reachability_Test.ReachabilityTest()
        critical_rg, noncritical_rg = None, None
        Calculate_Reachability.calculate_reachability(ag, noc_rg)
        Calculate_Reachability.OptimizeReachabilityRectangles(ag, Config.NumberOfRects)
        # ReachabilityReports.ReportReachability(ag)
        ReachabilityReports.ReportReachabilityInFile(ag, "ReachAbilityNodeReport")
        ReachabilityReports.ReportGSNoCFriendlyReachabilityInFile(ag)
    ####################################################################
    if Config.read_mapping_from_file:
        Mapping_Functions.read_mapping_from_file(tg, ag, shmu.SHM, noc_rg, critical_rg, noncritical_rg,
                                                 Config.mapping_file_path, logging)
        Scheduler.schedule_all(tg, ag, shmu.SHM, False, False, logging)
    else:
        best_tg, best_ag = Mapping.mapping(tg, ag, noc_rg, critical_rg, noncritical_rg, shmu.SHM, logging)
        if best_ag is not None and best_tg is not None:
            tg = copy.deepcopy(best_tg)
            ag = copy.deepcopy(best_ag)
            del best_tg, best_ag
            # SHM.AddCurrentMappingToMPM(tg)
            Mapping_Functions.write_mapping_to_file(ag, "mapping_report")
    if Config.Mapping_Dstr_Drawing:
        Mapping_Reports.draw_mapping_distribution(ag, shmu)
    if Config.Mapping_Drawing:
        Mapping_Reports.draw_mapping(tg, ag, shmu.SHM, "Mapping_post_opt")
    if Config.Scheduling_Drawing:
        Scheduling_Reports.generate_gantt_charts(tg, ag, "SchedulingTG")
    ####################################################################
    # PMC-Graph
    # at this point we assume that the system health map knows about the initial faults from
    # the diagnosis process
    if Config.GeneratePMCG:
        pmcg_start_time = time.time()
        if Config.OneStepDiagnosable:
            pmcg = TestSchedulingUnit.GenerateOneStepDiagnosablePMCG(ag, shmu.SHM)
        else:
            pmcg = TestSchedulingUnit.GenerateSequentiallyDiagnosablePMCG(ag, shmu.SHM)
        test_tg = TestSchedulingUnit.GenerateTestTGFromPMCG(pmcg)
        print ("\033[92mTIME::\033[0m PMCG AND TTG GENERATION TOOK: "
               + str(round(time.time()-pmcg_start_time)) + " SECONDS")
        if Config.PMCG_Drawing:
            TestSchedulingUnit.DrawPMCG(pmcg)
        if Config.TTG_Drawing:
            TestSchedulingUnit.DrawTTG(test_tg)
        TestSchedulingUnit.InsertTestTasksInTG(pmcg, tg)
        Task_Graph_Reports.draw_task_graph(tg, ttg=test_tg)
        TestSchedulingUnit.MapTestTasks(tg, ag, shmu.SHM, noc_rg, logging)
        Scheduler.schedule_test_in_tg(tg, ag, shmu.SHM, False, logging)
        Scheduling_Reports.report_mapped_tasks(ag, logging)
        # TestSchedulingUnit.RemoveTestTasksFromTG(test_tg, tg)
        # Task_Graph_Reports.draw_task_graph(tg, TTG=test_tg)
        Scheduling_Reports.generate_gantt_charts(tg, ag, "SchedulingWithTTG")
    else:
        pmcg = None

    print ("===========================================")
    print ("SYSTEM IS UP...")

    TrafficTableGenerator.generate_noxim_traffic_table(ag, tg)
    TrafficTableGenerator.generate_gsnoc_traffic_table(ag, tg)
    if Config.GenMappingFrames:
        Mapping_Animation.generate_frames(tg, ag, shmu.SHM)
    return ag, shmu, noc_rg, critical_rg, noncritical_rg, pmcg
