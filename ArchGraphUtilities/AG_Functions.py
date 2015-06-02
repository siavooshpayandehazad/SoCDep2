__author__ = 'siavoosh'
import networkx

#todo: add virtual channel support AG...

def GenerateAG(PE_List,AG_Edge_List,AG_Edge_Port_List):
    print "PREPARING AN ARCHITECTURE GRAPH (AG)..."
    AG=networkx.DiGraph()
    for PE in PE_List:
        AG.add_node(PE,MappedTasks = [],Scheduling={},Utilization=0)

    for i in range(0,len(AG_Edge_List)):
        EDGE = AG_Edge_List[i]
        AG.add_edge(EDGE[0],EDGE[1],Port=AG_Edge_Port_List[i],MappedTasks = [],Scheduling={})  # UsedBandWidth
    print "\tNODES: ",AG.nodes(data=False)
    print "\tEDGES: ",AG.edges(data=False)
    print("ARCHITECTURE GRAPH (AG) IS READY...")
    return AG

def GenerateGenericTopologyAG(Topology):
    """
    Takes a generic topology: Mesh, line, ring etc. and returns AG
    :param Topology: a string with topology name
    :return: AG
    """
    AG=networkx.DiGraph()
    return AG
