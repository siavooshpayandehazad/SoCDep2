# Copyright (C) 2015 Siavoosh Payandeh Azad

from Scheduler import Scheduling_Functions_Nodes, Scheduling_Functions_Links
from ConfigAndPackages import Config
import statistics
import random
from math import ceil
from Mapping_Reports import draw_mapping
from RoutingAlgorithms import Routing
from ArchGraphUtilities import AG_Functions
import ConfigParser
from Scheduler.Scheduling_Functions import check_if_all_deadlines_are_met

def make_initial_mapping(tg, ctg, ag, shm, noc_rg, critical_rg, noncritical_rg, report,
                         logging, random_seed, iteration=None):
    """
    Generates Initial Mapping
    :param tg:  Task Graphs
    :param ctg: Clustered Task Graph
    :param ag:  Architecture Graph
    :param shm:     System Health Map
    :param noc_rg:   NoC Routing Graph
    :param critical_rg:  Critical Region Routing Graph
    :param noncritical_rg: Non-Critical Region Routing Graph
    :param report:
    :param logging: Logging File
    :return: True if mapping pass with success False if mapping fails
    """
    # todo: It Fails if it attempts n Times and fails... its not the best way to make sure...
    if report:
        print ("===========================================")
        print ("STARTING INITIAL MAPPING...")

    if random_seed is not None:
        logging.info("NEW ROUND RANDOM SEED: "+str(random_seed))
        random.seed(random_seed)
    else:
        random.seed(None)

    counter = 0
    while not try_initial_mapping(tg, ctg, ag, shm, noc_rg, critical_rg, noncritical_rg, report, logging):
        clear_mapping(tg, ctg, ag)
        counter += 1
        if counter == 10*len(ctg.nodes()):
            return False
    if report:
        print ("INITIAL MAPPING READY... ")
        if Config.viz.mapping:
            if iteration is None:
                draw_mapping(tg, ag, shm, "Mapping_init")
            else:
                draw_mapping(tg, ag, shm, "Mapping_init_"+str(iteration))
    return True


def try_initial_mapping(tg, ctg, ag, shm, noc_rg, critical_rg, noncritical_rg, report, logging):
    iteration = 0
    for cluster in ctg.nodes():
        destination_node = random.choice(ag.nodes())
        if Config.EnablePartitioning:
            while ctg.node[cluster]['Criticality'] != ag.node[destination_node]['Region']:
                destination_node = random.choice(ag.nodes())
        # print (CTG.node[Cluster]['Criticality'],AG.node[destination_node]['Region'])
        while not add_cluster_to_node(tg, ctg, ag, shm, noc_rg, critical_rg,
                                      noncritical_rg, cluster, destination_node, logging):
            iteration += 1
            destination_node = random.choice(ag.nodes())        # try another node
            if Config.EnablePartitioning:
                while ctg.node[cluster]['Criticality'] != ag.node[destination_node]['Region']:
                    destination_node = random.choice(ag.nodes())
            # print (CTG.node[Cluster]['Criticality'],AG.node[destination_node]['Region'])
            logging.info("\tMAPPING ATTEMPT: #"+str(iteration+1)+"FOR CLUSTER:"+str(cluster))
            if iteration == 10*len(ctg.nodes()):
                if report:
                    print ("\033[33mWARNING::\033[0m INITIAL MAPPING FAILED... AFTER "+str(iteration)+" ITERATIONS")
                logging.warning("INITIAL MAPPING FAILED...")
                clear_mapping(tg, ctg, ag)
                return False
        logging.info("MAPPED CLUSTER "+str(cluster)+" ON NODE "+str(destination_node))
        iteration = 0
    return True


