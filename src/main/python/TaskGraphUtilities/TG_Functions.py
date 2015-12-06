# Copyright (C) 2015 Siavoosh Payandeh Azad 

import networkx
import random
from ConfigAndPackages import Config
import TG_File_Parser


def generate_manual_task_graph(task_list, task_graph_edge_list, task_criticality_list,
                               task_wcet_list, task_graph_edge_weight):
    print("PREPARING TASK GRAPH (TG)...")
    task_graph = networkx.DiGraph()
    edge_criticality_list = []
    # IF both sender and receiver are critical then that transaction is critical
    for i in range(0, len(task_list)):
        task_graph.add_node(task_list[i], WCET=task_wcet_list[i], Criticality=task_criticality_list[i],
                            Cluster=None, Node=None, Priority=None, Distance=None, Release=0, Type='App')

    print ("\tCALCULATING THE CRITICALITY OF LINKS...")
    gateway_edges = []
    gateway_counter = 0
    for edge in task_graph_edge_list:
        if task_criticality_list[task_list.index(edge[0])] == 'H' and \
                task_criticality_list[task_list.index(edge[1])] == 'H':
            edge_criticality_list.append('H')
        elif task_criticality_list[task_list.index(edge[0])] == 'H' and \
                task_criticality_list[task_list.index(edge[1])] == 'L':
            # gateway to Low
            gateway_number = len(task_list)+gateway_counter
            task_graph.add_node(gateway_number, WCET=1, Criticality='GNH', Cluster=None, Node=None, Priority=None,
                                Distance=None, Release=0, Type='App')
            task_graph.add_edge(edge[0], gateway_number, Criticality='H', Link=[],
                                ComWeight=task_graph_edge_weight[task_graph_edge_list.index(edge)])
            task_graph.add_edge(gateway_number, edge[1], Criticality='L', Link=[],
                                ComWeight=task_graph_edge_weight[task_graph_edge_list.index(edge)])
            gateway_edges.append(edge)
            gateway_counter += 1

        elif task_criticality_list[task_list.index(edge[0])] == 'L' and \
                task_criticality_list[task_list.index(edge[1])] == 'H':
            # gateway to high
            gateway_number = len(task_list)+gateway_counter
            task_graph.add_node(gateway_number, WCET=1, Criticality='GH',
                                Cluster=None, Node=None, Priority=None, Distance=None, Release=0, Type='App')
            task_graph.add_edge(edge[0], gateway_number, Criticality='L', Link=[],
                                ComWeight=task_graph_edge_weight[task_graph_edge_list.index(edge)])
            task_graph.add_edge(gateway_number, edge[1], Criticality='H', Link=[],
                                ComWeight=task_graph_edge_weight[task_graph_edge_list.index(edge)])
            gateway_edges.append(edge)
            gateway_counter += 1
        else:
            edge_criticality_list.append('L')
    print ("\tLINKS CRITICALITY CALCULATED!")

    for edge in gateway_edges:
        task_graph_edge_list.remove(edge)

    for i in range(0, len(task_graph_edge_list)):
        task_graph.add_edge(task_graph_edge_list[i][0], task_graph_edge_list[i][1],
                            Criticality=edge_criticality_list[i], Link=[],
                            ComWeight=task_graph_edge_weight[i])  # Communication weight
    assign_distance(task_graph)
    print("TASK GRAPH (TG) IS READY...")
    return task_graph


def generate_random_task_graph(number_of_tasks, number_of_critical_tasks, number_of_edges,
                               wcet_range, edge_weight_range):
    task_graph = networkx.DiGraph()
    print("PREPARING RANDOM TASK GRAPH (TG)...")

    task_list = []
    task_criticality_list = []
    task_wcet_list = []
    task_graph_edge_list = []
    edge_criticality_list = []
    task_graph_edge_weight = []

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

        if (source_task, destination_task) not in task_graph_edge_list:
            task_graph_edge_list.append((source_task, destination_task))
            task_graph_edge_weight.append(random.randrange(1, edge_weight_range))

    for i in range(0, len(task_list)):
        task_graph.add_node(task_list[i], WCET=task_wcet_list[i], Criticality=task_criticality_list[i],
                            Cluster=None, Node=None, Priority=None, Distance=None, Release=0, Type='App')

    print ("\tCALCULATING THE CRITICALITY OF LINKS...")
    gateway_edges = []
    gateway_counter = 0
    for edge in task_graph_edge_list:
        if task_criticality_list[task_list.index(edge[0])] == 'H' and \
                task_criticality_list[task_list.index(edge[1])] == 'H':
            edge_criticality_list.append('H')
        elif task_criticality_list[task_list.index(edge[0])] == 'H' and \
                task_criticality_list[task_list.index(edge[1])] == 'L':
            # gateway to Low
            gateway_number = len(task_list) + gateway_counter
            task_graph.add_node(gateway_number, WCET=1, Criticality='GNH', Cluster=None, Node=None, Priority=None,
                                Distance=None, Release=0, Type='App')
            if not networkx.has_path(task_graph, gateway_number, edge[0]):
                task_graph.add_edge(edge[0], gateway_number, Criticality='H', Link=[],
                                    ComWeight=task_graph_edge_weight[task_graph_edge_list.index(edge)])
            if not networkx.has_path(task_graph, edge[1], gateway_number):
                task_graph.add_edge(gateway_number, edge[1], Criticality='L', Link=[],
                                    ComWeight=task_graph_edge_weight[task_graph_edge_list.index(edge)])
            gateway_edges.append(edge)
            gateway_counter += 1
        elif task_criticality_list[task_list.index(edge[0])] == 'L' and \
                task_criticality_list[task_list.index(edge[1])] == 'H':
            # gateway to high
            gateway_number = len(task_list)+gateway_counter
            task_graph.add_node(gateway_number, WCET=1, Criticality='GH', Cluster=None, Node=None, Priority=None,
                                Distance=None, Release=0, Type='App')
            if not networkx.has_path(task_graph, gateway_number, edge[0]):
                task_graph.add_edge(edge[0], gateway_number, Criticality='L', Link=[],
                                    ComWeight=task_graph_edge_weight[task_graph_edge_list.index(edge)])
            if not networkx.has_path(task_graph, edge[1], gateway_number):
                task_graph.add_edge(gateway_number, edge[1], Criticality='H', Link=[],
                                    ComWeight=task_graph_edge_weight[task_graph_edge_list.index(edge)])
            gateway_edges.append(edge)
            gateway_counter += 1
        else:
            edge_criticality_list.append('L')
    print ("\tLINKS CRITICALITY CALCULATED!")

    for edge in gateway_edges:
        task_graph_edge_list.remove(edge)

    for i in range(0, len(task_graph_edge_list)):
        # making sure that the graph is still acyclic
        if not networkx.has_path(task_graph, task_graph_edge_list[i][1], task_graph_edge_list[i][0]):
            task_graph.add_edge(task_graph_edge_list[i][0], task_graph_edge_list[i][1],
                                Criticality=edge_criticality_list[i], Link=[],
                                ComWeight=task_graph_edge_weight[i])  # Communication weight
    assign_distance(task_graph)
    print("TASK GRAPH (TG) IS READY...")
    return task_graph


