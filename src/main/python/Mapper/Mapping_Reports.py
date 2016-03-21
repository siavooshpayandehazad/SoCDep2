# Copyright (C) 2015 Siavoosh Payandeh Azad
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ConfigAndPackages import Config
from ArchGraphUtilities import AG_Functions
import random
import networkx


def report_mapping(ag, logging):
    """
    Reports mapping into log file
    :param ag: Architecture Graph
    :param logging: logging file
    :return: None
    """
    logging.info("===========================================")
    logging.info("      REPORTING MAPPING RESULT")
    logging.info("===========================================")
    for node in ag.nodes():
        logging.info("NODE: "+str(node)+" CONTAINS: "+str(ag.node[node]['PE'].mapped_tasks))
        logging.info("NODE: "+str(node)+"'s Router CONTAINS: "+str(ag.node[node]['Router'].mapped_tasks))
    for link in ag.edges():
        logging.info("LINK: "+str(link)+" CONTAINS: "+str(ag.edge[link[0]][link[1]]['MappedTasks']))
    return None


def draw_mapping_distribution(ag, shmu):
    """
    Draws mapping Task Number and Utilization Distribution
    :param ag: Architecture Graph
    :param shmu: System health Monitoring Unit
    :return: None
    """
    print ("===========================================")
    print ("GENERATING MAPPING DISTRIBUTIONS VISUALIZATION...")
    fig_num = plt.figure(figsize=(4*Config.ag.x_size, 4*Config.ag.y_size))
    fig_util = plt.figure(figsize=(4*Config.ag.x_size, 4*Config.ag.y_size))
    max_number_of_tasks = 0
    max_utilization = 0
    for node in ag.nodes():
        max_number_of_tasks = max(len(ag.node[node]['PE'].mapped_tasks), max_number_of_tasks)
        max_utilization = max(ag.node[node]['PE'].utilization, max_utilization)

    for node in ag.nodes():
        location = AG_Functions.return_node_location(node)
        x_size = float(Config.ag.x_size)
        y_size = float(Config.ag.y_size)
        z_size = float(Config.ag.y_size)
        num = 255*len(ag.node[node]['PE'].mapped_tasks)/float(max_number_of_tasks)
        util = 255*ag.node[node]['PE'].utilization/float(max_utilization)
        if shmu.SHM.node[node]['NodeHealth']:
            if not ag.node[node]['PE'].dark:
                color = '#%02X%02X%02X' % (255, 255-num, 255-num)
            else:
                color = 'gray'
        else:   # node is broken
            color = '#7B747B'
        fig_num.gca().add_patch(patches.Rectangle((location[0]/x_size+location[2]/(z_size*x_size**2),
                                                   location[1]/y_size+location[2]/(z_size*y_size**2)),
                                width=0.15, height=0.15, facecolor=color,
                                edgecolor="black", linewidth=3, zorder=z_size-location[2]))
        if shmu.SHM.node[node]['NodeHealth']:
            if not ag.node[node]['PE'].dark:
                color = '#%02X%02X%02X' % (255, 255-util, 255-util)
            else:
                color = 'gray'
        else:   # node is broken
            color = '#7B747B'
        fig_util.gca().add_patch(patches.Rectangle((location[0]/x_size+location[2]/(z_size*x_size**2),
                                                    location[1]/y_size+location[2]/(z_size*y_size**2)),
                                 width=0.15, height=0.15, facecolor=color,
                                 edgecolor="black", linewidth=3, zorder=z_size-location[2]))

    fig_num.text(0.25, 0.03, 'Distribution of number of the tasks on the network', fontsize=15)
    fig_util.text(0.25, 0.03, 'Distribution of utilization of network nodes', fontsize=15)
    fig_num.savefig("GraphDrawings/Mapping_Num.png", bbox_inches='tight')
    fig_util.savefig("GraphDrawings/Mapping_Util.png", bbox_inches='tight')
    fig_num.clf()
    fig_util.clf()
    plt.close(fig_num)
    plt.close(fig_util)
    print ("\033[35m* VIZ::\033[0mMAPPING UTILIZATION DISTRIBUTION DRAWING CREATED AT: GraphDrawings/Mapping_Util.png")
    print ("\033[35m* VIZ::\033[0mMAPPING TASK NUMBER DISTRIBUTION DRAWING CREATED AT: GraphDrawings/Mapping_Num.png")
    return None


