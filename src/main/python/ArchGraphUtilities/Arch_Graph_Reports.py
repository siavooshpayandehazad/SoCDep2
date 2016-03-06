# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
import networkx
from ConfigAndPackages import Config
from AG_Functions import return_node_location
import math


def draw_ag(ag, file_name):
    """
    Generates Visualizations of the Architecture Graph and saves it in "GraphDrawings/FileName.png"
    :param ag: Architecture Graph
    :param file_name: Name of the file for saving the graph
    :return: None
    """
    position = {}
    color_list = []

    number_of_layers = Config.ag.z_size
    largest_number = Config.ag.x_size*Config.ag.y_size*Config.ag.z_size - 1
    node_size = math.log10(largest_number)*60
    # print "Node Size", node_size

    node_distance_x = 0.2 * (number_of_layers+1)
    node_distance_y = 0.2 * (number_of_layers+1)

    offset_x = 0.2
    offset_y = 0.2

    plt.figure(num=None, figsize=(3*Config.ag.x_size, 3*Config.ag.y_size), dpi=350)

    for Node in ag.nodes():
        x, y, z = return_node_location(Node)
        position[Node] = [(x*node_distance_x)+(z*offset_x), (y*node_distance_y)+(z*offset_y)]
        # print (x*node_distance_x)+(z*offset_x), (y*node_distance_y)+(z*offset_y)
        if ag.node[Node]['Region'] == 'H':
            color_list.append('#FF878B')
        elif ag.node[Node]['Region'] == 'GH':   # gateway to high critical
            color_list.append('#FFC29C')
        elif ag.node[Node]['Region'] == 'GNH':  # gateway to Non-high critical
            color_list.append('#928AFF')
        else:
            color_list.append('#CFECFF')

    # POS = networkx.spring_layout(AG)

    networkx.draw(ag, pos=position, with_labels=True, node_size=node_size, arrows=True,
                  node_color=color_list, font_size=7, linewidths=1)
    plt.savefig("GraphDrawings/"+file_name+".png")
    plt.clf()
    return None


def draw_vl_opt():
    """
    Draws the cost evolution for the vl optimization
    :return: None
    """
    print ("===========================================")
    print ("GENERATING VL OPTIMIZATION VISUALIZATIONS...")
    fig, ax1 = plt.subplots()
    solution_num = None
    try:
        vl_cost_file = open('Generated_Files/Internal/vl_opt_cost.txt', 'r')
        cost = []
        line = vl_cost_file.readline()
        max_cost = float(line)
        max_cost_list = [max_cost]
        cost.append(float(line))
        while line != "":
            cost.append(float(line))
            if float(line) > max_cost:
                max_cost = float(line)
            max_cost_list.append(max_cost)
            line = vl_cost_file.readline()
        solution_num = range(0, len(cost))
        vl_cost_file.close()
        # print len(solution_num), len(cost)
        ax1.set_ylabel('vl placement Cost')
        ax1.set_xlabel('Iteration #')
        ax1.plot(solution_num, cost, '#5095FD', solution_num, max_cost_list, 'r')

        if Config.vl_opt.vl_opt_alg == 'IterativeLocalSearch':
            for Iteration in range(1, Config.vl_opt.ils_iteration+2):
                x1 = x2 = Iteration * Config.vl_opt.ls_iteration
                y1 = 0
                y2 = max(cost)*1.2
                ax1.plot((x1, x2), (y1, y2), 'g--')

    except IOError:
        print ('CAN NOT OPEN Generated_Files/Internal/vl_opt_cost.txt')

    if Config.vl_opt.vl_opt_alg == 'SimulatedAnnealing':
        try:
            sa_temp_file = open('Generated_Files/Internal/vlp_sa_temp.txt', 'r')
            temp = []
            line = sa_temp_file.readline()
            temp.append(float(line))
            while line != '':
                temp.append(float(line))
                line = sa_temp_file.readline()
            sa_temp_file.close()
            # print len(temp), len(solution_num)
            ax2 = ax1.twinx()
            ax2.plot(solution_num, temp, 'g--')
            ax2.set_ylabel('Temperature')
            for tl in ax2.get_yticklabels():
                tl.set_color('g')
        except IOError:
            print ('CAN NOT OPEN vlp_sa_temp.txt')

    plt.savefig("GraphDrawings/vl_opt_process.png", dpi=300)
    plt.clf()
    plt.close(fig)
    print ("\033[35m* VIZ::\033[0mVL OPTIMIZATION PROCESS GRAPH CREATED AT: GraphDrawings/vl_opt_process.png")
    return None
