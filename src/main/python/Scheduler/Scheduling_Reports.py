# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
from Scheduling_Functions_Routers import FindLastAllocatedTimeOnRouter
from Scheduling_Functions_Nodes import FindLastAllocatedTimeOnNode
from Scheduling_Functions_Links import FindLastAllocatedTimeOnLink
from ConfigAndPackages import Config
import random

##########################################################################
#
#                           SCHEDULING REPORT
#
#
##########################################################################
def ReportMappedTasks(AG, logging):
    logging.info("===========================================")
    logging.info("          REPORTING SCHEDULING ")
    logging.info("===========================================")
    for Node in AG.nodes():
        logging.info("NODE"+str(Node)+"CONTAINS THE FOLLOWING TASKS:"+str(AG.node[Node]['PE'].MappedTasks) +
                     "\tWITH SCHEDULING:"+str(AG.node[Node]['PE'].Scheduling))
    for Link in AG.edges():
        logging.info("LINK" + str(Link)+"CONTAINS THE FOLLOWING TG's Edges:" +
                     str(AG.edge[Link[0]][Link[1]]['MappedTasks']) + "\tWITH SCHEDULING:" +
                     str(AG.edge[Link[0]][Link[1]]['Scheduling']))

    return None


##########################################################################
#
#
#                   Generating Gantt Charts
#
##########################################################################
def GenerateGanttCharts(TG, AG, FileName):
    print ("===========================================")
    print ("GENERATING SCHEDULING GANTT CHARTS...")
    NodeMakeSpanList = []
    RouterMakeSpanList = []
    LinkMakeSpanList = []
    for Node in AG.nodes():
        NodeMakeSpanList.append(FindLastAllocatedTimeOnNode(TG, AG, Node, logging=None))
        RouterMakeSpanList.append(FindLastAllocatedTimeOnRouter(TG, AG, Node, logging=None))
    for link in AG.edges():
        LinkMakeSpanList.append(FindLastAllocatedTimeOnLink(TG, AG, link, logging=None))
    if len(LinkMakeSpanList) > 0:
        MAX_Time_Link = max(LinkMakeSpanList)
    else:
        MAX_Time_Link = 0
    if len(NodeMakeSpanList) > 0:
        MAX_Time_Node = max(NodeMakeSpanList)
    else:
        MAX_Time_Node = 0
    if len(RouterMakeSpanList) > 0:
        MAX_Time_Router = max(RouterMakeSpanList)
    else:
        MAX_Time_Router = 0
    Max_Time = max(MAX_Time_Link, MAX_Time_Node, MAX_Time_Router)

    NodeCounter = 0
    RouterCounter = 0
    LinkCounter = 0
    for Node in AG.nodes():
        if len(AG.node[Node]['PE'].MappedTasks) > 0:
            NodeCounter += 1
        if len(AG.node[Node]['Router'].MappedTasks) > 0:
            RouterCounter += 1
    for Link in AG.edges():
        if len(AG.edge[Link[0]][Link[1]]['MappedTasks']) > 0:
            LinkCounter += 1
    NumberOfPlots = NodeCounter + LinkCounter + RouterCounter
    if NumberOfPlots < 10:
        NumberOfPlots = 10
    count = 1
    fig = plt.figure(figsize=(Max_Time/10+1, NumberOfPlots/2))
    plt.subplots_adjust(hspace=0.1)
    count, ax1 = Add_PEs_To_Drawing(TG, AG, NumberOfPlots, fig, NodeCounter, LinkCounter, Max_Time, count)
    count, ax1 = Add_Routers_To_Drawing(TG, AG, NumberOfPlots, fig, NodeCounter, LinkCounter, Max_Time, count)
    count, ax1 = Add_Links_To_Drawing(TG, AG, NumberOfPlots, fig, NodeCounter, LinkCounter,
                                      RouterCounter, Max_Time, count)

    if LinkCounter+NodeCounter+RouterCounter > 0:
        ax1.xaxis.set_ticks_position('bottom')
    plt.savefig("GraphDrawings/"+FileName+".png", dpi=200)
    plt.clf()
    plt.close(fig)
    print ("\033[35m* VIZ::\033[0mSCHEDULING GANTT CHARTS CREATED AT: GraphDrawings/Scheduling.png")
    return None


