# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import matplotlib.pyplot as plt
from ConfigAndPackages import Config
import TG_Functions


def ReportTaskGraph(TG,logging):
    print ("===========================================")
    print ("      REPORTING TASK GRAPH")
    print ("===========================================")
    logging.info('TASK GRAPH REPORT:')
    logging.info('TASK GRAPH Type:\t'+str(Config.TG_Type))
    for Node in TG.nodes():
        massage = "TASK:"+str(Node)+"\tWCET:"+ str(TG.node[Node]['WCET'])+"\tCRITICALITY:"+str(TG.node[Node]['Criticality'])+\
            "\tCLUSTER:"+str(TG.node[Node]['Cluster'])+"\tNODE:"+str(TG.node[Node]['Node'])+"\tPRIORITY:"+\
                  str(TG.node[Node]['Priority']) + "\tRELEASE:"+str(TG.node[Node]['Release'])
        logging.info(massage)
        print (massage)
    print ("====================")
    print ("EDGES:")
    for Edge in TG.edges():
        massage= "EDGE: "+str(Edge)+"\tCRITICALITY: "+str(TG.edge[Edge[0]][Edge[1]]['Criticality'])+"\tLINK: "+\
                str(TG.edge[Edge[0]][Edge[1]]['Link'])+"\tCOM WEIGHTt: "+str(TG.edge[Edge[0]][Edge[1]]['ComWeight'])
        logging.info(massage)
        print (massage)
    return None

def DrawTaskGraph(TG, TTG=None):
    print ("DRAWING TASK GRAPH...")
    fig = plt.figure()
    NodeColors=[]
    for Node in TG.nodes():
        if TG.node[Node]['Criticality']== 'H':
            NodeColors.append('#FF878B')
        elif TG.node[Node]['Criticality']== 'GH':
            NodeColors.append('#FFC29C')
        elif TG.node[Node]['Criticality']== 'GNH':
            NodeColors.append('#928AFF')
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
        width = 1000
        height = 10000
        pos = {}
        MaxDistance = TG_Functions.CalculateMaxDistance(TG)
        for CurrentDistance in range(0, MaxDistance+1):
            NumTasksWithSameDistance = 0
            for node in TG.nodes():
                if TG.node[node]['Type'] == 'App':
                    Distance=TG.node[node]['Distance']
                    if CurrentDistance == Distance:
                        NumTasksWithSameDistance+=1

            Counter = 0
            for node in TG.nodes():
                if TG.node[node]['Type'] == 'App':
                    Distance=TG.node[node]['Distance']
                    if CurrentDistance == Distance:
                        Counter+=1
                        pos[node] = (Counter*(width/NumTasksWithSameDistance)+width,
                                     (MaxDistance-CurrentDistance)*height/MaxDistance)
        if TTG is not None:
            TempPos=networkx.shell_layout(TTG)
            for TestNode in TG.nodes():
                if TG.node[TestNode]['Type'] == 'Test':
                    pos[TestNode] = [TempPos[TestNode][0]*(width/2)+width/2,
                                       TempPos[TestNode][1]*(height/2)+height/2]

    networkx.draw_networkx_nodes(TG, pos, with_labels=True, node_color=NodeColors, node_size= 50)
    networkx.draw_networkx_edges(TG, pos, edge_color=TG_Edge_Weight, edge_cmap=plt.cm.Reds, width=3, arrows= False)
    networkx.draw_networkx_edges(TG, pos,  arrows= False, width=0.5)
    networkx.draw_networkx_labels(TG, pos, font_size=4)
    #networkx.draw_networkx_edge_labels(TG, pos, edge_labels=dict(zip(TG_Edge_List, TG_Edge_Weight)), font_size=10, label_pos=0.7)

    if TTG is None:
        plt.savefig("GraphDrawings/TG.png", dpi=200)
    else:
        plt.savefig("GraphDrawings/TG_And_TTG.png", dpi=200)
    plt.clf()
    print ("\033[35m* VIZ::\033[0mTASK GRAPH DRAWINGS CREATED AT: GraphDrawings/TG.png")
    return None

