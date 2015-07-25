# Copyright (C) 2015 Siavoosh Payandeh Azad 

import copy
from Mapper import Mapping_Functions
from ConfigAndPackages import Config
from Scheduler import Scheduler,Scheduling_Functions,Scheduling_Reports
import random
from math import exp
from collections import deque
from scipy import stats

def OptimizeMapping_SA(TG, CTG, AG, NoCRG, CriticalRG, NonCriticalRG, SHM,
                                      IterationNum, CostDataFile, logging):

    print "==========================================="
    print "STARTING MAPPING OPTIMIZATION...USING SIMULATED ANNEALING..."
    MappingCostFile = open('Generated_Files/Internal/'+CostDataFile+'.txt','a')
    MappingProcessFile = open('Generated_Files/Internal/MappingProcess.txt','w')
    SATemperatureFile = open('Generated_Files/Internal/SATemp.txt','w')
    SACostSlopeFile = open('Generated_Files/Internal/SACostSlope.txt','w')

    if Config.CoolingMethod == 'Adaptive':
        CostMonitor = deque([])
    else:
        CostMonitor = []

    if Config.DistanceBetweenMapping:
        InitMapString = Mapping_Functions.MappingIntoString(TG)
        if Config.Mapping_CostFunctionType == 'CONSTANT':
            Mapping_Functions.ClearMapping(TG,CTG,AG)
            if not Mapping_Functions.MakeInitialMapping(TG, CTG, AG, SHM, NoCRG,
                                                        CriticalRG, NonCriticalRG, True, logging):
                raise ValueError("FEASIBLE MAPPING NOT FOUND...")
    else:
        InitMapString = None

    CurrentTG=copy.deepcopy(TG)
    CurrentAG=copy.deepcopy(AG)
    CurrentCTG=copy.deepcopy(CTG)
    CurrentCost = Mapping_Functions.CostFunction(TG,AG,SHM,False,InitialMappingString=InitMapString)
    StartingCost = CurrentCost

    BestTG = copy.deepcopy(TG)
    BestAG=copy.deepcopy(AG)
    BestCTG=copy.deepcopy(CTG)
    BestCost = CurrentCost

    InitialTemp = Config.SA_InitialTemp
    SATemperatureFile.write(str(InitialTemp)+"\n")
    Temperature = InitialTemp
    slope = None
    ZeroSlopeCounter = 0
    for i in range(0,IterationNum):
        # move to another solution

        NewTG, NewCTG, NewAG = MoveToAnotherSolution(CurrentTG, CurrentCTG, CurrentAG,  NoCRG,
                                                     SHM, CriticalRG, NonCriticalRG, logging)
        Scheduling_Functions.ClearScheduling(NewAG,NewTG)
        Scheduler.ScheduleAll(NewTG,NewAG,SHM,False,False)

        # calculate the cost of new solution
        NewCost = Mapping_Functions.CostFunction(NewTG, NewAG, SHM, False, InitialMappingString=InitMapString)

        if NewCost<BestCost:
            BestTG = copy.deepcopy(NewTG)
            BestAG=copy.deepcopy(NewAG)
            BestCTG=copy.deepcopy(NewCTG)
            BestCost = NewCost
            print "\033[33m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:","{0:.2f}".format(NewCost)
        # calculate the probability P of accepting the solution
        Prob = Metropolis(CurrentCost, NewCost, Temperature)
        # print "Prob:",Prob
        # throw the coin with probability P
        if Prob > random.random():
            # accept the new solution
            CurrentTG = copy.deepcopy(NewTG)
            CurrentAG = copy.deepcopy(NewAG)
            CurrentCTG = copy.deepcopy(NewCTG)
            CurrentCost = NewCost
            if slope is not None:
                print "\033[32m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:","{0:.2f}".format(CurrentCost), "\tProb:", \
                      "{0:.2f}".format(Prob), "\tTemp:", "{0:.2f}".format(Temperature), "\t Iteration:", i, "\tSLOPE:", \
                      "{0:.2f}".format(slope)
            else:
                print "\033[32m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:","{0:.2f}".format(CurrentCost), "\tProb:", \
                      "{0:.2f}".format(Prob), "\tTemp:", "{0:.2f}".format(Temperature), "\t Iteration:", i
        else:
            # move back to initial solution
            pass
        # update Temp
        MappingProcessFile.write(Mapping_Functions.MappingIntoString(CurrentTG)+"\n")
        SATemperatureFile.write(str(Temperature)+"\n")
        MappingCostFile.write(str(CurrentCost)+"\n")


        if Config.CoolingMethod == 'Adaptive':
            if len(CostMonitor)> Config.CostMonitorQueSize :
                CostMonitor.appendleft(CurrentCost)
                CostMonitor.pop()
            else:
                CostMonitor.appendleft(CurrentCost)
            slope = CalculateSlopeOfCost(CostMonitor)
            if slope == 0:
                ZeroSlopeCounter +=1
            else:
                ZeroSlopeCounter = 0
            SACostSlopeFile.write(str(slope)+"\n")
        Temperature = NextTemp(InitialTemp, i, IterationNum, Temperature, slope)
        if ZeroSlopeCounter == Config.MaxSteadyState or Temperature <= 0:
            print "NO IMPROVEMENT POSSIBLE..."
            break
    MappingCostFile.close()
    MappingProcessFile.close()
    SATemperatureFile.close()
    SACostSlopeFile.close()
    print "-------------------------------------"
    print "STARTING COST:",StartingCost,"\tFINAL COST:",BestCost
    print "IMPROVEMENT:","{0:.2f}".format(100*(StartingCost-BestCost)/StartingCost),"%"
    return BestTG, BestCTG, BestAG


def NextTemp(InitialTemp, Iteration, MaxIteration, CurrentTemp, Slope=None):
    if Config.CoolingMethod == 'Linear':
        Temp =(float(MaxIteration-Iteration)/MaxIteration)*InitialTemp
    elif Config.CoolingMethod == 'Exponential':
        Temp = CurrentTemp * Config.SA_Alpha
    elif Config.CoolingMethod == 'Adaptive':
        Temp = CurrentTemp
        if Iteration > Config.CostMonitorQueSize:
            if Slope < Config.SlopeRangeForCooling and Slope > 0:
                Temp = CurrentTemp * Config.SA_Alpha
    elif Config.CoolingMethod == 'Markov':
        Temp = InitialTemp - (Iteration/Config.MarkovNum)*Config.MarkovTempStep
    else:
        raise ValueError('Invalid Cooling Method for SA...')
    return Temp

def CalculateSlopeOfCost(CostMonitor):
    slope = 0
    if len(CostMonitor)>2:
        x = range(0,len(CostMonitor))
        y = list(CostMonitor)
        slope = stats.linregress(x,y)[0]
    if len(CostMonitor) == 2:
        slope = list(CostMonitor)[1]-list(CostMonitor)[0]
    return slope

def Metropolis(CurrentCost, NewCost, Temperature):
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
