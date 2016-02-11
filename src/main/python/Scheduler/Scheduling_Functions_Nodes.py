# Copyright (C) 2015 Siavoosh Payandeh Azad

from math import ceil
import Scheduling_Functions_Tasks

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
    # logging.info ("\t\tADDING TASK: "+str(Task)+" TO NODE: "+str(Node))
    # logging.info ("\t\tSTARTING TIME: "+str(StartTime)+" ENDING TIME:"+str(EndTime))
    AG.node[Node]['PE'].Scheduling[Task] = [StartTime, EndTime]
    TG.node[Task]['Node'] = Node
    return True


def FindLastAllocatedTimeOnNode(TG, AG, Node, logging=None):
    if logging is not None:
        logging.info ("\t\tFINDING LAST ALLOCATED TIME ON NODE "+str(Node))
    LastAllocatedTime = 0
    if len(AG.node[Node]['PE'].MappedTasks) > 0:
        if logging is not None:
            logging.info ("\t\t\tMAPPED TASKS ON THE NODE: "+str(AG.node[Node]['PE'].MappedTasks))
        for Task in AG.node[Node]['PE'].MappedTasks:
            if Task in AG.node[Node]['PE'].Scheduling:
                StartTime = AG.node[Node]['PE'].Scheduling[Task][0]
                EndTime = AG.node[Node]['PE'].Scheduling[Task][1]
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


def FindFirstEmptySlotForTaskOnNode(TG, AG, SHM, Node, Task, PredecessorEndTime, logging):
    """

    :param TG:
    :param AG:
    :param SHM: System Health Map
    :param Node:
    :param Task:
    :param PredecessorEndTime:
    :param logging:
    :return:
    """

    FirstPossibleMappingTime = PredecessorEndTime

    NodeSpeedDown = 1+((100.0-SHM.node[Node]['NodeSpeed'])/100)
    TaskExecutionOnNode = ceil(TG.node[Task]['WCET']*NodeSpeedDown)

    StartTimeList = []
    EndTimeList = []
    for Task in AG.node[Node]['PE'].Scheduling.keys():
        StartTimeList.append(AG.node[Node]['PE'].Scheduling[Task][0])
        EndTimeList.append(AG.node[Node]['PE'].Scheduling[Task][1])
    StartTimeList.sort()
    EndTimeList.sort()
    Found = False
    for i in range(0, len(StartTimeList)-1):
        if EndTimeList[i]>= PredecessorEndTime:
            Slot = StartTimeList[i+1]-EndTimeList[i]
            if Slot >= TaskExecutionOnNode:
                FirstPossibleMappingTime = EndTimeList[i]
                Found = True
                break
    if Found == False:
        FirstPossibleMappingTime = max(FirstPossibleMappingTime,
                                       Scheduling_Functions_Tasks.find_task_asap_scheduling(TG, AG, SHM,
                                                                                            Task, Node, logging)[0])
    return FirstPossibleMappingTime