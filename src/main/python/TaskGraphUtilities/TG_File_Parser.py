# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import TG_Functions


def generate_task_graph_from_xml():
    task_graph = networkx.DiGraph()
    print("PREPARING TASK GRAPH (TG) FROM XML FILE...")
    # Todo...
    return task_graph


def generate_task_graph_from_dot(file_path):
    task_graph = networkx.DiGraph()
    print("PREPARING TASK GRAPH (TG) FROM DOT FILE...")

    try:
        task_graph_dot_file = open(file_path, 'r')
        while True:
            line = task_graph_dot_file.readline()
            if "->" in line:
                edge_list = line.split()
                # print EdgeList[0], EdgeList[2], EdgeList[6]
                if edge_list[0] not in task_graph.nodes():
                    task_graph.add_node(edge_list[0], WCET=1, Criticality='L', Cluster=None, Node=None, Priority=None,
                                        Distance=None, Release=0, Type='App')
                if edge_list[2] not in task_graph.nodes():
                    task_graph.add_node(edge_list[2], WCET=1, Criticality='L', Cluster=None, Node=None, Priority=None,
                                        Distance=None, Release=0, Type='App')
                # TODO: the edge weight is not correct... i should think about it...
                communication_weight = 1
                task_graph.add_edge(edge_list[0], edge_list[2], Criticality='L', Link=[],
                                    ComWeight=communication_weight)
            if line == '':
                break
    except IOError:
        raise ValueError('CAN NOT OPEN', file_path)
    TG_Functions.assign_distance(task_graph)
    print("TASK GRAPH (TG) IS READY...")
    return task_graph