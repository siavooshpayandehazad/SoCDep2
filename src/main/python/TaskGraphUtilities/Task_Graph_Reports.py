# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import matplotlib.pyplot as plt
from ConfigAndPackages import Config
import TG_Functions


def report_task_graph(tg, logging):
    print ("===========================================")
    print ("      REPORTING TASK GRAPH")
    print ("===========================================")
    logging.info('TASK GRAPH REPORT:')
    logging.info('TASK GRAPH Type:\t'+str(Config.tg.type))
    for Node in tg.nodes():
        massage = "TASK:"+str(Node)+"\tWCET:"+str(tg.node[Node]['task'].wcet)+"\tCRITICALITY:" +\
                  str(tg.node[Node]['task'].criticality)+"\tCLUSTER:"+str(tg.node[Node]['task'].cluster) +\
                  "\tNODE:"+str(tg.node[Node]['task'].node)+"\tPRIORITY:"+str(tg.node[Node]['task'].priority) +\
                  "\tRELEASE:"+str(tg.node[Node]['task'].release)
        logging.info(massage)
        print (massage)
    print ("====================")
    print ("EDGES:")
    for Edge in tg.edges():
        massage = "EDGE: "+str(Edge)+"\tCRITICALITY: "+str(tg.edge[Edge[0]][Edge[1]]['Criticality'])+"\tLINK: " +\
                  str(tg.edge[Edge[0]][Edge[1]]['Link'])+"\tCOM WEIGHTt: "+str(tg.edge[Edge[0]][Edge[1]]['ComWeight'])
        logging.info(massage)
        print (massage)
    number_of_flits = 0
    for Edge in tg.edges():
        number_of_flits += tg.edge[Edge[0]][Edge[1]]['ComWeight']
    print "# OF FLITS:", number_of_flits
    print "# OF PACKETS:", len(tg.edges())
    return None


def draw_task_graph(tg, ttg=None):
    print ("DRAWING TASK GRAPH...")
    plt.figure()
    node_colors = []
    for Node in tg.nodes():
        if tg.node[Node]['task'].criticality == 'H':
            node_colors.append('#FF878B')
        elif tg.node[Node]['task'].criticality == 'GH':
            node_colors.append('#FFC29C')
        elif tg.node[Node]['task'].criticality == 'GNH':
            node_colors.append('#928AFF')
        else:
            node_colors.append('#A0CBE2')
    edge_colors = []
    for Edge in tg.edges():
        if tg.edge[Edge[0]][Edge[1]]['Criticality'] == 'H':
            edge_colors.append('red')
        else:
            edge_colors.append('black')
    tg_edge_list = []
    tg_edge_weight = []
    for Edge in tg.edges():
        tg_edge_list.append(Edge)
        tg_edge_weight.append(tg.edge[Edge[0]][Edge[1]]['ComWeight'])

    if Config.tg.type == "RandomIndependent":
        pos = networkx.shell_layout(tg)
    else:
        width = 1000
        height = 10000
        pos = {}
        max_distance = TG_Functions.calculate_max_distance(tg)
        for current_distance in range(0, max_distance+1):
            num_tasks_with_same_distance = 0
            for node in tg.nodes():
                if tg.node[node]['task'].type == 'App':
                    distance = tg.node[node]['task'].distance
                    if current_distance == distance:
                        num_tasks_with_same_distance += 1
            counter = 0
            for node in tg.nodes():
                if tg.node[node]['task'].type == 'App':
                    distance = tg.node[node]['task'].distance
                    if current_distance == distance:
                        counter += 1
                        pos[node] = (counter*(width/num_tasks_with_same_distance)+width,
                                     (max_distance-current_distance)*height/max_distance)
        if ttg is not None:
            temp_pos = networkx.shell_layout(ttg)
            for test_node in tg.nodes():
                if tg.node[test_node]['task'].type == 'Test':
                    pos[test_node] = [temp_pos[test_node][0]*(width/2)+width/2, 
                                      temp_pos[test_node][1]*(height/2)+height/2]

    networkx.draw_networkx_nodes(tg, pos, with_labels=True, node_color=node_colors, node_size=50)
    networkx.draw_networkx_edges(tg, pos, edge_color=tg_edge_weight, edge_cmap=plt.cm.Reds, width=3, arrows=False)
    networkx.draw_networkx_edges(tg, pos,  arrows=False, width=0.5)
    networkx.draw_networkx_labels(tg, pos, font_size=4)
    # networkx.draw_networkx_edge_labels(TG, pos, edge_labels=dict(zip(tg_edge_list, tg_edge_weight)),
    #                                    font_size=10, label_pos=0.7)
    if ttg is None:
        plt.savefig("GraphDrawings/TG.png", dpi=200, bbox_inches='tight')
    else:
        plt.savefig("GraphDrawings/TG_And_TTG.png", dpi=200, bbox_inches='tight')
    plt.clf()
    print ("\033[35m* VIZ::\033[0mTASK GRAPH DRAWINGS CREATED AT: GraphDrawings/TG.png")
    return None