def Add_PEs_To_Drawing(TG, AG, NumberOfPlots, fig, NodeCounter, LinkCounter, Max_Time, Count):
    ax1 = None
    for Node in AG.nodes():
        if len(AG.node[Node]['PE'].MappedTasks) > 0:
            ax1 = fig.add_subplot(NumberOfPlots, 1, Count)
            for Task in AG.node[Node]['PE'].MappedTasks:
                    PE_T = []
                    PE_P = []
                    PE_P.append(0)
                    PE_T.append(0)
                    Slack_T = []
                    Slack_P = []
                    Slack_T.append(0)
                    Slack_P.append(0)
                    TaskColor = 'w'
                    if Task in AG.node[Node]['PE'].Scheduling:
                        if TG.node[Task]['Criticality'] == 'H':
                            StartTime = AG.node[Node]['PE'].Scheduling[Task][0]
                            TaskLength = AG.node[Node]['PE'].Scheduling[Task][1]-AG.node[Node]['PE'].Scheduling[Task][0]
                            EndTime = StartTime + (TaskLength/(Config.Task_SlackCount+1))
                            PE_T.append(StartTime)
                            PE_P.append(0)
                            PE_T.append(StartTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0)
                            TaskColor = '#FF878B'
                            if Config.Task_SlackCount > 0:
                                StartTime = EndTime
                                EndTime = StartTime + (TaskLength / (Config.Task_SlackCount+1)) * Config.Task_SlackCount
                                Slack_T.append(StartTime)
                                Slack_P.append(0)
                                Slack_T.append(StartTime)
                                Slack_P.append(0.1)
                                Slack_T.append(EndTime)
                                Slack_P.append(0.1)
                                Slack_T.append(EndTime)
                                Slack_P.append(0)
                        else:
                            StartTime = AG.node[Node]['PE'].Scheduling[Task][0]
                            EndTime = AG.node[Node]['PE'].Scheduling[Task][1]
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
                                if TG.node[Task]['Type'] == 'Test':
                                    if 'S' in Task:
                                        TaskColor = '#FFDA3D'
                                    else:
                                        TaskColor = '#FFEAA7'
                                else:
                                    TaskColor = '#CFECFF'
                    PE_T.append(Max_Time)
                    PE_P.append(0)
                    ax1.fill_between(PE_T, PE_P, 0, facecolor=TaskColor, edgecolor='k')
                    if Config.Task_SlackCount > 0:
                        ax1.fill_between(Slack_T, Slack_P, 0, facecolor='#808080', edgecolor='k')
            plt.setp(ax1.get_yticklabels(), visible=False)
            if Count < LinkCounter + NodeCounter:
                plt.setp(ax1.get_xticklabels(), visible=False)

            for Task in AG.node[Node]['PE'].MappedTasks:
                if Task in AG.node[Node]['PE'].Scheduling:
                    StartTime = AG.node[Node]['PE'].Scheduling[Task][0]
                    if TG.node[Task]['Criticality'] == 'H':
                        TaskLength = (AG.node[Node]['PE'].Scheduling[Task][1] -
                                      AG.node[Node]['PE'].Scheduling[Task][0])/(Config.Task_SlackCount+1)
                        ax1.text(StartTime+(TaskLength)/2 - len(str(Task))/2, 0.01, str(Task), fontsize=10)
                        EndTime = AG.node[Node]['PE'].Scheduling[Task][1]
                        if Config.Task_SlackCount > 0:
                            ax1.text((StartTime+TaskLength+EndTime)/2 - len(str(Task)+'S')/2,
                                     0.01, str(Task)+'S', fontsize=5)
                    else:
                        EndTime = AG.node[Node]['PE'].Scheduling[Task][1]
                        ax1.text((StartTime+EndTime)/2 - len(str(Task))/2, 0.01, str(Task), fontsize=5)
            ax1.yaxis.set_label_coords(-0.08, 0)
            ax1.set_ylabel(r'PE'+str(Node), size=14, rotation=0)
            Count += 1
    return Count, ax1


