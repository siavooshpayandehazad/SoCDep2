# Copyright (C) 2015 Siavoosh Payandeh Azad

# Acknowledgement This mapping is based on "Bandwidth-Constrained Mapping of Cores onto NoC Architectures"
# paper by Srinivasan Murali and Giovanni De Micheli.

# On November 13th 2015, the following sections were added by Behrad Niazmand
# Swapping phase of NMAP algorithm

import copy
import random
from TaskGraphUtilities import TG_Functions
from ArchGraphUtilities import AG_Functions
from Scheduler import Scheduler
from Mapper import Mapping_Functions
from RoutingAlgorithms import Calculate_Reachability


def n_map(tg, ag, noc_rg, critical_rg, non_critical_rg, shm, logging):
    """
    Performs NMap Mapping algorithm
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param noc_rg: NoC Routing Graph
    :param critical_rg: NoC Routing Graph for Critical Region
    :param non_critical_rg: NoC Routing Graph for Non-Critical Region
    :param shm: System Health Map
    :param logging: logging File
    :return: TG and AG
    """
    print ("===========================================")
    print ("STARTING N-MAP MAPPING...\n")

    if len(tg.nodes()) > len(ag.nodes()):
        raise ValueError("Number of tasks should be smaller or equal to number of PEs")

    mapped_tasks = []
    unmapped_tasks = copy.deepcopy(tg.nodes())
    allocated_nodes = []
    unallocated_nodes = copy.deepcopy(ag.nodes())

    # remove all broken nodes from unallocated_nodes list
    for node in unallocated_nodes:
        if not shm.node[node]['NodeHealth']:
            unallocated_nodes.remove(node)
            print ("REMOVED BROKEN NODE "+str(node)+" FROM UN-ALLOCATED NODES")

    print ("------------------")
    print ("STEP 1:")
    # step 1: find the task with highest weighted communication volume
    tasks_com_dict = TG_Functions.tasks_communication_weight(tg)
    sorted_tasks_com = sorted(tasks_com_dict, key=tasks_com_dict.get, reverse=True)
    print ("\t SORTED TASKS BY COMMUNICATION WEIGHT:\n"+"\t "+str(sorted_tasks_com))
    print ("\t -------------")
    chosen_task = sorted_tasks_com[0]
    print ("\t CHOSEN TASK: "+str(chosen_task))
    mapped_tasks.append(chosen_task)
    print ("\t ADDED TASK "+str(chosen_task)+"TO MAPPED TASKS LIST")
    unmapped_tasks.remove(chosen_task)
    print ("\t REMOVED TASK "+str(chosen_task)+"FROM UN-MAPPED TASKS LIST")

    print ("------------------")
    print ("STEP 2:")
    node_neighbors_dict = AG_Functions.node_neighbors(ag, shm)
    sorted_node_neighbors = sorted(node_neighbors_dict, key=node_neighbors_dict.get, reverse=True)
    max_neighbors_node = AG_Functions.max_node_neighbors(node_neighbors_dict, sorted_node_neighbors)
    print ("\t SORTED NODES BY NUMBER OF NEIGHBOURS:\n"+"\t "+str(sorted_node_neighbors))
    print ("\t -------------")
    print ("\t NODES WITH MAX NEIGHBOURS:\t"+str(max_neighbors_node))
    chosen_node = random.choice(max_neighbors_node)

    print ("\t CHOSEN NODE: "+str(chosen_node))
    allocated_nodes.append(chosen_node)
    print ("\t ADDED NODE "+str(chosen_node)+" TO ALLOCATED NODES LIST")
    unallocated_nodes.remove(chosen_node)
    print ("\t REMOVED NODE "+str(chosen_node)+" FROM UN-ALLOCATED NODES LIST")
    # Map Chosen Task on Chosen Node...
    if Mapping_Functions.map_task_to_node(tg, ag, shm, noc_rg, critical_rg,
                                          non_critical_rg, chosen_task, chosen_node, logging):
        print ("\t \033[32m* NOTE::\033[0mTASK "+str(chosen_task)+" MAPPED ON NODE "+str(chosen_node))
    else:
        raise ValueError("Mapping task on node failed...")

    print ("------------------")
    print ("STEP 3:")
    while len(unmapped_tasks) > 0:
        print ("\033[33m==>\033[0m  UN-MAPPED TASKS #: "+str(len(unmapped_tasks)))
        print ("\t -------------")
        print ("\t STEP 3.1:")
        # find the unmapped task which communicates most with mapped_tasks
        max_com = 0
        unmapped_tasks_com = {}
        tasks_with_max_com_to_mapped = []
        for Task in unmapped_tasks:
            task_weight = 0
            for mapped_task in mapped_tasks:
                if (Task, mapped_task) in tg.edges():
                    task_weight += tg.edge[Task][mapped_task]["ComWeight"]
                if (mapped_task, Task) in tg.edges():
                    task_weight += tg.edge[mapped_task][Task]["ComWeight"]
            unmapped_tasks_com[Task] = task_weight
            if max_com < task_weight:
                max_com = task_weight
                tasks_with_max_com_to_mapped = [Task]
            elif max_com == task_weight:
                tasks_with_max_com_to_mapped.append(Task)
        print ("\t MAX COMMUNICATION WITH THE MAPPED TASKS: "+str(max_com))
        print ("\t TASK(S) WITH MAX COMMUNICATION TO MAPPED TASKS: "+str(tasks_with_max_com_to_mapped))
        if len(tasks_with_max_com_to_mapped) > 1:
            # multiple tasks with same comm to mapped
            # Find the one that communicate most with Un-mapped takss...
            candid_task_with_max_com_to_unmapped = []
            max_com = 0
            for CandidateTask in tasks_with_max_com_to_mapped:
                task_weight = 0
                for unmapped_task in unmapped_tasks:
                    if (Task, unmapped_task) in tg.edges():
                        task_weight += tg.edge[Task][unmapped_task]["ComWeight"]
                    if (unmapped_task, Task) in tg.edges():
                        task_weight += tg.edge[unmapped_task][Task]["ComWeight"]
                if task_weight > max_com:
                    candid_task_with_max_com_to_unmapped = [CandidateTask]
                elif task_weight == max_com:
                    candid_task_with_max_com_to_unmapped.append(CandidateTask)
            print ("\t CANDIDATE TASK(S) THAT COMMUNICATE MOST WITH UN_MAPPED: " +
                   str(candid_task_with_max_com_to_unmapped))
            if len(candid_task_with_max_com_to_unmapped) > 1:
                # if multiple tasks with the same com to unmmaped also,
                # choose randomly
                chosen_task = random.choice(candid_task_with_max_com_to_unmapped)
            else:
                chosen_task = candid_task_with_max_com_to_unmapped[0]
        else:
            chosen_task = tasks_with_max_com_to_mapped[0]
        print ("\t CHOSEN TASK: "+str(chosen_task))

        # Find the unallocated tile with lowest communication cost to/from the allocated_tiles_set.
        print ("\t -------------")
        print ("\t STEP 3.2:")
        min_cost = float("inf")
        node_candidates = []
        for unallocated_node in unallocated_nodes:
            cost = 0
            reachable = True
            for mapped_task in mapped_tasks:
                com_weight = 0
                if (chosen_task, mapped_task) in tg.edges():
                    # print ("TASK CONNECTED TO MAPPED TASK:", mapped_task)
                    com_weight += tg.edge[chosen_task][mapped_task]["ComWeight"]
                    destination_node = tg.node[mapped_task]['task'].node
                    # here we check if this node is even reachable from the chosen node?
                    if Calculate_Reachability.is_destination_reachable_from_source(noc_rg, unallocated_node,
                                                                                   destination_node):
                        manhatan_distance = AG_Functions.manhattan_distance(unallocated_node, destination_node)
                        cost += manhatan_distance * com_weight
                    else:
                        reachable = False
                elif (mapped_task, chosen_task) in tg.edges():
                    # print ("TASK CONNECTED TO MAPPED TASK:", mapped_task)
                    com_weight += tg.edge[mapped_task][chosen_task]["ComWeight"]
                    destination_node = tg.node[mapped_task]['task'].node
                    # here we check if this node is even reachable from the chosen node?
                    if Calculate_Reachability.is_destination_reachable_from_source(noc_rg, destination_node,
                                                                                   unallocated_node):
                        manhatan_distance = AG_Functions.manhattan_distance(unallocated_node, destination_node)
                        cost += manhatan_distance * com_weight
                    else:
                        reachable = False
            if reachable:
                if cost < min_cost:
                    node_candidates = [unallocated_node]
                    min_cost = cost
                elif cost == min_cost:
                    node_candidates.append(unallocated_node)
            else:
                print ("\t \033[33m* NOTE::\033[0m NODE "+str(unallocated_node)+" CAN NOT REACH...")
                pass
        print ("\t CANDIDATE NODES: "+str(node_candidates)+" MIN COST: "+str(min_cost))

        if len(node_candidates) == 0:
            raise ValueError("COULD NOT FIND A REACHABLE CANDIDATE NODE...")
        elif len(node_candidates) > 1:
            chosen_node = random.choice(node_candidates)
        elif len(node_candidates) == 1:
            chosen_node = node_candidates[0]
        else:
            # this means that the chosen task is not connected to any other task... so its cost is infinity
            chosen_node = random.choice(unallocated_nodes)

        mapped_tasks.append(chosen_task)
        print ("\t ADDED TASK "+str(chosen_task)+" TO MAPPED TASKS LIST")
        unmapped_tasks.remove(chosen_task)
        print ("\t REMOVED TASK "+str(chosen_task)+" FROM UN-MAPPED TASKS LIST")

        allocated_nodes.append(chosen_node)
        print ("\t ADDED NODE "+str(chosen_node)+" TO ALLOCATED NODES LIST")
        unallocated_nodes.remove(chosen_node)
        print ("\t REMOVED NODE "+str(chosen_node)+" FROM UN-ALLOCATED NODES LIST")

        if Mapping_Functions.map_task_to_node(tg, ag, shm, noc_rg, critical_rg,
                                              non_critical_rg, chosen_task, chosen_node, logging):
            print ("\t \033[32m* NOTE::\033[0mTASK "+str(chosen_task)+" MAPPED ON NODE "+str(chosen_node))
        else:
            raise ValueError("Mapping task on node failed...")

    # Added by Behrad (Still under development)
    # Swapping phase
    print "-----------------------"
    print "PHASE ONE IS DONE... STARTING SWAP PROCESS..."
    for node_id_1 in range(0, len(ag.nodes())-1):
        for node_id_2 in range(node_id_1+1, len(ag.nodes())-1):
            pass
            # Save current mapping in an array
            # Also save the mapping's csomm_cost in a variable
            comm_cost = calculate_com_cost(tg)

            # Swap (node_id_1 , node_id_2)
            swap_nodes(tg, ag, shm, noc_rg, critical_rg, non_critical_rg, node_id_1, node_id_2, logging)
            # Check and calculate communication cost for all communication flows in the task graph
            #   (which is equal to the total number of edges in the application graph
            #   starting from the communication flow with the largest communication volume first
            comm_cost_new = calculate_com_cost(tg)
            # If comm_cost of current mapping is the same or bigger than the previous mapping, discard mapping
            #   Revert back to previous mapping with better comm_cost
            # Else
            #   Save new mapping as better mapping with less comm_cost
            if comm_cost_new < comm_cost:
                print "\033[32m* NOTE::\033[0m BETTER SOLUTION FOUND WITH COST:", comm_cost_new
            else:
                pass
                # print "Reverting to old solution"
                swap_nodes(tg, ag, shm, noc_rg, critical_rg, non_critical_rg,
                           node_id_2, node_id_1, logging)
            # Reset the comm_cost after each swapping

    # End of Swapping phase
    print "SWAP PROCESS FINISHED..."
    Scheduler.schedule_all(tg, ag, shm, True, logging)
    return tg, ag


