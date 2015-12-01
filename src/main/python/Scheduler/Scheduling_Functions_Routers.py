__author__ = 'siavoosh'


def Add_TG_EdgeTo_Router(TG, AG, Edge, Node, batch, Prob, StartTime, EndTime, logging):
    logging.info ("\t\tADDING EDGE: "+str(Edge)+" FROM BATCH: "+str(batch)+" TO Router: "+str(Node))
    logging.info ("\t\tSTARTING TIME: "+str(StartTime)+" ENDING TIME: "+str(EndTime))
    if Edge in AG.node[Node]['Router'].Scheduling:
        AG.node[Node]['Router'].Scheduling[Edge].append([StartTime, EndTime, batch, Prob])
    else:
        AG.node[Node]['Router'].Scheduling[Edge] = [[StartTime, EndTime, batch, Prob]]
    return True


def FindLastAllocatedTimeOnRouter(TG, AG, Node, logging=None):
    if logging is not None:
        logging.info("\t\tFINDING LAST ALLOCATED TIME ON Router "+str(Node))
    LastAllocatedTime = 0
    if len(AG.node[Node]['Router'].MappedTasks) > 0:
        for Task in AG.node[Node]['Router'].MappedTasks.keys():
            if Task in AG.node[Node]['Router'].Scheduling:
                for ScheduleAndBatch in AG.node[Node]['Router'].Scheduling[Task]:
                    StartTime = ScheduleAndBatch[0]
                    EndTime = ScheduleAndBatch[1]
                    if StartTime is not None and EndTime is not None:
                        if logging is not None:
                            logging.info ("\t\t\tTASK STARTS AT: "+str(StartTime)+" AND ENDS AT: "+str(EndTime))
                        LastAllocatedTime = max(LastAllocatedTime, EndTime)
    else:
        if logging is not None:
            logging.info("\t\t\tNO SCHEDULED TASK FOUND")
        return 0
    if logging is not None:
        logging.info ("\t\t\tLAST ALLOCATED TIME:"+str(LastAllocatedTime))
    return LastAllocatedTime


def FindLastAllocatedTimeOnRouterForTask(TG, AG, Node, Edge, Prob, logging):
    logging.info("\t-------------------------")
    logging.info("\tFINDING LAST ALLOCATED TIME ON Router "+str(Node)+"\tFOR EDGE: "+str(Edge)+" WITH PROB: "+str(Prob))
    LastAllocatedTime = 0
    if len(AG.node[Node]['Router'].MappedTasks) > 0:
        for Task in AG.node[Node]['Router'].MappedTasks.keys():
            if Task in AG.node[Node]['Router'].Scheduling:
                for ScheduleAndBatch in AG.node[Node]['Router'].Scheduling[Task]:
                    StartTime = ScheduleAndBatch[0]
                    EndTime = ScheduleAndBatch[1]
                    TaskProb = ScheduleAndBatch[3]
                    if StartTime is not None and EndTime is not None:
                        logging.info("\t\tTASK "+str(Task)+" STARTS AT: " + str(StartTime) +
                                     "AND ENDS AT: " + str(EndTime) + " PROB: " + str(TaskProb))
                        SumOfProb = 0
                        if Task != Edge:
                            logging.info("\t\tEndTime:"+str(EndTime))
                            logging.info("\t\t\tStart  Stop  Prob          SumProb")
                            for OtherTask in AG.node[Node]['Router'].Scheduling:
                                for Schedule in AG.node[Node]['Router'].Scheduling[Task]:
                                    if OtherTask != Edge:
                                        # logging.info("Picked other task: "+str(OtherTask)+" With Schedule: "+str(Schedule))
                                        if Schedule[0] < EndTime <= Schedule[1]:
                                            SumOfProb += Schedule[3]
                                            logging.info("\t\t\t"+str(Schedule[0])+"   "+str(Schedule[1])+"   "
                                                         +str(Schedule[3])+"   "+str(SumOfProb))
                                    if SumOfProb + Prob > 1:
                                        break
                                if SumOfProb + Prob > 1:
                                        break
                            if SumOfProb + Prob > 1:
                                LastAllocatedTime = max(LastAllocatedTime, EndTime)
                                logging.info("\t\tAllocated Time Shifted to:"+str(LastAllocatedTime))
    else:
        logging.info("\t\t\tNO SCHEDULED TASK FOUND")
        return 0
    logging.info("\tLAST ALLOCATED TIME:"+str(LastAllocatedTime))
    return LastAllocatedTime