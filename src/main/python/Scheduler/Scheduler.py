# Copyright (C) 2015 Siavoosh Payandeh Azad

from TaskGraphUtilities import TG_Functions
from Scheduling_Functions import find_schedule_make_span
from Scheduling_Functions_Tasks import find_task_asap_scheduling, find_test_task_asap_scheduling
from Scheduling_Functions_Edges import find_edge_asap_scheduling_link, find_edge_asap_scheduling_router
from Scheduling_Functions_Edges import find_test_edge_asap_scheduling
from Scheduling_Functions_Links import add_tg_edge_to_link
from Scheduling_Functions_Nodes import add_tg_task_to_node
from Scheduling_Functions_Routers import add_tg_edge_to_router


def schedule_all(tg, ag, shm, report, logging):
    """

    :param tg: Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param report: report Switch
    :param logging: Logging file
    :return: None
    """
    logging.info("===========================================")
    logging.info("STARTING SCHEDULING PROCESS...")
    asap_scheduling(tg, ag, shm, report, logging=None)
    makespan = find_schedule_make_span(ag)
    logging.info("SCHEDULING MAKESPAN:"+str(makespan))
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
            if tg.node[task]['task'].type == 'App':
                if tg.node[task]['task'].distance == distance:
                    node = tg.node[task]['task'].node
                    # logging.info("\tSCHEDULING TASK "+str(task)+" ON NODE:"+str(node))
                    (start_time, end_time) = find_task_asap_scheduling(tg, ag, shm, task, node, logging)
                    add_tg_task_to_node(tg, ag, task, node, start_time, end_time, None)
                    for edge in tg.edges():
                        if edge[0] == task:
                            destination_node = tg.node[edge[1]]['task'].node
                            if len(tg.edge[edge[0]][edge[1]]['Link']) > 0:
                                for batch_and_link in tg.edge[edge[0]][edge[1]]['Link']:
                                    batch = batch_and_link[0]
                                    link = batch_and_link[1]
                                    probability = batch_and_link[2]
                                    # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON Router: "+str(link) +
                                    #             " FROM BATCH: "+str(batch))
                                    (start_time, end_time) = find_edge_asap_scheduling_router(tg, ag, edge, link[0],
                                                                                              batch, probability,
                                                                                              report, logging)
                                    add_tg_edge_to_router(ag, edge, link[0], batch, probability, start_time,
                                                          end_time, logging)
                                    # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON LINK: "+str(link) +
                                    #             " FROM BATCH: "+str(batch))
                                    (start_time, end_time) = find_edge_asap_scheduling_link(tg, ag, edge, link, batch,
                                                                                            probability, report,
                                                                                            logging)
                                    add_tg_edge_to_link(ag, edge, link, batch, probability, start_time, end_time,
                                                        logging)

                                    if destination_node == link[1]:
                                        # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON Router: "+str(link) +
                                        #             " FROM BATCH: "+str(batch))
                                        (start_time, end_time) = find_edge_asap_scheduling_router(tg, ag, edge, link[1],
                                                                                                  batch, probability,
                                                                                                  report, logging)
                                        add_tg_edge_to_router(ag, edge, link[1], batch, probability, start_time,
                                                              end_time, logging)
    if logging is not None:
        logging.info("DONE ASAP SCHEDULING...")
    return None


def alap_scheduling(logging=None):
    """

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
    Schedules the Test tasks
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
            if tg.node[Task]['task'].type == 'Test':
                if tg.node[Task]['task'].distance == distance:
                    node = tg.node[Task]['task'].node
                    # logging.info("\tSCHEDULING TASK "+str(Task)+" ON NODE:"+str(node))
                    (start_time, end_time) = find_test_task_asap_scheduling(tg, ag, shm, Task, node, logging)
                    add_tg_task_to_node(tg, ag, Task, node, start_time, end_time, None)
                    for edge in tg.edges():
                        destination_node = tg.node[edge[1]]['task'].node
                        if edge[0] == Task:
                            if len(tg.edge[edge[0]][edge[1]]['Link']) > 0:
                                for batch_and_link in tg.edge[edge[0]][edge[1]]['Link']:
                                    link = batch_and_link[1]
                                    batch = batch_and_link[0]
                                    probability = batch_and_link[2]
                                    # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON Router: "+str(link) +
                                    #             " FROM BATCH: "+str(batch))
                                    (start_time, end_time) = find_edge_asap_scheduling_router(tg, ag, edge, link[0],
                                                                                              batch, probability,
                                                                                              report, logging)
                                    add_tg_edge_to_router(ag, edge, link[0], batch, probability, start_time,
                                                          end_time, logging)
                                    # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON LINK: "+str(link) +
                                    #             " FROM BATCH: "+str(batch))
                                    (start_time, end_time) = find_test_edge_asap_scheduling(tg, ag, edge, link, batch,
                                                                                            probability, report,
                                                                                            logging)
                                    add_tg_edge_to_link(ag, edge, link, batch, probability, start_time, end_time,
                                                        logging)
                                    if destination_node == link[1]:
                                        # logging.info("\tSCHEDULING EDGE "+str(edge)+" ON Router: "+str(link) +
                                        #              " FROM BATCH: "+str(batch))
                                        (start_time, end_time) = find_edge_asap_scheduling_router(tg, ag, edge, link[1],
                                                                                                  batch, probability,
                                                                                                  report, logging)
                                        add_tg_edge_to_router(ag, edge, link[1], batch, probability, start_time,
                                                              end_time, logging)
    logging.info("DONE SCHEDULING...")
    return None
