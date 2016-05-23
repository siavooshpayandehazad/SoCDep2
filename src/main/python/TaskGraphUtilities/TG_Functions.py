# Copyright (C) 2015 Siavoosh Payandeh Azad 

import networkx
import random
from ConfigAndPackages import Config
import TG_File_Parser


class Task():     # Task class
    def __init__(self, wcet, criticality, cluster, node, priority, distance, release, type, deadline=None):
        self.wcet = wcet
        self.criticality = criticality
        self.cluster = cluster
        self.node = node
        self.priority = priority
        self.distance = distance
        self.release = release
        self.type = type
        self.deadline = random.randint(300, 350)    # todo: this should be fixed!


def generate_manual_tg(task_list, tg_edge_list, task_criticality_list, task_wcet_list, tg_edge_weight):
    print("PREPARING TASK GRAPH (TG)...")
    tg = networkx.DiGraph()
    edge_criticality_list = []
    # IF both sender and receiver are critical then that transaction is critical
    for i in range(0, len(task_list)):
        tg.add_node(task_list[i], task=Task(wcet=task_wcet_list[i], criticality=task_criticality_list[i],
                                            cluster=None, node=None, priority=None, distance=None,
                                            release=0, type='App'))
    print ("\tCALCULATING THE CRITICALITY OF LINKS...")
    gateway_edges = []
    gateway_counter = 0
    for edge in tg_edge_list:
        if task_criticality_list[task_list.index(edge[0])] == 'H' and \
                task_criticality_list[task_list.index(edge[1])] == 'H':
            edge_criticality_list.append('H')
        elif task_criticality_list[task_list.index(edge[0])] == 'H' and \
                task_criticality_list[task_list.index(edge[1])] == 'L':
            # gateway to Low
            gateway_number = len(task_list)+gateway_counter
            tg.add_node(gateway_number, task=Task(wcet=1, criticality='GNH',
                                                  cluster=None, node=None, priority=None, distance=None,
                                                  release=0, type='App'))
            tg.add_edge(edge[0], gateway_number, Criticality='H', Link=[],
                        ComWeight=tg_edge_weight[tg_edge_list.index(edge)])
            tg.add_edge(gateway_number, edge[1], Criticality='L', Link=[],
                        ComWeight=tg_edge_weight[tg_edge_list.index(edge)])
            gateway_edges.append(edge)
            gateway_counter += 1

        elif task_criticality_list[task_list.index(edge[0])] == 'L' and \
                task_criticality_list[task_list.index(edge[1])] == 'H':
            # gateway to high
            gateway_number = len(task_list)+gateway_counter
            tg.add_node(gateway_number, task=Task(wcet=1, criticality='GH', cluster=None, node=None,
                                                  priority=None, distance=None, release=0, type='App'))
            tg.add_edge(edge[0], gateway_number, Criticality='L', Link=[],
                        ComWeight=tg_edge_weight[tg_edge_list.index(edge)])
            tg.add_edge(gateway_number, edge[1], Criticality='H', Link=[],
                        ComWeight=tg_edge_weight[tg_edge_list.index(edge)])
            gateway_edges.append(edge)
            gateway_counter += 1
        else:
            edge_criticality_list.append('L')
    print ("\tLINKS CRITICALITY CALCULATED!")

    for edge in gateway_edges:
        tg_edge_list.remove(edge)

    for i in range(0, len(tg_edge_list)):
        tg.add_edge(tg_edge_list[i][0], tg_edge_list[i][1],
                    Criticality=edge_criticality_list[i], Link=[],
                    ComWeight=tg_edge_weight[i])  # Communication weight
    assign_distance(tg)
    print("TASK GRAPH (TG) IS READY...")
    return tg


