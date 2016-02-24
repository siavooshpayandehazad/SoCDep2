# Copyright (C) 2015 Siavoosh Payandeh Azad

import Scheduling_Functions_Nodes
from math import ceil
from ConfigAndPackages import Config


def find_task_asap_scheduling(tg, ag, shm, task, node, logging=None):
    """

    :param tg:
    :param ag:
    :param shm: System Health Map
    :param task:
    :param node:
    :param logging: logging file
    :return:
    """
    start_time = max(Scheduling_Functions_Nodes.find_last_allocated_time_on_node(ag, node, logging),
                     task_predecessors_finish_time(tg, ag, task),
                     tg.node[task]['Release'])
    # This includes the aging and lower frequency of the nodes of graph...
    # however, we do not include fractions of a cycle so we take ceiling of the execution time
    node_speed_down = 1+((100.0-shm.node[node]['NodeSpeed'])/100)
    task_execution_on_node = ceil(tg.node[task]['WCET']*node_speed_down)
    if tg.node[task]['Criticality'] == 'H':
        end_time = start_time+task_execution_on_node + Config.Task_SlackCount*task_execution_on_node
    else:
        end_time = start_time+task_execution_on_node
    return start_time, end_time


def find_test_task_asap_scheduling(tg, ag, shm, task, node, logging=None):
    """

    :param tg:
    :param ag:
    :param shm:  System Health Map
    :param task:
    :param node:
    :param logging:
    :return:
    """
    predecessor_finish_time = task_predecessors_finish_time(tg, ag, task)
    start_time = Scheduling_Functions_Nodes.find_first_empty_slot_for_task_on_node(tg, ag, shm, node, task,
                                                                                   predecessor_finish_time, logging)

    # This includes the aging and lower frequency of the nodes of graph...
    # however, we do not include fractions of a cycle so we take ceiling of the execution time
    node_speed_down = 1+((100.0-shm.node[node]['NodeSpeed'])/100)
    task_execution_on_node = ceil(tg.node[task]['WCET']*node_speed_down)
    end_time = start_time+task_execution_on_node
    return start_time, end_time


def find_task_alap_scheduling():
    # todo: Implement ALAP
    return None


def task_predecessors_finish_time(tg, ag, task):
    finish_time = 0
    if len(tg.predecessors(task)) > 0:
        for Predecessor in tg.predecessors(task):
            if tg.node[Predecessor]['Node'] is not None:    # predecessor is mapped
                    node = tg.node[Predecessor]['Node']
                    if Predecessor in ag.node[node]['PE'].scheduling:             # if this task is scheduled
                        finish_time = max(ag.node[node]['PE'].scheduling[Predecessor][1], finish_time)
    current_node = tg.node[task]['Node']
    for Edge in tg.edges():
        if Edge[1] == task:
            if Edge in ag.node[current_node]['Router'].scheduling:
                for ScheduleAndBatch in ag.node[current_node]['Router'].scheduling[Edge]:
                    finish_time = max(ScheduleAndBatch[1], finish_time)
    return finish_time
