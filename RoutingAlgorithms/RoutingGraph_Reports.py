# Copyright (C) 2015 Siavoosh Payandeh Azad

import re
from ArchGraphUtilities import AG_Functions
import matplotlib.pyplot as plt
import networkx
from ConfigAndPackages import Config
import matplotlib.patches as patches


def Draw2DRG(RoutingGraph):
    POS ={}
    ColorList =[]
    plt.figure(figsize=(10*Config.Network_X_Size, 10*Config.Network_Y_Size))
    distance = 100*Config.Network_Z_Size
    step= (distance*0.8)/Config.Network_Z_Size
    for node in RoutingGraph.nodes():
        Node = int(re.search(r'\d+', node).group())
        Location = AG_Functions.ReturnNodeLocation(Node)
        circle1 = plt.Circle((Location[0]*distance + step*Location[2] , Location[1]*distance+ step*Location[2]),radius=35, color='#8ABDFF', fill=False)
        plt.gca().add_patch(circle1)

        circle2 = plt.Circle((Location[0]*distance+ step*Location[2] + 45, Location[1]*distance+ step*Location[2] - 50), radius=10, color='#FF878B', fill=False)
        plt.gca().add_patch(circle2)

        plt.text(Location[0]*distance+ step*Location[2] - 30, Location[1]*distance+ step*Location[2] + 30, str(Node), fontsize=15)

        OffsetX = 0
        OffsetY = 0

        if 'N' in node:
            OffsetY += 30
            if 'I'in node:
                ColorList.append('#CFECFF')
                OffsetX += 12
            else:
                ColorList.append('#FF878B')
                OffsetX -= 12
        elif 'S' in node:
            OffsetY -= 30
            if 'I'in node:
                ColorList.append('#CFECFF')
                OffsetX -= 12
            else:
                ColorList.append('#FF878B')
                OffsetX += 12
        elif 'W' in node:
            OffsetX -= 30
            if 'I'in node:
                ColorList.append('#CFECFF')
                OffsetY += 12
            else:
                ColorList.append('#FF878B')
                OffsetY -= 12

        elif 'E' in node:
            OffsetX += 30
            if 'I'in node:
                ColorList.append('#CFECFF')
                OffsetY -= 12
            else:
                ColorList.append('#FF878B')
                OffsetY += 12

        if 'L' in node:
            if 'I'in node:
                ColorList.append('#CFECFF')
                OffsetX += 44
                OffsetY -= 56
            else:
                ColorList.append('#FF878B')
                OffsetX += 48
                OffsetY -= 48

        if 'U' in node:
            OffsetY = 16
            if 'I'in node:
                ColorList.append('#CFECFF')
                OffsetX -= 15
            else:
                ColorList.append('#FF878B')
                OffsetX += 15

        if 'D' in node:
            OffsetY = -16
            if 'I'in node:
                ColorList.append('#CFECFF')
                OffsetX -= 15
            else:
                ColorList.append('#FF878B')
                OffsetX += 15

        POS[node] = [Location[0]*distance+OffsetX+ step*Location[2],Location[1]*distance+OffsetY+ step*Location[2]]

    networkx.draw(RoutingGraph,POS,with_labels=False,arrows=False,node_size=30,node_color=ColorList)


    plt.text(0, -100, 'X', fontsize=15)
    plt.text(-100, 0, 'Y', fontsize=15)
    plt.text(-45, -45, 'Z', fontsize=15)

    plt.gca().add_patch(patches.Arrow(-100, -100, 100, 0, width=10))
    plt.gca().add_patch(patches.Arrow(-100, -100, 50, 50, width=10))
    plt.gca().add_patch(patches.Arrow(-100, -100, 0, 100, width=10))

    plt.savefig("GraphDrawings/RG.png",dpi=100)
    plt.clf()
    print  "\033[35m* VIZ::\033[0mROUTING GRAPH DRAWING CREATED AT: GraphDrawings/RG.png"
    return None