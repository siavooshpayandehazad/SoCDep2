# Copyright (C) 2015 Siavoosh Payandeh Azad

from RoutingAlgorithms import Routing
from Scheduler import Scheduling_Functions_Nodes, Scheduling_Functions_Links
from ConfigAndPackages import Config
import statistics
import random
from math import ceil


def make_initial_mapping(tg, ctg, ag, shm, noc_rg, critical_rg, noncritica_rg, report, logging):
    """
    Generates Initial Mapping
    :param tg:  Task Graph
    :param ctg: Clustered Task Graph
    :param ag:  Architecture Graph
    :param shm:     System Health Map
    :param noc_rg:   NoC Routing Graph
    :param critical_rg:  Critical Region Routing Graph
    :param noncritica_rg: Non-Critical Region Routing Graph
    :param report:
    :param logging: Logging File
    :return: True if mapping pass with success False if mapping fails
    """
    # todo: It Fails if it attempts n Times and fails... its not the best way to make sure...
    if report:
        print ("===========================================")
        print ("STARTING INITIAL MAPPING...")
    iteration = 0
    for cluster in ctg.nodes():
        destination_node = random.choice(ag.nodes())
        if Config.EnablePartitioning:
            while ctg.node[cluster]['Criticality'] != ag.node[destination_node]['Region']:
                destination_node = random.choice(ag.nodes())
        # print (CTG.node[Cluster]['Criticality'],AG.node[destination_node]['Region'])
        while not AddClusterToNode(tg, ctg, ag, shm, noc_rg, critical_rg,
                                   noncritica_rg, cluster, destination_node, logging):
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
    if report:
        print ("INITIAL MAPPING READY... ")
    return True


def MapTaskToNode(tg, ag, shm, noc_rg, critical_rg, noncritical_rg, task, node, logging):
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
    elif ag.node[node]['PE'].Dark:
        logging.info("CAN NOT MAP ON DARK NODE: "+str(node))
        return False

    logging.info( "\tADDING TASK:"+str(task)+"TO NODE:"+str(node))
    tg.node[task]['Node'] = node
    ag.node[node]['PE'].MappedTasks.append(task)
    ag.node[node]['PE'].Utilization += tg.node[task]['WCET']
    for edge in tg.edges():
        if task in edge:    # find all the edges that are connected to Task
            logging.info("\t\tEDGE:"+str(edge)+"CONTAINS Task:"+str(task))
            source_node = tg.node[edge[0]]['Node']
            destination_node = tg.node[edge[1]]['Node']
            if source_node is not None and destination_node is not None:    # check if both ends of this edge is mapped
                if source_node != destination_node:
                    # Find the links to be used
                    list_of_links, number_of_paths = Routing.FindRouteInRouteGraph(noc_rg, critical_rg, noncritical_rg,
                                                                source_node, destination_node, False)
                    # print number_of_paths, list_of_links
                    if list_of_links is not None:
                        logging.info("\t\t\tADDING PATH FROM NODE:"+str(source_node)+"TO NODE"+str(destination_node))
                        logging.info("\t\t\tLIST OF LINKS:"+str(list_of_links))
                        counter = 0

                        if tg.edge[edge[0]][edge[1]]["Criticality"] == 'H':
                            probability = 1         # we reserve the whole bandwidth for critical packets...
                        else:
                            probability = 1.0/number_of_paths

                        for path in list_of_links:
                            for link in path:
                                if edge in ag.edge[link[0]][link[1]]['MappedTasks'].keys():
                                    ag.edge[link[0]][link[1]]['MappedTasks'][edge].append((counter, probability))
                                    ag.node[link[0]]['Router'].MappedTasks[edge].append((counter, probability))
                                    logging.info("\t\t\t\tAdding Packet "+str(edge)+" To Router:"+str(link[0]))
                                else:
                                    ag.edge[link[0]][link[1]]['MappedTasks'][edge] = [(counter, probability)]
                                    ag.node[link[0]]['Router'].MappedTasks[edge] = [(counter, probability)]
                                    logging.info("\t\t\t\tAdding Packet "+str(edge)+" To Router:"+str(link[0]))

                                ag.node[path[len(path)-1][1]]['Router'].MappedTasks[edge] = [(counter, probability)]
                                logging.info("\t\t\t\tAdding Packet "+str(edge)+" To Router:"+str(path[len(path)-1][1]))

                                edge_list_of_links = list(batch[1] for batch in ag.edge[edge[0]][edge[1]]['Link'])
                                if link not in edge_list_of_links:
                                    tg.edge[edge[0]][edge[1]]['Link'].append((counter, link, probability))

                            counter += 1
                    else:
                        RemoveTaskFromNode(tg, ag, noc_rg, critical_rg, noncritical_rg, task, node, logging)
                        logging.warning("\tNO PATH FOUND FROM "+str(source_node)+" TO "+str(destination_node)+"...")
                        print ("NO PATH FOUND FROM "+str(source_node)+" TO "+str(destination_node)+" ...")
                        return False
    return True


