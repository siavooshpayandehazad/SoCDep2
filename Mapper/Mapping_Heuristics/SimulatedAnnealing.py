# Copyright (C) 2015 Siavoosh Payandeh Azad 



import copy
from Mapper import Mapping_Functions
from ConfigAndPackages import Config
from Scheduler import Scheduler,Scheduling_Functions,Scheduling_Reports
import random
from math import exp, log10, log1p
from collections import deque
from scipy import stats
import statistics

def OptimizeMapping_SA(TG, CTG, AG, NoCRG, CriticalRG, NonCriticalRG,
                       SHM, CostDataFile, logging):

    print ("===========================================")
    print ("STARTING MAPPING OPTIMIZATION...USING SIMULATED ANNEALING...")
    print ("STARTING TEMPERATURE: "+str(Config.SA_InitialTemp))
    print ("ANNEALING SCHEDULE: "+Config.SA_AnnealingSchedule)
    print ("TERMINATION CRITERIA: "+Config.TerminationCriteria)
    print ("================")

    if type(CostDataFile) is str:
        MappingCostFile = open('Generated_Files/Internal/'+CostDataFile+'.txt', 'a')
    else:
        raise ValueError("CostDataFile name is not string: "+str(CostDataFile))

    MappingProcessFile = open('Generated_Files/Internal/MappingProcess.txt', 'w')
    SATemperatureFile = open('Generated_Files/Internal/SATemp.txt', 'w')
    SACostSlopeFile = open('Generated_Files/Internal/SACostSlope.txt', 'w')
    SAHuangRaceFile = open('Generated_Files/Internal/SAHuangRace.txt', 'w')

    if Config.SA_AnnealingSchedule in ['Adaptive', 'Aart', 'Huang']:
        CostMonitor = deque([])
    else:
        CostMonitor = []

    if Config.DistanceBetweenMapping:
        InitMapString = Mapping_Functions.MappingIntoString(TG)
        if Config.Mapping_CostFunctionType == 'CONSTANT':
            Mapping_Functions.ClearMapping(TG,CTG,AG)
            if not Mapping_Functions.MakeInitialMapping(TG, CTG, AG, SHM, NoCRG, CriticalRG,
                                                        NonCriticalRG, True, logging):
                raise ValueError("FEASIBLE MAPPING NOT FOUND...")
    else:
        InitMapString = None

    CurrentTG = copy.deepcopy(TG)
    CurrentAG = copy.deepcopy(AG)
    CurrentCTG = copy.deepcopy(CTG)
    CurrentCost = Mapping_Functions.CostFunction(TG, AG, SHM, False, InitialMappingString=InitMapString)
    StartingCost = CurrentCost

    BestTG = copy.deepcopy(TG)
    BestAG = copy.deepcopy(AG)
    BestCTG = copy.deepcopy(CTG)
    BestCost = CurrentCost

    InitialTemp = Config.SA_InitialTemp
    SATemperatureFile.write(str(InitialTemp)+"\n")
    Temperature = InitialTemp
    slope = None
    ZeroSlopeCounter = 0
    StdDeviation = None

    # for Huang Annealing schedule
    Huang_Counter1 = 0
    Huang_Counter2 = 0
    Huang_Steady_Counter = 0
    IterationNum = Config.SimulatedAnnealingIteration
    #for i in range(0,IterationNum):
        # move to another solution
    i = 0
    while True:
        i += 1
        NewTG, NewCTG, NewAG = MoveToAnotherSolution(CurrentTG, CurrentCTG, CurrentAG,  NoCRG,
                                                     SHM, CriticalRG, NonCriticalRG, logging)
        Scheduling_Functions.ClearScheduling(NewAG, NewTG)
        Scheduler.ScheduleAll(NewTG, NewAG, SHM, False, False, logging)

        # calculate the cost of new solution
        NewCost = Mapping_Functions.CostFunction(NewTG, NewAG, SHM, False, InitialMappingString=InitMapString)

        if NewCost<BestCost:
            BestTG = copy.deepcopy(NewTG)
            BestAG = copy.deepcopy(NewAG)
            BestCTG = copy.deepcopy(NewCTG)
            BestCost = NewCost
            print ("\033[33m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:"+"{0:.2f}".format(NewCost)+
                  "\t ITERATION:"+str(i)+"\tIMPROVEMENT:"+"{0:.2f}".format(100*(StartingCost-NewCost)/StartingCost)+" %")
        # calculate the probability P of accepting the solution
        Prob = Metropolis(CurrentCost, NewCost, Temperature)
        # print ("Prob:", Prob)
        # throw the coin with probability P
        if Prob > random.random():
            # accept the new solution
            MoveAccepted = True
            CurrentTG = copy.deepcopy(NewTG)
            CurrentAG = copy.deepcopy(NewAG)
            CurrentCTG = copy.deepcopy(NewCTG)
            CurrentCost = NewCost
            if Config.SA_ReportSolutions:
                if slope is not None:
                    print ("\033[32m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:","{0:.2f}".format(CurrentCost),
                           "\tProb:", "{0:.2f}".format(Prob), "\tTemp:", "{0:.2f}".format(Temperature),
                           "\t Iteration:", i, "\tSLOPE:", "{0:.2f}".format(slope))
                if StdDeviation is not None:
                    print ("\033[32m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:","{0:.2f}".format(CurrentCost),
                           "\tProb:", "{0:.2f}".format(Prob), "\tTemp:", "{0:.2f}".format(Temperature),
                           "\t Iteration:", i, "\tSTD_DEV:", "{0:.2f}".format(StdDeviation))
                else:
                    print ("\033[32m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:","{0:.2f}".format(CurrentCost),
                           "\tProb:", "{0:.2f}".format(Prob), "\tTemp:", "{0:.2f}".format(Temperature),
                           "\t Iteration:", i)
        else:
            MoveAccepted = False
            # move back to initial solution
            pass
        # update Temp
        MappingProcessFile.write(Mapping_Functions.MappingIntoString(CurrentTG)+"\n")
        SATemperatureFile.write(str(Temperature)+"\n")
        MappingCostFile.write(str(CurrentCost)+"\n")

        if Config.SA_AnnealingSchedule == 'Adaptive':
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

        if Config.SA_AnnealingSchedule == 'Aart' :
            if len(CostMonitor) == Config.CostMonitorQueSize :
                StdDeviation = statistics.stdev(CostMonitor)
                CostMonitor.clear()
                # print (StdDeviation)
            else:
                CostMonitor.appendleft(CurrentCost)

        # Huang's annealing schedule is very much like Aart's Schedule... how ever, Aart's schedule stays in a fixed
        # temperature for a fixed number of steps, however, Huang's schedule decides about number of steps dynamically

        if Config.SA_AnnealingSchedule == 'Huang':
            CostMonitor.appendleft(CurrentCost)
            if len(CostMonitor)> 1:
                Huang_CostMean = sum(CostMonitor)/len(CostMonitor)
                Huang_CostStdDev = statistics.stdev(CostMonitor)
                if MoveAccepted:
                    if Huang_CostMean - Config.HuangAlpha * Huang_CostStdDev <= CurrentCost <= \
                                    Huang_CostMean + Config.HuangAlpha * Huang_CostStdDev:
                        Huang_Counter1 += 1
                    else:
                        Huang_Counter2 += 1
            # print (Huang_Counter1, Huang_Counter2)
            SAHuangRaceFile.write(str(Huang_Counter1)+" "+str(Huang_Counter2)+"\n")
            if Huang_Counter1 == Config.HuangTargetValue1:
                StdDeviation = statistics.stdev(CostMonitor)
                CostMonitor.clear()
                Huang_Counter1 = 0
                Huang_Counter2 = 0
                Huang_Steady_Counter = 0
            elif Huang_Counter2 == Config.HuangTargetValue2:
                Huang_Counter1 = 0
                Huang_Counter2 = 0
                StdDeviation = None
            elif Huang_Steady_Counter == Config.CostMonitorQueSize:
                StdDeviation = statistics.stdev(CostMonitor)
                CostMonitor.clear()
                Huang_Counter1 = 0
                Huang_Counter2 = 0
                Huang_Steady_Counter = 0
                print ("\033[36m* COOLING::\033[0m REACHED MAX STEADY STATE... PREPARING FOR COOLING...")
            else:
                StdDeviation = None

            Huang_Steady_Counter += 1

        Temperature = NextTemp(InitialTemp, i, IterationNum, Temperature, slope, StdDeviation)

        if Config.SA_AnnealingSchedule == 'Adaptive':
            if ZeroSlopeCounter == Config.MaxSteadyState:
                print ("NO IMPROVEMENT POSSIBLE...")
                break
        if Config.TerminationCriteria == 'IterationNum':
            if i == Config.SimulatedAnnealingIteration:
                print ("REACHED MAXIMUM ITERATION NUMBER...")
                break
        elif Config.TerminationCriteria == 'StopTemp':
            if Temperature <= Config.SA_StopTemp:
                print ("REACHED STOP TEMPERATURE...")
                break

    MappingCostFile.close()
    MappingProcessFile.close()
    SATemperatureFile.close()
    SACostSlopeFile.close()
    SAHuangRaceFile.close()
    print ("-------------------------------------")
    print ("STARTING COST:"+str(StartingCost)+"\tFINAL COST:"+str(BestCost))
    print ("IMPROVEMENT:"+"{0:.2f}".format(100*(StartingCost-BestCost)/StartingCost)+" %")
    return BestTG, BestCTG, BestAG


