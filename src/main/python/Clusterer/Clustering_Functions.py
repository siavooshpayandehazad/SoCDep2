# Copyright (C) 2015 Siavoosh Payandeh Azad 


import statistics
import Clustering_Reports
from ConfigAndPackages import Config
import random


def remove_task_from_ctg(tg, ctg, task):
    """
    Removes a Task from TG from Clustred Task graph
    :param tg: Task graph
    :param ctg: Clustered Task Graph
    :param task: Task ID
    :return: None
    """
    task_cluster = tg.node[task]['task'].cluster
    # print ("\tREMOVING TASK:", Task, " FROM CLUSTER:", task_cluster)
    for edge in tg.edges():
        if task in edge:
            weight_to_remove = tg.edge[edge[0]][edge[1]]['ComWeight']
            source_cluster = tg.node[edge[0]]['task'].cluster
            destination_cluster = tg.node[edge[1]]['task'].cluster
            if source_cluster is not None and destination_cluster is not None:
                if source_cluster != destination_cluster:
                    # print ("\t\tREMOVING TG EDGE:", edge, "WITH WEIGHT", weight_to_remove, "FROM CLUSTER:", \
                    #    source_cluster, "--->", destination_cluster)
                    if (source_cluster, destination_cluster) not in ctg.edges():
                        print ("\t\033[31mERROR\033[0m:: EDGE ", source_cluster, "--->",
                               destination_cluster, "DOESNT EXIST")
                        Clustering_Reports.report_ctg(ctg, "CTG_Error.png")
                        raise ValueError("remove_task_from_ctg::EDGE DOESNT EXIST")
                    else:
                        if ctg.edge[source_cluster][destination_cluster]['Weight'] - weight_to_remove >= 0:
                            ctg.edge[source_cluster][destination_cluster]['Weight'] -= weight_to_remove
                            if ctg.edge[source_cluster][destination_cluster]['Weight'] == 0:
                                ctg.remove_edge(source_cluster, destination_cluster)
                        else:
                            print ("\t\033[31mERROR\033[0m::FINAL WEIGHT IS NEGATIVE")
                            raise ValueError("remove_task_from_ctg::FINAL WEIGHT IS NEGATIVE")
    tg.node[task]['task'].cluster = None
    ctg.node[task_cluster]['TaskList'].remove(task)
    if len(ctg.node[task_cluster]['TaskList']) == 0:
        ctg.node[task_cluster]['Criticality'] = 'L'
    ctg.node[task_cluster]['Utilization'] -= tg.node[task]['task'].wcet
    return None


def add_task_to_ctg(tg, ctg, task, cluster):
    """
    Takes a Task from a Task Graph and adds it to a cluster in Cluster graph
    by adding related edges etc.
    :param tg: Task graph
    :param ctg:  clustered task graph
    :param task: Task to be added
    :param cluster: destination cluster fro mapping the Task
    :return: True if addition is success, False if otherwise...
    """
    # print ("\tADDING TASK:", task, " TO CLUSTER:", cluster)
    if len(ctg.node[cluster]['TaskList']) == 0:
        ctg.node[cluster]['Criticality'] = tg.node[task]['task'].criticality
    else:
        if Config.EnablePartitioning:
            if ctg.node[cluster]['Criticality'] == tg.node[task]['task'].criticality:
                pass
            else:
                return False
    ctg.node[cluster]['TaskList'].append(task)
    ctg.node[cluster]['Utilization'] += tg.node[task]['task'].wcet
    tg.node[task]['task'].cluster = cluster
    for edge in tg.edges():
        if task in edge:
            weight_to_add = tg.edge[edge[0]][edge[1]]['ComWeight']
            source_cluster = tg.node[edge[0]]['task'].cluster
            destination_cluster = tg.node[edge[1]]['task'].cluster
            if source_cluster is not None and destination_cluster is not None:
                if source_cluster != destination_cluster:
                    if (source_cluster, destination_cluster) in ctg.edges():
                        if Config.clustering.detailed_report:
                            print ("\t\tEDGE", source_cluster, "--->", destination_cluster,
                                   "ALREADY EXISTS... ADDING", weight_to_add, "TO WEIGHT...")
                        ctg.edge[source_cluster][destination_cluster]['Weight'] += weight_to_add
                    else:
                        if Config.clustering.detailed_report:
                            print ("\t\tEDGE", source_cluster, destination_cluster,
                                   "DOES NOT EXISTS... ADDING EDGE WITH WEIGHT:",
                                   tg.edge[edge[0]][edge[1]]['ComWeight'])
                        ctg.add_edge(source_cluster, destination_cluster, Weight=weight_to_add)
    return True