def Add_Routers_To_Drawing(TG, AG, NumberOfPlots, fig, NodeCounter, LinkCounter, Max_Time, Count):
    """
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param NumberOfPlots: Total Number of plots (All PEs that have mapping+All routers that pass a packet+all links)
    :param fig: a mathplotlib figure
    :param NodeCounter: counter that shows number of active nodes
    :param LinkCounter: counter that shows the number of active links
    :param Max_Time: maximum execution time on the network
    :param Count: counter of the number of plots added to this point
    :return: Count ,ax1
    """
    ax1 = None
    for Node in AG.nodes():
        if len(AG.node[Node]['Router'].MappedTasks) > 0:
            ax1 = fig.add_subplot(NumberOfPlots, 1, Count)
            SchedulList = []
            Zorder = len(AG.node[Node]['Router'].MappedTasks)
            for Task in AG.node[Node]['Router'].MappedTasks:
                PE_T = [0, 0]
                PE_P = [0.1, 0]
                EdgeColor = 'w'
                Slack_T = [0]
                Slack_P = [0]

                if Task in AG.node[Node]['Router'].Scheduling:
                    if TG.edge[Task[0]][Task[1]]['Criticality'] == 'H':
                        for BatchAndSchedule in AG.node[Node]['Router'].Scheduling:
                            StartTime = BatchAndSchedule[0]
                            BatchNum = BatchAndSchedule[2]
                            TaskLength = BatchAndSchedule[1] - StartTime
                            EndTime = StartTime + (TaskLength / (Config.Communication_SlackCount+1))
                            PE_T.append(StartTime)
                            PE_P.append(0)
                            PE_T.append(StartTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0)
                            EdgeColor = '#FF878B'
                            if Config.Communication_SlackCount > 0:
                                StartTime = EndTime
                                EndTime = StartTime + (TaskLength / (Config.Communication_SlackCount+1)) * Config.Communication_SlackCount
                                Slack_T.append(StartTime)
                                Slack_P.append(0)
                                Slack_T.append(StartTime)
                                Slack_P.append(0.1)
                                Slack_T.append(EndTime)
                                Slack_P.append(0.1)
                                Slack_T.append(EndTime)
                                Slack_P.append(0)
                        SchedulList.append((StartTime, EndTime, 1))
                        Zorder -= 1
                    else:
                        for BatchAndSchedule in AG.node[Node]['Router'].Scheduling[Task]:

                            StartTime = BatchAndSchedule[0]
                            EndTime = BatchAndSchedule[1]
                            BatchNum = BatchAndSchedule[2]
                            Prob = BatchAndSchedule[3]

                            PE_T.append(StartTime)
                            PE_P.append(0)
                            PE_T.append(StartTime)
                            PE_P.append(0.1 * Prob)

                            PastProb = 0
                            for AddedRect in SchedulList:
                                if AddedRect[0] <= StartTime < AddedRect[1]:
                                    PastProb += AddedRect[2]

                            if PastProb > 0:
                                PE_T.append(StartTime)
                                Prob = BatchAndSchedule[3]+PastProb
                                PE_P.append(0.1 * Prob)

                            UpDict = {}
                            for AddedRect in SchedulList:
                                if StartTime < AddedRect[0] < EndTime:
                                    if AddedRect[0] in UpDict:
                                        UpDict[AddedRect[0]] += AddedRect[2]
                                    else:
                                        UpDict[AddedRect[0]] = AddedRect[2]

                            DownDict = {}
                            for AddedRect in SchedulList:
                                if StartTime < AddedRect[1] < EndTime:
                                    if AddedRect[1] in DownDict:
                                        DownDict[AddedRect[1]] += AddedRect[2]
                                    else:
                                        DownDict[AddedRect[1]] = AddedRect[2]

                            for TimeInstant in sorted(UpDict.keys()+DownDict.keys()):
                                if TimeInstant in UpDict.keys():
                                    PE_T.append(TimeInstant)
                                    PE_P.append(0.1 * Prob)
                                    Prob = UpDict[TimeInstant] + Prob
                                    PE_T.append(TimeInstant)
                                    PE_P.append(0.1 * Prob)

                                if TimeInstant in DownDict.keys():
                                    PE_T.append(TimeInstant)
                                    PE_P.append(0.1 * Prob)
                                    Prob = Prob - DownDict[TimeInstant]
                                    PE_T.append(TimeInstant)
                                    PE_P.append(0.1 * Prob)

                            PastProb = 0
                            for AddedRect in SchedulList:
                                if AddedRect[0] < EndTime <= AddedRect[1]:
                                        PastProb += AddedRect[2]

                            if PastProb > 0:
                                PE_T.append(EndTime)
                                Prob = BatchAndSchedule[3]+PastProb
                                PE_P.append(0.1 * Prob)
                            else:
                                PE_T.append(EndTime)
                                PE_P.append(0.1 * BatchAndSchedule[3])
                            PE_T.append(EndTime)
                            PE_P.append(0)
                            random.seed(Task)
                            r = random.randrange(0, 255)
                            g = random.randrange(0, 255)
                            b = random.randrange(0, 255)
                            EdgeColor = '#%02X%02X%02X' % (r, g, b)
                            # EdgeColor = '#CFECFF'
                            # print TryOutList
                            SchedulList.append((StartTime, EndTime, BatchAndSchedule[3]))
                            Zorder -= 1

                PE_T.append(Max_Time)
                PE_P.append(0)
                PE_T.append(Max_Time)
                PE_P.append(0.1)
                PE_T.append(Max_Time)
                PE_P.append(0)
                if TG.node[Task[0]]['Type'] == 'Test' or TG.node[Task[1]]['Type'] == 'Test':
                    ax1.fill_between(PE_T, PE_P, 0, color=EdgeColor, edgecolor='k', zorder= Zorder, hatch='\\')
                else:
                    ax1.fill_between(PE_T, PE_P, 0, color=EdgeColor, edgecolor=EdgeColor, zorder=Zorder)
                if Config.Communication_SlackCount > 0:
                    ax1.fill_between(Slack_T, Slack_P, 0, color='#808080', edgecolor='#808080')

            plt.setp(ax1.get_yticklabels(), visible=False)
            if Count < LinkCounter+NodeCounter:
                plt.setp(ax1.get_xticklabels(), visible=False)

            ax1.yaxis.set_label_coords(-0.08, 0)
            ax1.set_ylabel(r'R'+str(Node), size=14, rotation=0)
            Count += 1
    return Count, ax1


