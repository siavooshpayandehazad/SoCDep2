# Copyright (C) 2015 Siavoosh Payandeh Azad

# This part of the project is based on 1967 research paper:
# "On the Connection Assignment Problem of Diagnosable Systems", by
# FRANCO P. PREPARATA, GERNOT METZE  AND ROBERT T. CHIEN
# all the variable names are the same as in the paper...

import networkx
from fractions import gcd
import matplotlib.pyplot as plt
from ConfigAndPackages import Config
from Mapper import Mapping_Functions
import random, copy

def GenerateOneStepDiagnosablePMCG(AG,SHM):
    print ("===========================================")
    print ("PREPARING ONE STEP DIAGNOSABLE PMC GRAPH (PMCG)...")
    PMCG = networkx.DiGraph()
    for PE in AG.nodes():
        if SHM.SHM.node[PE]['NodeHealth']:
            PMCG.add_node(PE)

    # we would like to have one-step t-fault diagnosable system
    n = len(PMCG.nodes())     # number of processors in the system
    delta = 2

    # One-step t-fault diagnosable system S is called optimal if
    # n = 2*t + 1 and each unit is tested exactly by t units.
    if Config.TFaultDiagnosable is not None:
        t = Config.TFaultDiagnosable
    else:
        t = int((n-1)/2)

    # before reading this, please read the comment next to this part... about delta_M
    # If we have a system D_delta,t then
    # (delta, n) = 1  ===>  1. S is one-step t-fault diagnosable
    #                       2. D_delta,t, is an optimal design.
    for i in range(0,n):
        if gcd(delta,n) == 1:
            break
        delta += 1

    # A system S is said to belong to a design D_delta,t
    # link from u_i to u_j exists if and only if <===> j-i = delta*m (modulo n) and m in [1,2,...,t]
    delta_M = []
    for m in range(1, t+1):
        if (delta*m % n) not in delta_M:
            delta_M.append(delta*m % n)

    for TesterNode in PMCG.nodes():
        for TestedNode in PMCG.nodes():
            if (TesterNode - TestedNode)%n in delta_M:
                #print "Connecting:",TesterNode, "to", TestedNode, "---> i-j = ", (TesterNode - TestedNode)%n, "mod", n
                PMCG.add_edge(TesterNode, TestedNode, Weight=0)
    print ("PMC GRAPH (PMCG) IS READY...")
    return PMCG



def GenerateSequentiallyDiagnosablePMCG(AG,SHM):
    print ("===========================================")
    print ("PREPARING SEQUENTIALLY DIAGNOSABLE PMC GRAPH (PMCG)...")
    PMCG = networkx.DiGraph()
    for PE in AG.nodes():
        if SHM.SHM.node[PE]['NodeHealth']:
            PMCG.add_node(PE)

    n = len(PMCG.nodes())     # number of processors in the system
    # the theorem says there is a a sequentially diagnosable system with    N = n+2t-2

    if Config.TFaultDiagnosable is not None:
        t = Config.TFaultDiagnosable
    else:
        t = int((n-1)/2)

    for TesterNode in PMCG.nodes():
        for TestedNode in PMCG.nodes():
            if (TesterNode - TestedNode)%n == 1:
                PMCG.add_edge(TesterNode, TestedNode, Weight=0)

    Counter = 0
    ChosenTestedNode = PMCG.nodes()[0]
    while Counter < 2*t-2:
        ChosenTester = random.choice(PMCG.nodes())
        # print (ChosenTester, Counter)
        if ChosenTester != 0 and ChosenTester != n-1 and (ChosenTester,ChosenTestedNode) not in PMCG.edges():
            PMCG.add_edge(ChosenTester, ChosenTestedNode, Weight=0)
            Counter += 1
    return PMCG