def map_task_to_node(tg, ag, shm, noc_rg, critical_rg, noncritical_rg, task, node, logging):
    """
    Maps a task from Task Graph to a specific Node in Architecture Graph
    :param tg:  Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param noc_rg: NoC Routing Graph
    :param critical_rg: NoC Routing Graph for the Cirtical Section
    :param noncritical_rg: NoC Routing graph for non-critical section
    :param task:    Task to be Mapped
    :param node:    Chosen Node for mapping
    :param logging: logging file
    :return: true if can successfully map task to node else returns fails
    """
    if not shm.node[node]['NodeHealth']:
        logging.info("CAN NOT MAP ON BROKEN NODE: "+str(node))
        return False
    elif ag.node[node]['PE'].dark:
        logging.info("CAN NOT MAP ON DARK NODE: "+str(node))
        return False

    logging.info("\tADDING TASK: "+str(task)+"TO NODE:"+str(node))
    tg.node[task]['task'].node = node
    ag.node[node]['PE'].mapped_tasks.append(task)
    ag.node[node]['PE'].utilization += tg.node[task]['task'].wcet
    for edge in tg.edges():
        if task in edge:    # find all the edges that are connected to Task
            # logging.info("\t\tEDGE:"+str(edge)+"CONTAINS Task:"+str(task))
            source_node = tg.node[edge[0]]['task'].node
            destination_node = tg.node[edge[1]]['task'].node
            if source_node is not None and destination_node is not None:    # check if both ends of this edge is mapped
                if source_node != destination_node:
                    # Find the links to be used
                    list_of_links, number_of_paths = Routing.find_route_in_route_graph(noc_rg, critical_rg,
                                                                                       noncritical_rg, source_node,
                                                                                       destination_node, False)
                    # print number_of_paths, list_of_links
                    if list_of_links is not None:
                        # logging.info("\t\t\tADDING PATH FROM NODE:"+str(source_node)+"TO NODE"+str(destination_node))
                        # logging.info("\t\t\tLIST OF LINKS:"+str(list_of_links))
                        counter = 0

                        if tg.edge[edge[0]][edge[1]]["Criticality"] == 'H':
                            probability = 1         # we reserve the whole bandwidth for critical packets...
                        else:
                            probability = 1.0/number_of_paths

                        for path in list_of_links:
                            for link in path:
                                if edge in ag.edge[link[0]][link[1]]['MappedTasks'].keys():
                                    ag.edge[link[0]][link[1]]['MappedTasks'][edge].append((counter, probability))
                                    ag.node[link[0]]['Router'].mapped_tasks[edge].append((counter, probability))
                                    # logging.info("\t\t\t\tAdding Packet "+str(edge)+" To Router:"+str(link[0]))
                                else:
                                    ag.edge[link[0]][link[1]]['MappedTasks'][edge] = [(counter, probability)]
                                    ag.node[link[0]]['Router'].mapped_tasks[edge] = [(counter, probability)]
                                    # logging.info("\t\t\t\tAdding Packet "+str(edge)+" To Router:"+str(link[0]))

                                ag.node[path[len(path)-1][1]]['Router'].mapped_tasks[edge] = [(counter, probability)]
                                # logging.info("\t\t\t\tAdding Packet "+str(edge) +
                                #              " To Router:"+str(path[len(path)-1][1]))

                                edge_list_of_links = list(batch[1] for batch in tg.edge[edge[0]][edge[1]]['Link'])
                                if link not in edge_list_of_links:
                                    tg.edge[edge[0]][edge[1]]['Link'].append((counter, link, probability))

                            counter += 1
                    else:
                        remove_task_from_node(tg, ag, noc_rg, critical_rg, noncritical_rg, task, node, logging)
                        logging.warning("\tNO PATH FOUND FROM "+str(source_node)+" TO "+str(destination_node)+"...")
                        print ("NO PATH FOUND FROM "+str(source_node)+" TO "+str(destination_node)+" ...")
                        return False
    return True


