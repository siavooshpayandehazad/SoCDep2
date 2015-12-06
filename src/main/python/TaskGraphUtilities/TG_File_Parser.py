# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import TG_Functions

def GenerateTGFromXML(FilePath):
    TG = networkx.DiGraph()
    print("PREPARING TASK GRAPH (TG) FROM XML FILE...")
    # Todo...
    return TG

def GenerateTGFromDOT(FilePath):
    TG = networkx.DiGraph()
    print("PREPARING TASK GRAPH (TG) FROM DOT FILE...")

    try:
        TG_DOT_File = open(FilePath, 'r')
        while True:
            line = TG_DOT_File.readline()
            if "->" in line:
                EdgeList = line.split()
                # print EdgeList[0], EdgeList[2], EdgeList[6]
                if EdgeList[0] not in TG.nodes():
                    TG.add_node(EdgeList[0], WCET=1, Criticality='L', Cluster=None, Node=None, Priority=None,
                                Distance=None, Release=0, Type='App')
                if EdgeList[2] not in TG.nodes():
                    TG.add_node(EdgeList[2], WCET=1, Criticality='L', Cluster=None, Node=None, Priority=None,
                                Distance=None, Release=0, Type='App')
                # TODO: the edge weight is not correct... i should think about it...
                CommunicationWeight = 1
                TG.add_edge(EdgeList[0], EdgeList[2], Criticality='L', Link=[], ComWeight=CommunicationWeight)
            if line == '':
                break
    except IOError:
        raise ValueError('CAN NOT OPEN', FilePath)
    TG_Functions.assign_distance(TG)
    print("TASK GRAPH (TG) IS READY...")
    return TG