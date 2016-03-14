# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
import networkx
from ConfigAndPackages import Config
from AG_Functions import return_node_location, return_node_number
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


def gen_latex_ag(ag, shm):
    """
    Generates a latex (.tex) file that will draw the architecture graph along with health of links
    and partitioning information
    :param ag: Architecture graph
    :param shm: System Health Map
    :return: None
    """
    if Config.ag.z_size > 1:
        return None

    latex_ag_file = open('Generated_Files/Latex/ag.tex', 'w')

    latex_ag_file.write("\\documentclass[12pt]{article}\n")
    latex_ag_file.write("\\usepackage{tikz}\n")
    latex_ag_file.write("\definecolor{critical}{RGB}{255,204,204}\n")
    latex_ag_file.write("\definecolor{non_critical}{RGB}{255,255,255}\n")
    latex_ag_file.write("\definecolor{gate_to_critical}{RGB}{204,229,255}\n")
    latex_ag_file.write("\definecolor{gate_to_non_critical}{RGB}{178,102,255}\n")
    latex_ag_file.write("\\begin{document}\n")
    latex_ag_file.write("\\begin{tikzpicture}\n")

    node_size = 1
    bend = 10
    for j in range(0, Config.ag.y_size):
        for i in range(0, Config.ag.x_size):
            start_x = i*2*node_size
            start_y = j*2*node_size

            node_number = return_node_number(i, j, 0)
            if ag.node[node_number]['Region'] == 'L':
                color = 'non_critical'
            elif ag.node[node_number]['Region'] == 'H':
                color = 'critical'
            elif ag.node[node_number]['Region'] == 'GH':
                color = 'gate_to_critical'
            elif ag.node[node_number]['Region'] == 'GNH':
                color = 'gate_to_non_critical'
            else:
                color = 'white'

            latex_ag_file.write("\\draw [fill="+color+"] ("+str(start_x)+","+str(start_y)+") rectangle (" +
                                str(start_x+node_size)+","+str(start_y+node_size)+");\n")

            latex_ag_file.write("\\node[text width=0.5cm] at ("+str(start_x+node_size*0.5)+"," +
                                str(start_y+node_size*0.5)+") {"+str(node_number)+"};\n")

            if i < Config.ag.x_size-1:
                if ag.has_edge(return_node_number(i, j, 0), return_node_number(i+1, j, 0)):
                    if shm.edge[return_node_number(i, j, 0)][return_node_number(i+1, j, 0)]["LinkHealth"]:
                        color = 'blue'
                    else:
                        color = 'red'
                    latex_ag_file.write("\\draw [line width=0.5mm, "+color+"][ -latex ] (" +
                                        str(start_x+node_size)+","+str(start_y+node_size*0.25) +
                                        ") -- ("+str(start_x+2*node_size)+","+str(start_y+node_size*0.25)+");\n")

                if ag.has_edge(return_node_number(i+1, j, 0), return_node_number(i, j, 0)):
                    if shm.edge[return_node_number(i+1, j, 0)][return_node_number(i, j, 0)]["LinkHealth"]:
                        color = 'blue'
                    else:
                        color = 'red'
                    latex_ag_file.write("\\draw [line width=0.5mm, "+color+"][ -latex ] (" +
                                        str(start_x+2*node_size)+","+str(start_y+node_size*0.75) +
                                        ") -- ("+str(start_x+node_size)+","+str(start_y+node_size*0.75)+");\n")

            if j < Config.ag.y_size-1:

                if ag.has_edge(return_node_number(i, j, 0), return_node_number(i, j+1, 0)):
                    if shm.edge[return_node_number(i, j, 0)][return_node_number(i, j+1, 0)]["LinkHealth"]:
                        color = 'blue'
                    else:
                        color = 'red'
                    latex_ag_file.write("\\draw [line width=.5mm, "+color+"][ -latex ] (" +
                                        str(start_x+node_size*0.25)+"," + str(start_y+node_size) +
                                        ") -- ("+str(start_x+node_size*0.25)+","+str(start_y+node_size*2)+");\n")

                if ag.has_edge(return_node_number(i, j+1, 0), return_node_number(i, j, 0)):
                    if shm.edge[return_node_number(i, j+1, 0)][return_node_number(i, j, 0)]["LinkHealth"]:
                        color = 'blue'
                    else:
                        color = 'red'
                    latex_ag_file.write("\\draw [line width=0.5mm, "+color+"][ -latex ] (" +
                                        str(start_x+node_size*0.75)+","+str(start_y+node_size*2) +
                                        ") -- ("+str(start_x+node_size*0.75)+","+str(start_y+node_size)+");\n")

            if j == Config.ag.y_size-1:
                if ag.has_edge(return_node_number(i, j, 0), return_node_number(i, 0, 0)):
                    if shm.edge[return_node_number(i, j, 0)][return_node_number(i, 0, 0)]["LinkHealth"]:
                        color = 'blue'
                    else:
                        color = 'red'
                    latex_ag_file.write("\\draw [line width=.5mm, "+color+"][ -latex ] (" +
                                        str(start_x+node_size)+"," + str(start_y) +
                                        ") to  [bend left="+str(bend)+"] ("+str(start_x+node_size)+"," +
                                        str(node_size)+");\n")
                if ag.has_edge(return_node_number(i, 0, 0), return_node_number(i, j, 0)):
                    if shm.edge[return_node_number(i, 0, 0)][return_node_number(i, j, 0)]["LinkHealth"]:
                        color = 'blue'
                    else:
                        color = 'red'
                    latex_ag_file.write("\\draw [line width=.5mm, "+color+"][ -latex ] (" +
                                        str(start_x)+"," + str(node_size) +
                                        ") to  [bend left="+str(bend)+"] ("+str(start_x)+"," +
                                        str(start_y)+");\n")

            if i == Config.ag.x_size-1:
                if ag.has_edge(return_node_number(i, j, 0), return_node_number(0, j, 0)):

                    if shm.edge[return_node_number(i, j, 0)][return_node_number(0, j, 0)]["LinkHealth"]:
                        color = 'blue'
                    else:
                        color = 'red'
                    latex_ag_file.write("\\draw [line width=.5mm, "+color+"][ -latex ] (" +
                                        str(start_x)+"," + str(start_y) +
                                        ") to  [bend left="+str(bend)+"] ("+str(node_size)+"," +
                                        str(start_y)+");\n")
                if ag.has_edge(return_node_number(0, j, 0), return_node_number(i, j, 0)):
                    if shm.edge[return_node_number(0, j, 0)][return_node_number(i, j, 0)]["LinkHealth"]:
                        color = 'blue'
                    else:
                        color = 'red'
                    latex_ag_file.write("\\draw [line width=.5mm, "+color+"][ -latex ] (" +
                                        str(node_size)+"," + str(start_y+node_size) +
                                        ") to  [bend left="+str(bend)+"] ("+str(start_x)+"," +
                                        str(start_y+node_size)+");\n")

    latex_ag_file.write("\\end{tikzpicture}\n")
    latex_ag_file.write("\\end{document}\n")
    latex_ag_file.close()
    return None