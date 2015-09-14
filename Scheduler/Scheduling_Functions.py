# Copyright (C) 2015 Siavoosh Payandeh Azad 

from math import ceil
from ConfigAndPackages import Config

def FindScheduleMakeSpan(AG):
    MakeSpan = 0
    for Node in AG.nodes():
        for Task in AG.node[Node]['MappedTasks']:
            MakeSpan = max(AG.node[Node]['Scheduling'][Task][1], MakeSpan)
    return MakeSpan


################################################################
def ClearScheduling(AG, TG):
    for Node in AG.nodes():
        AG.node[Node]['Scheduling'] = {}
    for Link in AG.edges():
        AG.edge[Link[0]][Link[1]]['Scheduling'] = {}
    return None


##########################################################################
#
#                       ADDING TASK AND EDGE TO
#                               RESOURCES
#
##########################################################################
def Add_TG_TaskToNode(TG, AG, Task, Node, StartTime, EndTime, logging):
    """
    Adds a Task from Task Graph with specific Start time and end time to mapped node in architecture graph
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param Task: Task ID
    :param Node: Node ID
    :param StartTime: Scheduling time for Task
    :param EndTime: Task duration for scheduling
    :param logging: logging file
    :return: True
    """
    logging.info ("\t\tADDING TASK: "+str(Task)+" TO NODE: "+str(Node))
    logging.info ("\t\tSTARTING TIME: "+str(StartTime)+" ENDING TIME:"+str(EndTime))
    AG.node[Node]['Scheduling'][Task] = [StartTime, EndTime]
    TG.node[Task]['Node'] = Node
    return True


def Add_TG_EdgeTo_link(TG, AG, Edge, Link, batch, Prob, StartTime, EndTime, logging):
    logging.info ("\t\tADDING EDGE: "+str(Edge)+" FROM BATCH: "+str(batch)+" TO LINK: "+str(Link))
    logging.info ("\t\tSTARTING TIME: "+str(StartTime)+" ENDING TIME: "+str(EndTime))
    if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']:
        AG.edge[Link[0]][Link[1]]['Scheduling'][Edge].append([StartTime, EndTime, batch, Prob])
    else:
        AG.edge[Link[0]][Link[1]]['Scheduling'][Edge] = [[StartTime, EndTime, batch, Prob]]
    return True

##########################################################################
#
#                   CALCULATING SCHEDULING STARTING TIME
#
#
##########################################################################


def FindTask_ASAP_Scheduling(TG, AG, SHM, Task, Node, logging):
    CriticalityLevel = TG.node[Task]['Criticality']
    StartTime = max(FindLastAllocatedTimeOnNode(TG, AG, Node, logging),
                    FindTaskPredecessorsFinishTime(TG, AG, Task, CriticalityLevel),
                    TG.node[Task]['Release'])
    # This includes the aging and lower frequency of the nodes of graph...
    # however, we do not include fractions of a cycle so we take ceiling of the execution time
    NodeSpeedDown = 1+((100.0-SHM.SHM.node[Node]['NodeSpeed'])/100)
    TaskExecutionOnNode = ceil(TG.node[Task]['WCET']*NodeSpeedDown)
    if TG.node[Task]['Criticality'] == 'H':
        EndTime = StartTime+TaskExecutionOnNode + Config.Task_SlackCount*TaskExecutionOnNode
    else:
        EndTime = StartTime+TaskExecutionOnNode
    return StartTime, EndTime
################################################################


def FindEdge_ASAP_Scheduling(TG, AG, Edge, Link, batch, Prob, Report, logging):
    StartTime = max(FindLastAllocatedTimeOnLinkForTask(TG, AG, Link, Edge, Prob, logging),
                    FindEdgePredecessorsFinishTime(TG, AG, Edge, batch, Link))
    EdgeExecutionOnLink = TG.edge[Edge[0]][Edge[1]]['ComWeight']
    if TG.edge[Edge[0]][Edge[1]]['Criticality'] == 'H':
        EndTime = StartTime+EdgeExecutionOnLink+Config.Communication_SlackCount*EdgeExecutionOnLink
    else:
        EndTime = StartTime+EdgeExecutionOnLink
    return StartTime, EndTime


