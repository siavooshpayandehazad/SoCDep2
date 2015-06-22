__author__ = 'siavoosh'

import copy

from ConfigAndPackages import Config
from Mapper import Mapping
from Scheduler import Scheduling_Reports
from SystemHealthMonitoring import SystemHealthMonitor
from TaskGraphUtilities import Task_Graph_Reports,TG_Functions
from RoutingAlgorithms import Routing,Calculate_Reachability,ReachabilityReports
from ArchGraphUtilities import Arch_Graph_Reports,AG_Functions,AG_Test
from Scheduler import TrafficTableGenerator


def InitializeSystem(logging):
    TG = copy.deepcopy(TG_Functions.GenerateTG())
    Task_Graph_Reports.ReportTaskGraph(TG, logging)
    Task_Graph_Reports.DrawTaskGraph(TG)
    TG_Functions.CheckAcyclic(TG, logging)
    ####################################################################
    AG = copy.deepcopy(AG_Functions.GenerateAG(logging))
    AG_Functions.UpdateAGRegions(AG)
    AG_Test.AG_Test()
    Arch_Graph_Reports.DrawArchGraph(AG)
    ####################################################################
    SHM = SystemHealthMonitor.SystemHealthMonitor()
    SHM.SetUp_NoC_SystemHealthMap(AG, Config.TurnsHealth)
    # SHM.Report_NoC_SystemHealthMap()
    print "==========================================="
    print "SYSTEM IS UP..."
    # Here we are injecting initial faults of the system
    SHM.ApplyInitialFaults()
    NoCRG = copy.deepcopy(Routing.GenerateNoCRouteGraph(AG, SHM, Config.UsedTurnModel, Config.DebugInfo, Config.DebugDetails))
    # NoCRG = Routing.GenerateNoCRouteGraphFromFile(AG, SHM, Config.RoutingFilePath, Config.DebugInfo, Config.DebugDetails)

    # in case of partitioning, we have to route based on different Route-graphs
    if Config.EnablePartitioning:
        CriticalRG, NonCriticalRG = Calculate_Reachability.CalculateReachabilityWithRegions(AG,SHM)
        ReachabilityReports.ReportGSNoCFriendlyReachabilityInFile(AG)
    else:
        CriticalRG, NonCriticalRG = None, None
    ####################################################################
    BestTG, BestAG = Mapping.Mapping(TG, AG, NoCRG, CriticalRG, NonCriticalRG, SHM, logging)
    if BestAG is not None and BestTG is not None:
        TG = copy.deepcopy(BestTG)
        AG = copy.deepcopy(BestAG)
        del BestTG, BestAG
        # SHM.AddCurrentMappingToMPM(TG)
    # SHM.RandomFaultInjection()
    # SHM.ReportMPM()

    Scheduling_Reports.GenerateGanttCharts(TG, AG)
    TrafficTableGenerator.GenerateNoximTrafficTable()
    TrafficTableGenerator.GenerateGSNoCTrafficTable(AG, TG)
    """
    Reachability_Test.ReachabilityTest()
    Calculate_Reachability.CalculateReachability(AG, NoCRG)
    ReachabilityReports.ReportReachability(AG)
    ReachabilityReports.ReportReachabilityInFile(AG, "ReachAbilityNodeReport")
    Calculate_Reachability.OptimizeReachabilityRectangles(AG, Config.NumberOfRects)
    ReachabilityReports.ReportReachability(AG)
    ReachabilityReports.ReportReachabilityInFile(AG, "ReachAbilityRectReport")
    ReachabilityReports.ReportGSNoCFriendlyReachabilityInFile(AG)
    """
    return TG, AG, NoCRG, SHM, CriticalRG, NonCriticalRG