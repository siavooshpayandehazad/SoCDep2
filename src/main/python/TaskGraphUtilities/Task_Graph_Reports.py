# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import matplotlib.pyplot as plt
from ConfigAndPackages import Config
import TG_Functions


def ReportTaskGraph(tg, logging):
    print ("===========================================")
    print ("      REPORTING TASK GRAPH")
    print ("===========================================")
    logging.info('TASK GRAPH REPORT:')
    logging.info('TASK GRAPH Type:\t'+str(Config.TG_Type))
    for Node in tg.nodes():
        massage = "TASK:"+str(Node)+"\tWCET:"+ str(tg.node[Node]['WCET'])+"\tCRITICALITY:"+str(tg.node[Node]['Criticality'])+\
            "\tCLUSTER:"+str(tg.node[Node]['Cluster'])+"\tNODE:"+str(tg.node[Node]['Node'])+"\tPRIORITY:"+\
                  str(tg.node[Node]['Priority']) + "\tRELEASE:"+str(tg.node[Node]['Release'])
        logging.info(massage)
        print (massage)
    print ("====================")
    print ("EDGES:")
    for Edge in tg.edges():
        massage= "EDGE: "+str(Edge)+"\tCRITICALITY: "+str(tg.edge[Edge[0]][Edge[1]]['Criticality'])+"\tLINK: "+\
                str(tg.edge[Edge[0]][Edge[1]]['Link'])+"\tCOM WEIGHTt: "+str(tg.edge[Edge[0]][Edge[1]]['ComWeight'])
        logging.info(massage)
        print (massage)
    return None

def DrawTaskGraph(tg, ttg=None):
    print ("DRAWING TASK GRAPH...")
    fig = plt.figure()
    NodeColors=[]
    for Node in tg.nodes():
        if tg.node[Node]['Criticality']== 'H':
            NodeColors.append('#FF878B')
        elif tg.node[Node]['Criticality']== 'GH':
            NodeColors.append('#FFC29C')
        elif tg.node[Node]['Criticality']== 'GNH':
            NodeColors.append('#928AFF')
        else:
            NodeColors.append('#A0CBE2')
    Edge_Colors=[]
    for Edge in tg.edges():
        if tg.edge[Edge[0]][Edge[1]]['Criticality']== 'H':
            Edge_Colors.append('red')
        else:
            Edge_Colors.append('black')
    TG_Edge_List=[]
    TG_Edge_Weight=[]
    for Edge in tg.edges():
        TG_Edge_List.append(Edge)
        TG_Edge_Weight.append(tg.edge[Edge[0]][Edge[1]]['ComWeight'])


    if Config.TG_Type == "RandomIndependent":
        pos=networkx.shell_layout(tg)
    else:
        width = 1000
        height = 10000
        pos = {}
        MaxDistance = TG_Functions.calculate_max_distance(tg)
        for CurrentDistance in range(0, MaxDistance+1):
            NumTasksWithSameDistance = 0
            for node in tg.nodes():
                if tg.node[node]['Type'] == 'App':
                    Distance=tg.node[node]['Distance']
                    if CurrentDistance == Distance:
                        NumTasksWithSameDistance+=1

            Counter = 0
            for node in tg.nodes():
                if tg.node[node]['Type'] == 'App':
                    Distance=tg.node[node]['Distance']
                    if CurrentDistance == Distance:
                        Counter+=1
                        pos[node] = (Counter*(width/NumTasksWithSameDistance)+width,
                                     (MaxDistance-CurrentDistance)*height/MaxDistance)
        if ttg is not None:
            TempPos=networkx.shell_layout(ttg)
            for TestNode in tg.nodes():
                if tg.node[TestNode]['Type'] == 'Test':
                    pos[TestNode] = [TempPos[TestNode][0]*(width/2)+width/2,
                                       TempPos[TestNode][1]*(height/2)+height/2]

    networkx.draw_networkx_nodes(tg, pos, with_labels=True, node_color=NodeColors, node_size= 50)
    networkx.draw_networkx_edges(tg, pos, edge_color=TG_Edge_Weight, edge_cmap=plt.cm.Reds, width=3, arrows= False)
    networkx.draw_networkx_edges(tg, pos,  arrows= False, width=0.5)
    networkx.draw_networkx_labels(tg, pos, font_size=4)
    #networkx.draw_networkx_edge_labels(TG, pos, edge_labels=dict(zip(TG_Edge_List, TG_Edge_Weight)), font_size=10, label_pos=0.7)

    if ttg is None:
        plt.savefig("GraphDrawings/TG.png", dpi=200)
    else:
        plt.savefig("GraphDrawings/TG_And_TTG.png", dpi=200)
    plt.clf()
    print ("\033[35m* VIZ::\033[0mTASK GRAPH DRAWINGS CREATED AT: GraphDrawings/TG.png")
    return None

