# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import TG_Functions


def generate_tg_from_xml():
    tg = networkx.DiGraph()
    print("PREPARING TASK GRAPH (TG) FROM XML FILE...")
    # Todo...
    return tg


def generate_tg_from_dot(file_path):
    tg = networkx.DiGraph()
    print("PREPARING TASK GRAPH (TG) FROM DOT FILE...")

    try:
        tg_dot_file = open(file_path, 'r')
        while True:
            line = tg_dot_file.readline()
            if "->" in line:
                edge_list = line.split()
                # print EdgeList[0], EdgeList[2], EdgeList[6]
                if edge_list[0] not in tg.nodes():
                    tg.add_node(edge_list[0], WCET=1, Criticality='L', Cluster=None, Node=None, Priority=None,
                                Distance=None, Release=0, Type='App')
                if edge_list[2] not in tg.nodes():
                    tg.add_node(edge_list[2], WCET=1, Criticality='L', Cluster=None, Node=None, Priority=None,
                                Distance=None, Release=0, Type='App')
                # TODO: the edge weight is not correct... it should depend on the amount of data instead of being
                # constant ...
                communication_weight = 1
                tg.add_edge(edge_list[0], edge_list[2], Criticality='L', Link=[],
                            ComWeight=communication_weight)
            if line == '':
                break
    except IOError:
        raise ValueError('CAN NOT OPEN', file_path)
    TG_Functions.assign_distance(tg)
    print("TASK GRAPH (TG) IS READY...")
    return tg