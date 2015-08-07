# Copyright (C) Siavoosh Payandeh Azad

from  ConfigAndPackages import Config
from AG_Functions import ReturnNodeNumber, ReturnNodeLocation
from RoutingAlgorithms import Routing, Calculate_Reachability, RoutingGraph_Reports
import random, copy


def OptimizeAG_VL(AG, SHM, logging):
    if Config.VL_OptAlg == "LocalSearch":
        return OptimizeAG_VL_LocalSearch(AG, SHM, logging)
    elif Config.VL_OptAlg == "IterativeLocalSearch":
        return OptimizeAG_VL_IterativeLocalSearch(AG, SHM, logging)
    else:
        raise ValueError("VL_OptAlg parameter is not valid")


def OptimizeAG_VL_IterativeLocalSearch(AG, SHM, logging):

    BestVL_List = []

    for j in range(0, Config.AG_Opt_Iterations_ILS):
        RemoveAll_VL(SHM, AG)
        VL_List_init = copy.deepcopy(FindFeasibleAG_VL(AG, SHM))
        RG = copy.deepcopy(Routing.GenerateNoCRouteGraph(AG, SHM, Config.UsedTurnModel, False, False))
        Cost = Calculate_Reachability.ReachabilityMetric(AG, RG, False)

        if j == 0:
            print ("=====================================")
            print ("STARTING AG VERTICAL LINK PLACEMENT OPTIMIZATION")
            print ("NUMBER OF LINKS: "+str(Config.VerticalLinksNum))
            print ("NUMBER OF ITERATIONS: "+str(Config.AG_Opt_Iterations_ILS*Config.AG_Opt_Iterations_LS))
            print ("INITIAL REACHABILITY METRIC: "+str(Cost))
            StartingCost = Cost
            BestCost = Cost
            BestVL_List = VL_List_init[:]
        else:
            print ("\033[33m* NOTE::\033[0mSTARITNG NEW ROUND: "+str(j+1)+"\t STARTING COST:"+str(Cost))
            if Cost > BestCost:
                BestVL_List = VL_List_init[:]
                BestCost = Cost
                print ("\033[32m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:" +
                       str(Cost) + "\t ITERATION: "+str(j*Config.AG_Opt_Iterations_LS))

        VL_List = VL_List_init[:]

        for i in range(0, Config.AG_Opt_Iterations_LS):
            New_VL_List = copy.deepcopy(MoveToNewVLConfig(AG, SHM, VL_List))
            NewRG = Routing.GenerateNoCRouteGraph(AG, SHM, Config.UsedTurnModel, False, False)
            Cost = Calculate_Reachability.ReachabilityMetric(AG, NewRG, False)
            if Cost >= BestCost:
                VL_List = New_VL_List[:]
                if Cost > BestCost:
                    BestVL_List = VL_List[:]
                    BestCost = Cost
                    print ("\033[32m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:" +
                           str(Cost) + "\t ITERATION: "+str(j*Config.AG_Opt_Iterations_LS+i))
                else:
                    # print ("\033[33m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:" +
                    #        str(Cost) + "\t ITERATION: "+str(j*Config.AG_Opt_Iterations_LS+i))
                    pass
            else:
                ReturnToSolution(AG, SHM, VL_List)

    ReturnToSolution(AG, SHM, BestVL_List)
    print ("-------------------------------------")
    print ("STARTING COST:"+str(StartingCost)+"\tFINAL COST:"+str(BestCost))
    print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(BestCost-StartingCost)/StartingCost))+" %")
    return SHM


def OptimizeAG_VL_LocalSearch(AG, SHM, logging):
    RemoveAll_VL(SHM, AG)
    VL_List = FindFeasibleAG_VL(AG, SHM)
    RG = copy.deepcopy(Routing.GenerateNoCRouteGraph(AG, SHM, Config.UsedTurnModel, Config.DebugInfo, Config.DebugDetails))
    Cost = Calculate_Reachability.ReachabilityMetric(AG, RG, False)
    print ("=====================================")
    print ("STARTING AG VERTICAL LINK PLACEMENT OPTIMIZATION")
    print ("NUMBER OF LINKS: "+str(Config.VerticalLinksNum))
    print ("NUMBER OF ITERATIONS: "+str(Config.AG_Opt_Iterations))
    print ("INITIAL REACHABILITY METRIC: "+str(Cost))

    StartingCost = Cost
    BestCost = Cost

    for i in range(0, Config.AG_Opt_Iterations):
        New_VL_List = copy.deepcopy(MoveToNewVLConfig(AG, SHM, VL_List))
        NewRG = copy.deepcopy(Routing.GenerateNoCRouteGraph(AG, SHM, Config.UsedTurnModel, False, False))
        Cost = Calculate_Reachability.ReachabilityMetric(AG, NewRG, False)
        if Cost >= BestCost:
            VL_List = copy.deepcopy(New_VL_List)
            if Cost > BestCost:
                BestCost = Cost
                print ("\033[32m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:" + str(Cost) + "\t ITERATION: "+str(i))
            else:
                # print ("\033[33m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:" + str(Cost) + "\t ITERATION: "+str(i))
                pass
        else:
            ReturnToSolution(AG,SHM, VL_List)
            VL_List = copy.deepcopy(VL_List)
    print ("-------------------------------------")
    print ("STARTING COST:"+str(StartingCost)+"\tFINAL COST:"+str(BestCost))
    print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(BestCost-StartingCost)/StartingCost))+" %")
    return SHM