def RemoveTaskFromNode(tg, ag, noc_rg, critical_rg, noncritical_rg, task, Node, logging):
    """
    Removes a task from TG from a certain Node in AG
    :param tg:  Task Graph
    :param ag:  Architecture Graph
    :param noc_rg:   NoC routing graph
    :param critical_rg:  NoC routing Graph for Critical Section
    :param noncritical_rg:   NoC routing graph for non-Critical Section
    :param Task:    Task ID to be removed from Node
    :param Node:    Node with Task Mapped on it
    :param logging: logging File
    :return:    True if it removes task with sucess
    """
    if task not in ag.node[Node]['PE'].MappedTasks:
        raise ValueError("Trying removing Task from Node which is not the host")

    logging.info("\tREMOVING TASK:"+str(task)+"FROM NODE:"+str(Node))
    for edge in tg.edges():
        if task in edge:
            source_node = tg.node[edge[0]]['Node']
            destination_node = tg.node[edge[1]]['Node']
            if source_node is not None and destination_node is not None:
                if source_node != destination_node:
                    # Find the links to be used
                    list_of_links, number_of_paths = Routing.FindRouteInRouteGraph(noc_rg, critical_rg, noncritical_rg,
                                                                                   source_node, destination_node, False)
                    if list_of_links is not None:
                        logging.info("\t\t\tREMOVING PATH FROM NODE:"+str(source_node)+"TO NODE"+str(destination_node))
                        logging.info("\t\t\tLIST OF LINKS:"+str(list_of_links))
                        for path in list_of_links:
                            for link in path:
                                if edge in ag.edge[link[0]][link[1]]['MappedTasks'].keys():
                                    del ag.edge[link[0]][link[1]]['MappedTasks'][edge]
                                    del ag.node[link[0]]['Router'].MappedTasks[edge]
                                    logging.info("\t\t\t\tRemoving Packet "+str(edge)+" To Router:"+str(link[0]))
                                    for BatchAndLink in tg.edge[edge[0]][edge[1]]['Link']:
                                        if BatchAndLink[1] == link:
                                            tg.edge[edge[0]][edge[1]]['Link'].remove(BatchAndLink)
                            del ag.node[path[len(path)-1][1]]['Router'].MappedTasks[edge]
                            logging.info("\t\t\t\tRemoving Packet "+str(edge)+" To Router:"+str(path[len(path)-1][1]))
                    else:
                        logging.warning("\tNOTHING TO BE REMOVED...")
    tg.node[task]['Node'] = None
    ag.node[Node]['PE'].MappedTasks.remove(task)
    ag.node[Node]['PE'].Utilization -= tg.node[task]['WCET']
    return True


