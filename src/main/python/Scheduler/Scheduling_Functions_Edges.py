# Copyright (C) 2015 Siavoosh Payandeh Azad

import Scheduling_Functions_Links
import Scheduling_Functions_Routers
from ConfigAndPackages import Config


def find_edge_asap_scheduling_link(tg, ag, edge, link, batch, prob, report, logging=None):
    """
    Finds the earliest start and finish time for scheduling Edge from TG on Link from AG.
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param edge: Edge ID in TG to be scheduled on Link
    :param link: Link ID in AG for scheduling Edge on it
    :param batch: Edge's Batch
    :param prob: probability of Edge to actually going through Link
    :param report: Report Switch
    :param logging: logging File
    :return: Start Time and Stop Time
    """
    if report:
        print "Finding Edge", edge, " ASAP Scheduling on Link:", link
    start_time = max(Scheduling_Functions_Links.find_last_allocated_time_on_link_for_task(ag, link, edge,
                                                                                          prob, logging),
                     find_edge_predecessors_finish_time(tg, ag, edge, batch))
    edge_execution_on_link = tg.edge[edge[0]][edge[1]]['ComWeight']
    if tg.edge[edge[0]][edge[1]]['Criticality'] == 'H':
        end_time = start_time+edge_execution_on_link+Config.Communication_SlackCount*edge_execution_on_link
    else:
        end_time = start_time+edge_execution_on_link
    if report:
        print "Start time:", start_time, "End Time:", end_time
    return start_time, end_time


def find_edge_asap_scheduling_router(tg, ag, edge, node, batch, prob, report, logging=None):
    """
    Calculates the start time and end time for ASAP scheduling of an Edge on a Router
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param edge: Edge in TG to be mapped
    :param node: Node ID number for mapping Edge on its Router
    :param batch: Batch of the mapped Edge
    :param prob: Probability of Edge actually going through router
    :param report: Report Switch
    :param logging: logging File
    :return: Start Time and End time
    """
    if report:
        print "Finding Edge", edge, " ASAP Scheduling on router:", node
    start_time = max(Scheduling_Functions_Routers.find_last_allocated_time_on_router_for_task(ag, node, edge,
                                                                                              prob, logging),
                     find_edge_predecessors_finish_time(tg, ag, edge, batch))
    edge_execution_on_link = tg.edge[edge[0]][edge[1]]['ComWeight']
    if tg.edge[edge[0]][edge[1]]['Criticality'] == 'H':
        end_time = start_time+edge_execution_on_link+Config.Communication_SlackCount*edge_execution_on_link
    else:
        end_time = start_time+edge_execution_on_link
    if report:
        print "Start time:", start_time, "End Time:", end_time
    return start_time, end_time


def find_test_edge_asap_scheduling(tg, ag, edge, link, batch, prob, report, logging=None):
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
    if report:
        print "Finding Test Edge", edge, " ASAP Scheduling"
    start_time = max(Scheduling_Functions_Links.find_last_allocated_time_on_link_for_task(ag, link, edge,
                                                                                          prob, logging),
                     find_edge_predecessors_finish_time(tg, ag, edge, batch))
    edge_execution_on_link = tg.edge[edge[0]][edge[1]]['ComWeight']
    end_time = start_time+edge_execution_on_link
    if report:
        print "Start time:", start_time, "End Time:", end_time
    return start_time, end_time


def find_edge_alap_scheduling():
    # todo: Implement ALAP
    return None


def find_edge_predecessors_finish_time(tg, ag, edge, batch):
    """
    Finds and returns the maximum of predecessors of Edge's scheduled finish time
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param edge: Edge ID of task to be scheduled
    :param batch: Edge's Batch
    :return: Finish Time
    """
    finish_time = 0
    source_node = tg.node[edge[0]]['task'].node
    if edge[0] in ag.node[source_node]['PE'].scheduling:
        finish_time = max(ag.node[source_node]['PE'].scheduling[edge[0]][1], finish_time)

    for link in ag.edges():
            # if they are incoming links
            if edge in ag.edge[link[0]][link[1]]['Scheduling']:
                for ScheduleAndBatch in ag.edge[link[0]][link[1]]['Scheduling'][edge]:
                    if ScheduleAndBatch[2] == batch:
                        if ScheduleAndBatch[1] > finish_time:
                            if Config.FlowControl == "Wormhole":
                                finish_time = max(ScheduleAndBatch[0]+1, finish_time)
                            elif Config.FlowControl == "StoreAndForward":
                                finish_time = max(ScheduleAndBatch[1], finish_time)
                            else:
                                raise ValueError("FlowControl is not supported")

    for Node in ag.nodes():
        if edge in ag.node[Node]['Router'].scheduling:
            for ScheduleAndBatch in ag.node[Node]['Router'].scheduling[edge]:
                if ScheduleAndBatch[2] == batch:
                    if ScheduleAndBatch[1] > finish_time:
                        if Config.FlowControl == "Wormhole":
                            finish_time = max(ScheduleAndBatch[0]+1, finish_time)
                        elif Config.FlowControl == "StoreAndForward":
                            finish_time = max(ScheduleAndBatch[1], finish_time)
                        else:
                            raise ValueError("FlowControl is not supported")
    return finish_time
