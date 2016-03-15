# Copyright (C) 2015 Siavoosh Payandeh Azad


import networkx
import matplotlib.pyplot as plt


def report_ctg(ctg, filename):
    """
    Reports Clustered Task Graph in the Console and draws CTG in file
    :param ctg: clustered task graph
    :param filename: drawing file name
    :return: None
    """
    print "==========================================="
    print "      REPORTING CLUSTERED TASK GRAPH"
    print "==========================================="
    cluster_task_list_dict = {}
    cluster_weight_dict = {}
    for node in ctg.nodes():
        print ("\tCLUSTER #: "+str(node)+"\tTASKS:"+str(ctg.node[node]['TaskList'])+"\tUTILIZATION: " +
               str(ctg.node[node]['Utilization']))
        cluster_task_list_dict[node] = ctg.node[node]['TaskList']
    for edge in ctg.edges():
        print ("\tEDGE #: "+str(edge)+"\tWEIGHT: "+str(ctg.edge[edge[0]][edge[1]]['Weight']))
        cluster_weight_dict[edge] = ctg.edge[edge[0]][edge[1]]['Weight']
    print ("PREPARING GRAPH DRAWINGS...")
    pos = networkx.shell_layout(ctg)
    networkx.draw_networkx_nodes(ctg, pos, node_size=2200, node_color='#FAA5A5')
    networkx.draw_networkx_edges(ctg, pos)
    networkx.draw_networkx_edge_labels(ctg, pos, edge_labels=cluster_weight_dict)
    networkx.draw_networkx_labels(ctg, pos, labels=cluster_task_list_dict)
    plt.savefig("GraphDrawings/"+filename)
    plt.clf()
    print ("\033[35m* VIZ::\033[0mGRAPH DRAWINGS DONE, CHECK \"GraphDrawings/"+filename+"\"")
    return None


def viz_clustering_opt():
    """
    Visualizes the cost of solutions during clustering optimization process
    :return: None
    """
    print ("===========================================")
    print ("GENERATING CLUSTERING OPTIMIZATION VISUALIZATIONS...")

    try:
        clustering_cost_file = open('Generated_Files/Internal/ClusteringCost.txt', 'r')
        cost = []
        line = clustering_cost_file.readline()
        cost.append(float(line))
        min_cost = float(line)
        min_cost_list = [min_cost]
        while line != "":
            cost.append(float(line))
            if float(line) < min_cost:
                min_cost = float(line)
            min_cost_list.append(min_cost)
            line = clustering_cost_file.readline()
        solution_num = range(0, len(cost))
        clustering_cost_file.close()
        plt.plot(solution_num, cost, '#5095FD', solution_num, min_cost_list, 'r')
        plt.savefig("GraphDrawings/CTG_Opt_Process.png", dpi=300)
        plt.clf()
        print ("\033[35m* VIZ::\033[0mCLUSTERING OPTIMIZATION PROCESS CREATED AT: GraphDrawings/CTG_Opt_Process.png")
    except IOError:
        print ('CAN NOT OPEN ClusteringCost.txt')
    return None