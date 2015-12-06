# Copyright (C) 2015 Siavoosh Payandeh Azad
import networkx
from ConfigAndPackages import Config
import random
from math import ceil
import operator
# todo: add virtual channel support AG...


class Router():
    def __init__(self):
        self.Unreachable = {}
        self.MappedTasks = {}
        self.Scheduling = {}


class PE():     # PROCESSING ELEMENT
    def __init__(self):
        self.Utilization = 0
        self.Dark = False
        self.MappedTasks = []
        self.Scheduling = {}
        self.Type = 'Processor'       # Can be accelerator or something else


def GenerateManualAG(PE_List, AG_Edge_List, AG_Edge_Port_List):
    """
    Generates an architecture graph from manually defined AG in  Config file
    :param PE_List:  List of Processing Elements
    :param AG_Edge_List: List of Edges between PEs
    :param AG_Edge_Port_List:  Port connection for each of the links between PEs
    :return:
    """
    print("===========================================")
    print("PREPARING AN ARCHITECTURE GRAPH (AG)...")
    AG = networkx.DiGraph()
    for PE in PE_List:
        AG.add_node(PE, PE=PE(), Router=Router(), Region='L')
    for i in range(0, len(AG_Edge_List)):
        EDGE = AG_Edge_List[i]
        AG.add_edge(EDGE[0], EDGE[1], Port=AG_Edge_Port_List[i], MappedTasks={}, Scheduling={})
    print("\tNODES: "+str(AG.nodes(data=False)))
    print("\tEDGES: "+str(AG.edges(data=False)))
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
    SupportedTopologies = ['2DTorus', '2DMesh', '2DRing', '2DLine', '3DMesh']
    print ("===========================================")
    print ("PREPARING AN ARCHITECTURE GRAPH (AG)...")
    print ("TOPOLOGY: "+Topology)
    print ("X SIZE:"+str(SizeX))
    print ("Y SIZE:"+str(SizeY))
    print ("Z SIZE:"+str(SizeZ))
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
            AG.add_node(i, PE=PE(), Router=Router(), Region='N')
        for i in range(0, SizeX):
            CurrentNode = ReturnNodeNumber(i, 0, 0)
            NextNode = ReturnNodeNumber(i, SizeY-1, 0)
            logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
            logging.info("CONNECTING  "+str((SizeY-1)*SizeX+i)+" TO "+str(CurrentNode))
            AG.add_edge(CurrentNode, (SizeY-1)*SizeX+i, Port=('S', 'N'), MappedTasks={}, Scheduling={})
            AG.add_edge(NextNode, CurrentNode, Port=('N', 'S'), MappedTasks={}, Scheduling={})
        for j in range(0, SizeY):
            CurrentNode = ReturnNodeNumber(0, j, 0)
            NextNode = ReturnNodeNumber(SizeX-1, j, 0)
            logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
            logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
            AG.add_edge(CurrentNode, NextNode, Port=('W', 'E'), MappedTasks={}, Scheduling={})
            AG.add_edge(NextNode, CurrentNode, Port=('E', 'W'), MappedTasks={}, Scheduling={})
            for i in range(0, SizeX-1):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i+1, j, 0)
                logging.info("CONNECTING  " + str(CurrentNode) + " TO " + str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks={}, Scheduling={})
        for j in range(0, SizeY-1):
            for i in range(0, SizeX):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i, j+1, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('N', 'S'), MappedTasks={}, Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('S', 'N'), MappedTasks={}, Scheduling={})
    ##############################################################
    if Topology == '2DMesh':
        for i in range(0, SizeX*SizeY):
            AG.add_node(i, PE=PE(), Router=Router(),  Region='N')
        for j in range(0, SizeY):
            for i in range(0, SizeX-1):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i+1, j, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks={}, Scheduling={})
        for j in range(0, SizeY-1):
            for i in range(0, SizeX):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i, j+1, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('N', 'S'), MappedTasks={}, Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('S', 'N'), MappedTasks={}, Scheduling={})
    ##############################################################
    if Topology == '3DMesh':
        for i in range(0, SizeX*SizeY*SizeZ):
            AG.add_node(i, PE=PE(), Router=Router(), Region='N')
        for z in range(0, SizeZ):
            # connect the connections in each layer
            for y in range(0, SizeY):
                for x in range(0, SizeX-1):
                    CurrentNode = ReturnNodeNumber(x, y, z)
                    NextNode = ReturnNodeNumber(x+1, y, z)
                    AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                    AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks={}, Scheduling={})
            for y in range(0, SizeY-1):
                for x in range(0, SizeX):
                    CurrentNode = ReturnNodeNumber(x, y, z)
                    NextNode = ReturnNodeNumber(x, y+1, z)
                    AG.add_edge(CurrentNode, NextNode, Port=('N', 'S'), MappedTasks={}, Scheduling={})
                    AG.add_edge(NextNode, CurrentNode, Port=('S', 'N'), MappedTasks={}, Scheduling={})
        for z in range(0, SizeZ-1):
            # connect routers between layers.
            for y in range(0, SizeY):
                for x in range(0, SizeX):
                    CurrentNode = ReturnNodeNumber(x, y, z)
                    NextNode = ReturnNodeNumber(x, y, z+1)
                    AG.add_edge(CurrentNode, NextNode, Port=('U', 'D'), MappedTasks={}, Scheduling={})
                    AG.add_edge(NextNode, CurrentNode, Port=('D', 'U'), MappedTasks={}, Scheduling={})
    ##############################################################
    elif Topology == '2DRing':
        for i in range(0, SizeX*SizeY):
            AG.add_node(i, PE=PE(), Router=Router(), Region='N')
        for j in range(0, SizeY):
            CurrentNode = ReturnNodeNumber(0, j, 0)
            NextNode = ReturnNodeNumber(SizeX-1, j, 0)
            logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
            logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
            AG.add_edge(CurrentNode, j*SizeX+SizeX-1, Port=('W', 'E'), MappedTasks={}, Scheduling={})
            AG.add_edge(NextNode, CurrentNode, Port=('E', 'W'), MappedTasks={}, Scheduling={})
            for i in range(0, SizeX-1):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i+1, j, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks={}, Scheduling={})
    ##############################################################
    elif Topology == '2DLine':
        for i in range(0, SizeX*SizeY):
            AG.add_node(i, PE=PE(), Router=Router(), Region='N')
        for j in range(0, SizeY):
            for i in range(0, SizeX-1):
                CurrentNode = ReturnNodeNumber(i, j, 0)
                NextNode = ReturnNodeNumber(i+1, j, 0)
                logging.info("CONNECTING  "+str(CurrentNode)+" TO "+str(NextNode))
                logging.info("CONNECTING  "+str(NextNode)+" TO "+str(CurrentNode))
                AG.add_edge(CurrentNode, NextNode, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                AG.add_edge(NextNode, CurrentNode, Port=('W', 'E'), MappedTasks={}, Scheduling={})
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


def UpdateAGRegions(AG):
    """
    Takes an architecture graph and updates the node's Regions according to config file
    :param AG: Architecture graph
    :return: None
    """
    print ("===========================================")
    print ("UPDATING ARCHITECTURE GRAPH (AG) REGIONS...")
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
    NodeY = (NodeNumber / Config.Network_X_Size) % Config.Network_Y_Size
    NodeZ = NodeNumber / (Config.Network_Y_Size * Config.Network_X_Size)
    return NodeX, NodeY, NodeZ


def ReturnNodeNumber(NodeX, NodeY, NodeZ):
    """
    Takes cartesian location of a node and returns node id
    :param NodeX: Location of the node on X axis
    :param NodeY:  Location of the node on Y axis
    :param NodeZ: Location of the node on Z axis
    :return: ID of the node as an integer
    """
    NodeNumber = NodeZ * Config.Network_X_Size * Config.Network_Y_Size + NodeY * Config.Network_X_Size + NodeX
    return NodeNumber


def NodeNeighbors(AG, SHM):
    """
    :param AG: Architecture graph (directed graph)
    :param SHM: System Health Map
    :return: A dictionary with node number as the key and the number of neighbors as values
    """
    node_neighbor = {}
    for Node in AG.nodes():
        NumberOfNeighbours = 0
        for Link in AG.edges():
            if Node in Link:
                if SHM.edge[Link[0]][Link[1]]['LinkHealth']:
                    NumberOfNeighbours += 1
        node_neighbor[Node] = NumberOfNeighbours
    return node_neighbor


def MaxNodeNeighbors(NodeNeighbors, SortedNodeNeighbors):
    """
    :param NodeNeighbors: dictionary with nodes as keys and number of neighbors as values
    :param SortedNodeNeighbors: sorted list of nodes by number of neighbors
    :return: returns a list of nodes with maximum number of neighbors
    """
    MaxNeighbourNum = 0
    for node in SortedNodeNeighbors:
        if NodeNeighbors[node] > MaxNeighbourNum:
            MaxNeighbourNum = NodeNeighbors[node]
    MaxNeighbourNodes = []
    for node in SortedNodeNeighbors:
        if NodeNeighbors[node] == MaxNeighbourNum:
            MaxNeighbourNodes.append(node)
    return MaxNeighbourNodes


def ManhattanDistance(Node1, Node2):
    """
    Takes the node id of two nodes and returns the manhattan distance of those nodes
    :param Node1: Node id of 1st node
    :param Node2: Node id of 2nd node
    :return: returns manhattan distance between two nodes
    """
    x1, y1, z1 = ReturnNodeLocation(Node1)
    x2, y2, z2 = ReturnNodeLocation(Node2)

    return abs(x2-x1)+abs(y2-y1)+abs(z2-z1)


def SetupNetworkPartitioning(AG):
    """
    Takes Architecture Graph as parameter and different regions from
    Config File and Sets up the partitioning for different regions
    :param AG: Architecture Graph
    :return: None
    """
    # Todo: This needs to be tested...
    print ("===========================================")
    print ("SETTING UP NETWORK PARTITIONING...")
    NonCriticalNodes = []
    for node in AG.nodes():
        if node not in Config.CriticalRegionNodes:
            if node not in Config.GateToNonCritical:
                if node not in Config.GateToCritical:
                    NonCriticalNodes.append(node)

    for link in AG.edges():
        # ListOfBrokenLinks
        if link[0] in Config.CriticalRegionNodes and link[1] in NonCriticalNodes:
            Config.ListOfBrokenLinks.append(link)
        if link[0] in NonCriticalNodes and link[1] in Config.CriticalRegionNodes:
            Config.ListOfBrokenLinks.append(link)

        if link[0] in Config.GateToCritical and link[1] in NonCriticalNodes:
            Config.ListOfBrokenLinks.append(link)
        if link[0] in NonCriticalNodes and link[1] in Config.GateToNonCritical:
            Config.ListOfBrokenLinks.append(link)


        # VirtualBrokenLinksForNonCritical
        if link[0] in Config.GateToCritical and link[1] in Config.CriticalRegionNodes:
            Config.VirtualBrokenLinksForNonCritical.append(link)
        if link[0] in Config.GateToCritical and link[1] in Config.GateToNonCritical:
            Config.VirtualBrokenLinksForNonCritical.append(link)
        if link[0] in Config.GateToNonCritical and link[1] in Config.CriticalRegionNodes:
            Config.VirtualBrokenLinksForNonCritical.append(link)

        #  VirtualBrokenLinksForCritical
        if link[0] in Config.GateToNonCritical and link[1] in NonCriticalNodes:
            Config.VirtualBrokenLinksForCritical.append(link)

    print "ListOfBrokenLinks:", Config.ListOfBrokenLinks
    print "VirtualBrokenLinksForNonCritical:", Config.VirtualBrokenLinksForNonCritical
    print "VirtualBrokenLinksForCritical:", Config.VirtualBrokenLinksForCritical
    return None

def RandomDarkness(AG):
    """
    Takes the percentage of Dark Nodes form the Config File and turns of some Nodes.
    :param AG: Architecture Graph
    :return: None
    """
    NumberOfDarkNodes = int(ceil(len(AG.nodes())*Config.DarkSiliconPercentage))
    for i in range(0,NumberOfDarkNodes):
        Node = random.choice(AG.nodes())
        AG.node[Node]['PE'].Dark = True
    return None

def ReturnActiveNodes(AG):
    """
    Returns Nodes in AG which are active (Not falling in dark areas)
    :param AG: Architecture Graph
    :return: list of active nodes.
    """
    ActiveNodes = []
    for Node in AG.nodes():
        if not AG.node[Node]['PE'].Dark:
            ActiveNodes.append(Node)
    return ActiveNodes

def ReturnHealthyNodes(AG, SHM):
    """
    Returns Nodes in AG which are tagged Healthy in SHM
    :param AG: Architecture Graph
    :param SHM: System Health Map
    :return: List of healthy Nodes in AG
    """
    HealthyNodes = []
    for Node in AG.nodes():
        if SHM.node[Node]['NodeHealth']:
            HealthyNodes.append(Node)
    return HealthyNodes


def ReturnHealthyActiveNodes(AG, SHM):
    """
    Returns Nodes in AG which are tagged Healthy in SHM and are active
    :param AG: Architecture Graph
    :param SHM: System Health Map
    :return: list of Healthy Active nodes
    """
    HealthyActiveNodes = []
    for Node in AG.nodes():
        if SHM.node[Node]['NodeHealth']:
            if not AG.node[Node]['PE'].Dark:
                HealthyActiveNodes.append(Node)
    return HealthyActiveNodes