def remove_task_from_node(tg, ag, noc_rg, critical_rg, noncritical_rg, task, node, logging):
    """
    Removes a task from TG from a certain Node in AG
    :param tg:  Task Graph
    :param ag:  Architecture Graph
    :param noc_rg:   NoC routing graph
    :param critical_rg:  NoC routing Graph for Critical Section
    :param noncritical_rg:   NoC routing graph for non-Critical Section
    :param task:    Task ID to be removed from Node
    :param node:    Node with Task Mapped on it
    :param logging: logging File
    :return:    True if it removes task with sucess
    """
    if task not in ag.node[node]['PE'].mapped_tasks:
        raise ValueError("Trying removing Task from Node which is not the host")

    logging.info("\tREMOVING TASK:"+str(task)+"FROM NODE:"+str(node))
    for edge in tg.edges():
        if task in edge:
            source_node = tg.node[edge[0]]['task'].node
            destination_node = tg.node[edge[1]]['task'].node
            if source_node is not None and destination_node is not None:
                if source_node != destination_node:
                    # Find the links to be used
                    list_of_links, number_of_paths = Routing.find_route_in_route_graph(noc_rg, critical_rg,
                                                                                       noncritical_rg, source_node,
                                                                                       destination_node, False)
                    if list_of_links is not None:
                        # logging.info("\t\t\tREMOVING PATH FROM NODE:"+str(source_node) +
                        #              "TO NODE"+str(destination_node))
                        # logging.info("\t\t\tLIST OF LINKS:"+str(list_of_links))
                        for path in list_of_links:
                            for link in path:
                                if edge in ag.edge[link[0]][link[1]]['MappedTasks'].keys():
                                    del ag.edge[link[0]][link[1]]['MappedTasks'][edge]
                                    del ag.node[link[0]]['Router'].mapped_tasks[edge]
                                    # logging.info("\t\t\t\tRemoving Packet "+str(edge)+" To Router:"+str(link[0]))
                                    for BatchAndLink in tg.edge[edge[0]][edge[1]]['Link']:
                                        if BatchAndLink[1] == link:
                                            tg.edge[edge[0]][edge[1]]['Link'].remove(BatchAndLink)
                            del ag.node[path[len(path)-1][1]]['Router'].mapped_tasks[edge]
                            # logging.info("\t\t\t\tRemoving Packet "+str(edge)+" To Router:"+str(path[len(path)-1][1]))
                    else:
                        logging.warning("\tNOTHING TO BE REMOVED...")
    tg.node[task]['task'].node = None
    ag.node[node]['PE'].mapped_tasks.remove(task)
    ag.node[node]['PE'].utilization -= tg.node[task]['task'].wcet
    return True