def generate_random_independent_task_graph(number_of_tasks, wcet_range, release_range):
    task_graph = networkx.DiGraph()
    print("PREPARING RANDOM TASK GRAPH (TG) WITH INDEPENDENT TASKS...")

    task_list = []
    task_criticality_list = []
    task_wcet_list = []
    task_graph_release_list = []
    for i in range(0, number_of_tasks):
        task_list.append(i)
        task_criticality_list.append('L')
        counter = 0
        while counter < Config.NumberOfCriticalTasks:
            chosen_task = random.choice(task_list)
            if task_criticality_list[chosen_task] == 'L':
                task_criticality_list[chosen_task] = 'H'
                counter += 1
        task_wcet_list.append(random.randrange(1, wcet_range))
        task_graph_release_list.append(random.randrange(0, release_range))
    for i in range(0, len(task_list)):
        task_graph.add_node(task_list[i], WCET=task_wcet_list[i], Criticality=task_criticality_list[i],
                            Cluster=None, Node=None, Priority=None, Distance=None, Release=task_graph_release_list[i],
                            Type='App')

    print("RANDOM TASK GRAPH (TG) WITH INDEPENDENT TASKS IS READY...")
    return task_graph


def find_source_nodes(task_graph):
    """
    Takes a Task Graph and returns the source nodes of it in a list
    :param task_graph: Task Graph
    :return: List of source nodes
    """
    source_node = []
    for task in task_graph.nodes():
        if len(task_graph.predecessors(task)) == 0:
            source_node.append(task)
    return source_node


def assign_distance(task_graph):
    print("ASSIGNING PRIORITIES TO TASK GRAPH (TG)...")
    source_nodes = find_source_nodes(task_graph)
    for task in source_nodes:
        task_graph.node[task]['Distance'] = 0

    for task in task_graph.nodes():
        distance = []
        if task not in source_nodes:
            for Source in source_nodes:
                if networkx.has_path(task_graph, Source, task):
                    # shortest_paths=networkx.shortest_path(task_graph, Source, task)
                    # distance.append(len(shortest_paths)-1)
                    for path in networkx.all_simple_paths(task_graph, Source, task):
                        distance.append(len(path))
            task_graph.node[task]['Distance'] = max(distance)-1
    return None


########################################################
def generate_task_graph():
    if Config.TG_Type == 'RandomDependent':
        return generate_random_task_graph(Config.NumberOfTasks, Config.NumberOfCriticalTasks, Config.NumberOfEdges,
                                          Config.WCET_Range, Config.EdgeWeightRange)
    elif Config.TG_Type == 'RandomIndependent':
        return generate_random_independent_task_graph(Config.NumberOfTasks, Config.WCET_Range, Config.Release_Range)
    elif Config.TG_Type == 'Manual':
        return generate_manual_task_graph(Config.Task_List, Config.TG_Edge_List,
                                          Config.Task_Criticality_List, Config.Task_WCET_List, Config.TG_Edge_Weight)
    elif Config.TG_Type == 'FromDOTFile':
        return TG_File_Parser.generate_task_graph_from_dot(Config.TG_DOT_Path)
    else:
        raise ValueError('TG TYPE DOESNT EXIST...!!!')


########################################################
def calculate_max_distance(task_graph):
    max_distance = 0
    for Task in task_graph:
        if task_graph.node[Task]['Distance'] > max_distance:
            max_distance = task_graph.node[Task]['Distance']
    return max_distance


########################################################
def tasks_communication_weight(task_graph):
    """
    :param task_graph: Task graph
    :return: Returns a dictionary with task numbers as keys and total communication relevant to that task as value
    """
    tasks_com = {}
    for task in task_graph.nodes():
        task_com = 0
        for links in task_graph.edges():
            if task in links:
                task_com += task_graph.edge[links[0]][links[1]]["ComWeight"]
        tasks_com[task] = task_com
    return tasks_com