def generate_random_tg(number_of_tasks, number_of_critical_tasks, number_of_edges,
                       wcet_range, edge_weight_range):
    tg = networkx.DiGraph()
    print("PREPARING RANDOM TASK GRAPH (TG)...")
    random.seed(Config.tg.random_seed)
    task_list = []
    task_criticality_list = []
    task_wcet_list = []
    tg_edge_list = []
    edge_criticality_list = []
    tg_edge_weight = []

    for i in range(0, number_of_tasks):
        task_list.append(i)
        task_criticality_list.append('L')
        task_wcet_list.append(random.randrange(1, wcet_range))

    counter = 0
    while counter < number_of_critical_tasks:
        chosen_task = random.choice(task_list)
        if task_criticality_list[chosen_task] == 'L':
            task_criticality_list[chosen_task] = 'H'
            counter += 1

    for j in range(0, number_of_edges):
        source_task = random.choice(task_list)
        destination_task = random.choice(task_list)
        while source_task == destination_task:
            destination_task = random.choice(task_list)

        if (source_task, destination_task) not in tg_edge_list:
            tg_edge_list.append((source_task, destination_task))
            tg_edge_weight.append(random.randrange(1, edge_weight_range))

    for i in range(0, len(task_list)):
        tg.add_node(task_list[i], task=Task(wcet=task_wcet_list[i], criticality=task_criticality_list[i],
                                            cluster=None, node=None, priority=None, distance=None,
                                            release=0, type='App'))

    print ("\tCALCULATING THE CRITICALITY OF LINKS...")
    gateway_edges = []
    gateway_counter = 0
    for edge in tg_edge_list:
        if task_criticality_list[task_list.index(edge[0])] == 'H' and \
                task_criticality_list[task_list.index(edge[1])] == 'H':
            edge_criticality_list.append('H')
        elif task_criticality_list[task_list.index(edge[0])] == 'H' and \
                task_criticality_list[task_list.index(edge[1])] == 'L':
            # gateway to Low
            gateway_number = len(task_list) + gateway_counter
            tg.add_node(gateway_number, task=Task(wcet=1, criticality='GNH',
                                                  cluster=None, node=None, priority=None, distance=None,
                                                  release=0, type='App'))
            if not networkx.has_path(tg, gateway_number, edge[0]):
                tg.add_edge(edge[0], gateway_number, Criticality='H', Link=[],
                            ComWeight=tg_edge_weight[tg_edge_list.index(edge)])
            if not networkx.has_path(tg, edge[1], gateway_number):
                tg.add_edge(gateway_number, edge[1], Criticality='L', Link=[],
                            ComWeight=tg_edge_weight[tg_edge_list.index(edge)])
            gateway_edges.append(edge)
            gateway_counter += 1
        elif task_criticality_list[task_list.index(edge[0])] == 'L' and \
                task_criticality_list[task_list.index(edge[1])] == 'H':
            # gateway to high
            gateway_number = len(task_list)+gateway_counter
            tg.add_node(gateway_number, task=Task(wcet=1, criticality='GH',
                                                  cluster=None, node=None, priority=None, distance=None,
                                                  release=0, type='App'))
            if not networkx.has_path(tg, gateway_number, edge[0]):
                tg.add_edge(edge[0], gateway_number, Criticality='L', Link=[],
                            ComWeight=tg_edge_weight[tg_edge_list.index(edge)])
            if not networkx.has_path(tg, edge[1], gateway_number):
                tg.add_edge(gateway_number, edge[1], Criticality='H', Link=[],
                            ComWeight=tg_edge_weight[tg_edge_list.index(edge)])
            gateway_edges.append(edge)
            gateway_counter += 1
        else:
            edge_criticality_list.append('L')
    print ("\tLINKS CRITICALITY CALCULATED!")

    for edge in gateway_edges:
        tg_edge_list.remove(edge)

    for i in range(0, len(tg_edge_list)):
        # making sure that the graph is still acyclic
        if not networkx.has_path(tg, tg_edge_list[i][1], tg_edge_list[i][0]):
            tg.add_edge(tg_edge_list[i][0], tg_edge_list[i][1],
                        Criticality=edge_criticality_list[i], Link=[],
                        ComWeight=tg_edge_weight[i])  # Communication weight
    assign_distance(tg)
    print("TASK GRAPH (TG) IS READY...")
    return tg


