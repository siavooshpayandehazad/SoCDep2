# Copyright (C) 2015 Siavoosh Payandeh Azad 

from Mapper import Mapping_Functions
from Scheduler import Scheduling_Functions_Nodes,Scheduling_Reports
import copy
import random


def min_min_mapping(tg, ag, noc_rg, shm, logging):
    """
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param noc_rg: NoC Routing Graph
    :param shm: System Health Map
    :param logging: logging file
    :return: (TG, AG)
    """
    # this function finds the task with the smallest WCET and
    # maps it on the machine that can offer smallest completion time...
    # this means that the mapping algorithm has to take into account the mapping
    # of the edges of the task graph on the links.
    # Note:: this is a heuristic for independent tasks... so we are not going to
    # schedule any link
    # Note 2:: This heuristic is not taking task ciriticality into account...
    print ("===========================================")
    print ("STARTING MIN-MIN MAPPING")
    shortest_tasks = Mapping_Functions.unmapped_task_with_smallest_wcet(tg, logging)
    while len(shortest_tasks) > 0:
        task_to_be_mapped = shortest_tasks.pop()
        # map the task on the Node that yields smallest Completion time
        candidate_nodes = Mapping_Functions.nodes_with_smallest_ct(ag, tg, shm, task_to_be_mapped)
        print ("\tCANDIDATE NODES FOR MAPPING: "+str(candidate_nodes))
        if len(candidate_nodes) > 0:
            chosen_node = random.choice(candidate_nodes)
            print ("\t\tMAPPING TASK "+str(task_to_be_mapped)+" WITH RELEASE: " +
                   str(tg.node[task_to_be_mapped]['Release'])+" ---> NODE: "+str(chosen_node))
            tg.node[task_to_be_mapped]['Node'] = chosen_node
            ag.node[chosen_node]['PE'].MappedTasks.append(task_to_be_mapped)
            ag.node[chosen_node]['PE'].Utilization += tg.node[task_to_be_mapped]['WCET']

            node_speed_down = 1+((100.0-shm.node[chosen_node]['NodeSpeed'])/100)
            task_execution_on_node = tg.node[task_to_be_mapped]['WCET']*node_speed_down
            completion_on_node = tg.node[task_to_be_mapped]['Release'] + task_execution_on_node

            Scheduling_Functions_Nodes.Add_TG_TaskToNode(tg, ag, task_to_be_mapped, chosen_node,
                                                         tg.node[task_to_be_mapped]['Release'],
                                                         completion_on_node, logging)
        if len(shortest_tasks) == 0:
            shortest_tasks = Mapping_Functions.unmapped_task_with_smallest_wcet(tg, logging)
    print ("MIN-MIN MAPPING FINISHED...")
    Scheduling_Reports.report_mapped_tasks(ag, logging)
    return tg, ag


def Max_Min_Mapping (TG, AG, NoCRG, SHM, logging):
    """

    :param TG: Task Graph
    :param AG: Architecture Graph
    :param NoCRG: NoC Routing Graph
    :param SHM: System Health Map
    :param logging: logging file
    :return: (TG, AG)
    """
    # this function finds the task with the biggest WCET and
    # maps it on the machine that can offer smallest completion time...
    # this means that the mapping algorithm has to take into account the mapping
    # of the edges of the task graph on the links.
    # Note:: this is a heuristic for independent tasks... so we are not going to
    # schedule any link
    # Note 2:: This heuristic is not taking task ciriticality into account...
    print ("===========================================")
    print ("STARTING MAX-MIN MAPPING")
    LongestTasks = Mapping_Functions.unmapped_task_with_biggest_wcet(TG, logging)
    while len(LongestTasks)>0 :
        TaskToBeMapped = LongestTasks.pop()
        # map the task on the Node that yields smallest Completion time
        CandidateNodes=Mapping_Functions.nodes_with_smallest_ct(AG, TG, SHM, TaskToBeMapped)
        print ("CANDIDATE NODES FOR MAPPING: "+str(CandidateNodes))
        if len(CandidateNodes)>0:
            chosen_node=random.choice(CandidateNodes)
            if len(CandidateNodes)>1:
                print ("\tMAPPING TASK "+str(TaskToBeMapped)+" WITH RELEASE: "+str(TG.node[TaskToBeMapped]['Release'])+
                       " ---> NODE: "+str(chosen_node)+" (RANDOMLY CHOSEN FROM CANDIDATES)")
            else:
                print ("\tMAPPING TASK "+str(TaskToBeMapped)+" WITH RELEASE: "+str(TG.node[TaskToBeMapped]['Release'])+
                       " ---> NODE: "+str(chosen_node))
            TG.node[TaskToBeMapped]['Node'] = chosen_node
            AG.node[chosen_node]['PE'].MappedTasks.append(TaskToBeMapped)
            AG.node[chosen_node]['PE'].Utilization += TG.node[TaskToBeMapped]['WCET']

            node_speed_down = 1+((100.0-SHM.node[chosen_node]['NodeSpeed'])/100)
            task_execution_on_node = TG.node[TaskToBeMapped]['WCET']*node_speed_down
            completion_on_node = TG.node[TaskToBeMapped]['Release'] + task_execution_on_node

            Scheduling_Functions_Nodes.Add_TG_TaskToNode(TG, AG, TaskToBeMapped, chosen_node,
                                                         TG.node[TaskToBeMapped]['Release'],
                                                         completion_on_node, logging)

        if len(LongestTasks) == 0:
            LongestTasks = Mapping_Functions.unmapped_task_with_biggest_wcet(TG, logging)
    print ("MIN-MAX MAPPING FINISHED...")
    Scheduling_Reports.report_mapped_tasks(AG, logging)
    return TG, AG

