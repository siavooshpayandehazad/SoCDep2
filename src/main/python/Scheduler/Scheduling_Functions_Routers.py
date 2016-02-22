# Copyright (C) 2015 Siavoosh Payandeh Azad


def Add_TG_EdgeTo_Router(tg, ag, edge, node, batch, prob, start_time, end_time, logging=None):
    if logging is not None:
        logging.info("\t\tADDING EDGE: "+str(edge)+" FROM BATCH: "+str(batch)+" TO Router: "+str(node))
        logging.info("\t\tSTARTING TIME: "+str(start_time)+" ENDING TIME: "+str(end_time))
    if end_time < start_time:
        raise ValueError("End time smaller than Start time fpr router:", node)
    if edge in ag.node[node]['Router'].Scheduling:
        ag.node[node]['Router'].Scheduling[edge].append([start_time, end_time, batch, prob])
    else:
        ag.node[node]['Router'].Scheduling[edge] = [[start_time, end_time, batch, prob]]
    return True


def FindLastAllocatedTimeOnRouter(tg, ag, node, logging=None):
    if logging is not None:
        logging.info("\t\tFINDING LAST ALLOCATED TIME ON Router "+str(node))
    last_allocated_time = 0
    if len(ag.node[node]['Router'].MappedTasks) > 0:
        for Task in ag.node[node]['Router'].MappedTasks.keys():
            if Task in ag.node[node]['Router'].Scheduling:
                for ScheduleAndBatch in ag.node[node]['Router'].Scheduling[Task]:
                    start_time = ScheduleAndBatch[0]
                    end_time = ScheduleAndBatch[1]
                    if start_time is not None and end_time is not None:
                        if logging is not None:
                            logging.info("\t\t\tTASK STARTS AT: "+str(start_time)+" AND ENDS AT: "+str(end_time))
                        last_allocated_time = max(last_allocated_time, end_time)
    else:
        if logging is not None:
            logging.info("\t\t\tNO SCHEDULED TASK FOUND")
        return 0
    if logging is not None:
        logging.info("\t\t\tLAST ALLOCATED TIME:"+str(last_allocated_time))
    return last_allocated_time


def FindLastAllocatedTimeOnRouterForTask(TG, AG, Node, Edge, Prob, logging=None):
    if logging is not None:
        logging.info("\t-------------------------")
        logging.info("\tFINDING LAST ALLOCATED TIME ON Router "+str(Node)+"\tFOR EDGE: " +
                     str(Edge)+" WITH PROB: "+str(Prob))
    LastAllocatedTime = 0
    if len(AG.node[Node]['Router'].MappedTasks) > 0:
        for Task in AG.node[Node]['Router'].MappedTasks.keys():
            if Task in AG.node[Node]['Router'].Scheduling:
                for ScheduleAndBatch in AG.node[Node]['Router'].Scheduling[Task]:
                    StartTime = ScheduleAndBatch[0]
                    EndTime = ScheduleAndBatch[1]
                    TaskProb = ScheduleAndBatch[3]
                    if StartTime is not None and EndTime is not None:
                        if logging is not None:
                            logging.info("\t\tTASK "+str(Task)+" STARTS AT: " + str(StartTime) +
                                         "AND ENDS AT: " + str(EndTime) + " PROB: " + str(TaskProb))
                        SumOfProb = 0
                        if Task != Edge:
                            if logging is not None:
                                logging.info("\t\tEndTime:"+str(EndTime))
                                logging.info("\t\t\tStart  Stop  Prob          SumProb")
                            for OtherTask in AG.node[Node]['Router'].Scheduling:
                                for Schedule in AG.node[Node]['Router'].Scheduling[Task]:
                                    if OtherTask != Edge:
                                        if logging is not None:
                                            logging.info("Picked other task: "+str(OtherTask) +
                                                         " With Schedule: "+str(Schedule))
                                        if Schedule[0] < EndTime <= Schedule[1]:
                                            SumOfProb += Schedule[3]
                                            if logging is not None:
                                                logging.info("\t\t\t"+str(Schedule[0])+"   "+str(Schedule[1])+"   "
                                                             +str(Schedule[3])+"   "+str(SumOfProb))
                                    if SumOfProb + Prob > 1:
                                        break
                                if SumOfProb + Prob > 1:
                                        break
                            if SumOfProb + Prob > 1:
                                LastAllocatedTime = max(LastAllocatedTime, EndTime)
                                if logging is not None:
                                    logging.info("\t\tAllocated Time Shifted to:"+str(LastAllocatedTime))
    else:
        if logging is not None:
            logging.info("\t\t\tNO SCHEDULED TASK FOUND")
        return 0
    if logging is not None:
        logging.info("\tLAST ALLOCATED TIME:"+str(LastAllocatedTime))
    return LastAllocatedTime