# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
from Scheduling_Functions import FindLastAllocatedTimeOnNode,FindLastAllocatedTimeOnLink
from ConfigAndPackages import Config

##########################################################################
#
#                           SCHEDULING REPORT
#
#
##########################################################################
def ReportMappedTasks(AG,logging):
    logging.info( "===========================================")
    logging.info( "          REPORTING SCHEDULING ")
    logging.info( "===========================================")
    for Node in AG.nodes():
        logging.info( "NODE"+str(Node)+"CONTAINS THE FOLLOWING TASKS:"+str(AG.node[Node]['MappedTasks'])+
            "\tWITH SCHEDULING:"+str(AG.node[Node]['Scheduling']))
    for Link in AG.edges():
        logging.info( "LINK" + str(Link)+"CONTAINS THE FOLLOWING TG's Edges:" +
                      str(AG.edge[Link[0]][Link[1]]['MappedTasks']) + "\tWITH SCHEDULING:" +
                      str(AG.edge[Link[0]][Link[1]]['Scheduling']))

    return None


##########################################################################
#
#
#                   Generating Gantt Charts
#
##########################################################################
def GenerateGanttCharts(TG,AG):
    print "==========================================="
    print "GENERATING SCHEDULING GANTT CHARTS..."
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

    NodeCounter = 0
    EdgeCounter = 0
    for Node in AG.nodes():
        if len(AG.node[Node]['MappedTasks'])>0:
            NodeCounter += 1
    for Link in AG.edges():
        if len(AG.edge[Link[0]][Link[1]]['MappedTasks'])>0:
            EdgeCounter += 1
    NumberOfPlots = NodeCounter + EdgeCounter
    if NumberOfPlots<10:
        NumberOfPlots=10
    Count = 1
    fig = plt.figure(figsize=(Max_Time/10+5,NumberOfPlots/2))
    plt.subplots_adjust(hspace=0.1)
    for Node in AG.nodes():
        if len(AG.node[Node]['MappedTasks'])>0:
            ax1 = fig.add_subplot(NumberOfPlots, 1, Count)
            for Task in AG.node[Node]['MappedTasks']:
                    PE_T = []
                    PE_P = []
                    PE_P.append(0)
                    PE_T.append(0)
                    Slack_T = []
                    Slack_P = []
                    Slack_T.append(0)
                    Slack_P.append(0)
                    TaskColor = 'w'
                    if Task in AG.node[Node]['Scheduling']:
                        if TG.node[Task]['Criticality']=='H':
                            StartTime = AG.node[Node]['Scheduling'][Task][0]
                            TaskLength = AG.node[Node]['Scheduling'][Task][1] - AG.node[Node]['Scheduling'][Task][0]
                            EndTime = StartTime + (TaskLength / (Config.SlackCount+1))
                            PE_T.append(StartTime)
                            PE_P.append(0)
                            PE_T.append(StartTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0)
                            TaskColor = '#FF878B'
                            if Config.SlackCount > 0:
                                StartTime =EndTime
                                EndTime = StartTime + (TaskLength / (Config.SlackCount+1)) * Config.SlackCount
                                Slack_T.append(StartTime)
                                Slack_P.append(0)
                                Slack_T.append(StartTime)
                                Slack_P.append(0.1)
                                Slack_T.append(EndTime)
                                Slack_P.append(0.1)
                                Slack_T.append(EndTime)
                                Slack_P.append(0)
                        else:
                            StartTime = AG.node[Node]['Scheduling'][Task][0]
                            EndTime = AG.node[Node]['Scheduling'][Task][1]
                            PE_T.append(StartTime)
                            PE_P.append(0)
                            PE_T.append(StartTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0)
                            if TG.node[Task]['Criticality'] == 'GH':
                                TaskColor = '#FFC29C'
                            elif TG.node[Task]['Criticality'] == 'GNH':
                                TaskColor = '#928AFF'
                            else:
                                TaskColor = '#CFECFF'
                    PE_T.append(Max_Time)
                    PE_P.append(0)
                    ax1.fill_between(PE_T, PE_P, 0, facecolor = TaskColor, edgecolor='k')
                    if Config.SlackCount > 0:
                        ax1.fill_between(Slack_T, Slack_P, 0, facecolor='#808080', edgecolor='k')
            plt.setp(ax1.get_yticklabels(), visible=False)
            if Count < EdgeCounter + NodeCounter:
                plt.setp(ax1.get_xticklabels(), visible=False)

            for Task in AG.node[Node]['MappedTasks']:
                    if Task in AG.node[Node]['Scheduling']:
                        StartTime=AG.node[Node]['Scheduling'][Task][0]
                        if TG.node[Task]['Criticality']=='H':
                            TaskLength=(AG.node[Node]['Scheduling'][Task][1] - AG.node[Node]['Scheduling'][Task][0])/(Config.SlackCount+1)
                            ax1.text(StartTime+(TaskLength)/2 - len(str(Task))/2, 0.05, str(Task), fontsize=10)
                            EndTime=AG.node[Node]['Scheduling'][Task][1]
                            if Config.SlackCount > 0:
                                ax1.text((StartTime+TaskLength+EndTime)/2 - len(str(Task)+'S')/2, 0.05, str(Task)+'S', fontsize=10)
                        else:
                            EndTime=AG.node[Node]['Scheduling'][Task][1]
                            ax1.text((StartTime+EndTime)/2 - len(str(Task))/2, 0.05, str(Task), fontsize=10)
            ax1.set_ylabel(r'PE'+str(Node), size=14, rotation=0)
            Count += 1
    for Link in AG.edges():
        if len(AG.edge[Link[0]][Link[1]]['MappedTasks'])>0:
            ax1 = fig.add_subplot(NumberOfPlots,1,Count)
            for Task in AG.edge[Link[0]][Link[1]]['MappedTasks']:
                PE_T = []
                PE_P = []
                PE_P.append(0)
                PE_T.append(0)
                EdgeColor='w'
                Slack_T = []
                Slack_P = []
                Slack_P.append(0)
                Slack_T.append(0)
                if AG.edge[Link[0]][Link[1]]['Scheduling']:
                    if TG.edge[Task[0]][Task[1]]['Criticality']=='H':
                        StartTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][0]
                        TaskLength = AG.edge[Link[0]][Link[1]]['Scheduling'][Task][1] - AG.edge[Link[0]][Link[1]]['Scheduling'][Task][0]
                        EndTime= StartTime + (TaskLength / (Config.SlackCount+1))
                        PE_T.append(StartTime)
                        PE_P.append(0)
                        PE_T.append(StartTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0.1)
                        PE_T.append(EndTime)
                        PE_P.append(0)
                        EdgeColor = '#FF878B'
                        if Config.SlackCount > 0:
                            StartTime =EndTime
                            EndTime = StartTime + (TaskLength / (Config.SlackCount+1)) * Config.SlackCount
                            Slack_T.append(StartTime)
                            Slack_P.append(0)
                            Slack_T.append(StartTime)
                            Slack_P.append(0.1)
                            Slack_T.append(EndTime)
                            Slack_P.append(0.1)
                            Slack_T.append(EndTime)
                            Slack_P.append(0)
                    else:
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
                        EdgeColor = '#CFECFF'
                PE_T.append(Max_Time)
                PE_P.append(0)
                ax1.fill_between(PE_T, PE_P, 0 , color=EdgeColor, edgecolor='k')
                if Config.SlackCount > 0:
                    ax1.fill_between(Slack_T, Slack_P, 0 , color='#808080', edgecolor='k')
            plt.setp(ax1.get_yticklabels(), visible=False)
            if Count < EdgeCounter+NodeCounter:
                plt.setp(ax1.get_xticklabels(), visible=False)
            for Task in AG.edge[Link[0]][Link[1]]['MappedTasks']:
                if AG.edge[Link[0]][Link[1]]['Scheduling']:
                    StartTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][0]
                    if TG.edge[Task[0]][Task[1]]['Criticality']=='H':
                            TaskLength=(AG.edge[Link[0]][Link[1]]['Scheduling'][Task][1] - AG.edge[Link[0]][Link[1]]['Scheduling'][Task][0])/(Config.SlackCount+1)
                            stringToDisplay= str(Task[0])+"/"+str(Task[1])
                            ax1.text(StartTime+(TaskLength)/2 - len(str(stringToDisplay))/2, 0.05, stringToDisplay, fontsize=10)
                            EndTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][1]
                            stringToDisplay= str(Task[0])+"/"+str(Task[1])+'S'
                            if Config.SlackCount > 0:
                                ax1.text((StartTime+TaskLength+EndTime)/2 - len(str(stringToDisplay))/2, 0.05, stringToDisplay, fontsize=10)
                    else:
                        EndTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][1]
                        stringToDisplay= str(Task[0])+"/"+str(Task[1])
                        ax1.text((StartTime+EndTime)/2 - len(str(stringToDisplay))/2, 0.05, stringToDisplay, fontsize=10)
            ax1.set_ylabel(r'L'+str(Link), size=14, rotation=0)
            Count += 1
    if EdgeCounter+EdgeCounter > 0:
        ax1.xaxis.set_ticks_position('bottom')
    plt.savefig("GraphDrawings/Scheduling.png")
    plt.clf()
    plt.close(fig)
    print  "\033[35m* VIZ::\033[0mSCHEDULING GANTT CHARTS CREATED AT: GraphDrawings/Scheduling.png"
    return None