def ctg_cost_function(ctg):
    """
    This Function is calculating the cost of a solution for clustering optimization algorithm.
    :param ctg: The Clustered task graph
    :return: Cost
    """
    com_weight_list = []
    for edge in ctg.edges():
        com_weight_list .append(ctg.edge[edge[0]][edge[1]]['Weight'])

    cluster_utilization = []
    for node in ctg.nodes():
        cluster_utilization.append(ctg.node[node]['Utilization'])

    total_com_weight = sum(com_weight_list)
    max_com_weight = max(com_weight_list)
    max_util = max(cluster_utilization)
    avg_util = sum(cluster_utilization)/len(cluster_utilization)

    if Config.clustering.cost_function == 'SD':
        cluster_util_sd = statistics.stdev(cluster_utilization)
        com_weight_sd = statistics.stdev(com_weight_list)
        cost = cluster_util_sd + com_weight_sd
    elif Config.clustering.cost_function == 'SD+MAX':
        cluster_util_sd = statistics.stdev(cluster_utilization)
        com_weight_sd = statistics.stdev(com_weight_list)
        cost = max_com_weight + com_weight_sd + max_util + cluster_util_sd
    elif Config.clustering.cost_function == 'MAX':
        cost = max_com_weight + max_util
    elif Config.clustering.cost_function == 'MAXCOM':
        cost = max_com_weight
    elif Config.clustering.cost_function == 'AVGUTIL':
        cost = avg_util
    elif Config.clustering.cost_function == 'SUMCOM':
        cost = total_com_weight
    else:
        raise ValueError("clustering cost function is not valid")
    return cost


def clear_clustering(tg, ctg):
    """
    Clears a clustering that has been done. by removing the tasks in task-list of clusters,
    removing parent cluster of tasks and deleting all the edges in cluster graph.
    :param tg: Task Graph
    :param ctg: Clustered Task Graph
    :return: None
    """
    for node in tg.nodes():
        tg.node[node]['task'].cluster = None
    for cluster in ctg.nodes():
        ctg.node[cluster]['TaskList'] = []
        ctg.node[cluster]['Utilization'] = 0
        ctg.node[cluster]['Criticality'] = None
    for edge in ctg.edges():
        ctg.remove_edge(edge[0], edge[1])
    return None


def ctg_opt_move(tg, ctg, iteration, logging):
    """
    Controls the Optimization moves for CTG optimization
    :param tg: Task Graph
    :param ctg: Clustered Task Graph
    :param iteration: Iteration number that this move is happening in it.
    :param logging: logging file
    :return: None
    """
    if Config.clustering.opt_move == 'RandomTaskMove':
        random_task_move(tg, ctg, iteration, logging)
    elif Config.clustering.opt_move == 'Swap':
        task_swap(tg, ctg, iteration, logging)
    elif Config.clustering.opt_move == 'Circulate':
        task_circulation()
    return None


def random_task_move(tg, ctg, iteration, logging):
    """
    Randomly chooses one task from CTG and moves it from its cluster to another random cluster
    :param tg: Task Graph
    :param ctg: Clustered Task Graph
    :param logging: logging file
    :return: None
    """
    random_seed = Config.clustering.random_seed
    random.seed(Config.mapping_random_seed)
    for i in range(0, iteration):
        random_seed = random.randint(1, 100000)
    random.seed(random_seed)
    logging.info("Moving to next solution: random_seed: "+str(random_seed)+"    iteration: "+str(iteration))

    random_task = random.choice(tg.nodes())
    random_task_cluster = tg.node[random_task]['task'].cluster
    # remove it and all its connections from CTG
    remove_task_from_ctg(tg, ctg, random_task)
    # randomly choose another cluster
    # move the task to the cluster and add the connections
    random_cluster = random.choice(ctg.nodes())
    while not add_task_to_ctg(tg, ctg, random_task, random_cluster):
        # remove_task_from_ctg(tg, ctg, random_task)
        add_task_to_ctg(tg, ctg, random_task, random_task_cluster)
        # double_check_ctg(tg, ctg)
        random_task = random.choice(tg.nodes())
        random_task_cluster = tg.node[random_task]['task'].cluster

        remove_task_from_ctg(tg, ctg, random_task)
        random_cluster = random.choice(ctg.nodes())
    logging.info("TASK"+str(random_task)+"MOVED TO CLUSTER"+str(random_cluster)+"RESULTS IN UTILIZATION:" +
                 str(ctg.node[random_cluster]['Utilization']+tg.node[random_task]['task'].wcet))
    return None


