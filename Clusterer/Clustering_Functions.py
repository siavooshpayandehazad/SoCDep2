# Copyright (C) 2015 Siavoosh Payandeh Azad 


import statistics
import ClusteringReports
from ConfigAndPackages import Config

def RemoveTaskFromCTG(TG,CTG,Task):
    TaskCluster = TG.node[Task]['Cluster']
    #print "\tREMOVING TASK:", Task, " FROM CLUSTER:", TaskCluster
    for edge in TG.edges():
        if Task in edge:
            WeightToRemove = TG.edge[edge[0]][edge[1]]['ComWeight']
            SourceCluster = TG.node[edge[0]]['Cluster']
            DestCluster = TG.node[edge[1]]['Cluster']
            if SourceCluster is not None and DestCluster is not None:
                if SourceCluster != DestCluster:
                    #print "\t\tREMOVING TG EDGE:", edge, "WITH WEIGHT", WeightToRemove, "FROM CLUSTER:", \
                    #    SourceCluster, "--->", DestCluster
                    if (SourceCluster,DestCluster) not in CTG.edges():
                        print "\t\033[31mERROR\033[0m:: EDGE ",SourceCluster, "--->", DestCluster,"DOESNT EXIST"
                        ClusteringReports.ReportCTG(CTG,"CTG_Error.png")
                        raise ValueError("RemoveTaskFromCTG::EDGE DOESNT EXIST")
                    else:
                        if CTG.edge[SourceCluster][DestCluster]['Weight'] - WeightToRemove >= 0:
                            CTG.edge[SourceCluster][DestCluster]['Weight'] -= WeightToRemove
                            if CTG.edge[SourceCluster][DestCluster]['Weight'] == 0:
                                CTG.remove_edge(SourceCluster,DestCluster)
                        else:
                            print "\t\033[31mERROR\033[0m::FINAL WEIGHT IS NEGATIVE"
                            raise ValueError("RemoveTaskFromCTG::FINAL WEIGHT IS NEGATIVE")
    TG.node[Task]['Cluster'] = None
    CTG.node[TaskCluster]['TaskList'].remove(Task)
    if len(CTG.node[TaskCluster]['TaskList']) == 0:
        CTG.node[TaskCluster]['Criticality'] = 'L'
    CTG.node[TaskCluster]['Utilization'] -= TG.node[Task]['WCET']
    return None

def AddTaskToCTG(TG,CTG,Task,Cluster):
    """
    Takes a Task from a Task Graph and adds it to a cluster in Cluster graph
    by adding related edges etc.
    :param TG: Task graph
    :param CTG:  clustered task graph
    :param Task: Task to be added
    :param Cluster: destination cluster fro mapping the Task
    :return: True if addition is success, False if otherwise...
    """
    #print "\tADDING TASK:", Task, " TO CLUSTER:", Cluster
    if len(CTG.node[Cluster]['TaskList']) == 0 :
        CTG.node[Cluster]['Criticality'] = TG.node[Task]['Criticality']
    else:
        if Config.EnablePartitioning:
            if CTG.node[Cluster]['Criticality'] == TG.node[Task]['Criticality']:
                pass
            else:
                return False
    CTG.node[Cluster]['TaskList'].append(Task)
    CTG.node[Cluster]['Utilization']+= TG.node[Task]['WCET']
    TG.node[Task]['Cluster'] = Cluster
    for Edge in TG.edges():
        if Task in Edge:
            WeightToAdd = TG.edge[Edge[0]][Edge[1]]['ComWeight']
            SrcCluster = TG.node[Edge[0]]['Cluster']
            DstCluster = TG.node[Edge[1]]['Cluster']
            if SrcCluster is not None and DstCluster is not None:
                if SrcCluster != DstCluster:
                    if (SrcCluster, DstCluster) in CTG.edges():
                        if Config.Clustering_DetailedReport:
                            print "\t\tEDGE", SrcCluster,"--->", DstCluster, \
                                  "ALREADY EXISTS... ADDING", WeightToAdd, "TO WEIGHT..."
                        CTG.edge[SrcCluster][DstCluster]['Weight'] += WeightToAdd
                    else:
                        if Config.Clustering_DetailedReport:
                            print "\t\tEDGE", SrcCluster, DstCluster, "DOES NOT EXISTS... ADDING EDGE WITH WEIGHT:", \
                                  TG.edge[Edge[0]][Edge[1]]['ComWeight']
                        CTG.add_edge(SrcCluster, DstCluster, Weight=WeightToAdd)
    return True

def CostFunction(CTG):
    """
    This Function is calculating the cost of a solution for clustering optimization algorithm.
    :param CTG: The Clustered task graph
    :return: Cost
    """
    ComWeightList = []
    for edge in CTG.edges():
        ComWeightList .append(CTG.edge[edge[0]][edge[1]]['Weight'])


    ClusterUtilization = []
    for Node in CTG.nodes():
        ClusterUtilization.append(CTG.node[Node]['Utilization'])


    CommunicationWeight = sum(ComWeightList)
    MaxComWeight = max(ComWeightList)
    MaxUtil = max(ClusterUtilization)
    AvgUtil = sum(ClusterUtilization)/len(ClusterUtilization)
    ClusterUtilSD = statistics.stdev(ClusterUtilization)
    ComWeightSD = statistics.stdev(ComWeightList)

    # print "\tCOMWEIGHT:",CommunicationWeight,"STDEV:",ClusterUtilSD, "MAXUTIL:", MaxUtil, "AVG_UTIL:", AvgUtil

    if Config.Clustering_CostFunctionType == 'SD':
        Cost = ClusterUtilSD + ComWeightSD
    elif Config.Clustering_CostFunctionType == 'SD+MAX':
        Cost = MaxComWeight +  ComWeightSD  + MaxUtil  + ClusterUtilSD
    else:
        raise ValueError("Clustering_CostFunctionType is not valid")
    return Cost

def ClearClustering(TG, CTG):
    """
    Clears a clustering that has been done. by removing the tasks in task-list of clusters,
    removing parent cluster of tasks and deleting all the edges in cluster graph.
    :param TG: Task Graph
    :param CTG: Clustered Task Graph
    :return: None
    """
    for node in TG.nodes():
        TG.node[node]['Cluster'] = None
    for cluster in CTG.nodes():
        CTG.node[cluster]['TaskList'] = []
        CTG.node[cluster]['Utilization'] = 0
        CTG.node[cluster]['Criticality'] = None
    for edge in CTG.edges():
        CTG.remove_edge(edge[0], edge[1])
    return None


def DeleteEmptyClusters(CTG):
    for Cluster in CTG.nodes():
        if len(CTG.node[Cluster]['TaskList']) == 0:
            CTG.remove_node(Cluster)
    return None
