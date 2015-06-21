# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import os
import re
import Config

def GenerateNoCRouteGraph(AG,SystemHealthMap,TurnModel,Report,DetailedReport):
    """
    This function takes the Architecture graph and the health status of the Architecture
    and generates the route graph... route graph is a graph that has all the paths available
    and we can find graph algorithms to find paths...
    :param AG: Architecture Graph
    :param SystemHealthMap: System Health Map
    :return: RouteGraph
    """

    # ACKNOWLEDGEMENT:: The Routing Graph is based on the idea from Thilo Kogge's Master Thesis

    # all the links that go inside the router are called in
    #
    #              _______|____|______
    #             |       O    I      |
    #             |                  O|----> E out
    # W in ---->  |I                  |
    #             |                  I|<---- E in
    #             |                   |
    # W out <---- |O                  |
    #             |                 O/
    #             |_____I___O______I/
    #                   |   |
    #
    # the turns should be named with port 2 port naming convention...
    # E2N is a turn that connects input of East port of the router to
    # output of north

    # todo: add virtual channel support for the routing graph...
    if Report: print "==========================================="
    if Report: print "STARTING BUILDING ROUTING ARCHITECTURE..."
    if Report: ReportTurnModel(TurnModel)
    PortList = ['N','W','L','E','S']  # the order is crucial... do not change
                                      # to find out why its important, check: connect direct paths
    NoCRG = networkx.DiGraph()
    for node in AG.nodes():
        if DetailedReport:print "GENERATING PORTS:"
        for port in PortList:
            if DetailedReport:print "\t",str(node)+str(port)+str('I'),"&",str(node)+str(port)+str('O')
            NoCRG.add_node(str(node)+str(port)+str('I'),Node=node,Port=port,Dir='I')
            NoCRG.add_node(str(node)+str(port)+str('O'),Node=node,Port=port,Dir='O')
        if DetailedReport:print "CONNECTING LOCAL PATHS:"
        for port in PortList:       # connect local to every output port
            if port != 'L':
                NoCRG.add_edge(str(node)+str('L')+str('I'),str(node)+str(port)+str('O'))
                if DetailedReport:print "\t", 'L', "--->", port
                NoCRG.add_edge(str(node)+str(port)+str('I'),str(node)+str('L')+str('O'))
                if DetailedReport:print "\t", port, "--->", 'L'
        if DetailedReport:print "CONNECTING DIRECT PATHS:"
        for i in range(0,int(len(PortList))):   # connect direct paths
            if PortList[i] != 'L':
                if DetailedReport:print "\t", PortList[i], "--->", PortList[len(PortList)-1-i]
                inID= str(node)+str(PortList[i])+str('I')
                outID=str(node)+str(PortList[len(PortList)-1-i])+str('O')
                NoCRG.add_edge(inID,outID)

        if DetailedReport:print "CONNECTING TURNS:"
        for turn in TurnModel:
            if turn in SystemHealthMap.SHM.node[node]['TurnsHealth']:
                if SystemHealthMap.SHM.node[node]['TurnsHealth'][turn]:
                    InPort=turn[0]
                    OutPort=turn[2]
                    if InPort != OutPort:
                        NoCRG.add_edge(str(node)+str(InPort)+str('I'),str(node)+str(OutPort)+str('O'))
                    else:       # just for defensive programming reasons...
                        print "\033[31mERROR::\033[0m U-TURN DETECTED!"
                        print "TERMINATING THE PROGRAM..."
                        print "HINT: CHECK YOUR TURN MODEL!"
                        raise ValueError('U-TURN DETECTED IN TURN MODEL!')
                    if DetailedReport:print "\t", InPort, "--->", OutPort
        if DetailedReport:print "------------------------"

    for link in AG.edges():     # here we should connect connections between routers
        Port=AG.edge[link[0]][link[1]]['Port']
        if SystemHealthMap.SHM[link[0]][link[1]]['LinkHealth']:
            if DetailedReport:print "CONNECTING LINK:", link, "BY CONNECTING:", str(link[0])+str(Port[0])+str('-Out'),\
                "TO:", str(link[1])+str(Port[1])+str('-In')
            NoCRG.add_edge(str(link[0])+str(Port[0])+str('O'), str(link[1])+str(Port[1])+str('I'))
        else:
            if DetailedReport:print "BROKEN LINK:", link
    if Report: print "ROUTE GRAPH IS READY... "
    return NoCRG