def add_cluster_to_node(tg, ctg, ag, shm, noc_rg, critical_rg, noncritical_rg, cluster, node, logging):
    """
    Adds a Cluster from CTG and all its Task to a Node from Architecture Graph
    :param tg:  Task Graph
    :param ctg: Clustered Task Graph
    :param ag:  Architecture Graph
    :param shm: System Health Map
    :param noc_rg: NoC Routing Graph
    :param critical_rg: NoC Routing Graph for Critical region
    :param noncritical_rg: NoC routing Graph for Non-Critical Region
    :param cluster: ID Cluster to be mapped
    :param node: ID of the Node for mapping cluster on
    :param logging: logging file
    :return: True if maps the cluster successfully otherwise False
    """
    if not shm.node[node]['NodeHealth']:
        logging.info("CAN NOT MAP ON BROKEN NODE: "+str(node))
        return False
    elif ag.node[node]['PE'].dark:
        logging.info("CAN NOT MAP ON DARK NODE: "+str(node))
        return False

    # Adding The cluster to Node...
    logging.info("\tADDING CLUSTER: "+str(cluster)+"TO NODE:"+str(node))
    ctg.node[cluster]['Node'] = node
    for Task in ctg.node[cluster]['TaskList']:
        tg.node[Task]['task'].node = node
        ag.node[node]['PE'].mapped_tasks.append(Task)
    ag.node[node]['PE'].utilization += ctg.node[cluster]['Utilization']

    for ctg_edge in ctg.edges():
        if cluster in ctg_edge:     # find all the edges that are connected to cluster
            # logging.info("\t\tEDGE:"+str(ctg_edge)+"CONTAINS CLUSTER:"+str(cluster))
            source_node = ctg.node[ctg_edge[0]]['Node']
            destination_node = ctg.node[ctg_edge[1]]['Node']
            if source_node is not None and destination_node is not None:    # check if both ends of this edge is mapped
                if source_node != destination_node:
                    # Find the links to be used
                    list_of_links, number_of_paths = Routing.find_route_in_route_graph(noc_rg, critical_rg,
                                                                                       noncritical_rg, source_node,
                                                                                       destination_node, False)

                    list_of_edges = []
                    # print ("number_of_paths:", number_of_paths)
                    # print number_of_paths, list_of_links
                    if list_of_links is not None:
                            # find all the edges in TaskGraph that contribute to this edge in CTG
                            for tg_edge in tg.edges():
                                if tg.node[tg_edge[0]]['task'].cluster == ctg_edge[0] and \
                                        tg.node[tg_edge[1]]['task'].cluster == ctg_edge[1]:
                                    list_of_edges.append(tg_edge)
                    # print ("LIST OF LINKS:", list_of_links)
                    # add edges from list of edges to all links from list of links
                    # todo: I have to think more... this is not enough to add all the links there...
                    if list_of_links is not None and len(list_of_edges) > 0:
                        # logging.info("\t\t\tADDING PATH FROM NODE:"+str(source_node)+"TO NODE"+str(destination_node))
                        # logging.info("\t\t\tLIST OF LINKS:"+str(list_of_links))
                        # logging.info("\t\t\tLIST OF EDGES:"+str(list_of_edges))
                        counter = 0
                        for path in list_of_links:
                            for link in path:
                                for chosen_edge in list_of_edges:
                                    if tg.edge[chosen_edge[0]][chosen_edge[1]]["Criticality"] == 'H':
                                        probability = 1         # we reserve the whole bandwidth for critical packets...
                                    else:
                                        probability = 1.0/number_of_paths

                                    if chosen_edge in ag.edge[link[0]][link[1]]['MappedTasks'].keys():
                                        ag.edge[link[0]][link[1]]['MappedTasks'][chosen_edge].append((counter,
                                                                                                      probability))
                                        ag.node[link[0]]['Router'].mapped_tasks[chosen_edge].append((counter,
                                                                                                    probability))
                                        # logging.info("\t\t\t\tAdding Packet "+str(chosen_edge)+" To Router:" +
                                        #              str(link[0]))
                                    else:
                                        ag.edge[link[0]][link[1]]['MappedTasks'][chosen_edge] = [(counter, probability)]
                                        ag.node[link[0]]['Router'].mapped_tasks[chosen_edge] = [(counter, probability)]
                                        # logging.info("\t\t\t\tAdding Packet "+str(chosen_edge)+" To Router:" +
                                        #              str(link[0]))
                                    edge_list_of_links = list(batch[1] for batch in
                                                              tg.edge[chosen_edge[0]][chosen_edge[1]]['Link'])
                                    if link not in edge_list_of_links:
                                        tg.edge[chosen_edge[0]][chosen_edge[1]]['Link'].append((counter, link,
                                                                                                probability))

                            for chosen_edge in list_of_edges:
                                if tg.edge[chosen_edge[0]][chosen_edge[1]]["Criticality"] == 'H':
                                    probability = 1         # we reserve the whole bandwidth for critical packets...
                                else:
                                    probability = 1.0/number_of_paths
                                ag.node[path[len(path)-1][1]]['Router'].mapped_tasks[chosen_edge] = \
                                    [(counter, probability)]
                                # logging.info("\t\t\t\tAdding Packet "+str(chosen_edge)+" To Router:" +
                                #             str(path[len(path)-1][1]))
                            counter += 1
                    else:
                        logging.warning("\tNO PATH FOUND FROM SOURCE TO DESTINATION...")
                        logging.info("REMOVING ALL THE MAPPED CONNECTIONS FOR CLUSTER "+str(cluster))
                        remove_cluster_from_node(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg,
                                                 cluster, node, logging)
                        return False
    return True


