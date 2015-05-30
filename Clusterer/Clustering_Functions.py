__author__ = 'siavoosh'
import networkx
import matplotlib.pyplot as plt
import statistics

def ReportCTG(CTG,filename):
    print "==========================================="
    print "      REPORTING CLUSTERED TASK GRAPH"
    print "==========================================="
    ClusterTaskListDicForDraw = {}
    ClusterWeightDicForDraw = {}
    for node in CTG.nodes():
        print "\tCLUSTER #:", node, "\tTASKS:", CTG.node[node]['TaskList'], "\tUTILIZATION:",CTG.node[node]['Utilization']
        ClusterTaskListDicForDraw[node] = CTG.node[node]['TaskList']
    for edge in CTG.edges():
        print "\tEDGE #:", edge, "\tWEIGHT:", CTG.edge[edge[0]][edge[1]]['Weight']
        ClusterWeightDicForDraw[edge] = CTG.edge[edge[0]][edge[1]]['Weight']
    print "PREPARING GRAPH DRAWINGS..."
    pos = networkx.shell_layout(CTG)
    networkx.draw_networkx_nodes(CTG, pos, node_size=2200)
    networkx.draw_networkx_edges(CTG, pos)
    networkx.draw_networkx_edge_labels(CTG, pos, edge_labels=ClusterWeightDicForDraw)
    networkx.draw_networkx_labels(CTG, pos, labels=ClusterTaskListDicForDraw)
    plt.savefig("GraphDrawings/"+filename)
    plt.clf()
    print "GRAPH DRAWINGS DONE, CHECK \"GraphDrawings/"+filename,"\""
    print "==========================================="
    return None

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
                        print "\t\033[31mERROR\033[0m:: EDGE DOESNT EXIST"
                        ReportCTG(CTG,"CTG_Error.png")
                        DoubleCheckCTG(TG,CTG)
                    if CTG.edge[SourceCluster][DestCluster]['Weight'] - WeightToRemove >= 0:
                        CTG.edge[SourceCluster][DestCluster]['Weight'] -= WeightToRemove
                        if CTG.edge[SourceCluster][DestCluster]['Weight'] == 0:
                            CTG.remove_edge(SourceCluster,DestCluster)
                    else:
                        print "\t\033[31mERROR\033[0m::FINAL WEIGHT IS NEGATIVE"
    TG.node[Task]['Cluster'] = None
    CTG.node[TaskCluster]['TaskList'].remove(Task)
    CTG.node[TaskCluster]['Utilization']-=  TG.node[Task]['WCET']
    return None

def AddTaskToCTG(TG,CTG,Task,Cluster,MaXBandWidth):
    """
    Takes a Task from a Task Graph and adds it to a cluster in Cluster graph
    by adding related edges etc.
    :param TG: Task graph
    :param CTG:  clustered task graph
    :param Task: Task to be added
    :param Cluster: destination cluster fro mapping the Task
    :param MaXBandWidth: Maximum bandwidth of the links on the architecture graph
    :return: True if addition is success, False if otherwise...
    """
    #print "\tADDING TASK:", Task, " TO CLUSTER:", Cluster
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
                        #print "\t\tEDGE", SrcCluster,"--->", DstCluster, "ALREADY EXISTS... ADDING", WeightToAdd, "TO WEIGHT..."
                        CTG.edge[SrcCluster][DstCluster]['Weight'] += WeightToAdd
                    else:
                        #print "\t\tEDGE", SrcCluster, DstCluster, "DOES NOT EXISTS... ADDING EDGE WITH WEIGHT:", \
                        #TG.edge[Edge[0]][Edge[1]]['ComWeight']
                        CTG.add_edge(SrcCluster, DstCluster, Weight=WeightToAdd)
    """for cluster in CTG.nodes():
        if CTG.node[cluster]['Utilization'] > 100:
            print "\t\033[33mWARNING\033[0m::OVER UTILIZATION... REVERTING THE PROCESS"
            return False
    for edge in CTG.edges():
        if CTG.edge[edge[0]][edge[1]]['Weight'] > MaXBandWidth:
            print "\t\033[33mWARNING\033[0m::BANDWIDTH VIOLATION... REVERTING THE PROCESS"
            return False
    """
    return True

def CostFunction(CTG):
    """
    This Function is calculating the cost of a solution for clustering optimization algorithm.
    :param CTG: The Clustered task graph
    :return: Cost
    """
    Cost = 0
    CommunicationWeight=0
    for edge in CTG.edges():
        CommunicationWeight += CTG.edge[edge[0]][edge[1]]['Weight']

    ClusterUtilization=[]
    for Node in CTG.nodes():
        ClusterUtilization.append(CTG.node[Node]['Utilization'])

    StandardDev=statistics.stdev(ClusterUtilization)
    #print "\tCOMWEIGHT:",CommunicationWeight,"STDEV:",StandardDev
    Cost=CommunicationWeight + StandardDev
    return Cost

def ClearClustering(TG,CTG):
    """
    Clears a clustering that has been done. by removing the tasks in task-list of clusters,
    removing parent cluster of tasks and deleting all the edges in cluster graph.
    :param TG:
    :param CTG:
    :return:
    """
    for node in TG.nodes():
        TG.node[node]['Cluster'] = None
    for cluster in CTG.nodes():
        CTG.node[cluster]['TaskList'] = []
        CTG.node[cluster]['Utilization'] = 0
    for edge in CTG.edges():
        CTG.remove_edge(edge[0], edge[1])
    return None

def DoubleCheckCTG(TG,CTG):
    """
    Checks if the clusters info in TG matches with the information in the CTG.
    :param TG: Task Graph
    :param CTG: Clustered Task Graph
    :return:
    """
    for Task in TG.nodes():
        Cluster= TG.node[Task]['Cluster']
        if Cluster in CTG.nodes():
            if Task not in CTG.node[Cluster]['TaskList']:
                print "DOUBLE CHECKING CTG with TG: \t\033[31mFAILED\033[0m"
                print "TASK",Task,"DOES NOT EXIST IN CLUSTER:",Cluster
                ReportCTG(CTG,"CTG_DoubleCheckError.png")
                return False
            else:
                #print "DOUBLE CHECKING CTG with TG: OK!"
                None
        else:
            print "DOUBLE CHECKING CTG with TG: \t\033[31mFAILED\033[0m"
            print "CLUSTER", Cluster," DOESNT EXIST...!!!"
            ReportCTG(CTG,"CTG_DoubleCheckError.png")
    return True