def GenerateNoCRouteGraphFromFile(AG,SystemHealthMap,RoutingFilePath,Report,DetailedReport):
    """
    This function might come very handy specially in relation to different routing algorithms that we can
    implement to increase reachability... (for example odd-even)
    :param AG: Architecture graph
    :param SystemHealthMap: System health map
    :param RoutingFilePath: is the path to a file that contains routing information for each individual router
    :param Report: boolean, which decides if function should print reports to console?
    :return:
    """
    if Report:print "==========================================="
    if Report:print "STARTING BUILDING ROUTING ARCHITECTURE..."
    NoCRG = networkx.DiGraph()
    try:
        RoutingFile = open(RoutingFilePath, 'r')
    except IOError:
        print 'CAN NOT OPEN', RoutingFilePath
    while True:
        line = RoutingFile.readline()
        if "Ports" in line:
            Ports = RoutingFile.readline()
            PortList = Ports.split( )
            if DetailedReport: print "PortList", PortList
        if "Node" in line:
            NodeID = int(re.search(r'\d+', line).group())
            if DetailedReport:print "NodeID",NodeID
            if DetailedReport:print "GENERATING PORTS:"
            for port in PortList:
                if DetailedReport:print "\t",str(NodeID)+str(port)+str('I'),"&",str(NodeID)+str(port)+str('O')
                NoCRG.add_node(str(NodeID)+str(port)+str('I'),Node=NodeID,Port=port,Dir='I')
                NoCRG.add_node(str(NodeID)+str(port)+str('O'),Node=NodeID,Port=port,Dir='O')
            if DetailedReport:print "CONNECTING LOCAL PATHS:"
            for port in PortList:       # connect local to every output port
                if port != 'L':
                    NoCRG.add_edge(str(NodeID)+str('L')+str('I'),str(NodeID)+str(port)+str('O'))
                    if DetailedReport:print "\t", 'L', "--->", port
                    NoCRG.add_edge(str(NodeID)+str(port)+str('I'),str(NodeID)+str('L')+str('O'))
                    if DetailedReport:print "\t", port, "--->", 'L'
            if DetailedReport:print "CONNECTING DIRECT PATHS:"
            for i in range(0,int(len(PortList))):   # connect direct paths
                if PortList[i] != 'L':
                    if DetailedReport:print "\t", PortList[i], "--->", PortList[len(PortList)-1-i]
                    inID = str(NodeID)+str(PortList[i])+str('I')
                    outID = str(NodeID)+str(PortList[len(PortList)-1-i])+str('O')
                    NoCRG.add_edge(inID,outID)
            if DetailedReport:print "CONNECTING TURNS:"
            line = RoutingFile.readline()
            TurnsList = line.split()
            for turn in TurnsList:
                if turn in SystemHealthMap.SHM.node[NodeID]['TurnsHealth']:
                    if SystemHealthMap.SHM.node[NodeID]['TurnsHealth'][turn]:
                        InPort = turn[0]
                        OutPort = turn[2]
                        if InPort != OutPort:
                            NoCRG.add_edge(str(NodeID)+str(InPort)+str('I'),str(NodeID)+str(OutPort)+str('O'))
                        else:   # just for defensive programming reasons...
                            print "\033[31mERROR::\033[0m U-TURN DETECTED!"
                            print "TERMINATING THE PROGRAM..."
                            print "HINT: CHECK YOUR TURN MODEL!"
                            raise ValueError('U-TURN DETECTED IN TURN MODEL!')
                        if DetailedReport:print "\t", InPort, "--->", OutPort
            if DetailedReport:print "------------------------"
        if line == '':
            break
    for link in AG.edges():     # here we should connect connections between routers
        Port = AG.edge[link[0]][link[1]]['Port']
        if SystemHealthMap.SHM[link[0]][link[1]]['LinkHealth']:
            if DetailedReport:print "CONNECTING LINK:", link, "BY CONNECTING:", str(link[0])+str(Port[0])+str('-Out'),\
                "TO:", str(link[1])+str(Port[1])+str('-In')
            NoCRG.add_edge(str(link[0])+str(Port[0])+str('O'), str(link[1])+str(Port[1])+str('I'))
        else:
            if DetailedReport:print "BROKEN LINK:", link
    if Report: print "ROUTE GRAPH IS READY... "
    return NoCRG


def ReportTurnModel(TurnModel):
    """
    prints the turn model for a 2D network in the console
    Only usable if there is a uniform Turn model over the network
    :param TurnModel: set of allowed turns in a 2D network
    :return: None
    """
    print "\tUSING TURN MODEL: ", TurnModel
    return None


def UpdateNoCRouteGraph(SystemHealthMap,NewEvent):
    """
     we would like to eliminate the path or turn that is not working anymore...
    :param SystemHealthMap: System Health Map
    :param NewEvent: new fault that has happened...
    :return:
    """
    # ToDo: Updating NoCRouteGraph
    return None


def FindRouteInRouteGraph(NoCRG,SourceNode,DestinationNode,ReturnAllPaths,Report):
    """
    :param NoCRG: NoC Routing Graph
    :param SourceNode: Source node on AG
    :param DestinationNode: Destination node on AG
    :param ReturnAllPaths: boolean that decides to return shortest path or all the paths between two nodes
    :return: return a path (by name of links) on AG from source to destination if possible, None if not.
    """
    Source = str(SourceNode)+str('L') + str('I')
    Destination = str(DestinationNode) + str('L') + str('O')
    if networkx.has_path(NoCRG,Source,Destination):
        # ToDO: fixing the routing for partitioned network
        # if Config.EnablePartitioning:
        #        pass
        # else:
            ShortestPath = networkx.shortest_path(NoCRG,Source,Destination)
            AllPaths = list(networkx.all_simple_paths(NoCRG,Source,Destination))
            ShortestLinks = []
            for i in range (0,len(ShortestPath)-1):
                #if ShortestPath[i][0] != ShortestPath[i+1][0]:
                if int(re.search(r'\d+', ShortestPath[i]).group()) != int(re.search(r'\d+', ShortestPath[i+1]).group()):
                    ShortestLinks.append((int(re.search(r'\d+', ShortestPath[i]).group()),int(re.search(r'\d+', ShortestPath[i+1]).group())))
            AllLinks = []
            for j in range(0, len(AllPaths)):
                Path = AllPaths[j]
                Links = []
                for i in range (0,len(Path)-1):
                    if int(re.search(r'\d+', Path[i]).group()) != int(re.search(r'\d+', Path[i+1]).group()):
                        Links.append((int(re.search(r'\d+', Path[i]).group()),int(re.search(r'\d+', Path[i+1]).group())))
                AllLinks.append(Links)
            if Report:print "\t\tFINDING PATH(S) FROM: ", Source, "TO:", Destination," ==>", AllLinks if ReturnAllPaths else ShortestLinks
            if ReturnAllPaths:
                return AllLinks
            else:
                return ShortestLinks
    else:
        if Report:print "\t\tNO PATH FOUND FROM: ", Source, "TO:", Destination
        return None