def remove_cluster_from_node(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg, cluster, node, logging):
    """
    removes a cluster and all its tasks from a certain Node from Architecture Graph(AG)
    :param tg: Task Graph
    :param ctg: Clustered task Graph
    :param ag:  Architecture Graph
    :param noc_rg: NoC Routing Graph
    :param critical_rg: NoC routing Graph of critical Region
    :param noncritical_rg: NoC Routing Graph of non-Critical Region
    :param cluster: ID of The cluster to be mapped
    :param node: ID of the node for mapping the cluster on
    :param logging: logging file
    :return: True if can successfully remove cluster from Node
    """
    logging.info("\tREMOVING CLUSTER:"+str(cluster)+"FROM NODE:"+str(node))
    for ctg_edge in ctg.edges():
        if cluster in ctg_edge:     # find all the edges that are connected to Cluster
            source_node = ctg.node[ctg_edge[0]]['Node']
            destination_node = ctg.node[ctg_edge[1]]['Node']
            if source_node is not None and destination_node is not None:    # check if both ends of this edge is mapped
                if source_node != destination_node:
                    # Find the links to be used
                    list_of_links, number_of_paths = Routing.find_route_in_route_graph(noc_rg, critical_rg,
                                                                                       noncritical_rg, source_node,
                                                                                       destination_node, False)
                    list_of_edges = []
                    if list_of_links is not None:
                        # find all the edges in TaskGraph that contribute to this edge in CTG
                        for tg_edge in tg.edges():
                            if tg.node[tg_edge[0]]['task'].cluster == ctg_edge[0] and \
                                    tg.node[tg_edge[1]]['task'].cluster == ctg_edge[1]:
                                list_of_edges.append(tg_edge)

                    # remove edges from list of edges to all links from list of links
                    if list_of_links is not None and len(list_of_edges) > 0:
                        # logging.info("\t\t\tREMOVING PATH FROM NODE:"+str(source_node) +
                        #              "TO NODE"+str(destination_node))
                        # logging.info("\t\t\tLIST OF LINKS:"+str(list_of_links))
                        # logging.info("\t\t\tLIST OF EDGES:"+str(list_of_edges))
                        for path in list_of_links:
                            for Link in path:
                                for chosen_edge in list_of_edges:
                                    if chosen_edge in ag.edge[Link[0]][Link[1]]['MappedTasks'].keys():
                                        del ag.edge[Link[0]][Link[1]]['MappedTasks'][chosen_edge]
                                        if chosen_edge in ag.node[Link[0]]['Router'].mapped_tasks.keys():
                                            del ag.node[Link[0]]['Router'].mapped_tasks[chosen_edge]
                                        # logging.info("\t\t\t\tRemoving Packet "+str(chosen_edge) +
                                        #             " To Router:"+str(Link[0]))
                                        for LinkAndBatch in tg.edge[chosen_edge[0]][chosen_edge[1]]['Link']:
                                            if LinkAndBatch[1] == Link:
                                                tg.edge[chosen_edge[0]][chosen_edge[1]]['Link'].remove(LinkAndBatch)
                            for chosen_edge in list_of_edges:
                                if chosen_edge in ag.node[path[len(path)-1][1]]['Router'].mapped_tasks:
                                    del ag.node[path[len(path)-1][1]]['Router'].mapped_tasks[chosen_edge]
                                    # logging.info("\t\t\t\tRemoving Packet "+str(chosen_edge)+" To Router:" +
                                    #             str(path[len(path)-1][1]))
                    else:
                        logging.warning("\tNOTHING TO BE REMOVED...")
    ctg.node[cluster]['Node'] = None
    for task in ctg.node[cluster]['TaskList']:
        tg.node[task]['task'].node = None
        ag.node[node]['PE'].mapped_tasks.remove(task)
    ag.node[node]['PE'].utilization -= ctg.node[cluster]['Utilization']
    return True


def clear_mapping(tg, ctg, ag):
    """
    Removes the mapping and clears TG, AG and CTG mapping related attributes
    :param tg: Task Graph
    :param ctg: Clustered Task Graph
    :param ag: Architecture Graph
    :return: True
    """
    for node in tg.nodes():
        tg.node[node]['task'].node = None
    for edge in tg.edges():
        tg.edge[edge[0]][edge[1]]['Link'] = []
    for cluster in ctg.nodes():
        ctg.node[cluster]['Node'] = None
    for node in ag.nodes():
        ag.node[node]['PE'].mapped_tasks = []
        ag.node[node]['PE'].utilization = 0
        ag.node[node]['PE'].scheduling = {}

        ag.node[node]['Router'].scheduling = {}
        ag.node[node]['Router'].mapped_tasks = {}

    for link in ag.edges():
        ag.edge[link[0]][link[1]]['MappedTasks'] = {}
        ag.edge[link[0]][link[1]]['Scheduling'] = {}
    return True