def MinExecutionTime(TG, AG, SHM, logging):
    """
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param SHM: System Health Map
    :param logging: logging file
    :return: (TG, AG)
    """
    # this sounds a little stupid because there are no job specific machines...
    # we can Add Specific Accelerators or define different run time on different
    # PEs so this becomes more interesting...
    print ("===========================================")
    print ("STARTING MIN EXECUTION TIME MAPPING")
    for task_to_be_mapped in TG.nodes():
        chosen_node = random.choice(Mapping_Functions.fastest_nodes(AG, SHM, task_to_be_mapped))
        TG.node[task_to_be_mapped]['Node'] = chosen_node
        AG.node[chosen_node]['PE'].MappedTasks.append(task_to_be_mapped)
        AG.node[chosen_node]['PE'].Utilization += TG.node[task_to_be_mapped]['WCET']

        node_speed_down = 1+((100.0-SHM.node[chosen_node]['NodeSpeed'])/100)
        task_execution_on_node = TG.node[task_to_be_mapped]['WCET']*node_speed_down
        completion_on_node = TG.node[task_to_be_mapped]['Release'] + task_execution_on_node

        Scheduling_Functions_Nodes.Add_TG_TaskToNode(TG, AG, task_to_be_mapped, chosen_node,
                                                     TG.node[task_to_be_mapped]['Release'],
                                                     completion_on_node, logging)

        print ("\tTASK "+str(task_to_be_mapped)+" MAPPED ON NODE: "+str(chosen_node))
    print ("MIN EXECUTION TIME MAPPING FINISHED...")
    Scheduling_Reports.report_mapped_tasks(AG, logging)
    return TG, AG

def MinimumCompletionTime(tg, ag, shm, logging):
    """
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param logging: logging File
    :return: (TG, AG)
    """
    # The difference with Min Min or Max Min is that we don't add priorities to
    # tasks based on their WCET but we randomly choose a task and schedule it...
    # Note :: This heuristic is not taking task ciriticality into account...
    print ("===========================================")
    print ("STARTING MIN COMPLETION TIME MAPPING")
    for task_to_be_mapped in tg.nodes():
        chosen_node=random.choice(Mapping_Functions.nodes_with_smallest_ct(ag, tg, shm, task_to_be_mapped))
        tg.node[task_to_be_mapped]['Node'] = chosen_node
        ag.node[chosen_node]['PE'].MappedTasks.append(task_to_be_mapped)
        ag.node[chosen_node]['PE'].Utilization += tg.node[task_to_be_mapped]['WCET']

        node_speed_down = 1+((100.0-shm.node[chosen_node]['NodeSpeed'])/100)
        task_execution_on_node = tg.node[task_to_be_mapped]['WCET']*node_speed_down
        completion_on_node = tg.node[task_to_be_mapped]['Release'] + task_execution_on_node

        Scheduling_Functions_Nodes.Add_TG_TaskToNode(tg, ag, task_to_be_mapped, chosen_node,
                                                     tg.node[task_to_be_mapped]['Release'],
                                                     completion_on_node, logging)

        print ("\tTASK "+str(task_to_be_mapped)+" MAPPED ON NODE: "+str(chosen_node))
    print ("MIN COMPLETION TIME MAPPING FINISHED...")
    Scheduling_Reports.report_mapped_tasks(ag, logging)
    return tg, ag

def FirstFree(tg, ag, shm, logging):
    print ("===========================================")
    print ("STARTING FIRST FREE MAPPING")
    # Todo: to write the function

    print ("FIRST FREE MAPPING FINISHED...")
    Scheduling_Reports.report_mapped_tasks(ag, logging)
    return tg, ag