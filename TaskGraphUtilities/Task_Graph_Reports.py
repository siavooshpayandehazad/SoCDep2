# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import matplotlib.pyplot as plt
import Config
import TG_Functions

def ReportTaskGraph(TG,logging):
    print "==========================================="
    print "      REPORTING TASK GRAPH"
    print "==========================================="
    logging.info('TASK GRAPH REPORT:')
    logging.info('TASK GRAPH Type:\t'+str(Config.TG_Type))
    for Node in TG.nodes():
        massage = "TASK:"+str(Node)+"\tWCET:"+ str(TG.node[Node]['WCET'])+"\tCRITICALITY:"+str(TG.node[Node]['Criticality'])+\
            "\tCLUSTER:"+str(TG.node[Node]['Cluster'])+"\tNODE:"+str(TG.node[Node]['Node'])+"\tPRIORITY:"+\
                  str(TG.node[Node]['Priority']) + "\tRELEASE:"+str(TG.node[Node]['Release'])
        logging.info(massage)
        print massage
    print "===================="
    print "EDGES:"
    for Edge in TG.edges():
        massage= "EDGE:"+ str(Edge)+"\tCRITICALITY:"+str(TG.edge[Edge[0]][Edge[1]]['Criticality'])+"\tLINK:"+\
            str(TG.edge[Edge[0]][Edge[1]]['Link'])+"\tCOM WEIGHTt:"+str(TG.edge[Edge[0]][Edge[1]]['ComWeight'])
        logging.info(massage)
        print massage
    return None

def DrawTaskGraph(TG):
    print "DRAWING TASK GRAPH..."
    NodeColors=[]
    for Node in TG.nodes():
        if TG.node[Node]['Criticality']== 'H':
            NodeColors.append('r')
        else:
            NodeColors.append('#A0CBE2')
    Edge_Colors=[]
    for Edge in TG.edges():
        if TG.edge[Edge[0]][Edge[1]]['Criticality']== 'H':
            Edge_Colors.append('red')
        else:
            Edge_Colors.append('black')
    TG_Edge_List=[]
    TG_Edge_Weight=[]
    for Edge in TG.edges():
        TG_Edge_List.append(Edge)
        TG_Edge_Weight.append(TG.edge[Edge[0]][Edge[1]]['ComWeight'])


    if Config.TG_Type == "RandomIndependent":
        pos=networkx.shell_layout(TG)
    else:
        pos = {}
        MaxDistance = TG_Functions.CalculateMaxDistance(TG)
        for CurrentDistance in range(0,MaxDistance+1):
            Counter = 0
            for node in TG.nodes():
                Distance=TG.node[node]['Distance']
                if CurrentDistance== Distance:
                    Counter+=1
                    pos[node] = (Counter, MaxDistance-CurrentDistance)

    networkx.draw_networkx_nodes(TG,pos,with_labels=True,node_color=NodeColors)
    networkx.draw_networkx_edges(TG,pos,edge_color=Edge_Colors)
    networkx.draw_networkx_labels(TG,pos)
    networkx.draw_networkx_edge_labels(TG,pos,edge_labels=dict(zip(TG_Edge_List, TG_Edge_Weight)))
    plt.savefig("GraphDrawings/TG.png")
    plt.clf()
    print "TASK GRAPH DRAWINGS READY..."
    return None