def mapping_cost_function(tg, ag, shm, report, initial_mapping_string=None):
    """
    Calculates the Costs of a mapping based on the configurations of Config file
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param report: If true prints cost function report to Command-line
    :param initial_mapping_string: Initial mapping string used for calculating distance from the current mapping
    :return: cost of the mapping
    """

    node_makespan_list = []
    link_makespan_list = []
    for node in ag.nodes():
        if shm.node[node]['NodeHealth'] and (not ag.node[node]['PE'].dark):
            node_makespan_list.append(Scheduling_Functions_Nodes.find_last_allocated_time_on_node(ag, node,
                                                                                                  logging=None))
    for link in ag.edges():
        if shm.edge[link[0]][link[1]]['LinkHealth']:
            link_makespan_list.append(Scheduling_Functions_Links.find_last_allocated_time_on_link(ag, link,
                                                                                                  logging=None))
    node_makspan_sd = statistics.stdev(node_makespan_list)
    node_makspan_max = max(node_makespan_list)
    link_makspan_sd = statistics.stdev(link_makespan_list)
    link_makspan_max = max(link_makespan_list)

    node_util_list = []
    link_util_list = []
    for node in ag.nodes():
        if shm.node[node]['NodeHealth'] and (not ag.node[node]['PE'].dark):
            node_util_list.append(AG_Functions.return_node_util(tg, ag, node))
    for link in ag.edges():
            link_util_list.append(AG_Functions.return_link_util(tg,ag,link))
    node_util_sd = statistics.stdev(node_util_list)
    link_util_sd = statistics.stdev(link_util_list)

    if Config.Mapping_CostFunctionType == 'SD':
        cost = node_makspan_sd + link_makspan_sd
    elif Config.Mapping_CostFunctionType == 'Node_SD':
        cost = node_makspan_sd
    elif Config.Mapping_CostFunctionType == 'Link_Util_SD':
        cost = link_util_sd
    elif Config.Mapping_CostFunctionType == 'Node_Util_SD':
        cost = node_util_sd
    elif Config.Mapping_CostFunctionType == 'Util_SD':
        cost = node_util_sd + link_util_sd
    elif Config.Mapping_CostFunctionType == 'Link_SD':
        cost = link_makspan_sd
    elif Config.Mapping_CostFunctionType == 'SD+MAX':
        cost = node_makspan_max + node_makspan_sd + link_makspan_sd + link_makspan_max
    elif Config.Mapping_CostFunctionType == 'MAX':
        cost = node_makspan_max + link_makspan_max
    elif Config.Mapping_CostFunctionType == 'CONSTANT':
        cost = 1
    else:
        raise ValueError("Mapping_CostFunctionType is not valid")

    distance = None
    if initial_mapping_string is not None:
        distance = hamming_distance_of_mapping(initial_mapping_string, mapping_into_string(tg))
        cost += 20* distance
    if report:
        print ("===========================================")
        print ("      REPORTING MAPPING COST")
        print ("===========================================")
        print ("NODES MAKE SPAN MAX:"+str(node_makspan_max))
        print ("NODES MAKE SPAN STANDARD DEVIATION:"+str(node_makspan_sd))
        print ("LINKS MAKE SPAN MAX:"+str(link_makspan_max))
        print ("LINKS MAKE SPAN STANDARD DEVIATION:"+str(link_makspan_sd))
        if distance is not None:
            print ("DISTANCE FROM STARTING SOLUTION:"+str(distance))
        print ("MAPPING SCHEDULING COST:"+str(cost))

    if cost == 0:
            raise ValueError("Mapping with 0 cost... Something is wrong here...")
    if check_if_all_deadlines_are_met(tg, ag):
        return cost
    else:
        return cost+1000



def calculate_reliability_cost(tg, logging):
    # todo...
    cost = 0
    for edge in tg.edges():
        node1 = tg.node[edge[0]]['task'].node
        node2 = tg.node[edge[1]]['task'].node
        logging.info("PACKET FROM NODE "+str(node1)+"TO NODE "+str(node2))
    return cost


def unmapped_task_with_smallest_wcet(tg, logging):
    """
    Finds the list of shortest(with Smallest WCET) unmapped Tasks from TG...
    :param tg: Task Graph
    :param logging: logging File
    :return: list of shortest un-mapped Tasks
    """
    shortest_tasks = []
    smallest_wcet = Config.tg.wcet_range
    for node in tg.nodes():
        if tg.node[node]['task'].node is None:
            if tg.node[node]['task'].wcet < smallest_wcet:
                smallest_wcet = tg.node[node]['task'].wcet
    logging.info("THE SHORTEST WCET OF UNMAPPED TASKS IS:"+str(smallest_wcet))
    for node in tg.nodes():
        if tg.node[node]['task'].node is None:
            if tg.node[node]['task'].wcet == smallest_wcet:
                shortest_tasks.append(node)
    logging.info("THE LIST OF SHORTEST UNMAPPED TASKS:"+str(shortest_tasks))
    return shortest_tasks