def draw_mapping(tg, ag, shm, mapping_file_name):
    """
    This function draws the tasks on tiles of network. this would be very useful to check how our
    mapping optimization is acting...
    :param tg: Task Graph
    :param ag: Architecture Graph
    :param shm: System Health Map
    :param mapping_file_name: string containing name of the file in which the mapping would be generated
    :return: None
    """
    print ("===========================================")
    print ("GENERATING MAPPING VISUALIZATION...")
    fig = plt.figure(figsize=(4*Config.ag.x_size, 4*Config.ag.y_size))
    color_list = []
    position = {}
    x_size = float(Config.ag.x_size)
    y_size = float(Config.ag.y_size)
    z_size = float(Config.ag.z_size)
    node_size = 0.3
    step_size = node_size * 1.08
    distance = step_size * z_size * 1.2
    for node in ag.nodes():
        location = AG_Functions.return_node_location(node)
        if shm.node[node]['NodeHealth']:
            if not ag.node[node]['PE'].dark:
                if Config.EnablePartitioning:
                    if node in Config.CriticalRegionNodes:
                        color = '#FF878B'
                    elif node in Config.GateToNonCritical:
                        color = '#928AFF'
                    elif node in Config.GateToCritical:
                        color = '#FFC29C'
                    else:
                        color = 'white'
                else:
                    color = 'white'
            else:
                color = 'gray'
        else:   # node is broken
            color = '#7B747B'

        fig.gca().add_patch(patches.Rectangle(((distance*location[0])+location[2]*step_size,
                                               (distance*location[1])+location[2]*step_size),
                                              width=node_size, height=node_size, facecolor=color,
                                              linewidth=3, alpha=0.5))

        plt.text((distance*location[0])+location[2]*step_size,
                 (distance*location[1])+location[2]*step_size+node_size, str(node), fontsize=15)
        if location[0] < x_size-1:
            x = distance*(location[0])+location[2]*step_size+node_size
            y = distance*(location[1])+location[2]*step_size+(node_size/2)
            plt.plot([x, x+distance-node_size], [y, y], color='black', lw=3)
            # plt.gca().add_patch(patches.Arrow(x, y, 1.0/x_size - 0.1, 0, width=0.01))
        if location[1] < y_size-1:
            x = distance*(location[0])+location[2]*step_size+(node_size/2)
            y = distance*(location[1])+location[2]*step_size+node_size
            # plt.plot([y, y], [x, x+1.0/x_size - 0.1], color ='black')
            plt.plot([x, x], [y, y+distance-node_size], color='black', lw=3)

        number_of_task_in_row = 4
        offset_x = -(node_size/(2*number_of_task_in_row))
        offset_y = node_size / (number_of_task_in_row+1)
        task_count = 0
        for task in ag.node[node]['PE'].mapped_tasks:
            offset_x += node_size / number_of_task_in_row
            if task_count == number_of_task_in_row:
                task_count = 0
                offset_x = (node_size/(2*number_of_task_in_row))
                offset_y += node_size / number_of_task_in_row
            random.seed(task)
            r = random.randrange(0, 255)
            g = random.randrange(0, 255)
            b = random.randrange(0, 255)
            color = '#%02X%02X%02X' % (r, g, b)
            color_list.append(color)
            position[task] = (distance*location[0]+location[2]*step_size+offset_x,
                              distance*location[1]+location[2]*step_size+offset_y)
            task_count += 1
    task_size = 800/Config.ag.z_size
    networkx.draw(tg, position, with_labels=True, node_size=task_size, node_color=color_list, width=0, alpha=0.5)
    fig.text(0.35, 0.1, 'Mapping visualization for network nodes', fontsize=15)

    plt.text(0, -node_size*2/3, 'X', fontsize=15)
    plt.text(-node_size*2/3, 0, 'Y', fontsize=15)
    plt.text(-node_size*2/3 + node_size/3, -node_size*2/3 + node_size/3, 'Z', fontsize=15)

    plt.gca().add_patch(patches.Arrow(-node_size*2/3, -node_size*2/3, node_size, 0, width=node_size/10))
    plt.gca().add_patch(patches.Arrow(-node_size*2/3, -node_size*2/3, node_size/3, node_size/3, width=node_size/10))
    plt.gca().add_patch(patches.Arrow(-node_size*2/3, -node_size*2/3, 0, node_size, width=node_size/10))

    fig.savefig("GraphDrawings/"+mapping_file_name+".png", bbox_inches='tight')
    plt.clf()
    plt.close(fig)
    print ("\033[35m* VIZ::\033[0mMAPPING DRAWING CREATED AT: GraphDrawings/"+mapping_file_name+".png")
    return None