def NextTemp(InitialTemp, Iteration, MaxIteration, CurrentTemp, Slope=None, StdDeviation = None):
    if Config.SA_AnnealingSchedule == 'Linear':
        Temp = (float(MaxIteration-Iteration)/MaxIteration)*InitialTemp
        print ("\033[36m* COOLING::\033[0m CURRENT TEMP:"+str(Temp))
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Exponential':
        Temp = CurrentTemp * Config.SA_Alpha
        print ("\033[36m* COOLING::\033[0m CURRENT TEMP:"+str(Temp))
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Logarithmic':
        # this is based on "A comparison of simulated annealing cooling strategies"
        # by Yaghout Nourani and Bjarne Andresen
        Temp = Config.LogCoolingConstant * (1.0/log10(1+(Iteration+1)))     # iteration should be > 1 so I added 1
        print ("\033[36m* COOLING::\033[0m CURRENT TEMP:"+str(Temp))
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Adaptive':
        Temp = CurrentTemp
        if Iteration > Config.CostMonitorQueSize:
            if Slope < Config.SlopeRangeForCooling and Slope > 0:
                Temp = CurrentTemp * Config.SA_Alpha
                print ("\033[36m* COOLING::\033[0m CURRENT TEMP:"+str(Temp))
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Markov':
        Temp = InitialTemp - (Iteration/Config.MarkovNum)*Config.MarkovTempStep
        if Temp < CurrentTemp:
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP:"+str(Temp))
        if Temp <= 0:
            Temp = CurrentTemp
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Aart':
        # This is coming from the following paper:
        # Job Shop Scheduling by Simulated Annealing Author(s): Peter J. M. van Laarhoven,
        # Emile H. L. Aarts, Jan Karel Lenstra
        if Iteration%Config.CostMonitorQueSize == 0 and StdDeviation is not None and StdDeviation != 0:
            Temp = float(CurrentTemp)/(1+(CurrentTemp*(log1p(Config.Delta)/StdDeviation)))
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP:"+str(Temp))
        elif StdDeviation == 0:
            Temp = float(CurrentTemp)*Config.SA_Alpha
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP:"+str(Temp))
        else:
            Temp = CurrentTemp
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Huang':
        if StdDeviation is not None and StdDeviation != 0:
            Temp = float(CurrentTemp)/(1+(CurrentTemp*(log1p(Config.Delta)/StdDeviation)))
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP:"+str(Temp))
        elif StdDeviation == 0:
            Temp = float(CurrentTemp)*Config.SA_Alpha
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP:"+str(Temp))
        else:
            Temp = CurrentTemp
