# Copyright (C) 2015 Siavoosh Payandeh Azad
import networkx
from ConfigAndPackages import Config
import operator
# todo: add virtual channel support AG...


def GenerateManualAG(PE_List, AG_Edge_List, AG_Edge_Port_List):
    print "==========================================="
    print "PREPARING AN ARCHITECTURE GRAPH (AG)..."
    AG = networkx.DiGraph()
    for PE in PE_List:
        AG.add_node(PE, MappedTasks=[], Scheduling={}, Utilization=0, Unreachable={}, Region = 'L')
    for i in range(0, len(AG_Edge_List)):
        EDGE = AG_Edge_List[i]
        AG.add_edge(EDGE[0], EDGE[1], Port=AG_Edge_Port_List[i], MappedTasks=[], Scheduling={})
    print "\tNODES: ", AG.nodes(data=False)
    print "\tEDGES: ", AG.edges(data=False)
    print("ARCHITECTURE GRAPH (AG) IS READY...")
    return AG


def GenerateGenericTopologyAG(Topology, SizeX, SizeY, SizeZ, logging):
    """
    Takes a generic topology: 2DTorus, 2DMesh, 2DLine, 2DRing etc. and returns AG
    :param Topology: a string with topology name
    :SizeX: size of network in X dimension
    :SizeY: size of network in Y dimension
    :SizeZ: size of network in Z dimension
    :logging: logging file
    :return: AG
    """
    SupportedTopologies = ['2DSpidergon', '2DTorus', '2DMesh', '2DRing', '2DLine']
    print "==========================================="
    print "PREPARING AN ARCHITECTURE GRAPH (AG)..."
    print "TOPOLOGY:", Topology
    print "X SIZE:", SizeX
    print "Y SIZE:", SizeY
    print "Z SIZE:", SizeZ
    AG = networkx.DiGraph()

    if Topology not in SupportedTopologies:
        logging.error("TOPOLOGY NOT SUPPORTED...")
        raise ValueError('TOPOLOGY ', Topology, ' is NOT SUPPORTED...')

    logging.info("GENERATING ARCHITECTURE GRAPH (AG)...")
    if Topology == '2DSpidergon':
        if SizeX == SizeY:
            # Todo: write spidergon
            pass
    if Topology == '2DTorus':
        for i in range(0, SizeX*SizeY):
            AG.add_node(i, MappedTasks=[], Scheduling={}, Utilization=0, Unreachable={}, Region = 'N')
        for i in range(0, SizeX):
            CurrentNode = ReturnNodeNumber(i, 0, 0)
            NextNode = ReturnNodeNumber(i, SizeY-1, 0)
            logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
            logging.info("CONNECTING  "+str((SizeY-1)*SizeX+i)+" TO "+str(CurrentNode))
            AG.add_edge(CurrentNode, (SizeY-1)*SizeX+i, Port=('S', 'N'), MappedTasks=[], Scheduling={})
            AG.add_edge(NextNode, CurrentNode, Port=('N', 'S'), MappedTasks=[], Scheduling={})
        for j in range(0, SizeY):
            CurrentNode = ReturnNodeNumber(0, j, 0)
            NextNode = ReturnNodeNumber(SizeX-1, j, 0)
            logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
            logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
            AG.add_edge(CurrentNode, NextNode, Port=('W', 'E'), MappedTasks=[], Scheduling={})
            AG.add_edge(NextNode, CurrentNode, Port=('E', 'W'), MappedTasks=[], Scheduling={})
            for i in range(0, SizeX-1):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i+1, j, 0)
                logging.info("CONNECTING  " + str(CurrentNode) + " TO " + str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks=[], Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks=[], Scheduling={})
        for j in range(0, SizeY-1):
            for i in range(0, SizeX):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i, j+1, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('N', 'S'), MappedTasks=[], Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('S', 'N'), MappedTasks=[], Scheduling={})
    ##############################################################
    if Topology == '2DMesh':
        for i in range(0, SizeX*SizeY):
            AG.add_node(i, MappedTasks=[], Scheduling={}, Utilization=0, Unreachable={}, Region = 'N')
        for j in range(0, SizeY):
            for i in range(0, SizeX-1):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i+1, j, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks=[], Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks=[], Scheduling={})
        for j in range(0, SizeY-1):
            for i in range(0, SizeX):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i, j+1, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('N', 'S'), MappedTasks=[], Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('S', 'N'), MappedTasks=[], Scheduling={})
    ##############################################################
    if Topology == '3DMesh':
        for i in range(0, SizeX*SizeY*SizeZ):
            AG.add_node(i, MappedTasks=[], Scheduling={}, Utilization=0, Unreachable={}, Region = 'N')
        for z in range(0,SizeZ):
            # connect the connections in each layer
            for y in range(0, SizeY):
                for x in range(0, SizeX-1):
                    CurrentNode = ReturnNodeNumber(x, y, z)
                    NextNode = ReturnNodeNumber(x+1, y, z)
                    AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks=[], Scheduling={})
                    AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks=[], Scheduling={})
            for y in range(0, SizeY-1):
                for x in range(0, SizeX):
                    CurrentNode = ReturnNodeNumber(x, y, z)
                    NextNode = ReturnNodeNumber(x, y+1, z)
                    AG.add_edge(CurrentNode, NextNode, Port=('N', 'S'), MappedTasks=[], Scheduling={})
                    AG.add_edge(NextNode, CurrentNode, Port=('S', 'N'), MappedTasks=[], Scheduling={})
        for z in  range(0, SizeZ-1):
            # connect routers between layers.
            for y in range(0, SizeY):
                for x in range(0, SizeX):
                    CurrentNode = ReturnNodeNumber(x, y, z)
                    NextNode = ReturnNodeNumber(x, y, z+1)
                    AG.add_edge(CurrentNode, NextNode, Port=('U', 'D'), MappedTasks=[], Scheduling={})
                    AG.add_edge(NextNode, CurrentNode, Port=('D', 'U'), MappedTasks=[], Scheduling={})
    ##############################################################
    elif Topology == '2DRing':
        for i in range(0, SizeX*SizeY):
            AG.add_node(i, MappedTasks=[], Scheduling={}, Utilization=0, Unreachable={}, Region = 'N')
        for j in range(0, SizeY):
            CurrentNode = ReturnNodeNumber(0, j, 0)
            NextNode = ReturnNodeNumber(SizeX-1, j, 0)
            logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
            logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
            AG.add_edge(CurrentNode, j*SizeX+SizeX-1, Port=('W', 'E'), MappedTasks=[], Scheduling={})
            AG.add_edge(NextNode, CurrentNode, Port=('E', 'W'), MappedTasks=[], Scheduling={})
            for i in range(0, SizeX-1):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i+1, j, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks=[], Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks=[], Scheduling={})
    ##############################################################
    elif Topology == '2DLine':
        for i in range(0, SizeX*SizeY):
            AG.add_node(i, MappedTasks=[], Scheduling={}, Utilization=0, Unreachable={}, Region = 'N')
        for j in range(0, SizeY):
            for i in range(0, SizeX-1):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i+1, j, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks=[], Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks=[], Scheduling={})
    print("ARCHITECTURE GRAPH (AG) IS READY...")
    return AG


