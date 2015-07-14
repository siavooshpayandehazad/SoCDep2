# Copyright (C) 2015 Siavoosh Payandeh Azad 

import copy
from Mapper import Mapping_Functions
from ConfigAndPackages import Config
from Scheduler import Scheduler,Scheduling_Functions,Scheduling_Reports
import random
from math import exp

def OptimizeMapping_SA(TG, CTG, AG, NoCRG, CriticalRG, NonCriticalRG, SHM,
                                      IterationNum, CostDataFile, logging):

    print "==========================================="
    print "STARTING MAPPING OPTIMIZATION...USING SIMULATED ANNEALING..."
    MappingCostFile = open('Generated_Files/Internal/'+CostDataFile+'.txt','a')
    MappingProcessFile = open('Generated_Files/Internal/MappingProcess.txt','w')
    SATemperatureFile = open('Generated_Files/Internal/SATemp.txt','w')

    CurrentTG=copy.deepcopy(TG)
    CurrentAG=copy.deepcopy(AG)
    CurrentCTG=copy.deepcopy(CTG)
    CurrentCost = Mapping_Functions.CostFunction(TG,AG,SHM,False)
    StartingCost = CurrentCost

    BestTG = copy.deepcopy(TG)
    BestAG=copy.deepcopy(AG)
    BestCTG=copy.deepcopy(CTG)
    BestCost = CurrentCost

    InitialTemp = Config.SA_InitialTemp
    SATemperatureFile.write(str(InitialTemp)+"\n")
    Temperature = InitialTemp
    for i in range(0,IterationNum):
        # move to another solution

        NewTG, NewCTG, NewAG = MoveToAnotherSolution(CurrentTG, CurrentCTG, CurrentAG,  NoCRG,
                                                     SHM, CriticalRG, NonCriticalRG, logging)
        Scheduling_Functions.ClearScheduling(NewAG,NewTG)
        Scheduler.ScheduleAll(NewTG,NewAG,SHM,False,False)

        # calculate the cost of new solution
        NewCost = Mapping_Functions.CostFunction(NewTG, NewAG, SHM, False)

        if NewCost<BestCost:
            BestTG = copy.deepcopy(NewTG)
            BestAG=copy.deepcopy(NewAG)
            BestCTG=copy.deepcopy(NewCTG)
            BestCost = NewCost
            print "\033[33m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:","{0:.2f}".format(NewCost)
        # calculate the probability P of accepting the solution
        Prob = CalculateProbability(CurrentCost, NewCost, Temperature)
        # print "Prob:",Prob
        # throw the coin with probability P
        if Prob > random.random():
            # accept the new solution
            CurrentTG = copy.deepcopy(NewTG)
            CurrentAG = copy.deepcopy(NewAG)
            CurrentCTG = copy.deepcopy(NewCTG)
            CurrentCost = NewCost
            print "\033[32m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:","{0:.2f}".format(CurrentCost), "\tProb:", \
                  "{0:.2f}".format(Prob), "\tTemp:", "{0:.2f}".format(Temperature), "\t Iteration:", i
        else:
            # move back to initial  solution
            pass
        # update Temp
        MappingProcessFile.write(Mapping_Functions.MappingIntoString(CurrentTG)+"\n")
        SATemperatureFile.write(str(Temperature)+"\n")
        MappingCostFile.write(str(CurrentCost)+"\n")
        Temperature = NextTemp(InitialTemp, i, IterationNum)

    MappingCostFile.close()
    MappingProcessFile.close()
    SATemperatureFile.close()
    print "-------------------------------------"
    print "STARTING COST:",StartingCost,"\tFINAL COST:",BestCost
    print "IMPROVEMENT:","{0:.2f}".format(100*(StartingCost-BestCost)/StartingCost),"%"
    return BestTG, BestCTG, BestAG


def NextTemp(InitialTemp, Iteration, MaxIteration):
    if Config.CoolingMethod == 'Linear':
        Temp =float((MaxIteration-Iteration))/MaxIteration*InitialTemp
    elif Config.CoolingMethod == 'Exponential':
        Temp = InitialTemp * (Config.SA_Alpha**Iteration)
    else:
        raise ValueError('Invalid Cooling Method for SA...')
    return Temp


def CalculateProbability(CurrentCost, NewCost, Temperature):
    if NewCost > CurrentCost:
        P = exp((CurrentCost-NewCost)/Temperature)
    else:
        P = 1.0
    return P


def MoveToAnotherSolution (TG, CTG, AG, NoCRG, SHM, CriticalRG, NonCriticalRG, logging):
    ClusterToMove= random.choice(CTG.nodes())
    CurrentNode=CTG.node[ClusterToMove]['Node']
    Mapping_Functions.RemoveClusterFromNode(TG,CTG,AG,NoCRG,CriticalRG, NonCriticalRG,
                                            ClusterToMove,CurrentNode,logging)
    DestNode = random.choice(AG.nodes())
    if Config.EnablePartitioning:
        while(CTG.node[ClusterToMove]['Criticality']!= AG.node[DestNode]['Region']):
            DestNode = random.choice(AG.nodes())
    TryCounter = 0
    while not Mapping_Functions.AddClusterToNode(TG,CTG,AG,SHM,NoCRG,CriticalRG, NonCriticalRG,
                                                 ClusterToMove,DestNode,logging):

            # If AddClusterToNode fails it automatically removes all the connections...
            # we need to add the cluster to the old place...
            Mapping_Functions.AddClusterToNode(TG,CTG,AG,SHM,NoCRG,CriticalRG, NonCriticalRG,
                                               ClusterToMove,CurrentNode,logging)
            TryCounter+=1
            if TryCounter >= 3*len(AG.nodes()):
                print "CAN NOT FIND ANY FEASIBLE SOLUTION... ABORTING LOCAL SEARCH..."
                return TG,CTG,AG

            # choosing another cluster to move
            ClusterToMove= random.choice(CTG.nodes())
            CurrentNode=CTG.node[ClusterToMove]['Node']
            Mapping_Functions.RemoveClusterFromNode(TG,CTG,AG,NoCRG,CriticalRG, NonCriticalRG,
                                                    ClusterToMove,CurrentNode,logging)
            DestNode = random.choice(AG.nodes())
            if Config.EnablePartitioning:
                while(CTG.node[ClusterToMove]['Criticality']!=AG.node[DestNode]['Region']):
                    DestNode = random.choice(AG.nodes())

    return TG,CTG,AG