#   ----------------------------------------------------------------
    else:
        raise ValueError('Invalid Cooling Method for SA...')
    return Temp


def CalculateSlopeOfCost(CostMonitor):
    slope = 0
    if len(CostMonitor) > 2:
        x = range(0, len(CostMonitor))
        y = list(CostMonitor)
        slope = stats.linregress(x, y)[0]
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
    Mapping_Functions.RemoveClusterFromNode(TG, CTG, AG, NoCRG, CriticalRG, NonCriticalRG,
                                            ClusterToMove, CurrentNode, logging)
    DestNode = random.choice(AG.nodes())
    if Config.EnablePartitioning:
        while(CTG.node[ClusterToMove]['Criticality']!= AG.node[DestNode]['Region']):
            DestNode = random.choice(AG.nodes())
    TryCounter = 0
    while not Mapping_Functions.AddClusterToNode(TG, CTG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG,
                                                 ClusterToMove, DestNode, logging):

            # If AddClusterToNode fails it automatically removes all the connections...
            # we need to add the cluster to the old place...
            Mapping_Functions.AddClusterToNode(TG, CTG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG,
                                               ClusterToMove, CurrentNode, logging)
            TryCounter+=1
            if TryCounter >= 3*len(AG.nodes()):
                print ("CAN NOT FIND ANY FEASIBLE SOLUTION... ABORTING LOCAL SEARCH...")
                return TG,CTG,AG

            # choosing another cluster to move
            ClusterToMove= random.choice(CTG.nodes())
            CurrentNode=CTG.node[ClusterToMove]['Node']
            Mapping_Functions.RemoveClusterFromNode(TG, CTG, AG, NoCRG, CriticalRG, NonCriticalRG,
                                                    ClusterToMove, CurrentNode, logging)
            DestNode = random.choice(AG.nodes())
            if Config.EnablePartitioning:
                while(CTG.node[ClusterToMove]['Criticality']!=AG.node[DestNode]['Region']):
                    DestNode = random.choice(AG.nodes())

    return TG, CTG, AG