def GenerateAG(logging):
    """
    This function generates the architecture graph based on the configuration in Config File
    :param logging: logging file
    :return: returns the generated Architecture Graph
    """
    if Config.AG_Type == 'Generic':
        return GenerateGenericTopologyAG(Config.NetworkTopology, Config.Network_X_Size,
                                         Config.Network_Y_Size, Config.Network_Z_Size, logging)
    elif Config.AG_Type == 'Manual':
        return GenerateManualAG(Config.PE_List, Config.AG_Edge_List, Config.AG_Edge_Port_List)
    else:
        raise ValueError('AG TYPE DOESNT EXIST...!!!')


def UpdateAGRegions (AG):
    print "==========================================="
    print "UPDATING ARCHITECTURE GRAPH (AG) REGIONS..."
    for Node in AG.nodes():
        if Node in Config.CriticalRegionNodes:
            AG.node[Node]['Region'] = 'H'
        elif Node in Config.GateToCritical:
            AG.node[Node]['Region'] = 'GH'
        elif Node in Config.GateToNonCritical:
            AG.node[Node]['Region'] = 'GNH'
        else:
            AG.node[Node]['Region'] = 'L'
    print("ARCHITECTURE GRAPH (AG) REGIONS UPDATED...")
    return None


def ReturnNodeLocation(NodeNumber):
    """
    calculates the Cartesian location of the node
    Examples:
    ReturnNodeLocation(0) = (0,0,0)
    ReturnNodeLocation(Config.Network_X_Size * Config.Network_Y_Size * Config.Network_Z_Size - 1) =
            (Config.Network_X_Size -1, Config.Network_Y_Size - 1, Config.Network_Z_Size -1)
    :param NodeNumber: The node id used in AG
    :return: Cartesian location of the node in the form of (x,y,z)
    """
    NodeX = NodeNumber % Config.Network_X_Size
    NodeY = NodeNumber / Config.Network_X_Size
    NodeZ = NodeNumber / (Config.Network_Y_Size * Config.Network_X_Size)
    return NodeX, NodeY, NodeZ

def ReturnNodeNumber(NodeX, NodeY, NodeZ):
    NodeNumber = NodeZ*Config.Network_X_Size*Config.Network_Y_Size + NodeY*Config.Network_X_Size+NodeX
    return NodeNumber


def NodeNeighbors(AG, SHM):
    NodeNeighbor = {}
    for Node in AG.nodes():
        NumberOfNeighbours = 0
        for Link in AG.edges():
            if Node in Link:
                if SHM.SHM.edge[Link[0]][Link[1]]['LinkHealth']:
                    NumberOfNeighbours += 1
        NodeNeighbor[Node] = NumberOfNeighbours
    return NodeNeighbor


def MaxNodeNeighbors(NodeNeighbors, SortedNodeNeighbors):
    MaxNeighbourNum = 0
    for node in SortedNodeNeighbors:
        if NodeNeighbors[node] > MaxNeighbourNum:
            MaxNeighbourNum = NodeNeighbors[node]
    MaxNeighbourNodes = []
    for node in SortedNodeNeighbors:
        if NodeNeighbors[node] == MaxNeighbourNum:
            MaxNeighbourNodes.append(node)
    return MaxNeighbourNodes


def ManhattanDistance(Node1,Node2):
    x1,y1,z1 = ReturnNodeLocation(Node1)
    x2,y2,z2 = ReturnNodeLocation(Node2)

    return abs(x2-x1)+abs(y2-y1)+abs(z2-z1)