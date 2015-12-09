# Copyright (C) Siavoosh Payandeh Azad

import copy, time

from ConfigAndPackages import Config
from Mapper import Mapping, Mapping_Reports, Mapping_Animation
from Scheduler import Scheduling_Reports, TrafficTableGenerator, Scheduler
from SystemHealthMonitoring import SystemHealthMonitoringUnit, SHMU_Reports, SHMU_Functions, TestSchedulingUnit, SHMU_Test
from TaskGraphUtilities import Task_Graph_Reports, TG_Functions, TG_Test
from RoutingAlgorithms import Routing, Calculate_Reachability, ReachabilityReports, RoutingGraph_Reports, Reachability_Test
from ArchGraphUtilities import Arch_Graph_Reports, AG_Functions, AG_Test, Optimize_3D_AG


def initialize_system(logging):
    """
    Generates the Task graoh, Architecture Graph, System Health Monitoring Unit, NoC routing graph(s) and
    Test Task Graphs and does the mapping and scheduling and returns to the user the initial system
    :param logging: logging file
    :return:  task_graph, arch_graph, SHMU, NoCRG, CriticalRG, NonCriticalRG, PMCG
    """
    task_graph = copy.deepcopy(TG_Functions.generate_task_graph())
    Task_Graph_Reports.ReportTaskGraph(task_graph, logging)
    Task_Graph_Reports.DrawTaskGraph(task_graph)
    if Config.TestMode:
        TG_Test.CheckAcyclic(task_graph, logging)
    ####################################################################
    arch_graph = copy.deepcopy(AG_Functions.generate_arch_graph(logging))
    AG_Functions.update_arch_graph_regions(arch_graph)
    AG_Functions.random_darkness(arch_graph)
    if Config.EnablePartitioning:
        AG_Functions.setup_network_partitioning(arch_graph)
    if Config.TestMode:
        AG_Test.arch_graph_test()
    if Config.FindOptimumAG:
        Arch_Graph_Reports.draw_arch_graph(arch_graph, "AG_Full")
    else:
        Arch_Graph_Reports.draw_arch_graph(arch_graph, "AG")
    ####################################################################
    Config.SetUpTurnsHealth()
    if Config.TestMode:
        SHMU_Test.TestSHMU(arch_graph)
    SHMU = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
    SHMU.SetUp_NoC_SystemHealthMap(arch_graph, Config.TurnsHealth)
    # Here we are injecting initial faults of the system: we assume these fault
    # information is obtained by post manufacturing system diagnosis
    if Config.FindOptimumAG:
        Optimize_3D_AG.optimize_arch_graph_vertical_links(arch_graph, SHMU, logging)
        Optimize_3D_AG.cleanup_arch_graph(arch_graph, SHMU)
        Arch_Graph_Reports.draw_arch_graph(arch_graph, "AG_VLOpt")
    SHMU_Functions.ApplyInitialFaults(SHMU)
    if Config.SHM_Drawing:
        SHMU_Reports.DrawSHM(SHMU.SHM)
        SHMU_Reports.DrawTempDistribution(SHMU.SHM)
    # SHM_Reports.Report_NoC_SystemHealthMap()
    ####################################################################
    RoutingGraphStartTime = time.time()
    if Config.SetRoutingFromFile:
        NoCRG = copy.deepcopy(Routing.GenerateNoCRouteGraphFromFile(arch_graph, SHMU, Config.RoutingFilePath,
                                                                    Config.DebugInfo, Config.DebugDetails))
    else:
        NoCRG = copy.deepcopy(Routing.GenerateNoCRouteGraph(arch_graph, SHMU, Config.UsedTurnModel,
                                                            Config.DebugInfo, Config.DebugDetails))
    print ("\033[92mTIME::\033[0m ROUTING GRAPH GENERATION TOOK: "
           + str(round(time.time()-RoutingGraphStartTime))+" SECONDS")
    # this is for double checking...
    if Config.FindOptimumAG:
        Calculate_Reachability.ReachabilityMetric(arch_graph, NoCRG, True)
    # Some visualization...
    if Config.RG_Draw:
        RoutingGraph_Reports.DrawRG(NoCRG)
    ####################################################################
    # in case of partitioning, we have to route based on different Route-graphs
    if Config.EnablePartitioning:
        CriticalRG, NonCriticalRG = Calculate_Reachability.calculate_reachability_with_regions(arch_graph, SHMU)
        ReachabilityReports.ReportGSNoCFriendlyReachabilityInFile(arch_graph)
    else:
        if Config.TestMode:
            Reachability_Test.ReachabilityTest()
        CriticalRG, NonCriticalRG = None, None
        Calculate_Reachability.calculate_reachability(arch_graph, NoCRG)
        Calculate_Reachability.OptimizeReachabilityRectangles(arch_graph, Config.NumberOfRects)
        # ReachabilityReports.ReportReachability(arch_graph)
        ReachabilityReports.ReportReachabilityInFile(arch_graph, "ReachAbilityNodeReport")
        ReachabilityReports.ReportGSNoCFriendlyReachabilityInFile(arch_graph)
    ####################################################################
    best_task_graph, BestAG = Mapping.Mapping(task_graph, arch_graph, NoCRG, CriticalRG, NonCriticalRG,
                                              SHMU.SHM, logging)
    if BestAG is not None and best_task_graph is not None:
        task_graph = copy.deepcopy(best_task_graph)
        arch_graph = copy.deepcopy(BestAG)
        del best_task_graph, BestAG
        # SHM.AddCurrentMappingToMPM(task_graph)
    if Config.Mapping_Dstr_Drawing:
        Mapping_Reports.DrawMappingDistribution(arch_graph, SHMU)
    if Config.Mapping_Drawing:
        Mapping_Reports.DrawMapping(task_graph, arch_graph, SHMU)
    Scheduling_Reports.GenerateGanttCharts(task_graph, arch_graph, "SchedulingTG")
    ####################################################################
    # PMC-Graph
    # at this point we assume that the system health map knows about the initial faults from
    # the diagnosis process
    if Config.GeneratePMCG:
        PMCGStartTime = time.time()
        if Config.OneStepDiagnosable:
            PMCG = TestSchedulingUnit.GenerateOneStepDiagnosablePMCG(arch_graph, SHMU)
        else:
            PMCG = TestSchedulingUnit.GenerateSequentiallyDiagnosablePMCG(arch_graph, SHMU.SHM)
        test_task_graph = TestSchedulingUnit.GenerateTestTGFromPMCG(PMCG)
        print ("\033[92mTIME::\033[0m PMCG AND TTG GENERATION TOOK: "
               + str(round(time.time()-PMCGStartTime)) + " SECONDS")
        if Config.PMCG_Drawing:
            TestSchedulingUnit.DrawPMCG(PMCG)
        if Config.TTG_Drawing:
            TestSchedulingUnit.DrawTTG(test_task_graph)
        TestSchedulingUnit.InsertTestTasksInTG(PMCG, task_graph)
        Task_Graph_Reports.DrawTaskGraph(task_graph, TTG=test_task_graph)
        TestSchedulingUnit.MapTestTasks(task_graph, arch_graph, SHMU.SHM, NoCRG, logging)
        Scheduler.ScheduleTestInTG(task_graph, arch_graph, SHMU.SHM, False, logging)
        Scheduling_Reports.report_mapped_tasks(arch_graph, logging)
        # TestSchedulingUnit.RemoveTestTasksFromTG(test_task_graph, task_graph)
        # Task_Graph_Reports.DrawTaskGraph(task_graph, TTG=test_task_graph)
        Scheduling_Reports.GenerateGanttCharts(task_graph, arch_graph, "SchedulingWithTTG")
    else:
        PMCG = None

    print ("===========================================")
    print ("SYSTEM IS UP...")

    TrafficTableGenerator.generate_noxim_traffic_table(arch_graph, task_graph)
    TrafficTableGenerator.generate_gsnoc_traffic_table(arch_graph, task_graph)
    if Config.GenMappingFrames:
        Mapping_Animation.GenerateFrames(task_graph, arch_graph, SHMU.SHM)
    return task_graph, arch_graph, SHMU, NoCRG, CriticalRG, NonCriticalRG, PMCG