def AddClusterToNode(TG, CTG, AG, shm, noc_rg, critical_rg, noncritical_rg, Cluster, Node, logging):
    """
    Adds a Cluster from CTG and all its Task to a Node from Architecture Graph
    :param TG:  Task Graph
    :param CTG: Clustered Task Graph
    :param AG:  Architecture Graph
    :param shm: System Health Map
    :param noc_rg: NoC Routing Graph
    :param critical_rg: NoC Routing Graph for Critical region
    :param noncritical_rg: NoC routing Graph for Non-Critical Region
    :param Cluster: ID Cluster to be mapped
    :param Node: ID of the Node for mapping cluster on
    :param logging: logging file
    :return: True if maps the cluster successfully otherwise False
    """
    if not shm.node[Node]['NodeHealth']:
        logging.info("CAN NOT MAP ON BROKEN NODE: "+str(Node))
        return False
    elif AG.node[Node]['PE'].Dark:
        logging.info("CAN NOT MAP ON DARK NODE: "+str(Node))
        return False

    # Adding The cluster to Node...
    logging.info("\tADDING CLUSTER:"+str(Cluster)+"TO NODE:"+str(Node))
    CTG.node[Cluster]['Node'] = Node
    for Task in CTG.node[Cluster]['TaskList']:
        TG.node[Task]['Node'] = Node
        AG.node[Node]['PE'].MappedTasks.append(Task)
    AG.node[Node]['PE'].Utilization += CTG.node[Cluster]['Utilization']

    for ctg_edge in CTG.edges():
        if Cluster in ctg_edge:     # find all the edges that are connected to Cluster
            logging.info("\t\tEDGE:"+str(ctg_edge)+"CONTAINS CLUSTER:"+str(Cluster))
            source_node = CTG.node[ctg_edge[0]]['Node']
            destination_node = CTG.node[ctg_edge[1]]['Node']
            if source_node is not None and destination_node is not None:    # check if both ends of this edge is mapped
                if source_node != destination_node:
                    list_of_links, number_of_paths = Routing.FindRouteInRouteGraph(noc_rg, critical_rg, noncritical_rg,
                                                                                   source_node, destination_node,
                                                                                   False)  # Find the links to be used
                    list_of_edges = []
                    # print ("number_of_paths:", number_of_paths)
                    # print number_of_paths, list_of_links
                    if list_of_links is not None:
                            # find all the edges in TaskGraph that contribute to this edge in CTG
                            for tg_edge in TG.edges():
                                if TG.node[tg_edge[0]]['Cluster'] == ctg_edge[0] and \
                                                TG.node[tg_edge[1]]['Cluster'] == ctg_edge[1]:
                                    list_of_edges.append(tg_edge)
                    # print ("LIST OF LINKS:", list_of_links)
                    # add edges from list of edges to all links from list of links
                    # todo: I have to think more... this is not enough to add all the links there...
                    if list_of_links is not None and len(list_of_edges) > 0:
                        logging.info("\t\t\tADDING PATH FROM NODE:"+str(source_node)+"TO NODE"+str(destination_node))
                        logging.info("\t\t\tLIST OF LINKS:"+str(list_of_links))
                        logging.info("\t\t\tLIST OF EDGES:"+str(list_of_edges))
                        counter = 0
                        for path in list_of_links:
                            for link in path:
                                for chosen_edge in list_of_edges:
                                    if TG.edge[chosen_edge[0]][chosen_edge[1]]["Criticality"] == 'H':
                                        probability = 1         # we reserve the whole bandwidth for critical packets...
                                    else:
                                        probability = 1.0/number_of_paths

                                    if chosen_edge in AG.edge[link[0]][link[1]]['MappedTasks'].keys():
                                        AG.edge[link[0]][link[1]]['MappedTasks'][chosen_edge].append((counter, probability))
                                        AG.node[link[0]]['Router'].MappedTasks[chosen_edge].append((counter, probability))
                                        logging.info("\t\t\t\tAdding Packet "+str(chosen_edge)+" To Router:" +
                                                     str(link[0]))
                                    else:
                                        AG.edge[link[0]][link[1]]['MappedTasks'][chosen_edge] = [(counter, probability)]
                                        AG.node[link[0]]['Router'].MappedTasks[chosen_edge] = [(counter, probability)]
                                        logging.info("\t\t\t\tAdding Packet "+str(chosen_edge)+" To Router:" +
                                                     str(link[0]))
                                    edge_list_of_links = list(batch[1] for batch in TG.edge[chosen_edge[0]][chosen_edge[1]]['Link'])
                                    if link not in edge_list_of_links:
                                        TG.edge[chosen_edge[0]][chosen_edge[1]]['Link'].append((counter, link, probability))

                            for chosen_edge in list_of_edges:
                                if TG.edge[chosen_edge[0]][chosen_edge[1]]["Criticality"] == 'H':
                                    probability = 1         # we reserve the whole bandwidth for critical packets...
                                else:
                                    probability = 1.0/number_of_paths
                                AG.node[path[len(path)-1][1]]['Router'].MappedTasks[chosen_edge] = [(counter, probability)]
                                logging.info("\t\t\t\tAdding Packet "+str(chosen_edge)+" To Router:"+str(path[len(path)-1][1]))
                            counter += 1
                    else:
                        logging.warning( "\tNO PATH FOUND FROM SOURCE TO DESTINATION...")
                        logging.info("REMOVING ALL THE MAPPED CONNECTIONS FOR CLUSTER "+str(Cluster))
                        RemoveClusterFromNode(TG, CTG, AG, noc_rg, critical_rg, noncritical_rg, Cluster, Node, logging)
                        return False
    return True


