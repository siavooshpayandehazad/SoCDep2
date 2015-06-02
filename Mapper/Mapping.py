

__author__ = 'siavoosh'
import random
import copy
from Scheduler import Scheduler,Scheduling_Functions
from Mapping_Functions import AddClusterToNode, ReportMapping,RemoveClusterFromNode,CostFunction,ClearMapping



def MakeInitialMapping(TG,CTG,AG,NoCRG,Report):
    if Report:print "==========================================="
    if Report:print "STARTING INITIAL MAPPING..."
    for Cluster in CTG.nodes():
        DestNode = random.choice(AG.nodes())
        Itteration=0
        while not AddClusterToNode(TG,CTG,AG,NoCRG,Cluster,DestNode,Report):
            Itteration+=1
            RemoveClusterFromNode(TG,CTG,AG,NoCRG,Cluster,DestNode,Report)
            DestNode = random.choice(AG.nodes())        #try another node
            if Report:print "\t-------------------------"
            if Report:print "\tMAPPING ATTEMPT: #",Itteration+1,"FOR CLUSTER:",Cluster
            if Itteration == 10* len(CTG.nodes()):
                print "\033[31mERROR::\033[0m INITIAL MAPPING FAILED..."
                ClearMapping(TG,CTG,AG)
                return False
    if Report:print "INITIAL MAPPING READY..."
    if Report: ReportMapping(AG)
    return True

def OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,IterationNum,Report,DetailedReport):
    if Report:print "==========================================="
    if Report:print "STARTING MAPPING OPTIMIZATION..."
    BestTG=copy.deepcopy(TG)
    BestAG=copy.deepcopy(AG)
    BestCTG=copy.deepcopy(CTG)
    BestCost=CostFunction(TG,AG,Report)
    StartingCost=BestCost
    for Iteration in range(0,IterationNum):
        if DetailedReport:print "\tITERATION:",Iteration
        ClusterToMove= random.choice(CTG.nodes())
        CurrentNode=CTG.node[ClusterToMove]['Node']
        RemoveClusterFromNode(TG,CTG,AG,NoCRG,ClusterToMove,CurrentNode,DetailedReport)
        DestNode = random.choice(AG.nodes())
        TryCounter=0
        while not AddClusterToNode(TG,CTG,AG,NoCRG,ClusterToMove,DestNode,DetailedReport):
            RemoveClusterFromNode(TG,CTG,AG,NoCRG,ClusterToMove,DestNode,DetailedReport)
            AddClusterToNode(TG,CTG,AG,NoCRG,ClusterToMove,CurrentNode,DetailedReport)
            ClusterToMove= random.choice(CTG.nodes())
            CurrentNode=CTG.node[ClusterToMove]['Node']
            RemoveClusterFromNode(TG,CTG,AG,NoCRG,ClusterToMove,CurrentNode,DetailedReport)
            DestNode = random.choice(AG.nodes())
            if TryCounter >= 3*len(AG.nodes()):
                print "CAN NOT FIND ANY SOLUTION... ABORTING MAPPING..."
                TG=copy.deepcopy(BestTG)
                AG=copy.deepcopy(BestAG)
                CTG=copy.deepcopy(BestCTG)
                Scheduling_Functions.ReportMappedTasks(AG)
                CostFunction(TG,AG,True)
                return (False,False,False)
            TryCounter+=1
        Scheduling_Functions.ClearScheduling(AG,TG)
        Scheduler.ScheduleAll(TG,AG,False,DetailedReport)
        CurrentCost=CostFunction(TG,AG,DetailedReport)
        if CurrentCost <= BestCost:
            if CurrentCost < BestCost:
                if Report:print "\033[32m* NOTE::\033[0mBETTER SOLUTION FOUND WITH COST:",CurrentCost , "\t ITERATION:",Iteration
            BestTG=copy.deepcopy(TG)
            BestAG=copy.deepcopy(AG)
            BestCTG=copy.deepcopy(CTG)
            BestCost=CurrentCost
        else:
            TG=copy.deepcopy(BestTG)
            AG=copy.deepcopy(BestAG)
            CTG=copy.deepcopy(BestCTG)
    if Report:print "-------------------------------------"
    if Report:print "STARTING COST:",StartingCost,"\tFINAL COST:",BestCost,"\tAFTER",IterationNum,"ITERATIONS"
    if Report:print "IMPROVEMENT:","{0:.2f}".format(100*(StartingCost-BestCost)/StartingCost),"%"
    if Report:Scheduling_Functions.ReportMappedTasks(AG)
    return (BestTG,BestCTG,BestAG)


def OptimizeMappingIterativeLocalSearch(TG,CTG,AG,NoCRG,IterationNum,SubIteration,Report,DetailedReport):
    if Report:print "==========================================="
    if Report:print "STARTING MAPPING OPTIMIZATION...USING ITERATIVE LOCAL SEARCH..."
    BestTG=copy.deepcopy(TG)
    BestAG=copy.deepcopy(AG)
    BestCTG=copy.deepcopy(CTG)
    BestCost=CostFunction(TG,AG,False)
    StartingCost = CostFunction(TG,AG,False)
    if Report:print "INITIAL COST:",StartingCost
    for Iteration in range(0,IterationNum):
        if DetailedReport:print "\tITERATION:",Iteration
        (CurrentTG,CurrentCTG,CurrentAG) = OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,SubIteration,False,DetailedReport)
        if CurrentTG is not False:
            CurrentCost=CostFunction(CurrentTG,CurrentAG,False)
            if CurrentCost <= BestCost:
                if CurrentCost < BestCost:
                    if Report:print "\033[32m* NOTE::\033[0mBETTER SOLUTION FOUND WITH COST:",CurrentCost , \
                        "\t ITERATION:",Iteration
                BestTG=copy.deepcopy(CurrentTG)
                BestAG=copy.deepcopy(CurrentAG)
                BestCTG=copy.deepcopy(CurrentCTG)
                BestCost = CurrentCost
        del CurrentTG
        del CurrentAG
        del CurrentCTG
        ClearMapping(TG,CTG,AG)
        MakeInitialMapping(TG,CTG,AG,NoCRG,False)
        Scheduler.ScheduleAll(TG,AG,False,False)
    if Report:print "-------------------------------------"
    if Report:print "STARTING COST:",StartingCost,"\tFINAL COST:",BestCost
    if Report:print "IMPROVEMENT:","{0:.2f}".format(100*(StartingCost-BestCost)/StartingCost),"%"
    return (BestTG,BestCTG,BestAG)

