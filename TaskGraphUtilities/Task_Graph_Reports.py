__author__ = 'siavoosh'
import networkx
import matplotlib.pyplot as plt

def ReportTaskGraph(TG):
    print "==========================================="
    print "      REPORTING TASK GRAPH"
    print "==========================================="
    for Node in TG.nodes():
        print "TASK:",Node,"\tWCET:", TG.node[Node]['WCET'],"\tCRITICALITY:",TG.node[Node]['Criticality'],\
            "\tCLUSTER:",TG.node[Node]['Cluster'],"\tNODE:",TG.node[Node]['Node'],"PRIORITY:",TG.node[Node]['Priority']
    print "===================="
    for Edge in TG.edges():
        print "EDGE:", Edge,"\tCRITICALITY:",TG.edge[Edge[0]][Edge[1]]['Criticality'],"\tLINK:",\
            TG.edge[Edge[0]][Edge[1]]['Link'], "\tCOM WEIGHTt:",TG.edge[Edge[0]][Edge[1]]['ComWeight']
    print "==========================================="
    return None

def DrawTaskGraph(TG,TG_Edge_List,TG_Edge_Weight):
    NodeColors=[]
    for Node in TG.nodes():
        if TG.node[Node]['Criticality']== 'H':
            NodeColors.append('r')
        else:
            NodeColors.append('b')
    pos=networkx.shell_layout(TG)
    networkx.draw_networkx_nodes(TG,pos,with_labels=True,node_color=NodeColors)
    networkx.draw_networkx_edges(TG,pos)
    networkx.draw_networkx_labels(TG,pos)
    networkx.draw_networkx_edge_labels(TG,pos,edge_labels=dict(zip(TG_Edge_List, TG_Edge_Weight)))
    plt.savefig("GraphDrawings/TG.png")
    plt.clf()
    return None