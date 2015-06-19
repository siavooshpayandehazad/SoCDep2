# Copyright (C) 2015 Siavoosh Payandeh Azad


import networkx
import matplotlib.pyplot as plt

def ReportCTG(CTG, filename):
    print "==========================================="
    print "      REPORTING CLUSTERED TASK GRAPH"
    print "==========================================="
    ClusterTaskListDicForDraw = {}
    ClusterWeightDicForDraw = {}
    for node in CTG.nodes():
        print "\tCLUSTER #:", node, "\tTASKS:", CTG.node[node]['TaskList'], "\tUTILIZATION:",CTG.node[node]['Utilization']
        ClusterTaskListDicForDraw[node] = CTG.node[node]['TaskList']
    for edge in CTG.edges():
        print "\tEDGE #:", edge, "\tWEIGHT:", CTG.edge[edge[0]][edge[1]]['Weight']
        ClusterWeightDicForDraw[edge] = CTG.edge[edge[0]][edge[1]]['Weight']
    print "PREPARING GRAPH DRAWINGS..."
    pos = networkx.shell_layout(CTG)
    networkx.draw_networkx_nodes(CTG, pos, node_size=2200)
    networkx.draw_networkx_edges(CTG, pos)
    networkx.draw_networkx_edge_labels(CTG, pos, edge_labels=ClusterWeightDicForDraw)
    networkx.draw_networkx_labels(CTG, pos, labels=ClusterTaskListDicForDraw)
    plt.savefig("GraphDrawings/"+filename)
    plt.clf()
    print "GRAPH DRAWINGS DONE, CHECK \"GraphDrawings/"+filename+"\""
    return None