def GenerateTestTGFromPMCG(PMCG):
    """
    Generates a test task graph to be scheduled in between the Tasks from TG on the
    Network to support PMCG. each edge in PMCG turns into a pair of tasks for a specific
    functional test to be mapped on the network.
    :param PMCG: PMC Graph
    :return: Test Task Graph
    """
    TTG = networkx.DiGraph()
    for edge in PMCG.edges():
        TTG.add_node("S"+str(edge[0])+str(edge[1]), Criticality='L', WCET=Config.NodeTestExeTime, Node=edge[1],
                     Cluster=None, Priority=None, Distance=0 , Release=0, Type= 'Test')
        TTG.add_node("R"+str(edge[0])+str(edge[1]), Criticality='L', WCET=1, Node=edge[0], Cluster=None,
                     Priority=None, Distance=1 , Release=0, Type= 'Test')
        TTG.add_edge("S"+str(edge[0])+str(edge[1]), "R"+str(edge[0])+str(edge[1]), ComWeight=Config.NodeTestComWeight,
                     Criticality='L', Link=[])
    return TTG


def InsertTestTasksInTG(PMCG, TG):
    # I dont know how we can use this at the moment!
    print ("===========================================")
    print ("INSERTING PMC TASKS FROM TG...")
    for edge in PMCG.edges():
        TG.add_node("S"+str(edge[0])+str(edge[1]), Criticality='L', WCET=Config.NodeTestExeTime, Node=edge[1],
                    Cluster=None, Priority=None, Distance=0 , Release=0, Type= 'Test')
        TG.add_node("R"+str(edge[0])+str(edge[1]), Criticality='L', WCET=1, Node=edge[0], Cluster=None,
                    Priority=None, Distance=1 , Release=0, Type= 'Test')
        TG.add_edge("S"+str(edge[0])+str(edge[1]), "R"+str(edge[0])+str(edge[1]), ComWeight=Config.NodeTestComWeight,
                    Criticality='L', Link=[])
    return TG


def RemoveTestTasksFromTG(TG):
    # I dont know how we can use this at the moment!
    print ("===========================================")
    print ("REMOVING PMC TASKS FROM TG...")
    for Task in TG.nodes():
        if TG.node[Task]['Type'] == 'Test':
            TG.remove_node(Task)
    return TG

def MapTestTasks(TG, AG, SHM, NoCRG, logging):
    for Task in TG.nodes():
        if TG.node[Task]['Type'] == 'Test':
            Node = TG.node[Task]['Node']
            Mapping_Functions.MapTaskToNode(TG, AG, SHM, NoCRG, None, None, Task, Node, logging)
    pass

def DrawPMCG(PMCG):
    print ("===========================================")
    print ("PREPARING PMC GRAPH (PMCG) DRAWINGS...")
    pos = networkx.circular_layout(PMCG)
    networkx.draw_networkx_nodes(PMCG, pos, node_size=500, color='b')
    networkx.draw_networkx_edges(PMCG, pos)
    networkx.draw_networkx_labels(PMCG, pos)
    plt.savefig("GraphDrawings/PMCG")
    plt.clf()
    print ("\033[35m* VIZ::\033[0m PMC GRAPH (PMCG) DRAWING CREATED AT:  GraphDrawings/PMCG.png")
    return None

def DrawTTG(TTG):
    print ("===========================================")
    print ("PREPARING TEST TASK GRAPH (TTG) DRAWINGS...")
    pos = networkx.circular_layout(TTG)
    networkx.draw_networkx_nodes(TTG, pos, node_size=500, color='b')
    networkx.draw_networkx_edges(TTG, pos)
    networkx.draw_networkx_labels(TTG, pos)
    plt.savefig("GraphDrawings/TTG")
    plt.clf()
    print ("\033[35m* VIZ::\033[0m TEST TASK GRAPH (TTG) DRAWING CREATED AT: GraphDrawings/TTG.png")
    return None

# TODO: Schedule TTG
# we probably need to add a type as attribute to the tasks, which shows if
# they belong to testing or normal operation...