def FindTask_ALAP_Scheduling(TG, AG, Task, Node, Report):
    # todo: Implement ALAP
    return None


def FindEdge_ALAP_Scheduling(TG, AG, Edge, Link, batch, Prob, Report, logging):
    # todo: Implement ALAP
    return None


##########################################################################
#
#                   CALCULATING LATEST STARTING TIME
#                           FOR TASK BASED ON
#                               PREDECESSORS
##########################################################################
def FindTaskPredecessorsFinishTime(TG, AG, Task, CriticalityLevel):
    FinishTime = 0
    if len(TG.predecessors(Task)) > 0:
        for Predecessor in TG.predecessors(Task):
            if TG.node[Predecessor]['Node'] is not None:    # predecessor is mapped
                # if TG.node[Predecessor]['Criticality'] == CriticalityLevel: #this is not quit right...
                    Node = TG.node[Predecessor]['Node']
                    if Predecessor in AG.node[Node]['Scheduling']:             # if this task is scheduled
                        FinishTime = max(AG.node[Node]['Scheduling'][Predecessor][1], FinishTime)
    for Edge in TG.edges():
        if Edge[1] == Task:
            # if TG.edge[Edge[0]][Edge[1]]['Criticality'] == CriticalityLevel:
                if len(TG.edge[Edge[0]][Edge[1]]['Link']) > 0:    # if the edge is mapped
                    # TG.edge[Edge[0]][Edge[1]]['Link'] is a list of tuples of (batch, Link)
                    for BatchAndLink in TG.edge[Edge[0]][Edge[1]]['Link']:     # for each link that this edge goes through
                        Link = BatchAndLink[1]
                        if len(AG.edge[Link[0]][Link[1]]['Scheduling']) > 0:
                            if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']:     # if this edge is scheduled
                                for ScheduleAndBatch in AG.edge[Link[0]][Link[1]]['Scheduling'][Edge]:
                                    EndTime = ScheduleAndBatch[1]
                                    FinishTime = max(EndTime, FinishTime)
    return FinishTime
################################################################


def FindEdgePredecessorsFinishTime(TG, AG, Edge, batch, CurrentLink):
    FinishTime = 0
    Node = TG.node[Edge[0]]['Node']
    if Edge[0] in AG.node[Node]['Scheduling']:
        if AG.node[Node]['Scheduling'][Edge[0]][1] > FinishTime:
            FinishTime = AG.node[Node]['Scheduling'][Edge[0]][1]

    for Link in AG.edges():
        if Link[1] == CurrentLink[0]:
            # if they are incoming links
            if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']:
                for ScheduleAndBatch in AG.edge[Link[0]][Link[1]]['Scheduling'][Edge]:
                    if ScheduleAndBatch[2] == batch:
                        if ScheduleAndBatch[1] > FinishTime:
                            FinishTime = ScheduleAndBatch[1]

    return FinishTime


##########################################################################
#
#                   CALCULATING LAST ALLOCATED TIME
#                           FOR RESOURCES
#
##########################################################################
def FindLastAllocatedTimeOnLink(TG, AG, Link, logging=None):
    if logging is not None:
        logging.info("\t\tFINDING LAST ALLOCATED TIME ON LINK "+str(Link))
    LastAllocatedTime = 0
    if len(AG.edge[Link[0]][Link[1]]['MappedTasks']) > 0:
        for Task in AG.edge[Link[0]][Link[1]]['MappedTasks'].keys():
            if Task in AG.edge[Link[0]][Link[1]]['Scheduling']:
                for ScheduleAndBatch in AG.edge[Link[0]][Link[1]]['Scheduling'][Task]:
                    StartTime = ScheduleAndBatch[0]
                    EndTime = ScheduleAndBatch[1]
                    if StartTime is not None and EndTime is not None:
                        if logging is not None:
                            logging.info ("\t\t\tTASK STARTS AT: "+str(StartTime)+" AND ENDS AT: "+str(EndTime))
                        LastAllocatedTime = max(LastAllocatedTime, EndTime)
    else:
        if logging is not None:
            logging.info("\t\t\tNO SCHEDULED TASK FOUND")
        return 0
    if logging is not None:
        logging.info ("\t\t\tLAST ALLOCATED TIME:"+str(LastAllocatedTime))
    return LastAllocatedTime


