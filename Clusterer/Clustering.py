__author__ = 'siavoosh'

import random
import copy

import networkx

from Clustering_Functions import ReportCTG, AddTaskToCTG, RemoveTaskFromCTG, ClearClustering, DoubleCheckCTG, \
    CostFunction,DeleteEmptyClusters


def TaskClusterGeneration(NumberOfClusters):
    """
    Generates a clustered task graph without any edges or tasks assigned to clusters.
    the number of clusters should be the same as the number of nodes in Architecture graph.
    :param NumberOfClusters: Number of clusters to be generated
    :return:
    """
    print "==========================================="
    print  "PREPARING FOR CLUSTERING THE TASK GRAPH..."
    print "   NUMBER OF CLUSTERS: ", NumberOfClusters
    CTG=networkx.DiGraph()
    for i in range(0, NumberOfClusters):
        CTG.add_node(i, TaskList=[], Node=None, Utilization=0)
    print "CLUSTERS GENERATED..."
    return CTG


def InitialClustering(TG, CTG):
    """
    Randomly assign the tasks to clusters to make the initial solution for optimization...
    :param TG: Task Graph
    :param CTG: Clustered Task Graph
    :return: None
    """
    print "==========================================="
    print "STARTING INITIAL CLUSTERING..."
    for Task in TG.nodes():
        Itteration=0
        DestCluster = random.choice(CTG.nodes())
        while(not AddTaskToCTG(TG,CTG,Task,DestCluster)):
            RemoveTaskFromCTG(TG,CTG,Task)
            Itteration+=1
            DestCluster = random.choice(CTG.nodes())
            if Itteration == 10* len(CTG.nodes()):
                ClearClustering(TG,CTG)
                return False
    DoubleCheckCTG(TG,CTG)
    print "INITIAL CLUSTERED TASK GRAPH (CTG) READY..."
    ReportCTG(CTG,"CTG_Initial.png")
    return True

def ClusteringOptimization_LocalSearch(TG, CTG, NumberOfIter):
    """
    Local Search optimization for reducing the cost of a clustering solution
    :param TG: Task Graph
    :param CTG: Clustered Task Graph
    :param NumberOfIter: Number of iterations for local search
    :return: best answer (CTG) found by the search
    """
    print "==========================================="
    print "STARTING LOCAL SEARCH OPTIMIZATION FOR CTG..."
    Cost=CostFunction(CTG)
    StartingCost=Cost
    BestSolution=copy.deepcopy(CTG)
    BestTaskGraph=copy.deepcopy(TG)
    print "\tINITIAL COST:", Cost
    # choose a random task from TG
    for i in range(0,NumberOfIter):
        #print "\tITERATION:",i
        DoubleCheckCTG(TG,CTG)
        RandomTask = random.choice(TG.nodes())
        RandomTaskCluster = TG.node[RandomTask]['Cluster']
        #remove it and all its connections from CTG
        RemoveTaskFromCTG(TG,CTG,RandomTask)
        #randomly choose another cluster
        #move the task to the cluster and add the connections
        RandomCluster = random.choice(CTG.nodes())
        while not AddTaskToCTG(TG,CTG,RandomTask,RandomCluster):
            RemoveTaskFromCTG(TG,CTG,RandomTask)
            AddTaskToCTG(TG,CTG,RandomTask,RandomTaskCluster)
            DoubleCheckCTG(TG,CTG)
            RandomTask = random.choice(TG.nodes())
            RandomTaskCluster = TG.node[RandomTask]['Cluster']

            RemoveTaskFromCTG(TG,CTG,RandomTask)
            RandomCluster = random.choice(CTG.nodes())
            #print "TASK", RandomTask, "MOVED TO CLUSTER", RandomCluster, "RESULTS IN UTILIZATION:", \
            #    CTG.node[RandomCluster]['Utilization'] + TG.node[RandomTask]['WCET']
        NewCost=CostFunction(CTG)
        if NewCost <= Cost:
            if NewCost < Cost:
                print "\033[32m* NOTE::\033[0mBETTER SOLUTION FOUND WITH COST:\t",NewCost, "\t\tIteration #:",i
            BestSolution=copy.deepcopy(CTG)
            BestTaskGraph=copy.deepcopy(TG)
            Cost=NewCost
        else:
            CTG=copy.deepcopy(BestSolution)
            TG=copy.deepcopy(BestTaskGraph)
    DeleteEmptyClusters(BestSolution)
    print "-------------------------------------"
    print "STARTING COST:",StartingCost,"\tFINAL COST:",Cost,"\tAFTER",NumberOfIter,"ITERATIONS"
    print "IMPROVEMENT:","{0:.2f}".format(100*(StartingCost-Cost)/StartingCost),"%"
    return BestSolution,BestTaskGraph