def RemoveClusterFromNode(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg, cluster, node, logging):
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
                    list_of_links, number_of_paths = Routing.FindRouteInRouteGraph(noc_rg, critical_rg, noncritical_rg,
                                                                                   source_node, destination_node, False)
                    list_of_edges = []
                    if list_of_links is not None:
                        # find all the edges in TaskGraph that contribute to this edge in CTG
                        for tg_edge in tg.edges():
                            if tg.node[tg_edge[0]]['Cluster'] == ctg_edge[0] and \
                                            tg.node[tg_edge[1]]['Cluster'] == ctg_edge[1]:
                                list_of_edges.append(tg_edge)

                    # remove edges from list of edges to all links from list of links
                    if list_of_links is not None and len(list_of_edges) > 0:
                        logging.info("\t\t\tREMOVING PATH FROM NODE:"+str(source_node)+"TO NODE"+str(destination_node))
                        logging.info("\t\t\tLIST OF LINKS:"+str(list_of_links))
                        logging.info("\t\t\tLIST OF EDGES:"+str(list_of_edges))
                        for path in list_of_links:
                            for Link in path:
                                for chosen_edge in list_of_edges:
                                    if chosen_edge in ag.edge[Link[0]][Link[1]]['MappedTasks'].keys():
                                        del ag.edge[Link[0]][Link[1]]['MappedTasks'][chosen_edge]
                                        if chosen_edge in ag.node[Link[0]]['Router'].MappedTasks.keys():
                                            del ag.node[Link[0]]['Router'].MappedTasks[chosen_edge]
                                        logging.info("\t\t\t\tRemoving Packet "+str(chosen_edge) +
                                                     " To Router:"+str(Link[0]))
                                        for LinkAndBatch in tg.edge[chosen_edge[0]][chosen_edge[1]]['Link']:
                                            if LinkAndBatch[1] == Link:
                                                tg.edge[chosen_edge[0]][chosen_edge[1]]['Link'].remove(LinkAndBatch)
                            for chosen_edge in list_of_edges:
                                if chosen_edge in ag.node[path[len(path)-1][1]]['Router'].MappedTasks:
                                    del ag.node[path[len(path)-1][1]]['Router'].MappedTasks[chosen_edge]
                                    logging.info("\t\t\t\tRemoving Packet "+str(chosen_edge)+" To Router:" +
                                                 str(path[len(path)-1][1]))
                    else:
                        logging.warning("\tNOTHING TO BE REMOVED...")
    ctg.node[cluster]['Node'] = None
    for task in ctg.node[cluster]['TaskList']:
        tg.node[task]['Node'] = None
        ag.node[node]['PE'].MappedTasks.remove(task)
    ag.node[node]['PE'].Utilization -= ctg.node[cluster]['Utilization']
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
        tg.node[node]['Node'] = None
    for edge in tg.edges():
        tg.edge[edge[0]][edge[1]]['Link'] = []
    for cluster in ctg.nodes():
        ctg.node[cluster]['Node'] = None
    for node in ag.nodes():
        ag.node[node]['PE'].MappedTasks = []
        ag.node[node]['PE'].Utilization = 0
        ag.node[node]['PE'].Scheduling = {}

        ag.node[node]['Router'].Scheduling = {}
        ag.node[node]['Router'].MappedTasks = {}

    for link in ag.edges():
        ag.edge[link[0]][link[1]]['MappedTasks'] = {}
        ag.edge[link[0]][link[1]]['Scheduling'] = {}
    return True