################################################################
def FindLastAllocatedTimeOnLinkForTask(TG, AG, Link, Edge, Prob, logging):
    logging.info("\t-------------------------")
    logging.info("\tFINDING LAST ALLOCATED TIME ON LINK "+str(Link)+"\tFOR EDGE: "+str(Edge)+" WITH PROB: "+str(Prob))
    LastAllocatedTime = 0
    if len(AG.edge[Link[0]][Link[1]]['MappedTasks']) > 0:
        for Task in AG.edge[Link[0]][Link[1]]['MappedTasks'].keys():
            if Task in AG.edge[Link[0]][Link[1]]['Scheduling']:
                for ScheduleAndBatch in AG.edge[Link[0]][Link[1]]['Scheduling'][Task]:
                    StartTime = ScheduleAndBatch[0]
                    EndTime = ScheduleAndBatch[1]
                    TaskProb = ScheduleAndBatch[3]
                    if StartTime is not None and EndTime is not None:
                        logging.info("\t\tTASK "+str(Task)+" STARTS AT: " + str(StartTime) +
                                     "AND ENDS AT: " + str(EndTime) + " PROB: " + str(TaskProb))
                        SumOfProb = 0
                        if Task != Edge:
                            logging.info("\t\tEndTime:"+str(EndTime))
                            logging.info("\t\t\tStart  Stop  Prob          SumProb")
                            for OtherTask in AG.edge[Link[0]][Link[1]]['Scheduling']:
                                for Schedule in AG.edge[Link[0]][Link[1]]['Scheduling'][Task]:
                                    if OtherTask != Edge:
                                        # logging.info("Picked other task: "+str(OtherTask)+" With Schedule: "+str(Schedule))
                                        if Schedule[0] < EndTime <= Schedule[1]:
                                            SumOfProb += Schedule[3]
                                            logging.info("\t\t\t"+str(Schedule[0])+"   "+str(Schedule[1])+"   "
                                                         +str(Schedule[3])+"   "+str(SumOfProb))
                                    if SumOfProb + Prob > 1:
                                        break
                                if SumOfProb + Prob > 1:
                                        break
                            if SumOfProb + Prob > 1:
                                LastAllocatedTime = max(LastAllocatedTime, EndTime)
                                logging.info("\t\tAllocated Time Shifted to:"+str(LastAllocatedTime))
    else:
        logging.info("\t\t\tNO SCHEDULED TASK FOUND")
        return 0
    logging.info("\tLAST ALLOCATED TIME:"+str(LastAllocatedTime))
    return LastAllocatedTime


def FindLastAllocatedTimeOnNode(TG, AG, Node, logging=None):
    if logging is not None:
        logging.info ("\t\tFINDING LAST ALLOCATED TIME ON NODE "+str(Node))
    LastAllocatedTime = 0
    if len(AG.node[Node]['MappedTasks']) > 0:
        if logging is not None:
            logging.info ("\t\t\tMAPPED TASKS ON THE NODE: "+str(AG.node[Node]['MappedTasks']))
        for Task in AG.node[Node]['MappedTasks']:
            if Task in AG.node[Node]['Scheduling']:
                StartTime = AG.node[Node]['Scheduling'][Task][0]
                EndTime = AG.node[Node]['Scheduling'][Task][1]
                if StartTime is not None and EndTime is not None:
                    if logging is not None:
                        logging.info ("\t\t\tTASK STARTS AT: "+str(StartTime)+" AND ENDS AT: "+str(EndTime))
                    if EndTime > LastAllocatedTime:
                        LastAllocatedTime = EndTime
    else:
        if logging is not None:
            logging.info("\t\t\tNO SCHEDULED TASK FOUND")
        return 0
    if logging is not None:
        logging.info("\t\t\tLAST ALLOCATED TIME: "+str(LastAllocatedTime))
    return LastAllocatedTime


def FindFirstEmptySlotForTaskOnNode(TG, AG, Node, Task):
    '''
    Should be used for Test Tasks
    :param TG:
    :param AG:
    :param Node:
    :param Task:
    :return:
    '''
    FirstPossibleMappingTime = None
    WCET = TG.node[Task]['WCET']
    ReleaseTime = TG.node[Task]['Release']
    # ToDo

    return FirstPossibleMappingTime