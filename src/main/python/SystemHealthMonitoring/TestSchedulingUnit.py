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
import random
from TaskGraphUtilities.TG_Functions import Task

def gen_one_step_diagnosable_pmcg(ag, shm):
    """

    :param ag: Architecture Unit
    :param shm: System Health Map
    :return:
    """
    print ("===========================================")
    print ("PREPARING ONE STEP DIAGNOSABLE PMC GRAPH (PMCG)...")
    pmcg = networkx.DiGraph()
    for PE in ag.nodes():
        if shm.node[PE]['NodeHealth']:
            pmcg.add_node(PE)

    # we would like to have one-step t-fault diagnosable system
    n = len(pmcg.nodes())     # number of processors in the system
    delta = 2

    # One-step t-fault diagnosable system S is called optimal if
    # n = 2*t + 1 and each unit is tested exactly by t units.
    if Config.TFaultDiagnosable is not None:
        t = Config.TFaultDiagnosable
    else:
        t = int((n-1)/2)

    # before reading this, please read the comment next to this part... about delta_m
    # If we have a system D_delta,t then
    # (delta, n) = 1  ===>  1. S is one-step t-fault diagnosable
    #                       2. D_delta,t, is an optimal design.
    for i in range(0, n):
        if gcd(delta, n) == 1:
            break
        delta += 1

    # A system S is said to belong to a design D_delta,t
    # link from u_i to u_j exists if and only if <===> j-i = delta*m (modulo n) and m in [1,2,...,t]
    delta_m = []
    for m in range(1, t+1):
        if (delta*m % n) not in delta_m:
            delta_m.append(delta*m % n)

    for TesterNode in pmcg.nodes():
        for TestedNode in pmcg.nodes():
            if (TesterNode - TestedNode) % n in delta_m:
                # print "Connecting:",TesterNode, "to", TestedNode, "---> i-j = ", (TesterNode - TestedNode)%n, "mod", n
                pmcg.add_edge(TesterNode, TestedNode, Weight=0)
    print ("PMC GRAPH (PMCG) IS READY...")
    return pmcg


def gen_sequentially_diagnosable_pmcg(ag, shm):
    print ("===========================================")
    print ("PREPARING SEQUENTIALLY DIAGNOSABLE PMC GRAPH (PMCG)...")
    pmcg = networkx.DiGraph()
    for PE in ag.nodes():
        if shm.node[PE]['NodeHealth']:
            pmcg.add_node(PE)

    n = len(pmcg.nodes())     # number of processors in the system
    # the theorem says there is a a sequentially diagnosable system with    N = n+2t-2

    if Config.TFaultDiagnosable is not None:
        t = Config.TFaultDiagnosable
    else:
        t = int((n-1)/2)

    for TesterNode in pmcg.nodes():
        for TestedNode in pmcg.nodes():
            if (TesterNode - TestedNode) % n == 1:
                pmcg.add_edge(TesterNode, TestedNode, Weight=0)

    counter = 0
    chosen_tested_node = pmcg.nodes()[0]
    while counter < 2*t-2:
        chosen_tester = random.choice(pmcg.nodes())
        # print (chosen_tester, counter)
        if chosen_tester != 0 and chosen_tester != n-1 and (chosen_tester, chosen_tested_node) not in pmcg.edges():
            pmcg.add_edge(chosen_tester, chosen_tested_node, Weight=0)
            counter += 1
    return pmcg


def generate_test_tg_from_pmcg(pmcg):
    """
    Generates a test task graph to be scheduled in between the Tasks from TG on the
    Network to support pmcg. each edge in pmcg turns into a pair of tasks for a specific
    functional test to be mapped on the network.
    :param pmcg: PMC Graph
    :return: Test Task Graph
    """
    ttg = networkx.DiGraph()
    for edge in pmcg.edges():
        ttg.add_node("S"+str(edge[0])+str(edge[1]), task=Task(wcet=Config.NodeTestExeTime, criticality='L',
                                                              cluster=None, node=edge[1], priority=None, distance=0,
                                                              release=0, type='Test'))

        ttg.add_node("R"+str(edge[0])+str(edge[1]), task=Task(wcet=1, criticality='L',
                                                              cluster=None, node=edge[0], priority=None, distance=1,
                                                              release=0, type='Test'))
        ttg.add_edge("S"+str(edge[0])+str(edge[1]), "R"+str(edge[0])+str(edge[1]), ComWeight=Config.NodeTestComWeight,
                     Criticality='L', Link=[])
    return ttg