def CostFunction(TG, AG, shm, Report, InitialMappingString = None):
    """
    Calculates the Costs of a mapping based on the configurations of Config file
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param shm: System Health Map
    :param Report: If true prints cost function report to Command-line
    :param InitialMappingString: Initial mapping string used for calculating distance from the current mapping
    :return: cost of the mapping
    """
    NodeMakeSpanList = []
    LinkMakeSpanList = []
    for Node in AG.nodes():
        if shm.node[Node]['NodeHealth'] and (not AG.node[Node]['PE'].Dark):
            NodeMakeSpanList.append(Scheduling_Functions_Nodes.FindLastAllocatedTimeOnNode(TG, AG, Node, logging=None))
    for link in AG.edges():
        if shm.edge[link[0]][link[1]]['LinkHealth']:
            LinkMakeSpanList.append(Scheduling_Functions_Links.FindLastAllocatedTimeOnLink(TG, AG, link, logging=None))
    NodeMakeSpan_Stdev = statistics.stdev(NodeMakeSpanList)
    NodeMakeSpan_Max = max(NodeMakeSpanList)
    LinkMakeSpan_Stdev = statistics.stdev(LinkMakeSpanList)
    LinkMakeSpan_Max = max(LinkMakeSpanList)

    if Config.Mapping_CostFunctionType == 'SD':
        cost = NodeMakeSpan_Stdev + LinkMakeSpan_Stdev
    elif Config.Mapping_CostFunctionType == 'SD+MAX':
        cost = NodeMakeSpan_Max + NodeMakeSpan_Stdev + LinkMakeSpan_Stdev + LinkMakeSpan_Max
    elif Config.Mapping_CostFunctionType == 'MAX':
        cost = NodeMakeSpan_Max + LinkMakeSpan_Max
    elif Config.Mapping_CostFunctionType == 'CONSTANT':
        cost = 1
    else:
        raise ValueError("Mapping_CostFunctionType is not valid")

    Distance = None
    if InitialMappingString is not None:
        Distance = HammingDistanceOfMapping(InitialMappingString,MappingIntoString(TG))
        cost+= Distance
    if Report:
        print ("===========================================")
        print ("      REPORTING MAPPING COST")
        print ("===========================================")
        print ("NODES MAKE SPAN MAX:"+str(NodeMakeSpan_Max))
        print ("NODES MAKE SPAN STANDARD DEVIATION:"+str(NodeMakeSpan_Stdev))
        print ("LINKS MAKE SPAN MAX:"+str(LinkMakeSpan_Max))
        print ("LINKS MAKE SPAN STANDARD DEVIATION:"+str(LinkMakeSpan_Stdev))
        if Distance is not None:
            print ("DISTANCE FROM STARTING SOLUTION:"+str(Distance))
        print ("MAPPING SCHEDULING COST:"+str(cost))

    if cost== 0:
            raise ValueError("Mapping with 0 cost... Something is wrong here...")
    return cost


def CalculateReliabilityCost(tg, noc_rg, logging):
    # todo...
    cost = 0
    for edge in tg.edges():
        node1 = tg.node[edge[0]]['Node']
        node2 = tg.node[edge[1]]['Node']
        logging.info("PACKET FROM NODE "+str(node1)+"TO NODE "+str(node2))

    return cost


def FindUnMappedTaskWithSmallestWCET(tg, logging):
    """
    Finds the list of shortest(with Smallest WCET) unmapped Tasks from TG...
    :param tg: Task Graph
    :param logging: logging File
    :return: list of shortest un-mapped Tasks
    """
    shortest_tasks = []
    smallest_wcet = Config.WCET_Range
    for node in tg.nodes():
        if tg.node[node]['Node'] is None:
            if tg.node[node]['WCET'] < smallest_wcet:
                smallest_wcet = tg.node[node]['WCET']
    logging.info("THE SHORTEST WCET OF UNMAPPED TASKS IS:"+str(smallest_wcet))
    for node in tg.nodes():
        if tg.node[node]['Node'] is None:
            if tg.node[node]['WCET'] == smallest_wcet:
                shortest_tasks.append(node)
    logging.info("THE LIST OF SHORTEST UNMAPPED TASKS:"+str(shortest_tasks))
    return shortest_tasks


def FindUnMappedTaskWithBiggestWCET(tg, logging):
    """
    Finds and returns a list of longest (with the biggest WCET) unmapped tasks from TG
    :param tg: Task Graph
    :param logging: logging File
    :return: list of longest unmapped tasks
    """
    longest_tasks = []
    biggest_wcet = 0
    for node in tg.nodes():
        if tg.node[node]['Node'] is None:
            if tg.node[node]['WCET'] > biggest_wcet:
                biggest_wcet= tg.node[node]['WCET']
    logging.info("THE LONGEST WCET OF UNMAPPED TASKS IS:"+str(biggest_wcet))
    for nodes in tg.nodes():
        if tg.node[nodes]['Node'] is None:
            if tg.node[nodes]['WCET'] == biggest_wcet:
                longest_tasks.append(nodes)
    logging.info("THE LIST OF LONGEST UNMAPPED TASKS:"+str(longest_tasks))
    return longest_tasks


