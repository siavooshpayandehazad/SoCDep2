__author__ = 'siavoosh'

import Scheduling_Functions_Links
from ConfigAndPackages import Config

def FindEdge_ASAP_Scheduling(TG, AG, Edge, Link, batch, Prob, Report, logging):
    StartTime = max(Scheduling_Functions_Links.FindLastAllocatedTimeOnLinkForTask(TG, AG, Link, Edge,
                                                                                  Prob, logging),
                    FindEdgePredecessorsFinishTime(TG, AG, Edge, batch, Link))
    EdgeExecutionOnLink = TG.edge[Edge[0]][Edge[1]]['ComWeight']
    if TG.edge[Edge[0]][Edge[1]]['Criticality'] == 'H':
        EndTime = StartTime+EdgeExecutionOnLink+Config.Communication_SlackCount*EdgeExecutionOnLink
    else:
        EndTime = StartTime+EdgeExecutionOnLink
    return StartTime, EndTime


def FindTestEdge_ASAP_Scheduling(TG, AG, Edge, Link, batch, Prob, Report, logging):
    StartTime = max(Scheduling_Functions_Links.FindLastAllocatedTimeOnLinkForTask(TG, AG, Link, Edge,
                                                                                  Prob, logging),
                    FindEdgePredecessorsFinishTime(TG, AG, Edge, batch, Link))
    EdgeExecutionOnLink = TG.edge[Edge[0]][Edge[1]]['ComWeight']
    EndTime = StartTime+EdgeExecutionOnLink

    return StartTime, EndTime




def FindEdge_ALAP_Scheduling(TG, AG, Edge, Link, batch, Prob, Report, logging):
    # todo: Implement ALAP
    return None


def FindEdgePredecessorsFinishTime(TG, AG, Edge, batch, CurrentLink):
    FinishTime = 0
    Node = TG.node[Edge[0]]['Node']
    if Edge[0] in AG.node[Node]['PE'].Scheduling:
        if AG.node[Node]['PE'].Scheduling[Edge[0]][1] > FinishTime:
            FinishTime = AG.node[Node]['PE'].Scheduling[Edge[0]][1]

    for Link in AG.edges():
        if Link[1] == CurrentLink[0]:
            # if they are incoming links
            if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']:
                for ScheduleAndBatch in AG.edge[Link[0]][Link[1]]['Scheduling'][Edge]:
                    if ScheduleAndBatch[2] == batch:
                        if ScheduleAndBatch[1] > FinishTime:
                            FinishTime = ScheduleAndBatch[1]

    return FinishTime