def unmapped_task_with_biggest_wcet(tg, logging):
    """
    Finds and returns a list of longest (with the biggest WCET) unmapped tasks from TG
    :param tg: Task Graph
    :param logging: logging File
    :return: list of longest unmapped tasks
    """
    longest_tasks = []
    biggest_wcet = 0
    for node in tg.nodes():
        if tg.node[node]['task'].node is None:
            if tg.node[node]['task'].wcet > biggest_wcet:
                biggest_wcet = tg.node[node]['task'].wcet
    logging.info("THE LONGEST WCET OF UNMAPPED TASKS IS:"+str(biggest_wcet))
    for nodes in tg.nodes():
        if tg.node[nodes]['task'].node is None:
            if tg.node[nodes]['task'].wcet == biggest_wcet:
                longest_tasks.append(nodes)
    logging.info("THE LIST OF LONGEST UNMAPPED TASKS:"+str(longest_tasks))
    return longest_tasks


def nodes_with_smallest_ct(ag, tg, shm, task):
    """
    finds nodes with smallest completion time of the task!
    THIS FUNCTION CAN BE STRICTLY USED FOR INDEPENDENT TGs
    :param ag: Arch Graph
    :param tg: Task Graph
    :param shm: System Health Map
    :param task: Task number
    :return: list of nodes with smallest completion time for Task
    """
    node_with_smallest_ct = []
    random_node = random.choice(ag.nodes())
    while (not shm.node[random_node]['NodeHealth']) or ag.node[random_node]['PE'].dark:
        random_node = random.choice(ag.nodes())
    node_speed_down = 1+((100.0-shm.node[random_node]['NodeSpeed'])/100)
    task_execution_on_node = tg.node[task]['task'].wcet*node_speed_down
    last_allocated_time_on_node = Scheduling_Functions_Nodes.find_last_allocated_time_on_node(ag, random_node,
                                                                                              logging=None)
    if last_allocated_time_on_node < tg.node[task]['task'].release:
        smallest_completion_time = tg.node[task]['task'].release + task_execution_on_node
    else:
        smallest_completion_time = last_allocated_time_on_node + task_execution_on_node
    for node in ag.nodes():
        if shm.node[node]['NodeHealth'] and (not ag.node[random_node]['PE'].dark):
            node_speed_down = 1+((100.0-shm.node[node]['NodeSpeed'])/100)
            task_execution_on_node = tg.node[task]['task'].wcet*node_speed_down
            last_allocated_time_on_node = Scheduling_Functions_Nodes.find_last_allocated_time_on_node(ag, node,
                                                                                                      logging=None)
            if last_allocated_time_on_node < tg.node[task]['task'].release:
                completion_on_node = tg.node[task]['task'].release + task_execution_on_node
            else:
                completion_on_node = last_allocated_time_on_node + task_execution_on_node

            if ceil(completion_on_node) < smallest_completion_time:
                smallest_completion_time = completion_on_node
    for node in ag.nodes():
        if shm.node[node]['NodeHealth'] and (not ag.node[random_node]['PE'].dark):
            node_speed_down = 1+((100.0-shm.node[node]['NodeSpeed'])/100)
            last_allocated_time_on_node = Scheduling_Functions_Nodes.find_last_allocated_time_on_node(ag, node,
                                                                                                      logging=None)
            task_execution_on_node = tg.node[task]['task'].wcet*node_speed_down
            if last_allocated_time_on_node < tg.node[task]['task'].release:
                completion_on_node = tg.node[task]['task'].release+task_execution_on_node
            else:
                completion_on_node = last_allocated_time_on_node+task_execution_on_node
            if completion_on_node == smallest_completion_time:
                node_with_smallest_ct.append(node)
    return node_with_smallest_ct


def fastest_nodes(ag, shm):
    """
    Finds the fastest Nodes in AG
    :param ag:  Architecture Graph
    :param shm: System Health Map
    :return:
    """
    # todo: we need to add some accelerator nodes which have some specific purpose and
    # enable different tasks to behave differently on them.
    fastest_nodes_list = []
    max_speedup = 0
    for node in ag.nodes():
        if not ag.node[node]['PE'].dark:
            if shm.node[node]['NodeSpeed'] > max_speedup:
                max_speedup = shm.node[node]['NodeSpeed']
    for node in ag.nodes():
        if not ag.node[node]['PE'].dark:
            if shm.node[node]['NodeSpeed'] == max_speedup:
                fastest_nodes_list.append(node)
    return fastest_nodes_list


def mapping_into_string(tg):
    """
    Takes a Mapped Task Graph and returns a string which contains the mapping information
    :param tg: Task Graph
    :return: A string containing mapping information
    """
    mapping_string = ""
    for task in tg.nodes():
        mapping_string += str(tg.node[task]['task'].node) + " "
    return mapping_string