def task_swap(tg, ctg, iteration, logging):
    """
    randomly chooses 2 tasks in CTG and swaps them.
    :param tg: Task Graph
    :param ctg: Clustered Task Graph
    :param logging: logging file
    :return: None
    """
    random_seed = Config.clustering.random_seed
    random.seed(Config.mapping_random_seed)
    for i in range(0, iteration):
        random_seed = random.randint(1, 100000)
    random.seed(random_seed)
    logging.info("Moving to next solution: random_seed: "+str(random_seed)+"    iteration: "+str(iteration))

    random_cluster1 = None
    random_cluster2 = None

    while random_cluster1 == random_cluster2:
        random_cluster1 = random.choice(ctg.nodes())
        while len(ctg.node[random_cluster1]['TaskList']) == 0:
            random_cluster1 = random.choice(ctg.nodes())
        random_cluster2 = random.choice(ctg.nodes())
        while len(ctg.node[random_cluster2]['TaskList']) == 0:
            random_cluster2 = random.choice(ctg.nodes())

    random_task1 = random.choice(ctg.node[random_cluster1]['TaskList'])
    random_task2 = random.choice(ctg.node[random_cluster2]['TaskList'])

    remove_task_from_ctg(tg, ctg, random_task1)
    remove_task_from_ctg(tg, ctg, random_task2)

    task1_clustering = add_task_to_ctg(tg, ctg, random_task1, random_cluster2)
    task2_clustering = add_task_to_ctg(tg, ctg, random_task2, random_cluster1)

    while not (task1_clustering and task2_clustering):
        if task1_clustering:
            remove_task_from_ctg(tg, ctg, random_task1)
        if task2_clustering:
            remove_task_from_ctg(tg, ctg, random_task2)

        add_task_to_ctg(tg, ctg, random_task1, random_cluster1)
        add_task_to_ctg(tg, ctg, random_task2, random_cluster2)

        # here we are back to normal...
        random_cluster1 = None
        random_cluster2 = None

        while random_cluster1 == random_cluster2:
            random_cluster1 = random.choice(ctg.nodes())
            while len(ctg.node[random_cluster1]['TaskList']) == 0:
                random_cluster1 = random.choice(ctg.nodes())
            random_cluster2 = random.choice(ctg.nodes())
            while len(ctg.node[random_cluster2]['TaskList']) == 0:
                random_cluster2 = random.choice(ctg.nodes())

        random_task1 = random.choice(ctg.node[random_cluster1]['TaskList'])
        random_task2 = random.choice(ctg.node[random_cluster2]['TaskList'])

        remove_task_from_ctg(tg, ctg, random_task1)
        remove_task_from_ctg(tg, ctg, random_task2)

        task1_clustering = add_task_to_ctg(tg, ctg, random_task1, random_cluster2)
        task2_clustering = add_task_to_ctg(tg, ctg, random_task2, random_cluster1)

    logging.info("TASK "+str(random_task1) + " FROM CLUSTER " + str(random_cluster1) + " SWAPPED WITH TASK " +
                 str(random_task2)+" FROM CLUSTER "+str(random_cluster2))
    return None


def task_circulation():
    # todo... Circulate N tasks...
    return None


def remove_empty_clusters(ctg):
    """
    Takes a ctg and deletes the empty clusters
    :param ctg: Clustered Task Graph
    :return: None
    """
    for cluster in ctg.nodes():
        if len(ctg.node[cluster]['TaskList']) == 0:
            ctg.remove_node(cluster)
    return None
