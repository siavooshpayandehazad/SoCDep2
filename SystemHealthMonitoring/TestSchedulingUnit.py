# Copyright (C) 2015 Siavoosh Payandeh Azad

# This part of the project is based on 1967 research paper:
# "On the Connection Assignment Problem of Diagnosable Systems", by
# FRANCO P. PREPARATA, GERNOT METZE  AND ROBERT T. CHIEN

import networkx
from fractions import gcd
import matplotlib.pyplot as plt
from ConfigAndPackages import Config

def GeneratePMCG(AG):
    print "==========================================="
    print "PREPARING PMC GRAPH (PMCG)..."
    PMCG = networkx.DiGraph()
    for PE in AG.nodes():
        PMCG.add_node(PE)

    # we would like to have one-step t-fault diagnosable system
    n = len(AG.nodes())     # number of processors in the system
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
        # print delta*m % n
        if (delta*m % n) in delta_M:
            pass
        else:
            delta_M.append(delta*m % n)

    # print "n:", n, "t:", t, "delta:", delta
    # print "delta*M: ", delta_M , "mod", n

    for TesterNode in AG.nodes():
        for TestedNode in AG.nodes():
            if (TesterNode - TestedNode)%n in delta_M:
                #print "Connecting:",TesterNode, "to", TestedNode, "---> i-j = ", (TesterNode - TestedNode)%n, "mod", n
                PMCG.add_edge(TesterNode, TestedNode, Weight=0)
    print "PMC GRAPH (PMCG) IS READY..."
    return PMCG

def DrawPMCG(PMCG):
    print "==========================================="
    print "PREPARING PMC GRAPH (PMCG) DRAWINGS..."
    pos = networkx.shell_layout(PMCG)
    networkx.draw_networkx_nodes(PMCG, pos, node_size=500)
    networkx.draw_networkx_edges(PMCG, pos)
    networkx.draw_networkx_labels(PMCG, pos)
    plt.savefig("GraphDrawings/PMCG")
    plt.clf()
    print "PMC GRAPH (PMCG) DRAWING IS READY..."
    return None