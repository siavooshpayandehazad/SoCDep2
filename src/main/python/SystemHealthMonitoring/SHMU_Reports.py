# Copyright (C) 2015 Siavoosh Payandeh Azad


import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ConfigAndPackages import Config
from ArchGraphUtilities import AG_Functions


def report_noc_shm(shmu):
    """
    Reports the system health map in the console
    :param shmu: system health monitoring unit
    :return: None
    """
    print ("===========================================")
    print ("      REPORTING SYSTEM HEALTH MAP")
    print ("===========================================")
    for node in shmu.SHM.nodes():
        print ("\tNODE:", node)
        print ("\t\tNODE HEALTH:", shmu.SHM.node[node]['NodeHealth'])
        print ("\t\tNODE SPEED:", shmu.SHM.node[node]['NodeSpeed'])
        print ("\t\tTURNS:", shmu.SHM.node[node]['TurnsHealth'])
        print ("\t==============")
    for edge in shmu.SHM.edges():
        print ("\tLINK:", edge, "\t", shmu.SHM.edge[edge[0]][edge[1]]['LinkHealth'])
    return None


def report_the_event(fault_location, fault_type):
    print ("===========================================")
    if fault_type == 'T':    # Transient Fault
            string_to_print = "\033[33mSHM:: Event:\033[0m Transient Fault happened at "
    else:   # Permanent Fault
            string_to_print = "\033[33mSHM:: Event:\033[0m Permanent Fault happened at "
    if type(fault_location) is tuple:
            string_to_print += 'Link ' + str(fault_location)
    elif type(fault_location) is dict:
            turn = fault_location[fault_location.keys()[0]]
            node = fault_location.keys()[0]
            string_to_print += 'Turn ' + str(turn) + ' of Node ' + str(node)
    else:
            string_to_print += 'Node ' + str(fault_location)
    print (string_to_print)
    return None


def report_mpm(shmu):
    """

    :param shmu: System Health Monitoring Unit
    :return:
    """
    print ("===========================================")
    print ("      REPORTING MOST PROBABLE MAPPING ")
    print ("===========================================")
    for item in shmu.MPM:
        print ("KEY:", item, "\t\tMAPPING:", shmu.MPM[item])
    return None


def draw_temp_distribution(shm):
    """

    :param shm: System Health Map
    :return:
    """
    print ("===========================================")
    print ("GENERATING TEMPERATURE DISTRIBUTIONS VISUALIZATION...")
    fig_util = plt.figure(figsize=(4*Config.ag.x_size, 4*Config.ag.y_size))
    max_temp = 0
    for node in shm.nodes():
        max_temp = max(shm.node[node]['NodeTemp'], max_temp)

    for node in shm.nodes():
        location = AG_Functions.return_node_location(node)
        x_size = float(Config.ag.x_size)
        y_size = float(Config.ag.y_size)
        z_size = float(Config.ag.y_size)

        x_offset = location[2]/(z_size*x_size)
        y_offset = location[2]/(z_size*y_size)

        temp = 255*(float(shm.node[node]['RouterTemp'])/Config.MaxTemp)
        if shm.node[node]['NodeHealth']:
            color = '#%02X%02X%02X' % (temp, 0, 255-temp)
        else:   # node is broken
            color = '#7B747B'
        fig_util.gca().add_patch(patches.Rectangle((location[0]/x_size+x_offset,
                                                    location[1]/y_size+y_offset),
                                                   width=0.08, height=0.08, facecolor=color,
                                                   edgecolor="black", linewidth=3, zorder=z_size-location[2]))

        temp = 255*(float(shm.node[node]['NodeTemp'])/Config.MaxTemp)

        if shm.node[node]['NodeHealth']:
            color = '#%02X%02X%02X' % (temp, 0, 255-temp)
        else:   # node is broken
            color = '#7B747B'
        fig_util.gca().add_patch(patches.Rectangle((location[0]/x_size+x_offset+0.05,
                                                    location[1]/y_size+y_offset),
                                                   width=0.03, height=0.03, facecolor=color,
                                                   edgecolor="black", linewidth=3, zorder=z_size-location[2]))

    fig_util.text(0.25, 0.03, 'Distribution of temperature of network nodes', fontsize=15)
    fig_util.savefig("GraphDrawings/Temp_Distribute.png", dpi=100)
    fig_util.clf()
    plt.close(fig_util)
    print("\033[35m* VIZ::\033[0mMAPPING UTILIZATION DISTRIBUTION DRAWING " +
          "CREATED AT: GraphDrawings/Temp_Distribute.png")
    return None