def insert_test_tasks_in_tg(pmcg, tg):
    # I don't know how we can use this at the moment!
    print ("===========================================")
    print ("INSERTING PMC TASKS FROM TG...")

    for edge in pmcg.edges():
        tg.add_node("S"+str(edge[0])+str(edge[1]), task=Task(wcet=Config.NodeTestExeTime, criticality='L',
                                                              cluster=None, node=edge[1], priority=None, distance=0,
                                                              release=0, type='Test'))

        tg.add_node("R"+str(edge[0])+str(edge[1]), task=Task(wcet=1, criticality='L',
                                                              cluster=None, node=edge[0], priority=None, distance=1,
                                                              release=0, type='Test'))
        tg.add_edge("S"+str(edge[0])+str(edge[1]), "R"+str(edge[0])+str(edge[1]), ComWeight=Config.NodeTestComWeight,
                     Criticality='L', Link=[])

    #for edge in pmcg.edges():
    #    tg.add_node("S"+str(edge[0])+str(edge[1]), Criticality='L', WCET=Config.NodeTestExeTime, Node=edge[1],
    #                Cluster=None, Priority=None, Distance=0, Release=0, Type='Test')
    #    tg.add_node("R"+str(edge[0])+str(edge[1]), Criticality='L', WCET=1, Node=edge[0], Cluster=None,
    #                Priority=None, Distance=1, Release=0, Type='Test')
    #    tg.add_edge("S"+str(edge[0])+str(edge[1]), "R"+str(edge[0])+str(edge[1]), ComWeight=Config.NodeTestComWeight,
    #                Criticality='L', Link=[])
    return tg


def remove_test_tasks_from_tg(tg):
    # I don't know how we can use this at the moment!
    print ("===========================================")
    print ("REMOVING PMC TASKS FROM TG...")
    for task_id in tg.nodes():
        if tg.node[task_id]['task'].type == 'Test':
            tg.remove_node(task_id)
    return tg


def map_test_tasks(tg, ag, shm, noc_rg, logging):
    """

    :param tg: Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param noc_rg: NoC Routing GRaph
    :param logging: logging file
    :return: None
    """
    for task_id in tg.nodes():
        if tg.node[task_id]['task'].type == 'Test':
            node = tg.node[task_id]['task'].node
            if not Mapping_Functions.map_task_to_node(tg, ag, shm, noc_rg, None, None, task_id, node, logging):
                raise ValueError(" MAPPING TEST TASK FAILED WHILE TYING TO MAP ", task_id, "ON NODE", node)
    return None


def draw_pmcg(pmcg):
    print ("===========================================")
    print ("PREPARING PMC GRAPH (PMCG) DRAWINGS...")
    pos = networkx.circular_layout(pmcg)
    networkx.draw_networkx_nodes(pmcg, pos, node_size=300, color='b')
    networkx.draw_networkx_edges(pmcg, pos)
    networkx.draw_networkx_labels(pmcg, pos)
    plt.savefig("GraphDrawings/PMCG")
    plt.clf()
    print ("\033[35m* VIZ::\033[0m PMC GRAPH (PMCG) DRAWING CREATED AT:  GraphDrawings/PMCG.png")
    return None


def draw_ttg(ttg):
    print ("===========================================")
    print ("PREPARING TEST TASK GRAPH (TTG) DRAWINGS...")

    pos = networkx.circular_layout(ttg, scale=6)
    networkx.draw_networkx_nodes(ttg, pos, node_size=200, color='b')
    networkx.draw_networkx_edges(ttg, pos)
    networkx.draw_networkx_labels(ttg, pos, font_size=8)
    plt.savefig("GraphDrawings/TTG")
    plt.clf()
    print ("\033[35m* VIZ::\033[0m TEST TASK GRAPH (TTG) DRAWING CREATED AT: GraphDrawings/TTG.png")
    return None