def FindNodeWithSmallestCompletionTime(ag, tg, shm, task):
    """
    THIS FUNCTION CAN BE STRICTLY USED FOR INDEPENDENT TGs
    :param ag: Arch Graph
    :param tg: Task Graph
    :param shm: System Health Map
    :param task: Task number
    :return: list of nodes with smallest completion time for Task
    """
    node_with_smallest_ct = []
    random_node = random.choice(ag.nodes())
    while (not shm.node[random_node]['NodeHealth']) or ag.node[random_node]['PE'].Dark:
        random_node = random.choice(ag.nodes())
    node_speed_down = 1+((100.0-shm.node[random_node]['NodeSpeed'])/100)
    task_execution_on_node = tg.node[task]['WCET']*node_speed_down
    last_allocated_time_on_node = Scheduling_Functions_Nodes.FindLastAllocatedTimeOnNode(tg, ag, random_node, None)
    if last_allocated_time_on_node < tg.node[task]['Release']:
        smallest_completion_time = tg.node[task]['Release'] + task_execution_on_node
    else:
        smallest_completion_time = last_allocated_time_on_node + task_execution_on_node
    for node in ag.nodes():
        if shm.node[node]['NodeHealth'] and (not ag.node[random_node]['PE'].Dark):
            node_speed_down = 1+((100.0-shm.node[node]['NodeSpeed'])/100)
            task_execution_on_node = tg.node[task]['WCET']*node_speed_down
            last_allocated_time_on_node = Scheduling_Functions_Nodes.FindLastAllocatedTimeOnNode(tg, ag, node, None)
            if last_allocated_time_on_node < tg.node[task]['Release']:
                completion_on_node = tg.node[task]['Release'] + task_execution_on_node
            else:
                completion_on_node = last_allocated_time_on_node + task_execution_on_node

            if ceil(completion_on_node) < smallest_completion_time:
                smallest_completion_time = completion_on_node
    for node in ag.nodes():
        if shm.node[node]['NodeHealth'] and (not ag.node[random_node]['PE'].Dark):
            node_speed_down = 1+((100.0-shm.node[node]['NodeSpeed'])/100)
            last_allocated_time_on_node = Scheduling_Functions_Nodes.FindLastAllocatedTimeOnNode(tg, ag, node, None)
            task_execution_on_node = tg.node[task]['WCET']*node_speed_down
            completion_on_node = 0
            if last_allocated_time_on_node < tg.node[task]['Release']:
                completion_on_node = tg.node[task]['Release']+task_execution_on_node
            else:
                completion_on_node = last_allocated_time_on_node+task_execution_on_node
            if completion_on_node == smallest_completion_time:
                node_with_smallest_ct.append(node)
    return node_with_smallest_ct


def FindFastestNodes(ag, shm, task_to_be_mapped):
    """
    Finds the fastest Nodes in AG
    :param ag:  Architecture Graph
    :param shm: System Health Map
    :param task_to_be_mapped:
    :return:
    """
    # todo: we need to add some accelerator nodes which have some specific purpose and
    # enable different tasks to behave differently on them.
    fastest_nodes = []
    max_speedup = 0
    for node in ag.nodes():
        if not ag.node[node]['PE'].Dark:
            if shm.node[node]['NodeSpeed'] > max_speedup:
                max_speedup = shm.node[node]['NodeSpeed']
    for node in ag.nodes():
        if not ag.node[node]['PE'].Dark:
            if shm.node[node]['NodeSpeed'] == max_speedup:
                fastest_nodes.append(node)
    return fastest_nodes


def MappingIntoString(tg):
    """
    Takes a Mapped Task Graph and returns a string which contains the mapping information
    :param tg: Task Graph
    :return: A string containing mapping information
    """
    mapping_string = ""
    for task in tg.nodes():
        mapping_string += str(tg.node[task]['Node']) + " "
    return mapping_string


def HammingDistanceOfMapping(MappingString1, MappingString2):
    """
    Calculate the hamming distance between two mappings
    :param MappingString1: First mapping String
    :param MappingString2: 2nd Mapping string
    :return: hamming distance between two mappings
    """
    if type(MappingString1) is str and type(MappingString2) is str:
        Str1_List = MappingString1.split()
        Str2_List = MappingString2.split()

        if len(Str1_List) == len(Str2_List):
            distance = 0
            for i in range(0, len(Str1_List)):
                if Str2_List[i] != Str1_List[i]:
                    distance += 1
            return distance
        else:
            raise ValueError("Mapping strings are from different length")
    else:
        raise ValueError("The input mapping strings are of wrong types")