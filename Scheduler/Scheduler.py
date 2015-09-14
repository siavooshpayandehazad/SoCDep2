# Copyright (C) 2015 Siavoosh Payandeh Azad

from TaskGraphUtilities import TG_Functions
from Scheduling_Functions import Add_TG_TaskToNode
from Scheduling_Functions import FindScheduleMakeSpan
from Scheduling_Functions import FindEdge_ASAP_Scheduling, FindTask_ASAP_Scheduling
from Scheduling_Functions import Add_TG_EdgeTo_link


def ScheduleAll(TG, AG, SHM, Report, DetailedReport, logging):
    logging.info("===========================================")
    logging.info("STARTING SCHEDULING PROCESS...")
    ASAP_Scheduling(TG, AG, SHM, Report, logging)
    Makespan = FindScheduleMakeSpan(AG)
    logging.info("SCHEDULING MAKESPAN:"+str(Makespan))
    ALAP_Scheduling(TG, AG, SHM, Makespan, Report, logging)
    logging.info("DONE SCHEDULING...")
    return None


def ASAP_Scheduling(TG, AG, SHM, Report, logging):
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
                            if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                for BatchAndLink in TG.edge[Edge[0]][Edge[1]]['Link']:
                                    Link = BatchAndLink[1]
                                    Batch = BatchAndLink[0]
                                    Probability = BatchAndLink[2]
                                    logging.info("\tSCHEDULING EDGE "+str(Edge)+" ON LINK: "+str(Link)+
                                                 " FROM BATCH: "+str(Batch))
                                    (StartTime, EndTime) = FindEdge_ASAP_Scheduling(TG, AG, Edge, Link, Batch,
                                                                                    Probability, Report, logging)
                                    Add_TG_EdgeTo_link(TG, AG, Edge, Link, Batch, Probability, StartTime, EndTime,
                                                       logging)
    logging.info("DONE ASAP SCHEDULING...")
    return None


def ALAP_Scheduling(TG, AG, SHM, Makespan, Report, logging):

    return None


def ScheduleTestInTG(TG, AG, SHM, Report, logging):
    logging.info("===========================================")
    logging.info("STARTING SCHEDULING TEST TASKS IN TG...")
    for Distance in range(0, 2):
        for Task in TG.nodes():
            if TG.node[Task]['Type'] == 'Test':
                if TG.node[Task]['Distance'] == Distance:
                    Node = TG.node[Task]['Node']
                    logging.info("\tSCHEDULING TASK "+str(Task)+ " ON NODE:"+str(Node))
                    (StartTime, EndTime) = FindTask_ASAP_Scheduling(TG, AG, SHM, Task, Node, logging)
                    Add_TG_TaskToNode(TG, AG, Task, Node, StartTime, EndTime, logging)
                    for Edge in TG.edges():
                        if Edge[0] == Task:
                            if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                for BatchAndLink in TG.edge[Edge[0]][Edge[1]]['Link']:
                                    Link = BatchAndLink[1]
                                    Batch = BatchAndLink[0]
                                    Probability = BatchAndLink[2]
                                    logging.info("\tSCHEDULING EDGE "+str(Edge)+" ON LINK: "+str(Link)+
                                                 " FROM BATCH: "+str(Batch))
                                    (StartTime, EndTime) = FindEdge_ASAP_Scheduling(TG, AG, Edge, Link, Batch,
                                                                                  Probability, Report, logging)
                                    Add_TG_EdgeTo_link(TG, AG, Edge, Link, Batch, Probability, StartTime, EndTime,
                                                       logging)
    logging.info("DONE SCHEDULING...")
    return None