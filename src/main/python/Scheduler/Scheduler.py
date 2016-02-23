# Copyright (C) 2015 Siavoosh Payandeh Azad

from TaskGraphUtilities import TG_Functions
from Scheduling_Functions import find_schedule_make_span
from Scheduling_Functions_Tasks import find_task_asap_scheduling, find_test_task_asap_scheduling
from Scheduling_Functions_Edges import FindEdge_ASAP_Scheduling_Link, FindEdge_ASAP_Scheduling_Router
from Scheduling_Functions_Edges import FindTestEdge_ASAP_Scheduling
from Scheduling_Functions_Links import Add_TG_EdgeTo_link
from Scheduling_Functions_Nodes import Add_TG_TaskToNode
from Scheduling_Functions_Routers import Add_TG_EdgeTo_Router


def schedule_all(tg, ag, shm, report, detailed_report, logging):
    """

    :param tg: Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param report: report Switch
    :param detailed_report: Detailed report Switch
    :param logging: Logging file
    :return: None
    """
    logging.info("===========================================")
    logging.info("STARTING SCHEDULING PROCESS...")
    asap_scheduling(tg, ag, shm, report, logging=None)
    makespan = find_schedule_make_span(ag)
    logging.info("SCHEDULING MAKESPAN:"+str(makespan))
    alap_scheduling(tg, ag, shm, makespan, report, logging=None)
    logging.info("DONE SCHEDULING...")
    return None


def asap_scheduling(tg, ag, shm, report, logging=None):
    """

    :param tg:  Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param report: report Switch
    :param logging: logging file
    :return: None
    """
    if logging is not None:
        logging.info("STARTING ASAP SCHEDULING ...")
    max_distance = TG_Functions.calculate_max_distance(tg) + 1
    for distance in range(0, max_distance):
        for task in tg.nodes():
            if tg.node[task]['Type'] == 'App':
                if tg.node[task]['Distance'] == distance:
                    node = tg.node[task]['Node']
                    # logging.info("\tSCHEDULING TASK "+str(task)+" ON NODE:"+str(node))
                    (start_time, end_time) = find_task_asap_scheduling(tg, ag, shm, task, node, logging)
                    Add_TG_TaskToNode(tg, ag, task, node, start_time, end_time, logging)
                    for edge in tg.edges():
                        if edge[0] == task:
                            destination_node = tg.node[edge[1]]['Node']
                            if len(tg.edge[edge[0]][edge[1]]['Link']) > 0:
                                for batch_and_link in tg.edge[edge[0]][edge[1]]['Link']:
                                    batch = batch_and_link[0]
                                    link = batch_and_link[1]
                                    probability = batch_and_link[2]
                                    # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON Router: "+str(link) +
                                    #             " FROM BATCH: "+str(batch))
                                    (start_time, end_time) = FindEdge_ASAP_Scheduling_Router(tg, ag, edge, link[0],
                                                                                             batch, probability,
                                                                                             report, logging)
                                    Add_TG_EdgeTo_Router(tg, ag, edge, link[0], batch, probability, start_time,
                                                         end_time, logging)
                                    # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON LINK: "+str(link) +
                                    #             " FROM BATCH: "+str(batch))
                                    (start_time, end_time) = FindEdge_ASAP_Scheduling_Link(tg, ag, edge, link, batch,
                                                                                           probability, report,
                                                                                           logging)
                                    Add_TG_EdgeTo_link(tg, ag, edge, link, batch, probability, start_time, end_time,
                                                       logging)

                                    if destination_node == link[1]:
                                        # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON Router: "+str(link) +
                                        #             " FROM BATCH: "+str(batch))
                                        (start_time, end_time) = FindEdge_ASAP_Scheduling_Router(tg, ag, edge, link[1],
                                                                                                 batch, probability,
                                                                                                 report, logging)
                                        Add_TG_EdgeTo_Router(tg, ag, edge, link[1], batch, probability, start_time,
                                                             end_time, logging)
    if logging is not None:
        logging.info("DONE ASAP SCHEDULING...")
    return None


def alap_scheduling(tg, ag, shm, makespan, report, logging=None):
    """

    :param tg:  Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param makespan: Make span of Scheduling
    :param report: report switch
    :param logging: logging File
    :return: None
    """
    if logging is not None:
        logging.info("STARTING ALAP SCHEDULING ...")

    if logging is not None:
        logging.info("DONE ALAP SCHEDULING...")
    return None


def schedule_test_in_tg(tg, ag, shm, report, logging):
    """

    :param tg: Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param report: report Switch
    :param logging: logging File
    :return: None
    """
    logging.info("===========================================")
    logging.info("STARTING SCHEDULING TEST TASKS IN TG...")
    for distance in range(0, 2):
        for Task in tg.nodes():
            if tg.node[Task]['Type'] == 'Test':
                if tg.node[Task]['Distance'] == distance:
                    node = tg.node[Task]['Node']
                    # logging.info("\tSCHEDULING TASK "+str(Task)+" ON NODE:"+str(node))
                    (start_time, end_time) = find_test_task_asap_scheduling(tg, ag, shm, Task, node, logging)
                    Add_TG_TaskToNode(tg, ag, Task, node, start_time, end_time, logging)
                    for edge in tg.edges():
                        destination_node = tg.node[edge[1]]['Node']
                        if edge[0] == Task:
                            if len(tg.edge[edge[0]][edge[1]]['Link']) > 0:
                                for batch_and_link in tg.edge[edge[0]][edge[1]]['Link']:
                                    link = batch_and_link[1]
                                    batch = batch_and_link[0]
                                    probability = batch_and_link[2]
                                    # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON Router: "+str(link) +
                                    #             " FROM BATCH: "+str(batch))
                                    (start_time, end_time) = FindEdge_ASAP_Scheduling_Router(tg, ag, edge, link[0],
                                                                                             batch, probability,
                                                                                             report, logging)
                                    Add_TG_EdgeTo_Router(tg, ag, edge, link[0], batch, probability, start_time,
                                                         end_time, logging)
                                    # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON LINK: "+str(link) +
                                    #             " FROM BATCH: "+str(batch))
                                    (start_time, end_time) = FindTestEdge_ASAP_Scheduling(tg, ag, edge, link, batch,
                                                                                          probability, report, logging)
                                    Add_TG_EdgeTo_link(tg, ag, edge, link, batch, probability, start_time, end_time,
                                                       logging)
                                    if destination_node == link[1]:
                                        # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON Router: "+str(link) +
                                        #              " FROM BATCH: "+str(batch))
                                        (start_time, end_time) = FindEdge_ASAP_Scheduling_Router(tg, ag, edge, link[1],
                                                                                                 batch, probability,
                                                                                                 report, logging)
                                        Add_TG_EdgeTo_Router(tg, ag, edge, link[1], batch, probability, start_time,
                                                             end_time, logging)
    logging.info("DONE SCHEDULING...")
    return None
