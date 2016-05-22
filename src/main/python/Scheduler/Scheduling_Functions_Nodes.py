# Copyright (C) 2015 Siavoosh Payandeh Azad

from math import ceil
import Scheduling_Functions_Tasks


def add_tg_task_to_node(tg, ag, task_id, node, start_time, end_time, logging=None):
    """
    Adds a Task from Task Graph with specific Start time and end time to mapped node in architecture graph
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param task_id: Task ID
    :param node: Node ID
    :param start_time: Scheduling time for Task
    :param end_time: Task duration for scheduling
    :param logging: logging file
    :return: True
    """
    if logging is not None:
        logging.info("\t\tADDING TASK: "+str(task_id)+" TO NODE: "+str(node))
        logging.info("\t\tSTARTING TIME: "+str(start_time)+" ENDING TIME:"+str(end_time))
    ag.node[node]['PE'].scheduling[task_id] = [start_time, end_time]
    tg.node[task_id]['task'].node = node
    return True


def find_last_allocated_time_on_node(ag, node, logging=None):
    if logging is not None:
        logging.info("\t\tFINDING LAST ALLOCATED TIME ON NODE "+str(node))
    last_allocated_time = 0
    if len(ag.node[node]['PE'].mapped_tasks) > 0:
        if logging is not None:
            logging.info("\t\t\tMAPPED TASKS ON THE NODE: "+str(ag.node[node]['PE'].mapped_tasks))
        for Task in ag.node[node]['PE'].mapped_tasks:
            if Task in ag.node[node]['PE'].scheduling:
                start_time = ag.node[node]['PE'].scheduling[Task][0]
                end_time = ag.node[node]['PE'].scheduling[Task][1]
                if start_time is not None and end_time is not None:
                    if logging is not None:
                        logging.info("\t\t\tTASK STARTS AT: "+str(start_time)+" AND ENDS AT: "+str(end_time))
                    if end_time > last_allocated_time:
                        last_allocated_time = end_time
    else:
        if logging is not None:
            logging.info("\t\t\tNO SCHEDULED TASK FOUND")
        return 0
    if logging is not None:
        logging.info("\t\t\tLAST ALLOCATED TIME: "+str(last_allocated_time))
    return last_allocated_time


def find_first_empty_slot_for_task_on_node(tg, ag, shm, node, task_id, predecessor_end_time, logging=None):
    """

    :param tg: task graph
    :param ag:
    :param shm: System Health Map
    :param node:
    :param task_id: task id
    :param predecessor_end_time:
    :param logging:
    :return:
    """

    first_possible_mapping_time = predecessor_end_time

    node_speed_down = 1+((100.0-shm.node[node]['NodeSpeed'])/100)
    task_execution_on_node = ceil(tg.node[task_id]['task'].wcet*node_speed_down)

    start_time_list = []
    end_time_list = []
    for chosen_task in ag.node[node]['PE'].scheduling.keys():
        start_time_list.append(ag.node[node]['PE'].scheduling[chosen_task][0])
        end_time_list.append(ag.node[node]['PE'].scheduling[chosen_task][1])
    start_time_list.sort()
    end_time_list.sort()
    found = False
    for i in range(0, len(start_time_list)-1):
        if end_time_list[i] >= predecessor_end_time:
            slot = start_time_list[i+1]-end_time_list[i]
            if slot >= task_execution_on_node:
                first_possible_mapping_time = end_time_list[i]
                found = True
                break
    if not found:
        first_possible_mapping_time = max(first_possible_mapping_time,
                                          Scheduling_Functions_Tasks.find_task_asap_scheduling(tg, ag, shm,
                                                                                               task_id, node,
                                                                                               logging)[0])
    return first_possible_mapping_time
