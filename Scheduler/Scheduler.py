# Copyright (C) 2015 Siavoosh Payandeh Azad 

from TaskGraphUtilities import TG_Functions
from Scheduling_Functions import Add_TG_TaskToNode
from Scheduling_Functions import Add_TG_EdgeTo_link

def ScheduleAll(TG, AG, SHM, Report, DetailedReport, logging):
    logging.info("===========================================")
    logging.info("STARTING SCHEDULING PROCESS...")

    MaxDistance = TG_Functions.CalculateMaxDistance(TG) + 1
    for Distance in range(0, MaxDistance):
        for Task in TG.nodes():
            if TG.node[Task]['Distance'] == Distance:
                Node = TG.node[Task]['Node']
                logging.info("\tSCHEDULING TASK"+str(Task)+ "ON NODE:"+str(Node))
                Add_TG_TaskToNode(TG, AG, SHM, Task, Node, DetailedReport)
                for Edge in TG.edges():
                    if Edge[0] == Task:
                        if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                            for BatchAndLink in TG.edge[Edge[0]][Edge[1]]['Link']:
                                Link = BatchAndLink[1]
                                Batch = BatchAndLink[0]
                                Probability = BatchAndLink[2]
                                logging.info("\tSCHEDULING EDGE "+str(Edge)+" ON LINK: "+str(Link)+
                                             " FROM BATCH: "+str(Batch))
                                Add_TG_EdgeTo_link(TG, AG, Edge, Link, Batch, Probability, DetailedReport, logging)
    logging.info("DONE SCHEDULING...")
    return None