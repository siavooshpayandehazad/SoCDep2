# Copyright (C) 2015 Siavoosh Payandeh Azad


def add_tg_edge_to_link(ag, edge, link, batch, prob, start_time, end_time, logging=None):
    if logging is not None:
        logging.info("\t\tADDING EDGE: "+str(edge)+" FROM BATCH: "+str(batch)+" TO LINK: "+str(link))
        logging.info("\t\tSTARTING TIME: "+str(start_time)+" ENDING TIME: "+str(end_time))
    if edge in ag.edges[link]['Scheduling']:
        ag.edges[link]['Scheduling'][edge].append([start_time, end_time, batch, prob])
    else:
        ag.edges[link]['Scheduling'][edge] = [[start_time, end_time, batch, prob]]
    return True


def find_last_allocated_time_on_link(ag, link, logging=None):
    if logging is not None:
        logging.info("\t\tFINDING LAST ALLOCATED TIME ON LINK "+str(link))
    last_allocated_time = 0
    if len(ag.edges[link]['MappedTasks']) > 0:
        for Task in ag.edges[link]['MappedTasks'].keys():
            if Task in ag.edges[link]['Scheduling']:
                for ScheduleAndBatch in ag.edges[link]['Scheduling'][Task]:
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


################################################################
def find_last_allocated_time_on_link_for_task(ag, link, edge, prob, logging=None):
    if logging is not None:
        logging.info("\t-------------------------")
        logging.info("\tFINDING LAST ALLOCATED TIME ON LINK "+str(link)+"\tFOR EDGE: "+str(edge) +
                     " WITH PROB: "+str(prob))
    last_allocated_time = 0
    if len(ag.edges[link]['MappedTasks']) > 0:
        for Task in ag.edges[link]['MappedTasks'].keys():
            if Task in ag.edges[link]['Scheduling']:
                for ScheduleAndBatch in ag.edges[link]['Scheduling'][Task]:
                    start_time = ScheduleAndBatch[0]
                    end_time = ScheduleAndBatch[1]
                    task_prob = ScheduleAndBatch[3]
                    if start_time is not None and end_time is not None:
                        if logging is not None:
                            logging.info("\t\tTASK "+str(Task)+" STARTS AT: " + str(start_time) +
                                         "AND ENDS AT: " + str(end_time) + " PROB: " + str(task_prob))
                        sum_of_prob = 0
                        if Task != edge:
                            if logging is not None:
                                logging.info("\t\tend_time:"+str(end_time))
                                logging.info("\t\t\tStart  Stop  Prob          SumProb")
                            for OtherTask in ag.edges[link]['Scheduling']:
                                for Schedule in ag.edges[link]['Scheduling'][Task]:
                                    if OtherTask != edge:
                                        if logging is not None:
                                            logging.info("Picked other task: "+str(OtherTask) +
                                                         " With Schedule: "+str(Schedule))
                                        if Schedule[0] < end_time <= Schedule[1]:
                                            sum_of_prob += Schedule[3]
                                            if logging is not None:
                                                logging.info("\t\t\t"+str(Schedule[0])+"   "+str(Schedule[1])+"   " +
                                                             str(Schedule[3])+"   "+str(sum_of_prob))
                                    if sum_of_prob + prob > 1:
                                        break
                                if sum_of_prob + prob > 1:
                                        break
                            if sum_of_prob + prob > 1:
                                last_allocated_time = max(last_allocated_time, end_time)
                                if logging is not None:
                                    logging.info("\t\tAllocated Time Shifted to:"+str(last_allocated_time))
    else:
        if logging is not None:
            logging.info("\t\t\tNO SCHEDULED TASK FOUND")
        return 0
    if logging is not None:
        logging.info("\tLAST ALLOCATED TIME:"+str(last_allocated_time))
    return last_allocated_time
