# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
import networkx
from ConfigAndPackages import Config
from AG_Functions import ReturnNodeLocation

def DrawArchGraph(AG):
    POS ={}
    ColorList = []
    NumberOfLayers = Config.Network_Z_Size
    for Node in AG.nodes():
        x,y,z = ReturnNodeLocation(Node)
        offsetX = Config.Network_X_Size* 100
        offsetY = Config.Network_Y_Size* 100
        POS[Node]= [x*100*Config.Network_X_Size*NumberOfLayers+z*offsetX, y*100*Config.Network_Y_Size*NumberOfLayers+z*offsetY]
        if AG.node[Node]['Region'] == 'H':
            ColorList.append('#FF878B')
        elif AG.node[Node]['Region'] == 'GH':   # gateway to high critical
            ColorList.append('#FFC29C')
        elif AG.node[Node]['Region'] == 'GNH':  # gateway to Non-high critical
            ColorList.append('#928AFF')
        else:
            ColorList.append('#CFECFF')
    # POS = networkx.spring_layout(AG)

    networkx.draw(AG,POS,with_labels=True,node_size=300,node_color=ColorList)
    plt.savefig("GraphDrawings/AG.png")
    plt.clf()
    return None