def draw_shm(shm, iteration=None):
    """

    :param shm: System Health Map
    :return:
    """
    print ("===========================================")
    print ("GENERATING SYSTEM HEALTH MAP DRAWING...")

    x_size = float(Config.ag.x_size)
    y_size = float(Config.ag.y_size)
    z_size = float(Config.ag.z_size)

    fig = plt.figure(figsize=(10*x_size, 10*y_size))
    if z_size == 1:
        plt.ylim([0, 1])
        plt.xlim([0, 1])
    else:
        plt.ylim([0, z_size])
        plt.xlim([0, z_size])

    for node in shm.nodes():
        location = AG_Functions.return_node_location(node)
        x = (location[0]/x_size)*z_size
        y = (location[1]/y_size)*z_size
        z = (location[2]/z_size)
        x_offset = z
        y_offset = z

        font_size = 35 / z_size
        plt.text(x+0.155+x_offset, y+0.055+y_offset, str(node), fontsize=font_size)
        circle_router = plt.Circle((x+0.1+x_offset, y+0.1+y_offset), 0.05, facecolor='w')
        plt.gca().add_patch(circle_router)
        if shm.node[node]['NodeHealth']:
            color = 'w'
        else:
            color = 'r'
        circle_node = plt.Circle((x+0.14+x_offset, y+0.06+y_offset), 0.01, facecolor=color)
        plt.gca().add_patch(circle_node)

        for turn in shm.node[node]['TurnsHealth']:
            if shm.node[node]['TurnsHealth'][turn]:
                color = 'black'
            else:
                color = 'r'

            if turn == 'S2E':
                plt.gca().add_patch(patches.Arrow(x+0.11+x_offset, y+0.065+y_offset, 0.015,
                                                  0.015, width=0.01, color=color))
            elif turn == 'E2S':
                plt.gca().add_patch(patches.Arrow(x+0.135+x_offset, y+0.08+y_offset, -0.015,
                                                  -0.015, width=0.01, color=color))
            elif turn == 'W2N':
                plt.gca().add_patch(patches.Arrow(x+0.065+x_offset, y+0.117+y_offset, 0.015,
                                                  0.015, width=0.01, color=color))
            elif turn == 'N2W':
                plt.gca().add_patch(patches.Arrow(x+0.09+x_offset, y+0.132+y_offset, -0.015,
                                                  -0.015, width=0.01, color=color))
            elif turn == 'N2E':
                plt.gca().add_patch(patches.Arrow(x+0.12+x_offset, y+0.132+y_offset, 0.015,
                                                  -0.015, width=0.01, color=color))
            elif turn == 'E2N':
                plt.gca().add_patch(patches.Arrow(x+0.125+x_offset, y+0.117+y_offset, -0.015,
                                                  0.015, width=0.01, color=color))
            elif turn == 'W2S':
                plt.gca().add_patch(patches.Arrow(x + 0.075+x_offset, y + 0.08+y_offset, 0.015,
                                                  -0.015, width=0.01, color=color))
            elif turn == 'S2W':
                plt.gca().add_patch(patches.Arrow(x + 0.080+x_offset, y + 0.065+y_offset, -0.015,
                                                  0.015, width=0.01, color=color))

            if shm.node[node]['TurnsHealth'][turn]:
                color = 'black'
            else:
                color = 'r'

            if turn == 'N2U':
                circle_node = plt.Circle((x+0.09+x_offset, y+0.142+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)

            elif turn == 'N2D':
                circle_node = plt.Circle((x+0.11+x_offset, y+0.142+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                circle_node = plt.Circle((x+0.11+x_offset, y+0.142+y_offset), 0.001, facecolor='b')
                plt.gca().add_patch(circle_node)

            elif turn == 'S2U':
                circle_node = plt.Circle((x+0.11+x_offset, y+0.057+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)

            elif turn == 'S2D':
                circle_node = plt.Circle((x+0.09+x_offset, y+0.057+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                circle_node = plt.Circle((x+0.09+x_offset, y+0.057+y_offset), 0.001, facecolor='b')
                plt.gca().add_patch(circle_node)

            elif turn == 'E2U':
                circle_node = plt.Circle((x+0.142+x_offset, y+0.11+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)

            elif turn == 'E2D':
                circle_node = plt.Circle((x+0.142+x_offset, y+0.09+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                circle_node = plt.Circle((x+0.142+x_offset, y+0.09+y_offset), 0.001, facecolor='b')
                plt.gca().add_patch(circle_node)

            elif turn == 'W2U':
                circle_node = plt.Circle((x+0.057+x_offset, y+0.09+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)

            elif turn == 'W2D':
                circle_node = plt.Circle((x+0.057+x_offset, y+0.11+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                circle_node = plt.Circle((x+0.057+x_offset, y+0.11+y_offset), 0.001, facecolor='b')
                plt.gca().add_patch(circle_node)

            elif turn == 'U2N':
                circle_node = plt.Circle((x+0.105+x_offset, y+0.111+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                circle_node = plt.Circle((x+0.105+x_offset, y+0.111+y_offset), 0.001, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                plt.gca().add_patch(patches.Arrow(x + 0.105+x_offset, y + 0.116+y_offset,
                                                  0, 0.01, width=0.01, color=color))

            elif turn == 'U2S':
                circle_node = plt.Circle((x+0.105+x_offset, y+0.086+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                circle_node = plt.Circle((x+0.105+x_offset, y+0.086+y_offset), 0.001, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                plt.gca().add_patch(patches.Arrow(x + 0.105+x_offset, y + 0.081+y_offset,
                                                  0, -0.01, width=0.01, color=color))

            elif turn == 'U2W':
                circle_node = plt.Circle((x+0.085+x_offset, y+0.093+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                circle_node = plt.Circle((x+0.085+x_offset, y+0.093+y_offset), 0.001, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                plt.gca().add_patch(patches.Arrow(x + 0.08+x_offset, y + 0.093+y_offset,
                                                  -0.01, 0, width=0.01, color=color))

            elif turn == 'U2E':
                circle_node = plt.Circle((x+0.115+x_offset, y+0.093+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                circle_node = plt.Circle((x+0.115+x_offset, y+0.093+y_offset), 0.001, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                plt.gca().add_patch(patches.Arrow(x + 0.12+x_offset, y + 0.093+y_offset,
                                                  0.01, 0, width=0.01, color=color))

            elif turn == 'D2N':
                circle_node = plt.Circle((x+0.095+x_offset, y+0.111+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                plt.gca().add_patch(patches.Arrow(x + 0.095+x_offset, y + 0.116+y_offset,
                                                  0, 0.01, width=0.01, color=color))

            elif turn == 'D2S':
                circle_node = plt.Circle((x+0.095+x_offset, y+0.086+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                plt.gca().add_patch(patches.Arrow(x + 0.095+x_offset, y + 0.081+y_offset,
                                                  0, -0.01, width=0.01, color=color))

            elif turn == 'D2W':
                circle_node = plt.Circle((x+0.085+x_offset, y+0.104+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                plt.gca().add_patch(patches.Arrow(x + 0.08+x_offset, y + 0.104+y_offset,
                                                  -0.01, 0, width=0.01, color=color))

            elif turn == 'D2E':
                circle_node = plt.Circle((x+0.115+x_offset, y+0.104+y_offset), 0.005, edgecolor=color, facecolor='w')
                plt.gca().add_patch(circle_node)
                plt.gca().add_patch(patches.Arrow(x + 0.12+x_offset, y + 0.104+y_offset,
                                                  0.01, 0, width=0.01, color=color))

    for link in shm.edges():
        if shm.edge[link[0]][link[1]]['LinkHealth']:
            color = 'black'
        else:
            color = 'r'
        source_loc = AG_Functions.return_node_location(link[0])
        destination_loc = AG_Functions.return_node_location(link[1])

        x = (source_loc[0]/x_size)*z_size
        y = (source_loc[1]/y_size)*z_size
        z = source_loc[2]/z_size
        x_offset = z
        y_offset = z

        dx = ((destination_loc[0] - source_loc[0])/x_size)
        dy = ((destination_loc[1] - source_loc[1])/y_size)
        dz = ((destination_loc[2] - source_loc[2])/z_size)
        if dz == 0:
            if dx == 0:
                if dy > 0:
                    plt.gca().add_patch(patches.Arrow(x+0.11+x_offset, y+0.15+y_offset,
                                                      0, dy*z_size - 0.1, width=0.01, color=color))
                else:
                    plt.gca().add_patch(patches.Arrow(x+0.09+x_offset, y+0.05+y_offset,
                                                      0, dy*z_size + 0.1, width=0.01, color=color))

            elif dy == 0:
                if dx > 0:
                    plt.gca().add_patch(patches.Arrow(x+0.15+x_offset, y+0.11+y_offset,
                                                      dx*z_size - 0.1, 0, width=0.01, color=color))
                else:
                    plt.gca().add_patch(patches.Arrow(x+0.05+x_offset, y+0.09+y_offset,
                                                      dx*z_size + 0.1, 0, width=0.01, color=color))
            else:
                raise ValueError("Can not draw link", link)
        elif dz > 0:
                z_offset = 1.4/z_size
                plt.gca().add_patch(patches.Arrow(x+0.130+x_offset, y+0.140+y_offset,
                                                  dz*z_offset, dz*z_offset, width=0.01, color=color))
        elif dz < 0:
                plt.gca().add_patch(patches.Arrow(x+0.07+x_offset, y+0.06+y_offset,
                                                  dz*z_offset, dz*z_offset, width=0.01, color=color))

    fig.text(0.25, 0.02, "System Health Map", fontsize=35)
    if iteration is None:
        plt.savefig("GraphDrawings/SHM.png", dpi=200)
    else:
        plt.savefig("GraphDrawings/SHM_"+str(iteration)+".png", dpi=200)
    plt.clf()
    plt.close(fig)
    print("\033[35m* VIZ::\033[0mSYSTEM HEALTH MAP DRAWING CREATED AT: GraphDrawings/SHM.png")
    return None