def generate_generic_tg():
    tg = networkx.DiGraph()
    # Todo: we have to make some sort of way to make a Task Graph that if i run it repeatedly, i can get the traffic
    print("PREPARING UNIFORM TASK GRAPH (TG)...")
    if Config.tg.generic_traffic == "random_uniform":
        # for each 2 nodes we make two pair of tasks:
        #           node 1 ----> node 2
        #           node 2 ----> node 1

        pass
    return tg


def generate_random_independent_tg(number_of_tasks, wcet_range, release_range):
    tg = networkx.DiGraph()
    print("PREPARING RANDOM TASK GRAPH (TG) WITH INDEPENDENT TASKS...")
    random.seed(Config.tg.random_seed)
    task_list = []
    task_criticality_list = []
    task_wcet_list = []
    tg_release_list = []
    for i in range(0, number_of_tasks):
        task_list.append(i)
        task_criticality_list.append('L')
        counter = 0
        while counter < Config.tg.num_of_critical_tasks:
            chosen_task = random.choice(task_list)
            if task_criticality_list[chosen_task] == 'L':
                task_criticality_list[chosen_task] = 'H'
                counter += 1
        task_wcet_list.append(random.randrange(1, wcet_range))
        tg_release_list.append(random.randrange(0, release_range))
    for i in range(0, len(task_list)):
        tg.add_node(task_list[i], task=Task(wcet=task_wcet_list[i], criticality=task_criticality_list[i],
                                            cluster=None, node=None, priority=None, distance=None,
                                            release=0, type='App'))

    print("RANDOM TASK GRAPH (TG) WITH INDEPENDENT TASKS IS READY...")
    return tg


def find_source_nodes(tg):
    """
    Takes a Task Graph and returns the source nodes of it in a list
    :param tg: Task Graph
    :return: List of source nodes
    """
    source_node = []
    for task in tg.nodes():
        if len(tg.predecessors(task)) == 0:
            source_node.append(task)
    return source_node


def assign_distance(tg):
    print("ASSIGNING PRIORITIES TO TASK GRAPH (TG)...")
    source_nodes = find_source_nodes(tg)
    for task in source_nodes:
        tg.node[task]['task'].distance = 0

    for task in tg.nodes():
        distance = []
        if task not in source_nodes:
            for Source in source_nodes:
                if networkx.has_path(tg, Source, task):
                    # shortest_paths=networkx.shortest_path(tg, Source, task)
                    # distance.append(len(shortest_paths)-1)
                    for path in networkx.all_simple_paths(tg, Source, task):
                        distance.append(len(path))
            tg.node[task]['task'].distance = max(distance)-1
    return None


########################################################
def generate_tg():
    if Config.tg.type == 'RandomDependent':
        return generate_random_tg(Config.tg.num_of_tasks, Config.tg.num_of_critical_tasks, Config.tg.num_of_edges,
                                  Config.tg.wcet_range, Config.tg.edge_weight_range)
    elif Config.tg.type == 'RandomIndependent':
        return generate_random_independent_tg(Config.tg.num_of_tasks, Config.tg.wcet_range, Config.tg.release_range)
    elif Config.tg.type == 'Manual':
        return generate_manual_tg(Config.Task_List, Config.TG_Edge_List,
                                  Config.Task_Criticality_List, Config.Task_WCET_List, Config.TG_Edge_Weight)
    elif Config.tg.type == 'FromDOTFile':
        return TG_File_Parser.generate_tg_from_dot(Config.tg.dot_file_path)
    elif Config.tg.type == 'GenericTraffic':
        return generate_generic_tg()
    else:
        raise ValueError('TG TYPE DOESNT EXIST...!!!')


########################################################
def calculate_max_distance(tg):
    max_distance = 0
    for node in tg.nodes():
        if tg.node[node]['task'].distance > max_distance:
            max_distance = tg.node[node]['task'].distance
    return max_distance


########################################################
def tasks_communication_weight(tg):
    """
    :param tg: Task graph
    :return: Returns a dictionary with task numbers as keys and total communication relevant to that task as value
    """
    tasks_com = {}
    for task in tg.nodes():
        task_com = 0
        for links in tg.edges():
            if task in links:
                task_com += tg.edge[links[0]][links[1]]["ComWeight"]
        tasks_com[task] = task_com
    return tasks_com
