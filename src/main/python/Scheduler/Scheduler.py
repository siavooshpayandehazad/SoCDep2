# Copyright (C) 2015 Siavoosh Payandeh Azad

from TaskGraphUtilities import TG_Functions
from Scheduling_Functions import FindScheduleMakeSpan
from Scheduling_Functions_Tasks import FindTask_ASAP_Scheduling, FindTestTask_ASAP_Scheduling
from Scheduling_Functions_Edges import FindEdge_ASAP_Scheduling_Link, FindEdge_ASAP_Scheduling_Router, FindTestEdge_ASAP_Scheduling
from Scheduling_Functions_Links import Add_TG_EdgeTo_link
from Scheduling_Functions_Nodes import Add_TG_TaskToNode
from Scheduling_Functions_Routers import Add_TG_EdgeTo_Router

def ScheduleAll(TG, AG, SHM, Report, DetailedReport, logging):
    """

    :param TG:
    :param AG:
    :param SHM: System Health Map
    :param Report:
    :param DetailedReport:
    :param logging:
    :return:
    """
    logging.info("===========================================")
    logging.info("STARTING SCHEDULING PROCESS...")
    ASAP_Scheduling(TG, AG, SHM, Report, logging)
    Makespan = FindScheduleMakeSpan(AG)
    logging.info("SCHEDULING MAKESPAN:"+str(Makespan))
    ALAP_Scheduling(TG, AG, SHM, Makespan, Report, logging)
    logging.info("DONE SCHEDULING...")
    return None


def ASAP_Scheduling(TG, AG, SHM, Report, logging):
    """

    :param TG:
    :param AG:
    :param SHM: System Health Map
    :param Report:
    :param logging:
    :return:
    """
    logging.info("STARTING ASAP SCHEDULING ...")
    MaxDistance = TG_Functions.CalculateMaxDistance(TG) + 1
    for Distance in range(0, MaxDistance):
        for Task in TG.nodes():
            if TG.node[Task]['Type'] == 'App':
                if TG.node[Task]['Distance'] == Distance:
                    Node = TG.node[Task]['Node']
                    logging.info("\tSCHEDULING TASK "+str(Task)+ " ON NODE:"+str(Node))
                    (StartTime, EndTime) = FindTask_ASAP_Scheduling(TG, AG, SHM, Task, Node, logging)
                    Add_TG_TaskToNode(TG, AG, Task, Node, StartTime, EndTime, logging)
                    for Edge in TG.edges():
                        if Edge[0] == Task:
                            DestinationNode = TG.node[Edge[1]]['Node']
                            if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                for BatchAndLink in TG.edge[Edge[0]][Edge[1]]['Link']:
                                    Batch = BatchAndLink[0]
                                    Link = BatchAndLink[1]
                                    Probability = BatchAndLink[2]
                                    logging.info("\tSCHEDULING EDGE "+str(Edge)+" ON Router: "+str(Link)+
                                                 " FROM BATCH: "+str(Batch))
                                    (StartTime, EndTime) = FindEdge_ASAP_Scheduling_Router(TG, AG, Edge, Link[0], Batch,
                                                                                           Probability, Report, logging)
                                    Add_TG_EdgeTo_Router(TG, AG, Edge, Link[0], Batch, Probability, StartTime,
                                                         EndTime, logging)
                                    logging.info("\tSCHEDULING EDGE "+str(Edge)+" ON LINK: "+str(Link)+
                                                 " FROM BATCH: "+str(Batch))
                                    (StartTime, EndTime) = FindEdge_ASAP_Scheduling_Link(TG, AG, Edge, Link, Batch,
                                                                                         Probability, Report, logging)
                                    Add_TG_EdgeTo_link(TG, AG, Edge, Link, Batch, Probability, StartTime, EndTime,
                                                       logging)

                                    if DestinationNode == Link[1]:
                                        logging.info("\tSCHEDULING EDGE "+str(Edge)+" ON Router: "+str(Link)+
                                                     " FROM BATCH: "+str(Batch))
                                        (StartTime, EndTime) = FindEdge_ASAP_Scheduling_Router(TG, AG, Edge, Link[1], Batch,
                                                                                               Probability, Report, logging)
                                        Add_TG_EdgeTo_Router(TG, AG, Edge, Link[1], Batch, Probability, StartTime,
                                                             EndTime, logging)

    logging.info("DONE ASAP SCHEDULING...")
    return None


def ALAP_Scheduling(TG, AG, SHM, Makespan, Report, logging):

    return None


def ScheduleTestInTG(TG, AG, SHM, Report, logging):
    """

    :param TG:
    :param AG:
    :param SHM: System Health Map
    :param Report:
    :param logging:
    :return:
    """
    logging.info("===========================================")
    logging.info("STARTING SCHEDULING TEST TASKS IN TG...")
    for Distance in range(0, 2):
        for Task in TG.nodes():
            if TG.node[Task]['Type'] == 'Test':
                if TG.node[Task]['Distance'] == Distance:
                    Node = TG.node[Task]['Node']
                    logging.info("\tSCHEDULING TASK "+str(Task)+ " ON NODE:"+str(Node))
                    (StartTime, EndTime) = FindTestTask_ASAP_Scheduling(TG, AG, SHM, Task, Node, logging)
                    Add_TG_TaskToNode(TG, AG, Task, Node, StartTime, EndTime, logging)
                    for Edge in TG.edges():
                        DestinationNode = TG.node[Edge[1]]['Node']
                        if Edge[0] == Task:
                            if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                for BatchAndLink in TG.edge[Edge[0]][Edge[1]]['Link']:
                                    Link = BatchAndLink[1]
                                    Batch = BatchAndLink[0]
                                    Probability = BatchAndLink[2]
                                    logging.info("\tSCHEDULING EDGE "+str(Edge)+" ON Router: "+str(Link)+
                                                 " FROM BATCH: "+str(Batch))
                                    (StartTime, EndTime) = FindEdge_ASAP_Scheduling_Router(TG, AG, Edge, Link[0], Batch,
                                                                                           Probability, Report, logging)
                                    Add_TG_EdgeTo_Router(TG, AG, Edge, Link[0], Batch, Probability, StartTime,
                                                         EndTime, logging)
                                    logging.info("\tSCHEDULING EDGE "+str(Edge)+" ON LINK: "+str(Link)+
                                                 " FROM BATCH: "+str(Batch))
                                    (StartTime, EndTime) = FindTestEdge_ASAP_Scheduling(TG, AG, Edge, Link, Batch,
                                                                                  Probability, Report, logging)
                                    Add_TG_EdgeTo_link(TG, AG, Edge, Link, Batch, Probability, StartTime, EndTime,
                                                       logging)
                                    if DestinationNode == Link[1]:
                                        logging.info("\tSCHEDULING EDGE "+str(Edge)+" ON Router: "+str(Link)+
                                                     " FROM BATCH: "+str(Batch))
                                        (StartTime, EndTime) = FindEdge_ASAP_Scheduling_Router(TG, AG, Edge, Link[1], Batch,
                                                                                               Probability, Report, logging)
                                        Add_TG_EdgeTo_Router(TG, AG, Edge, Link[1], Batch, Probability, StartTime,
                                                             EndTime, logging)
    logging.info("DONE SCHEDULING...")
    return None