def calculate_com_cost(tg):
    """
    Calculates the cost of the current mapping
    :param tg: Task Graph
    :return:  cost of the mapping
    """
    cost = 0
    for edge in tg.edges():
        task_1 = edge[0]
        task_2 = edge[1]
        node_1 = tg.node[task_1]['task'].node
        node_2 = tg.node[task_2]['task'].node
        com_weight = tg.edge[edge[0]][edge[1]]["ComWeight"]
        manhatan_distance = AG_Functions.manhattan_distance(node_1, node_2)
        cost += manhatan_distance * com_weight
    return cost


def swap_nodes(tg, ag, shm, noc_rg, critical_routing_graph,
               non_critical_routing_graph, node_1, node_2, logging):
    """
    Swaps tasks of two nodes with each other!
    :param tg:  Task Graph
    :param ag:  Architecture Graph
    :param shm: System Health Map
    :param noc_rg: NoC Routing Graph
    :param critical_routing_graph: NoC Routing Graph of Critical Region
    :param non_critical_routing_graph: NoC routing Graph of NonCritical Region
    :param node_1: first chosen node for swapping
    :param node_2:   2nd Chosen node for swapping
    :param logging: logging file
    :return: True if it successfully swaps two nodes tasks
    """
    if len(ag.node[node_1]['PE'].mapped_tasks) == 0 or len(ag.node[node_2]['PE'].mapped_tasks) == 0:
        raise ValueError("at least one of selected nodes for swapping doesnt have any tasks on it. ")

    task_1 = ag.node[node_1]['PE'].mapped_tasks[0]
    task_2 = ag.node[node_2]['PE'].mapped_tasks[0]
    Mapping_Functions.remove_task_from_node(tg, ag, noc_rg, critical_routing_graph,
                                            non_critical_routing_graph, task_1, node_1, logging)
    Mapping_Functions.remove_task_from_node(tg, ag, noc_rg, critical_routing_graph,
                                            non_critical_routing_graph, task_2, node_2, logging)
    if not Mapping_Functions.map_task_to_node(tg, ag, shm, noc_rg, critical_routing_graph,
                                              non_critical_routing_graph, task_1, node_2, logging):
        raise ValueError("swap_nodes FAILED WHILE TYING TO MAP FIRST CHOSEN TASK ON SECOND NODE ")
    if not Mapping_Functions.map_task_to_node(tg, ag, shm, noc_rg, critical_routing_graph,
                                              non_critical_routing_graph, task_2, node_1, logging):
        raise ValueError("swap_nodes FAILED WHILE TYING TO MAP SECOND CHOSEN TASK ON FIRST NODE ")
    return True