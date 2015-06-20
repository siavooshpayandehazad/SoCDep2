# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
import networkx
import Config

def DrawArchGraph(AG):
    POS ={}
    ColorList = []
    for Node in AG.nodes():
        POS[Node]= [(Node%(Config.Network_X_Size))*100,(Node/(Config.Network_X_Size))*100]
        if AG.node[Node]['Region'] == 'H':
            ColorList.append('#FF878B')
        elif AG.node[Node]['Region'] == 'GH':   # gateway to high critical
            ColorList.append('#FFC29C')
        elif AG.node[Node]['Region'] == 'GNH':  # gateway to Non-high critical
            ColorList.append('#928AFF')
        else:
            ColorList.append('#CFECFF')
    #POS=networkx.spring_layout(AG)

    networkx.draw(AG,POS,with_labels=True,node_size=900,node_color=ColorList)
    plt.savefig("GraphDrawings/AG.png")
    plt.clf()
    return None