__author__ = 'siavoosh'

import matplotlib.pyplot as plt
import networkx
import Config

def DrawArchGraph(AG):
    POS ={}
    for Node in AG.nodes():
        POS[Node]= [(Node%(Config.Network_X_Size))*100,(Node/(Config.Network_X_Size))*100]
    #pos=networkx.spring_layout(AG)
    networkx.draw(AG,POS,with_labels=True,node_size=1000,node_color='#A5FAFF')
    plt.savefig("GraphDrawings/AG.png")
    plt.clf()
    return None