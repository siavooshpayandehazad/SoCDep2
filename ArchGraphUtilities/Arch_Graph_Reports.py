__author__ = 'siavoosh'

import matplotlib.pyplot as plt
import networkx

def DrawArchGraph(AG):
    pos=networkx.spring_layout(AG)
    networkx.draw(AG,pos,with_labels=True,node_size=1200)
    plt.savefig("GraphDrawings/AG.png")
    plt.clf()
    return None