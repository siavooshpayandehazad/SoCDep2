# Copyright (C) Siavoosh Payandeh Azad

import copy, time

from ConfigAndPackages import Config
from Mapper import Mapping, Mapping_Reports, Mapping_Animation
from Scheduler import Scheduling_Reports
from SystemHealthMonitoring import SystemHealthMonitoringUnit, SHMU_Reports, SHMU_Functions, TestSchedulingUnit, SHMU_Test
from TaskGraphUtilities import Task_Graph_Reports, TG_Functions, TG_Test
from RoutingAlgorithms import Routing, Calculate_Reachability, ReachabilityReports, RoutingGraph_Reports, Reachability_Test
from ArchGraphUtilities import Arch_Graph_Reports, AG_Functions, AG_Test, Optimize_3D_AG
from Scheduler import TrafficTableGenerator, Scheduler



def InitializeSystem(logging):
    TG = copy.deepcopy(TG_Functions.GenerateTG())
    Task_Graph_Reports.ReportTaskGraph(TG, logging)
    Task_Graph_Reports.DrawTaskGraph(TG)
    if Config.TestMode:
        TG_Test.CheckAcyclic(TG, logging)
    ####################################################################
    AG = copy.deepcopy(AG_Functions.GenerateAG(logging))
    AG_Functions.UpdateAGRegions(AG)
    AG_Functions.RandomDarkness(AG)
    if Config.EnablePartitioning:
        AG_Functions.SetupNetworkPartitioning(AG)
    if Config.TestMode:
        AG_Test.AG_Test()
    if Config.FindOptimumAG:
        Arch_Graph_Reports.DrawArchGraph(AG, "AG_Full")
    else:
        Arch_Graph_Reports.DrawArchGraph(AG, "AG")
    ####################################################################
    Config.SetUpTurnsHealth()
    if Config.TestMode:
        SHMU_Test.TestSHMU(AG)
    SHMU = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
    SHMU.SetUp_NoC_SystemHealthMap(AG, Config.TurnsHealth)
    # Here we are injecting initial faults of the system: we assume these fault
    # information is obtained by post manufacturing system diagnosis
    if Config.FindOptimumAG:
        Optimize_3D_AG.OptimizeAG_VL(AG, SHMU, logging)
        Optimize_3D_AG.CleanUpAG(AG, SHMU)
        Arch_Graph_Reports.DrawArchGraph(AG, "AG_VLOpt")
    SHMU_Functions.ApplyInitialFaults(SHMU)
    if Config.SHM_Drawing:
        SHMU_Reports.DrawSHM(SHMU.SHM)
        SHMU_Reports.DrawTempDistribution(SHMU.SHM)
    # SHM_Reports.Report_NoC_SystemHealthMap()
    ####################################################################
    RoutingGraphStartTime = time.time()
    if Config.SetRoutingFromFile:
        NoCRG = copy.deepcopy(Routing.GenerateNoCRouteGraphFromFile(AG, SHMU, Config.RoutingFilePath,
                                                                    Config.DebugInfo, Config.DebugDetails))
    else:
        NoCRG = copy.deepcopy(Routing.GenerateNoCRouteGraph(AG, SHMU, Config.UsedTurnModel,
                                                            Config.DebugInfo, Config.DebugDetails))
    print ("\033[92mTIME::\033[0m ROUTING GRAPH GENERATION TOOK: "
           + str(round(time.time()-RoutingGraphStartTime))+" SECONDS")
    # this is for double checking...
    if Config.FindOptimumAG:
        Calculate_Reachability.ReachabilityMetric(AG, NoCRG, True)
    # Some visualization...
    if Config.RG_Draw:
        RoutingGraph_Reports.DrawRG(NoCRG)
    ####################################################################
    # in case of partitioning, we have to route based on different Route-graphs
    if Config.EnablePartitioning:
        CriticalRG, NonCriticalRG = Calculate_Reachability.CalculateReachabilityWithRegions(AG, SHMU)
        ReachabilityReports.ReportGSNoCFriendlyReachabilityInFile(AG)
    else:
        if Config.TestMode:
            Reachability_Test.ReachabilityTest()
        CriticalRG, NonCriticalRG = None, None
        Calculate_Reachability.CalculateReachability(AG, NoCRG)
        Calculate_Reachability.OptimizeReachabilityRectangles(AG, Config.NumberOfRects)
        # ReachabilityReports.ReportReachability(AG)
        ReachabilityReports.ReportReachabilityInFile(AG, "ReachAbilityNodeReport")
        ReachabilityReports.ReportGSNoCFriendlyReachabilityInFile(AG)
    ####################################################################
    BestTG, BestAG = Mapping.Mapping(TG, AG, NoCRG, CriticalRG, NonCriticalRG, SHMU.SHM, logging)
    if BestAG is not None and BestTG is not None:
        TG = copy.deepcopy(BestTG)
        AG = copy.deepcopy(BestAG)
        del BestTG, BestAG
        # SHM.AddCurrentMappingToMPM(TG)
    if Config.Mapping_Dstr_Drawing:
        Mapping_Reports.DrawMappingDistribution(AG, SHMU)
    if Config.Mapping_Drawing:
        Mapping_Reports.DrawMapping(TG, AG, SHMU)
    Scheduling_Reports.GenerateGanttCharts(TG, AG, "SchedulingTG")
    ####################################################################
    # PMC-Graph
    # at this point we assume that the system health map knows about the initial faults from
    # the diagnosis process
    if Config.GeneratePMCG:
        PMCGStartTime = time.time()
        if Config.OneStepDiagnosable:
            PMCG = TestSchedulingUnit.GenerateOneStepDiagnosablePMCG(AG, SHMU)
        else:
            PMCG = TestSchedulingUnit.GenerateSequentiallyDiagnosablePMCG(AG, SHMU.SHM)
        TTG = TestSchedulingUnit.GenerateTestTGFromPMCG(PMCG)
        print ("\033[92mTIME::\033[0m PMCG AND TTG GENERATION TOOK: "
               + str(round(time.time()-PMCGStartTime)) + " SECONDS")
        if Config.PMCG_Drawing:
            TestSchedulingUnit.DrawPMCG(PMCG)
        if Config.TTG_Drawing:
            TestSchedulingUnit.DrawTTG(TTG)
        TestSchedulingUnit.InsertTestTasksInTG(PMCG, TG)
        Task_Graph_Reports.DrawTaskGraph(TG, TTG=TTG)
        TestSchedulingUnit.MapTestTasks(TG, AG, SHMU.SHM, NoCRG, logging)
        Scheduler.ScheduleTestInTG(TG, AG, SHMU, False, logging)
        Scheduling_Reports.ReportMappedTasks(AG, logging)
        # TestSchedulingUnit.RemoveTestTasksFromTG(TTG, TG)
        # Task_Graph_Reports.DrawTaskGraph(TG, TTG=TTG)
        Scheduling_Reports.GenerateGanttCharts(TG, AG, "SchedulingWithTTG")
    else:
        PMCG = None

    print ("===========================================")
    print ("SYSTEM IS UP...")

    TrafficTableGenerator.GenerateNoximTrafficTable(AG, TG)
    TrafficTableGenerator.GenerateGSNoCTrafficTable(AG, TG)
    if Config.GenMappingFrames:
        Mapping_Animation.GenerateFrames(TG, AG, SHMU)
    return TG, AG, SHMU, NoCRG, CriticalRG, NonCriticalRG, PMCG