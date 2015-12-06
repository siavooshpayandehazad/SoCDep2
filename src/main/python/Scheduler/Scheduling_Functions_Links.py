# Copyright (C) 2015 Siavoosh Payandeh Azad


def Add_TG_EdgeTo_link(TG, AG, Edge, Link, batch, Prob, StartTime, EndTime, logging):
    logging.info ("\t\tADDING EDGE: "+str(Edge)+" FROM BATCH: "+str(batch)+" TO LINK: "+str(Link))
    logging.info ("\t\tSTARTING TIME: "+str(StartTime)+" ENDING TIME: "+str(EndTime))
    if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']:
        AG.edge[Link[0]][Link[1]]['Scheduling'][Edge].append([StartTime, EndTime, batch, Prob])
    else:
        AG.edge[Link[0]][Link[1]]['Scheduling'][Edge] = [[StartTime, EndTime, batch, Prob]]
    return True


def FindLastAllocatedTimeOnLink(TG, AG, Link, logging=None):
    if logging is not None:
        logging.info("\t\tFINDING LAST ALLOCATED TIME ON LINK "+str(Link))
    LastAllocatedTime = 0
    if len(AG.edge[Link[0]][Link[1]]['MappedTasks']) > 0:
        for Task in AG.edge[Link[0]][Link[1]]['MappedTasks'].keys():
            if Task in AG.edge[Link[0]][Link[1]]['Scheduling']:
                for ScheduleAndBatch in AG.edge[Link[0]][Link[1]]['Scheduling'][Task]:
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


################################################################
def FindLastAllocatedTimeOnLinkForTask(TG, AG, Link, Edge, Prob, logging):
    logging.info("\t-------------------------")
    logging.info("\tFINDING LAST ALLOCATED TIME ON LINK "+str(Link)+"\tFOR EDGE: "+str(Edge)+" WITH PROB: "+str(Prob))
    LastAllocatedTime = 0
    if len(AG.edge[Link[0]][Link[1]]['MappedTasks']) > 0:
        for Task in AG.edge[Link[0]][Link[1]]['MappedTasks'].keys():
            if Task in AG.edge[Link[0]][Link[1]]['Scheduling']:
                for ScheduleAndBatch in AG.edge[Link[0]][Link[1]]['Scheduling'][Task]:
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
                            for OtherTask in AG.edge[Link[0]][Link[1]]['Scheduling']:
                                for Schedule in AG.edge[Link[0]][Link[1]]['Scheduling'][Task]:
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