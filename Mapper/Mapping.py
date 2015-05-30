

__author__ = 'siavoosh'
import random
import copy
from ScheduleAndDepend.Scheduler import Scheduler
from ScheduleAndDepend.Scheduler import Scheduling_Functions
from ScheduleAndDepend.Mapper.Mapping_Functions import AddClusterToNode
from ScheduleAndDepend.Mapper.Mapping_Functions import RemoveClusterFromNode
from ScheduleAndDepend.Mapper.Mapping_Functions import ClearMapping
from ScheduleAndDepend.Mapper.Mapping_Functions import CostFunction


def MakeInitialMapping(TG,CTG,AG,NoCRG):
    print "STARTING INITIAL MAPPING..."
    for Cluster in CTG.nodes():
        DestNode = random.choice(AG.nodes())
        Itteration=0
        while not AddClusterToNode(TG,CTG,AG,NoCRG,Cluster,DestNode,True):
            Itteration+=1
            RemoveClusterFromNode(TG,CTG,AG,NoCRG,Cluster,DestNode,True)
            DestNode = random.choice(AG.nodes())        #try another node
            print "\t-------------------------"
            print "\tMAPPING ATTEMPT: #",Itteration+1,"FOR CLUSTER:",Cluster
            if Itteration == 10* len(CTG.nodes()):
                print "\033[31mERROR::\033[0m INITIAL MAPPING FAILED..."
                ClearMapping(TG,CTG,AG)
                return False
    print "INITIAL MAPPING READY..."
    return True

def OptimizeMappingLocalSearch(TG,CTG,AG,NoCRG,ItterationNum,Report):
    print "STARTING MAPPING OPTIMIZATION..."
    BestTG=copy.deepcopy(TG)
    BestAG=copy.deepcopy(AG)
    BestCTG=copy.deepcopy(CTG)
    BestCost=CostFunction(TG,AG,Report)
    StartingCost=BestCost
    for Iteration in range(0,ItterationNum):
        if Report:print "\tITERATION:",Iteration
        ClusterToMove= random.choice(CTG.nodes())
        CurrentNode=CTG.node[ClusterToMove]['Node']
        RemoveClusterFromNode(TG,CTG,AG,NoCRG,ClusterToMove,CurrentNode,Report)
        DestNode = random.choice(AG.nodes())
        TryCounter=0
        while not AddClusterToNode(TG,CTG,AG,NoCRG,ClusterToMove,DestNode,Report):
            RemoveClusterFromNode(TG,CTG,AG,NoCRG,ClusterToMove,DestNode,Report)
            AddClusterToNode(TG,CTG,AG,NoCRG,ClusterToMove,CurrentNode,Report)
            ClusterToMove= random.choice(CTG.nodes())
            CurrentNode=CTG.node[ClusterToMove]['Node']
            RemoveClusterFromNode(TG,CTG,AG,NoCRG,ClusterToMove,CurrentNode,Report)
            DestNode = random.choice(AG.nodes())
            if TryCounter >= 3*len(AG.nodes()):
                print "CAN NOT FIND ANY SOLUTION... ABORTING MAPPING..."
                TG=copy.deepcopy(BestTG)
                AG=copy.deepcopy(BestAG)
                CTG=copy.deepcopy(BestCTG)
                Scheduling_Functions.ReportMappedTasks(AG)
                CostFunction(TG,AG,True)
                return False
            TryCounter+=1
        Scheduling_Functions.ClearScheduling(AG,TG)
        Scheduler.ScheduleAll(TG,AG,False,Report)
        CurrentCost=CostFunction(TG,AG,Report)
        if CurrentCost <= BestCost:
            if CurrentCost < BestCost:
                print "\033[32m* NOTE::\033[0mBETTER SOLUTION FOUND WITH COST:",CurrentCost , "\t ITERATION:",Iteration
            BestTG=copy.deepcopy(TG)
            BestAG=copy.deepcopy(AG)
            BestCTG=copy.deepcopy(CTG)
            BestCost=CurrentCost
        else:
            TG=copy.deepcopy(BestTG)
            AG=copy.deepcopy(BestAG)
            CTG=copy.deepcopy(BestCTG)
    print "-------------------------------------"
    print "STARTING COST:",StartingCost,"\tFINAL COST:",BestCost,"\tAFTER",ItterationNum,"ITERATIONS"
    Scheduling_Functions.ReportMappedTasks(AG)
    CostFunction(TG,AG,True)
    return True


def OptimizeMappingIterativeLocalSearch(TG,CTG,AG,NoCRG,IterationNum,Report):

    return True