# Copyright (C) 2015 Siavoosh Payandeh Azad 

import random
import copy
from ConfigAndPackages import Config
import networkx


from Clustering_Functions import AddTaskToCTG, RemoveTaskFromCTG, ClearClustering, \
    CostFunction,DeleteEmptyClusters, CTG_OptimizationMove
from Clustering_Test import DoubleCheckCTG
from ClusteringReports import ReportCTG

def TaskClusterGeneration(NumberOfClusters):
    """
    Generates a clustered task graph without any edges or tasks assigned to clusters.
    the number of clusters should be the same as the number of nodes in Architecture graph.
    :param NumberOfClusters: Number of clusters to be generated
    :return: Empty Clustered Task Graph
    """
    print ("===========================================")
    print ("PREPARING FOR CLUSTERING THE TASK GRAPH...")
    print ("   NUMBER OF CLUSTERS: "+str(NumberOfClusters))
    CTG=networkx.DiGraph()
    for i in range(0, NumberOfClusters):
        CTG.add_node(i, TaskList=[], Node=None, Utilization=0, Criticality='L')
    print ("CLUSTERS GENERATED...")
    return CTG


def InitialClustering(TG, CTG):
    """
    Randomly assign the tasks to clusters to make the initial solution for optimization...
    :param TG: Task Graph
    :param CTG: Clustered Task Graph
    :return: True if successful, False otherwise
    """
    print ("===========================================")
    print ("STARTING INITIAL CLUSTERING...")
    for Task in TG.nodes():
        Itteration=0
        DestCluster = random.choice(CTG.nodes())
        while(not AddTaskToCTG(TG,CTG,Task,DestCluster)):
            # RemoveTaskFromCTG(TG,CTG,Task)
            Itteration+=1
            DestCluster = random.choice(CTG.nodes())
            if Itteration == 10* len(CTG.nodes()):
                ClearClustering(TG,CTG)
                return False
    # DoubleCheckCTG(TG,CTG)
    print ("INITIAL CLUSTERED TASK GRAPH (CTG) READY...")
    ReportCTG(CTG,"CTG_Initial.png")
    return True

def ClusteringOptimization_LocalSearch(TG, CTG, NumberOfIter, logging):
    """
    Local Search optimization for reducing the cost of a clustering solution
    :param TG: Task Graph
    :param CTG: Clustered Task Graph
    :param NumberOfIter: Number of iterations for local search
    :return: best answer (CTG) found by the search
    """
    ClusteringCostFile = open('Generated_Files/Internal/ClusteringCost.txt','w')
    print ("===========================================")
    print ("STARTING LOCAL SEARCH OPTIMIZATION FOR CTG...")
    Cost=CostFunction(CTG)
    StartingCost = Cost
    ClusteringCostFile.write(str(Cost)+"\n")
    BestSolution = copy.deepcopy(CTG)
    BestTaskGraph = copy.deepcopy(TG)
    print ("\tINITIAL COST: "+ str(Cost))
    # choose a random task from TG
    for i in range(0,NumberOfIter):

        # print ("\tITERATION:",i)
        if Config.TestMode:
            DoubleCheckCTG(TG,CTG)
        # Make a move!
        CTG_OptimizationMove(TG, CTG, logging)
        NewCost = CostFunction(CTG)
        ClusteringCostFile.write(str(NewCost)+"\n")
        if NewCost <= Cost:
            if NewCost < Cost:
                print ("\033[32m* NOTE::\033[0mBETTER SOLUTION FOUND WITH COST:\t"+str(NewCost)+"\t\tIteration #:"+str(i))
            BestSolution = copy.deepcopy(CTG)
            BestTaskGraph = copy.deepcopy(TG)
            Cost = NewCost
        else:
            CTG = copy.deepcopy(BestSolution)
            TG = copy.deepcopy(BestTaskGraph)
    ClusteringCostFile.close()
    DeleteEmptyClusters(BestSolution)
    # DoubleCheckCTG(BestTaskGraph,BestSolution)
    print ("-------------------------------------")
    print ("STARTING COST:"+str(StartingCost)+"\tFINAL COST: "+str(Cost)+"\tAFTER "+str(NumberOfIter)+" ITERATIONS")
    print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(StartingCost-Cost)/StartingCost))+" %")
    return BestSolution,BestTaskGraph