__author__ = 'siavoosh'
import networkx
import random
#todo: add virtual channel support AG...

def GenerateAG(PE_List,AG_Edge_List,AG_Edge_Port_List):
    print "==========================================="
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

def GenerateGenericTopologyAG(Topology,SizeX,SizeY,SizeZ,Report):
    """
    Takes a generic topology: 2DMesh, 2DLine, 2DRing etc. and returns AG
    :param Topology: a string with topology name
    :return: AG
    """
    print "==========================================="
    print "PREPARING AN ARCHITECTURE GRAPH (AG)..."
    print "TOPOLOGY:",Topology
    print "X SIZE:",SizeX
    print "Y SIZE:",SizeY
    print "Z SIZE:",SizeZ
    AG=networkx.DiGraph()
    for i in range(0,SizeX*SizeY):
        AG.add_node(i,MappedTasks = [],Scheduling={},Utilization=0,Speed=100)
    if Topology=='2DMesh':
        for j in range(0,SizeY):
            for i in range(0,SizeX-1):
                if Report:print "CONNECTING",j*(SizeX)+i,"TO",j*(SizeX)+i+1
                if Report:print "CONNECTING",j*(SizeX)+i+1,"TO",j*(SizeX)+i
                AG.add_edge(j*(SizeX)+i,j*(SizeX)+i+1,Port=('E','W'),MappedTasks = [],Scheduling={})
                AG.add_edge(j*(SizeX)+i+1,j*(SizeX)+i,Port=('W','E'),MappedTasks = [],Scheduling={})
        for j in range(0,SizeY-1):
            for i in range(0,SizeX):
                if Report:print "CONNECTING",j*(SizeX)+i,"TO",(j+1)*(SizeX)+i
                if Report:print "CONNECTING",(j+1)*SizeX+i,"TO",j*SizeX+i
                AG.add_edge(j*SizeX+i ,(j+1)*SizeX+i,Port=('N','S'),MappedTasks = [],Scheduling={})
                AG.add_edge((j+1)*SizeX+i,j*SizeX+i,Port=('S','N'),MappedTasks = [],Scheduling={})
    elif Topology=='2DRing':
        for j in range(0,SizeY):
            if Report:print "CONNECTING",j*(SizeX),"TO",j*(SizeX)+SizeX-1
            if Report:print "CONNECTING",j*(SizeX)+SizeX-1,"TO",j*(SizeX)
            AG.add_edge(j*(SizeX),j*(SizeX)+SizeX-1,Port=('W','E'),MappedTasks = [],Scheduling={})
            AG.add_edge(j*(SizeX)+SizeX-1,j*(SizeX),Port=('E','W'),MappedTasks = [],Scheduling={})
            for i in range(0,SizeX-1):
                if Report:print "CONNECTING",j*(SizeX)+i,"TO",j*(SizeX)+i+1
                if Report:print "CONNECTING",j*(SizeX)+i+1,"TO",j*(SizeX)+i
                AG.add_edge(j*(SizeX)+i,j*(SizeX)+i+1,Port=('E','W'),MappedTasks = [],Scheduling={})
                AG.add_edge(j*(SizeX)+i+1,j*(SizeX)+i,Port=('W','E'),MappedTasks = [],Scheduling={})
    elif Topology=='2DLine':
        for j in range(0,SizeY):
            for i in range(0,SizeX-1):
                if Report:print "CONNECTING",j*(SizeX)+i,"TO",j*(SizeX)+i+1
                if Report:print "CONNECTING",j*(SizeX)+i+1,"TO",j*(SizeX)+i
                AG.add_edge(j*(SizeX)+i,j*(SizeX)+i+1,Port=('E','W'),MappedTasks = [],Scheduling={})
                AG.add_edge(j*(SizeX)+i+1,j*(SizeX)+i,Port=('W','E'),MappedTasks = [],Scheduling={})
    print("ARCHITECTURE GRAPH (AG) IS READY...")
    return AG

