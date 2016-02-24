# Copyright (C) 2015 Siavoosh Payandeh Azad


def add_tg_edge_to_router(ag, edge, node, batch, prob, start_time, end_time, logging=None):
    if logging is not None:
        logging.info("\t\tADDING EDGE: "+str(edge)+" FROM BATCH: "+str(batch)+" TO Router: "+str(node))
        logging.info("\t\tSTARTING TIME: "+str(start_time)+" ENDING TIME: "+str(end_time))
    if end_time < start_time:
        raise ValueError("End time smaller than Start time fpr router:", node)
    if edge in ag.node[node]['Router'].scheduling:
        ag.node[node]['Router'].scheduling[edge].append([start_time, end_time, batch, prob])
    else:
        ag.node[node]['Router'].scheduling[edge] = [[start_time, end_time, batch, prob]]
    return True


def find_last_allocated_time_on_router(ag, node, logging=None):
    if logging is not None:
        logging.info("\t\tFINDING LAST ALLOCATED TIME ON Router "+str(node))
    last_allocated_time = 0
    if len(ag.node[node]['Router'].mapped_tasks) > 0:
        for Task in ag.node[node]['Router'].mapped_tasks.keys():
            if Task in ag.node[node]['Router'].scheduling:
                for ScheduleAndBatch in ag.node[node]['Router'].scheduling[Task]:
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


def find_last_allocated_time_on_router_for_task(ag, node, edge, prob, logging=None):
    if logging is not None:
        logging.info("\t-------------------------")
        logging.info("\tFINDING LAST ALLOCATED TIME ON Router "+str(node)+"\tFOR EDGE: " +
                     str(edge)+" WITH PROB: "+str(prob))
    last_allocated_time = 0
    if len(ag.node[node]['Router'].mapped_tasks) > 0:
        for task in ag.node[node]['Router'].mapped_tasks.keys():
            if task in ag.node[node]['Router'].scheduling:
                for ScheduleAndBatch in ag.node[node]['Router'].scheduling[task]:
                    start_time = ScheduleAndBatch[0]
                    end_time = ScheduleAndBatch[1]
                    task_prob = ScheduleAndBatch[3]
                    if start_time is not None and end_time is not None:
                        if logging is not None:
                            logging.info("\t\tTASK "+str(task)+" STARTS AT: " + str(start_time) +
                                         "AND ENDS AT: " + str(end_time) + " PROB: " + str(task_prob))
                        sum_of_prob = 0
                        if task != edge:
                            if logging is not None:
                                logging.info("\t\tEndTime:"+str(end_time))
                                logging.info("\t\t\tStart  Stop  Prob          SumProb")
                            for OtherTask in ag.node[node]['Router'].scheduling:
                                for schedule in ag.node[node]['Router'].scheduling[task]:
                                    if OtherTask != edge:
                                        if logging is not None:
                                            logging.info("Picked other task: "+str(OtherTask) +
                                                         " With Schedule: "+str(schedule))
                                        if schedule[0] < end_time <= schedule[1]:
                                            sum_of_prob += schedule[3]
                                            if logging is not None:
                                                logging.info("\t\t\t"+str(schedule[0])+"   "+str(schedule[1])+"   " +
                                                             str(schedule[3])+"   "+str(sum_of_prob))
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
