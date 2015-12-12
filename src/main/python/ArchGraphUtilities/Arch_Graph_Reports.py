# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
import networkx
from ConfigAndPackages import Config
from AG_Functions import return_node_location


def draw_ag(ag, file_name):
    """
    Generates Visualizations of the Architecture Graph and saves it in "GraphDrawings/FileName.png"
    :param ag: Architecture Graph
    :param file_name: Name of the file for saving the graph
    :return: None
    """
    position = {}
    color_list = []

    number_of_layers = Config.Network_Z_Size
    node_size = 700/number_of_layers

    node_distance_x = (6 * node_size * Config.Network_X_Size * (number_of_layers+1))
    node_distance_y = (6 * node_size * Config.Network_Y_Size * (number_of_layers+1))

    offset_x = (4 * node_size * Config.Network_X_Size)
    offset_y = (4 * node_size * Config.Network_Y_Size)

    for Node in ag.nodes():
        x, y, z = return_node_location(Node)
        position[Node] = [(x*node_distance_x)+z*offset_x, (y*node_distance_y)+z*offset_y]
        if ag.node[Node]['Region'] == 'H':
            color_list.append('#FF878B')
        elif ag.node[Node]['Region'] == 'GH':   # gateway to high critical
            color_list.append('#FFC29C')
        elif ag.node[Node]['Region'] == 'GNH':  # gateway to Non-high critical
            color_list.append('#928AFF')
        else:
            color_list.append('#CFECFF')

    # POS = networkx.spring_layout(AG)

    networkx.draw(ag, pos=position, with_labels=True, node_size=node_size, arrows=False,
                  node_color=color_list, font_size=5, linewidths=1)
    plt.savefig("GraphDrawings/"+file_name+".png", dpi=150)
    plt.clf()
    return None
