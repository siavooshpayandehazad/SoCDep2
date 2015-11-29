# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
import networkx
from ConfigAndPackages import Config
from AG_Functions import ReturnNodeLocation

def DrawArchGraph(AG, FileName):
    """
    Generates Visualizations of the Architecture Graph and saves it in "GraphDrawings/FileName.png"
    :param AG: Architecture Graph
    :param FileName: Name of the file for saving the graph
    :return: None
    """
    POS ={}
    ColorList = []

    NumberOfLayers = Config.Network_Z_Size
    NodeSize = 500/NumberOfLayers

    NodeDistanceX = (6 * NodeSize * Config.Network_X_Size * (NumberOfLayers+1))
    NodeDistanceY = (6 * NodeSize * Config.Network_Y_Size * (NumberOfLayers+1))

    offsetX = (4 * NodeSize * Config.Network_X_Size)
    offsetY = (4 * NodeSize * Config.Network_Y_Size)

    for Node in AG.nodes():
        x,y,z = ReturnNodeLocation(Node)
        POS[Node]= [(x*NodeDistanceX)+z*offsetX, (y*NodeDistanceY)+z*offsetY]
        if AG.node[Node]['Region'] == 'H':
            ColorList.append('#FF878B')
        elif AG.node[Node]['Region'] == 'GH':   # gateway to high critical
            ColorList.append('#FFC29C')
        elif AG.node[Node]['Region'] == 'GNH':  # gateway to Non-high critical
            ColorList.append('#928AFF')
        else:
            ColorList.append('#CFECFF')

    # POS = networkx.spring_layout(AG)

    networkx.draw(AG, POS, with_labels=True, node_size=NodeSize, arrows=False, node_color=ColorList, font_size=5, linewidths=1)
    plt.savefig("GraphDrawings/"+FileName+".png", dpi=150)
    plt.clf()
    return None
