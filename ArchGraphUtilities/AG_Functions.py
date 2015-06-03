__author__ = 'siavoosh'
import networkx
import random
#todo: add virtual channel support AG...

def GenerateAG(PE_List,AG_Edge_List,AG_Edge_Port_List):
    print "PREPARING AN ARCHITECTURE GRAPH (AG)..."
    AG=networkx.DiGraph()
    for PE in PE_List:
        AG.add_node(PE,MappedTasks = [],Scheduling={},Utilization=0)

    for i in range(0,len(AG_Edge_List)):
        EDGE = AG_Edge_List[i]
        AG.add_edge(EDGE[0],EDGE[1],Port=AG_Edge_Port_List[i],MappedTasks = [],Scheduling={})
    print "\tNODES: ",AG.nodes(data=False)
    print "\tEDGES: ",AG.edges(data=False)
    print("ARCHITECTURE GRAPH (AG) IS READY...")
    return AG

def GenerateGenericTopologyAG(Topology,SizeX,SizeY):
    """
    Takes a generic topology: Mesh, line, ring etc. and returns AG
    :param Topology: a string with topology name
    :return: AG
    """
    AG=networkx.DiGraph()
    for i in range(0,SizeX*SizeY):
            AG.add_node(i,MappedTasks = [],Scheduling={},Utilization=0,Speed=100)
    if Topology=='Mesh':
        None
    elif Topology=='Ring':
        None
    elif Topology=='Line':
        None
    return AG

