# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
from Scheduling_Functions import FindLastAllocatedTimeOnNode,FindLastAllocatedTimeOnLink
##########################################################################
#
#                                   REPORTS
#
#
##########################################################################
def ReportMappedTasks(AG):
    print "==========================================="
    print "          REPORTING SCHEDULING "
    print "==========================================="
    for Node in AG.nodes():
        print "NODE", Node,"CONTAINS THE FOLLOWING TASKS:",AG.node[Node]['MappedTasks'],\
            "\tWITH SCHEDULING:",AG.node[Node]['Scheduling']
    for Link in AG.edges():
        print "LINK", Link,"CONTAINS THE FOLLOWING TG's Edges:",AG.edge[Link[0]][Link[1]]['MappedTasks'],\
            "\tWITH SCHEDULING:",AG.edge[Link[0]][Link[1]]['Scheduling']

    return None
##########################################################################
def GenerateGanttCharts(TG,AG):
    NodeMakeSpanList=[]
    LinkMakeSpanList=[]
    for Node in AG.nodes():
        NodeMakeSpanList.append(FindLastAllocatedTimeOnNode(TG,AG,Node,False))
    for link in AG.edges():
        LinkMakeSpanList.append(FindLastAllocatedTimeOnLink(TG,AG,link,False))
    if len(LinkMakeSpanList)>0:
        MAX_Time_Link = max(LinkMakeSpanList)
    else:
        MAX_Time_Link = 0
    if len(NodeMakeSpanList)>0:
        MAX_Time_Node = max(NodeMakeSpanList)
    else:
        MAX_Time_Node = 0
    Max_Time = max(MAX_Time_Link,MAX_Time_Node)
    fig = plt.figure()
    plt.subplots_adjust(hspace=0.1)
    NodeCounter = 0
    EdgeCounter = 0
    for Node in AG.nodes():
        if len(AG.node[Node]['MappedTasks'])>0:
            NodeCounter += 1
    for Link in AG.edges():
        if len(AG.edge[Link[0]][Link[1]]['MappedTasks'])>0:
            EdgeCounter += 1
    NumberOfPlots = NodeCounter + EdgeCounter
    Count = 1
    for Node in AG.nodes():
        PE_T = []
        PE_P = []
        PE_P.append(0)
        PE_T.append(0)
        if len(AG.node[Node]['MappedTasks'])>0:
            ax1 = fig.add_subplot(NumberOfPlots ,1,Count)
            for Task in AG.node[Node]['MappedTasks']:
                    if Task in AG.node[Node]['Scheduling']:
                        StartTime=AG.node[Node]['Scheduling'][Task][0]
                        EndTime=AG.node[Node]['Scheduling'][Task][1]
                        PE_T.append(StartTime)
                        PE_P.append(0)
                        PE_T.append(StartTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0)
            PE_T.append(Max_Time)
            PE_P.append(0)
            plt.setp(ax1.get_yticklabels(), visible=False)
            if Count < EdgeCounter + NodeCounter:
                plt.setp(ax1.get_xticklabels(), visible=False)
            ax1.fill_between(PE_T, PE_P, 0 , color='b', edgecolor='k')
            ax1.set_ylabel(r'PE'+str(Node), size=14, rotation=0)
            Count += 1
    for Link in AG.edges():
        PE_T = []
        PE_P = []
        PE_P.append(0)
        PE_T.append(0)
        if len(AG.edge[Link[0]][Link[1]]['MappedTasks'])>0:
            ax1 = fig.add_subplot(NumberOfPlots,1,Count)
            for Task in AG.edge[Link[0]][Link[1]]['MappedTasks']:
                if AG.edge[Link[0]][Link[1]]['Scheduling']:
                        StartTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][0]
                        EndTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][1]
                        PE_T.append(StartTime)
                        PE_P.append(0)
                        PE_T.append(StartTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0)
            PE_T.append(Max_Time)
            PE_P.append(0)
            plt.setp(ax1.get_yticklabels(), visible=False)
            if Count < EdgeCounter+NodeCounter:
                plt.setp(ax1.get_xticklabels(), visible=False)
            ax1.fill_between(PE_T, PE_P, 0 , color='r', edgecolor='k')
            ax1.set_ylabel(r'L'+str(Link), size=14, rotation=0)
            Count += 1
    if EdgeCounter+EdgeCounter>0:
        ax1.xaxis.set_ticks_position('bottom')
    plt.savefig("GraphDrawings/Scheduling.png")
    plt.clf()
    return None