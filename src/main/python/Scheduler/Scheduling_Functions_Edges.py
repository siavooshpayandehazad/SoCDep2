# Copyright (C) 2015 Siavoosh Payandeh Azad

import Scheduling_Functions_Links, Scheduling_Functions_Routers
from ConfigAndPackages import Config

def FindEdge_ASAP_Scheduling_Link(TG, AG, Edge, Link, batch, Prob, Report, logging=None):
    """
    Finds the earliest start and finish time for scheduling Edge from TG on Link from AG.
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param Edge: Edge ID in TG to be scheduled on Link
    :param Link: Link ID in AG for scheduling Edge on it
    :param batch: Edge's Batch
    :param Prob: probability of Edge to actually going through Link
    :param Report: Report Switch
    :param logging: logging File
    :return: Start Time and Stop Time
    """
    StartTime = max(Scheduling_Functions_Links.FindLastAllocatedTimeOnLinkForTask(TG, AG, Link, Edge,
                                                                                  Prob, logging),
                    FindEdgePredecessorsFinishTime(TG, AG, Edge, batch))
    EdgeExecutionOnLink = TG.edge[Edge[0]][Edge[1]]['ComWeight']
    if TG.edge[Edge[0]][Edge[1]]['Criticality'] == 'H':
        EndTime = StartTime+EdgeExecutionOnLink+Config.Communication_SlackCount*EdgeExecutionOnLink
    else:
        EndTime = StartTime+EdgeExecutionOnLink
    return StartTime, EndTime


def FindEdge_ASAP_Scheduling_Router(TG, AG, Edge, Node, batch, Prob, Report, logging=None):
    """
    Calculates the start time and end time for ASAP scheduling of an Edge on a Router
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param Edge: Edge in TG to be mapped
    :param Node: Node ID number for mapping Edge on its Router
    :param batch: Batch of the mapped Edge
    :param Prob: Probability of Edge actually going through router
    :param Report: Report Switch
    :param logging: logging File
    :return: Start Time and End time
    """
    StartTime = max(Scheduling_Functions_Routers.FindLastAllocatedTimeOnRouterForTask(TG, AG, Node, Edge,
                                                                                      Prob, logging),
                    FindEdgePredecessorsFinishTime(TG, AG, Edge, batch))
    EdgeExecutionOnLink = TG.edge[Edge[0]][Edge[1]]['ComWeight']
    if TG.edge[Edge[0]][Edge[1]]['Criticality'] == 'H':
        EndTime = StartTime+EdgeExecutionOnLink+Config.Communication_SlackCount*EdgeExecutionOnLink
    else:
        EndTime = StartTime+EdgeExecutionOnLink
    return StartTime, EndTime


def FindTestEdge_ASAP_Scheduling(tg, ag, edge, link, batch, prob, report, logging=None):
    """
    Finds the start and end time for ASAP scheduling of a Test Edge on a link.
    Important note is that the Edge should be coming from "Test" type in TG.
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param edge: Test Edge to be mapped
    :param link: Link ID for Scheduling the TestEdge
    :param batch: Batch of the mapped Edge
    :param prob: probability of Edge actually passing through Link
    :param report: Report Switch
    :param logging: logging File
    :return: Start Time and End Time
    """
    start_time = max(Scheduling_Functions_Links.FindLastAllocatedTimeOnLinkForTask(tg, ag, link, edge,
                                                                                  prob, logging),
                    FindEdgePredecessorsFinishTime(tg, ag, edge, batch))
    edge_execution_on_link = tg.edge[edge[0]][edge[1]]['ComWeight']
    end_time = start_time+edge_execution_on_link

    return start_time, end_time



def FindEdge_ALAP_Scheduling(TG, AG, Edge, Link, batch, Prob, Report, logging):
    # todo: Implement ALAP
    return None


def FindEdgePredecessorsFinishTime(TG, AG, Edge, batch):
    """
    Finds and returns the maximum of predecessors of Edge's scheduled finish time
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param Edge: Edge ID of task to be scheduled
    :param batch: Edge's Batch
    :return: Finish Time
    """
    FinishTime = 0
    SourceNode = TG.node[Edge[0]]['Node']
    if Edge[0] in AG.node[SourceNode]['PE'].Scheduling:
        FinishTime = max (AG.node[SourceNode]['PE'].Scheduling[Edge[0]][1], FinishTime)

    for Link in AG.edges():
            # if they are incoming links
            if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']:
                for ScheduleAndBatch in AG.edge[Link[0]][Link[1]]['Scheduling'][Edge]:
                    if ScheduleAndBatch[2] == batch:
                        if ScheduleAndBatch[1] > FinishTime:
                            if Config.FlowControl == "Wormhole":
                                FinishTime = max (ScheduleAndBatch[0]+1,FinishTime)
                            elif Config.FlowControl == "StoreAndForward":
                                FinishTime = max (ScheduleAndBatch[1],FinishTime)
                            else:
                                raise ValueError("FlowControl is not supported")

    for Node in AG.nodes():
        if Edge in AG.node[Node]['Router'].Scheduling:
            for ScheduleAndBatch in AG.node[Node]['Router'].Scheduling[Edge]:
                if ScheduleAndBatch[2] == batch:
                    if ScheduleAndBatch[1] > FinishTime:
                        if Config.FlowControl == "Wormhole":
                            FinishTime = max (ScheduleAndBatch[0]+1,FinishTime)
                        elif Config.FlowControl == "StoreAndForward":
                            FinishTime = max (ScheduleAndBatch[1],FinishTime)
                        else:
                            raise ValueError("FlowControl is not supported")
    return FinishTime