def viz_mapping_opt(cost_file_name, iteration=None):
    """
    Visualizes the cost of solutions during local search mapping optimization process
    :param cost_file_name: Name of the Cost File (Holds values of cost function for different mapping steps)
    :return: None
    """
    print ("===========================================")
    print ("GENERATING MAPPING OPTIMIZATION VISUALIZATIONS...")

    fig, ax1 = plt.subplots()
    solution_num = None
    try:
        mapping_cost_file = open('Generated_Files/Internal/'+cost_file_name+'.txt', 'r')
        cost = []
        line = mapping_cost_file.readline()
        min_cost = float(line)
        min_cost_list = [min_cost]
        cost.append(float(line))
        while line != "":
            cost.append(float(line))
            if float(line) < min_cost:
                min_cost = float(line)
            min_cost_list.append(min_cost)
            line = mapping_cost_file.readline()
        solution_num = range(0, len(cost))
        mapping_cost_file.close()

        ax1.set_ylabel('Mapping Cost')
        ax1.set_xlabel('Iteration #')
        ax1.plot(solution_num, cost, '#5095FD', solution_num, min_cost_list, 'r')

        if Config.Mapping_Function == 'IterativeLocalSearch':
            for Iteration in range(1, Config.IterativeLocalSearchIterations+1):
                x1 = x2 = Iteration * Config.LocalSearchIteration
                y1 = 0
                y2 = max(cost)
                ax1.plot((x1, x2), (y1, y2), 'g')

    except IOError:
        print ('CAN NOT OPEN', cost_file_name+'.txt')

    if Config.Mapping_Function == 'SimulatedAnnealing':
        try:
            sa_temp_file = open('Generated_Files/Internal/SATemp.txt', 'r')
            temp = []
            line = sa_temp_file.readline()
            while line != '':
                temp.append(float(line))
                line = sa_temp_file.readline()
            sa_temp_file.close()
            # print (len(temp), len(solution_num))
            ax2 = ax1.twinx()
            ax2.plot(solution_num, temp, 'g--')
            ax2.set_ylabel('Temperature')
            for tl in ax2.get_yticklabels():
                tl.set_color('g')
        except IOError:
            print ('CAN NOT OPEN SATemp.txt')
    if iteration is None:
        plt.savefig("GraphDrawings/Mapping_Opt_Process.png", dpi=300)
        print ("\033[35m* VIZ::\033[0mMAPPING OPTIMIZATION PROCESS " +
               "GRAPH CREATED AT: GraphDrawings/Mapping_Opt_Process.png")
    else:
        plt.savefig("GraphDrawings/Mapping_Opt_Process_"+str(iteration)+".png", dpi=300)
        print ("\033[35m* VIZ::\033[0mMAPPING OPTIMIZATION PROCESS " +
               "GRAPH CREATED AT: GraphDrawings/Mapping_Opt_Process"+str(iteration)+".png")
    plt.clf()
    plt.close(fig)

    return None


def viz_cost_slope():
    """
    Visualises the mapping Cost slope for Simulated Annealing. This is like derivative of the cost graph.
    :return: None
    """
    print ("===========================================")
    print ("GENERATING MAPPING OPTIMIZATION COST SLOPE VISUALIZATION...")

    fig, ax1 = plt.subplots()
    try:
        cost_slope_file = open('Generated_Files/Internal/SAcost_slope.txt', 'r')
        cost_slope = []
        line = cost_slope_file.readline()
        while line != '':
            cost_slope.append(float(line))
            line = cost_slope_file.readline()
        cost_slope_file.close()
        # print (len(temp), len(solution_num))

        ax1.plot(range(0, len(cost_slope)), cost_slope)
        ax1.set_ylabel('Cost Slope')
        plt.savefig("GraphDrawings/Mapping_Cost_Slope.png")
        plt.clf()
        plt.close(fig)
        print ("\033[35m* VIZ::\033[0mSA COST SLOPE GRAPH CREATED AT: GraphDrawings/Mapping_Cost_Slope.png")
    except IOError:
            print ('CAN NOT OPEN SAcost_slope.txt')

    return None


def viz_huang_race():
    """
    Visualizes The progress of Huang's cooling scheduling counters progress
    :return:    None
    """
    print ("===========================================")
    print ("GENERATING HUANG COUNTERS STATES VISUALIZATION...")
    fig, ax1 = plt.subplots()
    try:
        huang_race_file = open('Generated_Files/Internal/SAHuangRace.txt', 'r')
        counter1 = []
        counter2 = []
        line = huang_race_file.readline()
        while line != '':
            counter_list = line.split()
            counter1.append(counter_list[0])
            counter2.append(counter_list[1])
            line = huang_race_file.readline()
        huang_race_file.close()

        ax1.plot(range(0, len(counter1)), counter1, 'b', range(0, len(counter2)), counter2, 'g')
        ax1.set_ylabel('Huang counters')
        plt.savefig("GraphDrawings/Mapping_HuangCounters.png", dpi=300)
        plt.clf()
        plt.close(fig)
        print ("\033[35m* VIZ::\033[0mSA HUANG COUNTERS GRAPH CREATED AT: GraphDrawings/Mapping_HuangCounters.png")
    except IOError:
            print ('CAN NOT OPEN SAHuangRace.txt')
    return None
