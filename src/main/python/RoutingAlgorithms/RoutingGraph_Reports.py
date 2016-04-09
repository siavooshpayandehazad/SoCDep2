# Copyright (C) 2015 Siavoosh Payandeh Azad

from re import search
from ArchGraphUtilities.AG_Functions import return_node_location
import matplotlib.pyplot as plt
from networkx import draw
from ConfigAndPackages import Config
import matplotlib.patches as patches


def report_turn_model(turn_model):
    """
    prints the turn model for a 2D network in the console
    Only usable if there is a uniform Turn model over the network
    :param turn_model: set of allowed turns in a 2D network
    :return: None
    """
    print "\tUSING TURN MODEL: ", turn_model
    return None


def draw_rg(rg):
    """
    draws routing graph in GraphDrawings/RG.png
    :param rg: routing graph
    :return: None
    """
    print ("===========================================")
    print ("GENERATING ROUTING GRAPH VISUALIZATION...")
    line_width = 2
    pos = {}
    color_list = []
    plt.figure(figsize=(10*Config.ag.x_size, 10*Config.ag.y_size))
    distance = 100*Config.ag.z_size
    step = (distance*0.8)/Config.ag.z_size
    for node in rg.nodes():
        chosen_node = int(search(r'\d+', node).group())
        location = return_node_location(chosen_node)
        circle1 = plt.Circle((location[0]*distance+step*location[2], location[1]*distance+step*location[2]),
                             radius=35, color='#8ABDFF', fill=False, lw=line_width)
        plt.gca().add_patch(circle1)

        circle2 = plt.Circle((location[0]*distance+step*location[2]+45, location[1]*distance+step*location[2]-50),
                             radius=10, color='#FF878B', fill=False, lw=line_width)
        plt.gca().add_patch(circle2)

        plt.text(location[0]*distance+step*location[2]-30, location[1]*distance+step*location[2]+30,
                 str(chosen_node), fontsize=45)

        offset_x = 0
        offset_y = 0

        if 'N' in node:
            offset_y += 30
            if 'I'in node:
                color_list.append('#CFECFF')
                offset_x += 12
            else:
                color_list.append('#FF878B')
                offset_x -= 12
        elif 'S' in node:
            offset_y -= 30
            if 'I'in node:
                color_list.append('#CFECFF')
                offset_x -= 12
            else:
                color_list.append('#FF878B')
                offset_x += 12
        elif 'W' in node:
            offset_x -= 30
            if 'I'in node:
                color_list.append('#CFECFF')
                offset_y += 12
            else:
                color_list.append('#FF878B')
                offset_y -= 12

        elif 'E' in node:
            offset_x += 30
            if 'I'in node:
                color_list.append('#CFECFF')
                offset_y -= 12
            else:
                color_list.append('#FF878B')
                offset_y += 12

        if 'L' in node:
            if 'I'in node:
                color_list.append('#CFECFF')
                offset_x += 44
                offset_y -= 56
            else:
                color_list.append('#FF878B')
                offset_x += 48
                offset_y -= 48

        if 'U' in node:
            offset_y = 16
            if 'I'in node:
                color_list.append('#CFECFF')
                offset_x -= 15
            else:
                color_list.append('#FF878B')
                offset_x += 15

        if 'D' in node:
            offset_y = -16
            if 'I'in node:
                color_list.append('#CFECFF')
                offset_x -= 15
            else:
                color_list.append('#FF878B')
                offset_x += 15

        pos[node] = [location[0]*distance+offset_x+step*location[2], location[1]*distance+offset_y+step*location[2]]

    draw(rg, pos, with_labels=False, arrows=False, node_size=140, node_color=color_list,
         linewidths=line_width, width=line_width)

    plt.text(0, -100, 'X', fontsize=15)
    plt.text(-100, 0, 'Y', fontsize=15)
    plt.text(-45, -45, 'Z', fontsize=15)

    plt.gca().add_patch(patches.Arrow(-100, -100, 100, 0, width=10))
    plt.gca().add_patch(patches.Arrow(-100, -100, 50, 50, width=10))
    plt.gca().add_patch(patches.Arrow(-100, -100, 0, 100, width=10))

    plt.savefig("GraphDrawings/RG.png", dpi=100)
    plt.clf()
    print ("\033[35m* VIZ::\033[0mROUTING GRAPH DRAWING CREATED AT: GraphDrawings/RG.png")
    return None
