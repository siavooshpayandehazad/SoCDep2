__author__ = 'siavoosh'

import Scheduling_Functions_Nodes
from math import ceil
from ConfigAndPackages import Config


def FindTask_ASAP_Scheduling(TG, AG, SHM, Task, Node, logging):
    """

    :param TG:
    :param AG:
    :param SHM: System Health Map
    :param Task:
    :param Node:
    :param logging:
    :return:
    """
    CriticalityLevel = TG.node[Task]['Criticality']
    StartTime = max(Scheduling_Functions_Nodes.FindLastAllocatedTimeOnNode(TG, AG, Node, logging),
                    FindTaskPredecessorsFinishTime(TG, AG, Task, CriticalityLevel),
                    TG.node[Task]['Release'])
    # This includes the aging and lower frequency of the nodes of graph...
    # however, we do not include fractions of a cycle so we take ceiling of the execution time
    NodeSpeedDown = 1+((100.0-SHM.node[Node]['NodeSpeed'])/100)
    TaskExecutionOnNode = ceil(TG.node[Task]['WCET']*NodeSpeedDown)
    if TG.node[Task]['Criticality'] == 'H':
        EndTime = StartTime+TaskExecutionOnNode + Config.Task_SlackCount*TaskExecutionOnNode
    else:
        EndTime = StartTime+TaskExecutionOnNode
    return StartTime, EndTime


def FindTestTask_ASAP_Scheduling(TG, AG, SHM, Task, Node, logging):
    """

    :param TG:
    :param AG:
    :param SHM:  System Health Map
    :param Task:
    :param Node:
    :param logging:
    :return:
    """
    CriticalityLevel = TG.node[Task]['Criticality']

    StartTime = Scheduling_Functions_Nodes.FindFirstEmptySlotForTaskOnNode(TG, AG, SHM, Node, Task,
                                                FindTaskPredecessorsFinishTime(TG, AG, Task, CriticalityLevel), logging)

    # This includes the aging and lower frequency of the nodes of graph...
    # however, we do not include fractions of a cycle so we take ceiling of the execution time
    NodeSpeedDown = 1+((100.0-SHM.node[Node]['NodeSpeed'])/100)
    TaskExecutionOnNode = ceil(TG.node[Task]['WCET']*NodeSpeedDown)
    EndTime = StartTime+TaskExecutionOnNode
    return StartTime, EndTime


def FindTask_ALAP_Scheduling(TG, AG, Task, Node, Report):
    # todo: Implement ALAP
    return None


def FindTaskPredecessorsFinishTime(TG, AG, Task, CriticalityLevel):
    FinishTime = 0
    if len(TG.predecessors(Task)) > 0:
        for Predecessor in TG.predecessors(Task):
            if TG.node[Predecessor]['Node'] is not None:    # predecessor is mapped
                # if TG.node[Predecessor]['Criticality'] == CriticalityLevel: #this is not quit right...
                    Node = TG.node[Predecessor]['Node']
                    if Predecessor in AG.node[Node]['PE'].Scheduling:             # if this task is scheduled
                        FinishTime = max(AG.node[Node]['PE'].Scheduling[Predecessor][1], FinishTime)
    #for Edge in TG.edges():
    #    if Edge[1] == Task:
    #        # if TG.edge[Edge[0]][Edge[1]]['Criticality'] == CriticalityLevel:
    #            if len(TG.edge[Edge[0]][Edge[1]]['Link']) > 0:    # if the edge is mapped
    #                # TG.edge[Edge[0]][Edge[1]]['Link'] is a list of tuples of (batch, Link)
    #                for BatchAndLink in TG.edge[Edge[0]][Edge[1]]['Link']:     # for each link that this edge goes through
    #                    Link = BatchAndLink[1]
    #                    if len(AG.edge[Link[0]][Link[1]]['Scheduling']) > 0:
    #                        if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']:     # if this edge is scheduled
    #                            for ScheduleAndBatch in AG.edge[Link[0]][Link[1]]['Scheduling'][Edge]:
    #                                EndTime = ScheduleAndBatch[1]
    #                                FinishTime = max(EndTime, FinishTime)
    CurrentNode = TG.node[Task]['Node']
    for Edge in TG.edges():
        if Edge[1] == Task:
            if Edge in AG.node[CurrentNode]['Router'].Scheduling:
                for ScheduleAndBatch in AG.node[CurrentNode]['Router'].Scheduling[Edge]:
                    FinishTime = max(ScheduleAndBatch[1], FinishTime)
    return FinishTime