def FindAll_VL(AG):
    VL_List = []
    for link in AG.edges():
        if ReturnNodeLocation(link[0])[2] != ReturnNodeLocation(link[1])[2]:    # these nodes are on different layers
            if link not in VL_List:
                VL_List.append(link)
    return VL_List


def RemoveAll_VL(SHM, AG):
    VL_List = FindAll_VL(AG)
    for VLink in VL_List:
        SHM.BreakLink(VLink, False)
    return None


def FindFeasibleAG_VL(AG, SHM):
    NewVL_Lists = []
    for i in range(0, Config.VerticalLinksNum):
        SourceX = random.randint(0, Config.Network_X_Size-1)
        SourceY = random.randint(0, Config.Network_Y_Size-1)
        SourceZ = random.randint(0, Config.Network_Z_Size-1)
        SourceNode = ReturnNodeNumber(SourceX,SourceY,SourceZ)
        PossibleZ=[]
        if SourceZ+1 <= Config.Network_Z_Size-1:
            PossibleZ.append(SourceZ+1)
        if 0 <= SourceZ-1:
            PossibleZ.append(SourceZ-1)
        DestinationNode = ReturnNodeNumber(SourceX, SourceY, random.choice(PossibleZ))
        while SHM.SHM.edge[SourceNode][DestinationNode]['LinkHealth']:
            SourceX = random.randint(0, Config.Network_X_Size-1)
            SourceY = random.randint(0, Config.Network_Y_Size-1)
            SourceZ = random.randint(0, Config.Network_Z_Size-1)
            SourceNode = ReturnNodeNumber(SourceX, SourceY, SourceZ)
            PossibleZ=[]
            if SourceZ + 1 <= Config.Network_Z_Size-1:
                PossibleZ.append(SourceZ+1)
            if 0 <= SourceZ-1:
                PossibleZ.append(SourceZ-1)
            DestinationNode = ReturnNodeNumber(SourceX, SourceY, random.choice(PossibleZ))

        # here we have a candidate to restore
        SHM.RestoreBrokenLink((SourceNode, DestinationNode), False)
        NewVL_Lists.append((SourceNode, DestinationNode))
    return NewVL_Lists


def ReturnToSolution(AG, SHM, VL_List):
    RemoveAll_VL(SHM, AG)
    for Link in VL_List:
        SHM.RestoreBrokenLink(Link, False)
    return None


def MoveToNewVLConfig(AG, SHM, VL_Lists):
    NewVL_Lists = copy.deepcopy(VL_Lists)
    ChosenLinkToFix = random.choice(NewVL_Lists)
    NewVL_Lists.remove(ChosenLinkToFix)
    SHM.BreakLink(ChosenLinkToFix, False)

    SourceX = random.randint(0, Config.Network_X_Size-1)
    SourceY = random.randint(0, Config.Network_Y_Size-1)
    SourceZ = random.randint(0, Config.Network_Z_Size-1)
    SourceNode = ReturnNodeNumber(SourceX, SourceY, SourceZ)
    PossibleZ = []
    if SourceZ + 1 <= Config.Network_Z_Size-1:
        PossibleZ.append(SourceZ + 1)
    if 0 <= SourceZ - 1:
        PossibleZ.append(SourceZ - 1)
    DestinationNode = ReturnNodeNumber(SourceX,SourceY,random.choice(PossibleZ))

    while SourceNode == DestinationNode or SHM.SHM.edge[SourceNode][DestinationNode]['LinkHealth']:
        SourceX = random.randint(0, Config.Network_X_Size-1)
        SourceY = random.randint(0, Config.Network_Y_Size-1)
        SourceZ = random.randint(0, Config.Network_Z_Size-1)
        SourceNode = ReturnNodeNumber(SourceX, SourceY, SourceZ)
        PossibleZ=[]
        if SourceZ+1 <= Config.Network_Z_Size-1:
            PossibleZ.append(SourceZ+1)
        if 0 <= SourceZ-1:
            PossibleZ.append(SourceZ-1)
        DestinationNode =  ReturnNodeNumber(SourceX, SourceY, random.choice(PossibleZ))
    # here we have a candidate to restore
    SHM.RestoreBrokenLink((SourceNode, DestinationNode), False)
    NewVL_Lists.append((SourceNode, DestinationNode))
    return NewVL_Lists


def CleanUpAG(AG, SHM):
    for link in SHM.SHM.edges():
        if not SHM.SHM.edge[link[0]][link[1]]['LinkHealth']:
            AG.remove_edge(link[0], link[1])
    return None