def Add_Links_To_Drawing(TG, AG, NumberOfPlots, fig, NodeCounter, LinkCounter, RouterCounter, Max_Time, Count):
    ax1 = None
    for Link in AG.edges():
        if len(AG.edge[Link[0]][Link[1]]['MappedTasks'])>0:
            ax1 = fig.add_subplot(NumberOfPlots, 1, Count)
            SchedulList = []
            Zorder = len(AG.edge[Link[0]][Link[1]]['MappedTasks'])
            for Task in AG.edge[Link[0]][Link[1]]['MappedTasks']:
                PE_T = [0, 0]
                PE_P = [0.1, 0]
                EdgeColor = 'w'
                Slack_T = [0]
                Slack_P = [0]

                if Task in AG.edge[Link[0]][Link[1]]['Scheduling']:
                    if TG.edge[Task[0]][Task[1]]['Criticality'] == 'H':
                        for BatchAndSchedule in AG.edge[Link[0]][Link[1]]['Scheduling'][Task]:
                            StartTime = BatchAndSchedule[0]
                            BatchNum = BatchAndSchedule[2]
                            TaskLength = BatchAndSchedule[1] - StartTime
                            EndTime = StartTime + (TaskLength / (Config.Communication_SlackCount+1))
                            PE_T.append(StartTime)
                            PE_P.append(0)
                            PE_T.append(StartTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0.1)
                            PE_T.append(EndTime)
                            PE_P.append(0)
                            EdgeColor = '#FF878B'
                            if Config.Communication_SlackCount > 0:
                                StartTime = EndTime
                                EndTime = StartTime + (TaskLength / (Config.Communication_SlackCount+1)) * Config.Communication_SlackCount
                                Slack_T.append(StartTime)
                                Slack_P.append(0)
                                Slack_T.append(StartTime)
                                Slack_P.append(0.1)
                                Slack_T.append(EndTime)
                                Slack_P.append(0.1)
                                Slack_T.append(EndTime)
                                Slack_P.append(0)
                        SchedulList.append((StartTime, EndTime, 1))
                        Zorder -= 1
                    else:
                        for BatchAndSchedule in AG.edge[Link[0]][Link[1]]['Scheduling'][Task]:

                            StartTime = BatchAndSchedule[0]
                            EndTime = BatchAndSchedule[1]
                            BatchNum = BatchAndSchedule[2]
                            Prob = BatchAndSchedule[3]

                            PE_T.append(StartTime)
                            PE_P.append(0)
                            PE_T.append(StartTime)
                            PE_P.append(0.1 * Prob)

                            PastProb = 0
                            for AddedRect in SchedulList:
                                if AddedRect[0] <= StartTime < AddedRect[1]:
                                    PastProb += AddedRect[2]

                            if PastProb > 0:
                                PE_T.append(StartTime)
                                Prob = BatchAndSchedule[3]+PastProb
                                PE_P.append(0.1 * Prob)

                            UpDict = {}
                            for AddedRect in SchedulList:
                                if StartTime < AddedRect[0] < EndTime:
                                    if AddedRect[0] in UpDict:
                                        UpDict[AddedRect[0]] += AddedRect[2]
                                    else:
                                        UpDict[AddedRect[0]] = AddedRect[2]

                            DownDict = {}
                            for AddedRect in SchedulList:
                                if StartTime < AddedRect[1] < EndTime:
                                    if AddedRect[1] in DownDict:
                                        DownDict[AddedRect[1]] += AddedRect[2]
                                    else:
                                        DownDict[AddedRect[1]] = AddedRect[2]

                            for TimeInstant in sorted(UpDict.keys()+DownDict.keys()):
                                if TimeInstant in UpDict.keys():
                                    PE_T.append(TimeInstant)
                                    PE_P.append(0.1 * Prob)
                                    Prob = UpDict[TimeInstant] + Prob
                                    PE_T.append(TimeInstant)
                                    PE_P.append(0.1 * Prob)

                                if TimeInstant in DownDict.keys():
                                    PE_T.append(TimeInstant)
                                    PE_P.append(0.1 * Prob)
                                    Prob = Prob - DownDict[TimeInstant]
                                    PE_T.append(TimeInstant)
                                    PE_P.append(0.1 * Prob)

                            PastProb = 0
                            for AddedRect in SchedulList:
                                if AddedRect[0] < EndTime <= AddedRect[1]:
                                        PastProb += AddedRect[2]

                            if PastProb > 0:
                                PE_T.append(EndTime)
                                Prob = BatchAndSchedule[3]+PastProb
                                PE_P.append(0.1 * Prob)
                            else:
                                PE_T.append(EndTime)
                                PE_P.append(0.1 * BatchAndSchedule[3])
                            PE_T.append(EndTime)
                            PE_P.append(0)
                            random.seed(Task)
                            r = random.randrange(0, 255)
                            g = random.randrange(0, 255)
                            b = random.randrange(0, 255)
                            EdgeColor = '#%02X%02X%02X' % (r, g, b)
                            # EdgeColor = '#CFECFF'
                            # print TryOutList
                            SchedulList.append((StartTime, EndTime, BatchAndSchedule[3]))
                            Zorder -= 1

                PE_T.append(Max_Time)
                PE_P.append(0)
                PE_T.append(Max_Time)
                PE_P.append(0.1)
                PE_T.append(Max_Time)
                PE_P.append(0)
                if TG.node[Task[0]]['Type'] == 'Test' or TG.node[Task[1]]['Type'] == 'Test':
                    ax1.fill_between(PE_T, PE_P, 0, color=EdgeColor, edgecolor='k', zorder= Zorder, hatch='\\')
                else:
                    ax1.fill_between(PE_T, PE_P, 0, color=EdgeColor, edgecolor=EdgeColor, zorder=Zorder)
                if Config.Communication_SlackCount > 0:
                    ax1.fill_between(Slack_T, Slack_P, 0, color='#808080', edgecolor='#808080')

            plt.setp(ax1.get_yticklabels(), visible=False)
            if Count < LinkCounter + NodeCounter + RouterCounter - 1:
                plt.setp(ax1.get_xticklabels(), visible=False)

            ax1.yaxis.set_label_coords(-0.08, 0)
            ax1.set_ylabel(r'L'+str(Link), size=14, rotation=0)
            Count += 1
    return Count, ax1