# Copyright (C) 2015 Siavoosh Payandeh Azad

import Scheduling_Functions_Nodes
from math import ceil
from ConfigAndPackages import Config


def find_task_asap_scheduling(tg, ag, shm, task, node, logging):
    """

    :param tg:
    :param ag:
    :param shm: System Health Map
    :param task:
    :param node:
    :param logging:
    :return:
    """
    criticality_level = tg.node[task]['Criticality']
    start_time = max(Scheduling_Functions_Nodes.FindLastAllocatedTimeOnNode(tg, ag, node, logging),
                     task_predecessors_finish_time(tg, ag, task, criticality_level),
                     tg.node[task]['Release'])
    # This includes the aging and lower frequency of the nodes of graph...
    # however, we do not include fractions of a cycle so we take ceiling of the execution time
    node_speed_down = 1+((100.0-shm.node[node]['NodeSpeed'])/100)
    task_execution_on_node = ceil(tg.node[task]['WCET']*node_speed_down)
    if tg.node[task]['Criticality'] == 'H':
        end_time = start_time+task_execution_on_node + Config.task_SlackCount*task_execution_on_node
    else:
        end_time = start_time+task_execution_on_node
    return start_time, end_time


def find_test_task_asap_scheduling(tg, ag, shm, task, node, logging):
    """

    :param tg:
    :param ag:
    :param shm:  System Health Map
    :param task:
    :param node:
    :param logging:
    :return:
    """
    criticality_level = tg.node[task]['Criticality']
    predecessor_finish_time = task_predecessors_finish_time(tg, ag, task, criticality_level)
    start_time = Scheduling_Functions_Nodes.FindFirstEmptySlotForTaskOnNode(tg, ag, shm, node, task,
                                                                            predecessor_finish_time, logging)

    # This includes the aging and lower frequency of the nodes of graph...
    # however, we do not include fractions of a cycle so we take ceiling of the execution time
    node_speed_down = 1+((100.0-shm.node[node]['NodeSpeed'])/100)
    task_execution_on_node = ceil(tg.node[task]['WCET']*node_speed_down)
    end_time = start_time+task_execution_on_node
    return start_time, end_time


def find_task_alap_scheduling(tg, ag, task, node, logging):
    # todo: Implement ALAP
    return None


def task_predecessors_finish_time(tg, ag, task, criticality_level):
    finish_time = 0
    if len(tg.predecessors(task)) > 0:
        for Predecessor in tg.predecessors(task):
            if tg.node[Predecessor]['Node'] is not None:    # predecessor is mapped
                # if tg.node[Predecessor]['Criticality'] == criticality_level: #this is not quit right...
                    Node = tg.node[Predecessor]['Node']
                    if Predecessor in ag.node[Node]['PE'].Scheduling:             # if this task is scheduled
                        finish_time = max(ag.node[Node]['PE'].Scheduling[Predecessor][1], finish_time)
    # for Edge in tg.edges():
    #    if Edge[1] == task:
    #        # if tg.edge[Edge[0]][Edge[1]]['Criticality'] == criticality_level:
    #            if len(tg.edge[Edge[0]][Edge[1]]['Link']) > 0:    # if the edge is mapped
    #                # tg.edge[Edge[0]][Edge[1]]['Link'] is a list of tuples of (batch, Link)
    #                # for each link that this edge goes through
    #                for BatchAndLink in tg.edge[Edge[0]][Edge[1]]['Link']:
    #                    Link = BatchAndLink[1]
    #                    if len(ag.edge[Link[0]][Link[1]]['Scheduling']) > 0:
    #                        if Edge in ag.edge[Link[0]][Link[1]]['Scheduling']:     # if this edge is scheduled
    #                            for ScheduleAndBatch in ag.edge[Link[0]][Link[1]]['Scheduling'][Edge]:
    #                                end_time = ScheduleAndBatch[1]
    #                                finish_time = max(end_time, finish_time)
    current_node = tg.node[task]['Node']
    for Edge in tg.edges():
        if Edge[1] == task:
            if Edge in ag.node[current_node]['Router'].Scheduling:
                for ScheduleAndBatch in ag.node[current_node]['Router'].Scheduling[Edge]:
                    finish_time = max(ScheduleAndBatch[1], finish_time)
    return finish_time