def hamming_distance_of_mapping(mapping_string1, mapping_string2):
    """
    Calculate the hamming distance between two mappings
    :param mapping_string1: First mapping String
    :param mapping_string2: 2nd Mapping string
    :return: hamming distance between two mappings
    """
    if type(mapping_string1) is str and type(mapping_string2) is str:
        str1_list = mapping_string1.split()
        str2_list = mapping_string2.split()

        if len(str1_list) == len(str2_list):
            distance = 0
            for i in range(0, len(str1_list)):
                if str2_list[i] != str1_list[i]:
                    distance += 1
            return distance
        else:
            raise ValueError("Mapping strings are from different length")
    else:
        raise ValueError("The input mapping strings are of wrong types")


def write_mapping_to_file(ag, file_name):
    """
    Writes the mapping configuration of the architecture graph into a file located at Generated Files
    :param ag: architecture graph
    :param file_name: name of the file
    :return: None
    """
    print("===========================================")
    print("WRITING MAPPING TO FILE...")
    mapping_file = open('Generated_Files/'+file_name+".txt", 'w')
    mapping_file.write("[nodes]\n")
    for node in ag.nodes():
        string_to_write = "node_"+str(node)+": "
        counter = 0
        for task in ag.node[node]['PE'].mapped_tasks:
            if counter < len(ag.node[node]['PE'].mapped_tasks)-1:
                string_to_write += str(task)+","
            else:
                string_to_write += str(task)+"\n"
            counter += 1
        mapping_file.write(string_to_write)

    # this section is not necessary
    # mapping_file.write("\n[routers]\n")
    # for node in ag.nodes():
    #     mapping_file.write("router_"+str(node)+": "+str(ag.node[node]['Router'].mapped_tasks)+"\n")

    # mapping_file.write("\n[links]\n")
    # for link in ag.edges():
    #    mapping_file.write("link_"+str(link[0])+"_"+str(link[1])+": " +
    #                       str(ag.edge[link[0]][link[1]]['MappedTasks'])+"\n")
    return None


def read_mapping_from_file(tg, ag, shm, noc_rg, critical_rg, noncritical_rg, file_path, logging):
    """
    gets an Architecture graph which doesnt have any tasks mapped on it, and reads the mapping from file
    and fills the map.
    :param tg: task graph
    :param ag: architecture graph
    :param shm: system health map
    :param noc_rg: noc routing graph
    :param critical_rg: noc_rg for critical region
    :param noncritical_rg: noc_rg for non-critical region
    :param file_path: path to mapping file
    :param logging: logging file
    :return: None
    """
    try:
        mapping_file = open(file_path, 'r')
        mapping_file.close()
    except IOError:
        raise ValueError('CAN NOT OPEN mapping_file')

    print("===========================================")
    print("READING MAPPING FROM FILE...")
    print "FILE LOCATED AT:", file_path
    mapping = ConfigParser.ConfigParser(allow_no_value=True)
    mapping.read(file_path)

    mapping_dict = {}
    for node in ag.nodes():
        mapping_dict[node] = map(int, mapping.get("nodes", "node_"+str(node)).split(","))

    for node in mapping_dict.keys():
        for task in mapping_dict[node]:
            map_task_to_node(tg, ag, shm, noc_rg, critical_rg, noncritical_rg, task, node, logging)

    return None


def clear_mapping_for_reconfiguration(tg, ag):
    """
    Removes the mapping and clears TG, AG and CTG mapping related attributes
    :param tg: Task Graph
    :param ag: Architecture Graph
    :return: True
    """
    for node in tg.nodes():
        tg.node[node]['task'].node = None
        tg.node[node]['task'].cluster = None
    for edge in tg.edges():
        tg.edge[edge[0]][edge[1]]['Link'] = []
    for node in ag.nodes():
        ag.node[node]['PE'].mapped_tasks = []
        ag.node[node]['PE'].utilization = 0
        ag.node[node]['PE'].scheduling = {}

        ag.node[node]['Router'].scheduling = {}
        ag.node[node]['Router'].mapped_tasks = {}

    for link in ag.edges():
        ag.edge[link[0]][link[1]]['MappedTasks'] = {}
        ag.edge[link[0]][link[1]]['Scheduling'] = {}
    return True
