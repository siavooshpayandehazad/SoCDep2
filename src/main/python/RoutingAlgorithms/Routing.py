# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import os
import re
from ConfigAndPackages import Config
import Calculate_Reachability
from ArchGraphUtilities import AG_Functions

def GenerateNoCRouteGraph(ag, SystemHealthMap, TurnModel, Report, DetailedReport):
    """
    This function takes the Architecture graph and the health status of the Architecture
    and generates the route graph... route graph is a graph that has all the paths available
    and we can find graph algorithms to find paths...
    :param ag: Architecture Graph
    :param SystemHealthMap: System Health Map
    :return: RouteGraph
    """

    # ACKNOWLEDGEMENT:: The Routing Graph is based on the idea from Thilo Kogge's Bachelor's Thesis

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
    if Report:
        print ("===========================================")
        print ("STARTING BUILDING ROUTING ARCHITECTURE...")
        ReportTurnModel(TurnModel)

    # the order is crucial... do not change
    # to find out why its important, check: connect direct paths
    if Config.Network_Z_Size == 1:
        port_list = ['N', 'W', 'L', 'E', 'S']
    elif Config.Network_Z_Size > 1:
        port_list = ['U', 'N', 'W', 'L', 'E', 'S', 'D']

    noc_rg = networkx.DiGraph()
    for node in ag.nodes():
        if DetailedReport:
            print ("GENERATING PORTS:")
        for port in port_list:
            if DetailedReport:
                print ("\t", str(node)+str(port)+str('I'), "&", str(node)+str(port)+str('O'))
            noc_rg.add_node(str(node)+str(port)+str('I'), Node=node, Port=port, Dir='I')
            noc_rg.add_node(str(node)+str(port)+str('O'), Node=node, Port=port, Dir='O')
        if DetailedReport:
            print ("CONNECTING LOCAL PATHS:")
        for port in port_list:       # connect local to every output port
            if port != 'L':
                noc_rg.add_edge(str(node)+str('L')+str('I'), str(node)+str(port)+str('O'))
                if DetailedReport:
                    print ("\t", 'L', "--->", port)
                noc_rg.add_edge(str(node)+str(port)+str('I'), str(node)+str('L')+str('O'))
                if DetailedReport:
                    print ("\t", port, "--->", 'L')
        if DetailedReport:
            print ("CONNECTING DIRECT PATHS:")
        for i in range(0, int(len(port_list))):   # connect direct paths
            if port_list[i] != 'L':
                if DetailedReport:
                    print ("\t", port_list[i], "--->", port_list[len(port_list)-1-i])
                in_id = str(node)+str(port_list[i])+str('I')
                out_id = str(node)+str(port_list[len(port_list)-1-i])+str('O')
                noc_rg.add_edge(in_id, out_id)

        if DetailedReport:
            print ("CONNECTING TURNS:")
        for turn in TurnModel:
            if turn in SystemHealthMap.SHM.node[node]['TurnsHealth']:
                if SystemHealthMap.SHM.node[node]['TurnsHealth'][turn]:
                    in_port = turn[0]
                    out_port = turn[2]
                    if in_port != out_port:
                        noc_rg.add_edge(str(node)+str(in_port)+str('I'), str(node)+str(out_port)+str('O'))
                    else:       # just for defensive programming reasons...
                        print ("\033[31mERROR::\033[0m U-TURN DETECTED!")
                        print ("TERMINATING THE PROGRAM...")
                        print ("HINT: CHECK YOUR TURN MODEL!")
                        raise ValueError('U-TURN DETECTED IN TURN MODEL!')
                    if DetailedReport:
                        print ("\t", in_port, "--->", out_port)
        if DetailedReport:
            print ("------------------------")

    for link in ag.edges():     # here we should connect connections between routers
        port = ag.edge[link[0]][link[1]]['Port']
        if SystemHealthMap.SHM[link[0]][link[1]]['LinkHealth']:
            if DetailedReport:
                print ("CONNECTING LINK:", link, "BY CONNECTING:", str(link[0])+str(port[0])+str('-Out'),
                       "TO:", str(link[1])+str(port[1])+str('-In'))
            noc_rg.add_edge(str(link[0])+str(port[0])+str('O'), str(link[1])+str(port[1])+str('I'))
        else:
            if DetailedReport:
                print ("BROKEN LINK:", link)
    if Report:
        print ("ROUTE GRAPH IS READY... ")
    return noc_rg


def GenerateNoCRouteGraphFromFile(AG, SystemHealthMap, RoutingFilePath, Report, DetailedReport):
    """
    This function might come very handy specially in relation to different routing algorithms that we can
    implement to increase reachability... (for example odd-even)
    :param AG: Architecture graph
    :param SystemHealthMap: System health map
    :param RoutingFilePath: is the path to a file that contains routing information for each individual router
    :param Report: boolean, which decides if function should print reports to console?
    :return:
    """
    if Report:print ("===========================================")
    if Report:print ("STARTING BUILDING ROUTING ARCHITECTURE...")
    NoCRG = networkx.DiGraph()
    try:
        RoutingFile = open(RoutingFilePath, 'r')
    except IOError:
        print ('CAN NOT OPEN', RoutingFilePath)
    NodesCoveredInFile = []
    while True:
        line = RoutingFile.readline()
        if "Ports" in line:
            Ports = RoutingFile.readline()
            port_list = Ports.split( )
            if DetailedReport:
                print ("PortList", port_list)
        if "Node" in line:
            NodeID = int(re.search(r'\d+', line).group())
            NodesCoveredInFile.append(NodeID)
            if DetailedReport:
                print ("NodeID", NodeID)
                print ("GENERATING PORTS:")
            for port in port_list:
                if DetailedReport:print ("\t", str(NodeID)+str(port)+str('I'), "&", str(NodeID)+str(port)+str('O'))
                NoCRG.add_node(str(NodeID)+str(port)+str('I'), Node=NodeID, Port=port, Dir='I')
                NoCRG.add_node(str(NodeID)+str(port)+str('O'), Node=NodeID, Port=port, Dir='O')
            if DetailedReport:print ("CONNECTING LOCAL PATHS:")
            for port in port_list:       # connect local to every output port
                if port != 'L':
                    NoCRG.add_edge(str(NodeID)+str('L')+str('I'), str(NodeID)+str(port)+str('O'))
                    if DetailedReport:print ("\t", 'L', "--->", port)
                    NoCRG.add_edge(str(NodeID)+str(port)+str('I'), str(NodeID)+str('L')+str('O'))
                    if DetailedReport:print ("\t", port, "--->", 'L')
            if DetailedReport:print ("CONNECTING DIRECT PATHS:")
            for i in range(0, int(len(port_list))):   # connect direct paths
                if port_list[i] != 'L':
                    if DetailedReport:print ("\t", port_list[i], "--->", port_list[len(port_list)-1-i])
                    in_id = str(NodeID)+str(port_list[i])+str('I')
                    out_id = str(NodeID)+str(port_list[len(port_list)-1-i])+str('O')
                    NoCRG.add_edge(in_id, out_id)
            if DetailedReport:print ("CONNECTING TURNS:")
            line = RoutingFile.readline()
            TurnsList = line.split()
            for turn in TurnsList:
                if turn in SystemHealthMap.SHM.node[NodeID]['TurnsHealth']:
                    if SystemHealthMap.SHM.node[NodeID]['TurnsHealth'][turn]:
                        InPort = turn[0]
                        OutPort = turn[2]
                        if InPort != OutPort:
                            NoCRG.add_edge(str(NodeID)+str(InPort)+str('I'), str(NodeID)+str(OutPort)+str('O'))
                        else:   # just for defensive programming reasons...
                            print ("\033[31mERROR::\033[0m U-TURN DETECTED!")
                            print ("TERMINATING THE PROGRAM...")
                            print ("HINT: CHECK YOUR TURN MODEL!")
                            raise ValueError('U-TURN DETECTED IN TURN MODEL!')
                        if DetailedReport:print ("\t", InPort, "--->", OutPort)
            if DetailedReport:print ("------------------------")
        if line == '':
            break
    for node in AG.nodes():
        if node not in NodesCoveredInFile:
            if DetailedReport:print ("GENERATING PORTS:")
            for port in port_list:
                if DetailedReport:print "\t", str(node)+str(port)+str('I'), "&", str(node)+str(port)+str('O')
                NoCRG.add_node(str(node)+str(port)+str('I'), Node=node, Port=port, Dir='I')
                NoCRG.add_node(str(node)+str(port)+str('O'), Node=node, Port=port, Dir='O')
            if DetailedReport:print ("CONNECTING LOCAL PATHS:")
            for port in port_list:       # connect local to every output port
                if port != 'L':
                    NoCRG.add_edge(str(node)+str('L')+str('I'), str(node)+str(port)+str('O'))
                    if DetailedReport:print ("\t", 'L', "--->", port)
                    NoCRG.add_edge(str(node)+str(port)+str('I'), str(node)+str('L')+str('O'))
                    if DetailedReport:print ("\t", port, "--->", 'L')
            if DetailedReport:print ("CONNECTING DIRECT PATHS:")
            for i in range(0,int(len(port_list))):   # connect direct paths
                if port_list[i] != 'L':
                    if DetailedReport:print ("\t", port_list[i], "--->", port_list[len(port_list)-1-i])
                    in_id = str(node)+str(port_list[i])+str('I')
                    out_id = str(node)+str(port_list[len(port_list)-1-i])+str('O')
                    NoCRG.add_edge(in_id, out_id)

    for link in AG.edges():     # here we should connect connections between routers
        Port = AG.edge[link[0]][link[1]]['Port']
        if SystemHealthMap.SHM[link[0]][link[1]]['LinkHealth']:
            if DetailedReport:print ("CONNECTING LINK:", link, "BY CONNECTING:", str(link[0])+str(Port[0])+str('-Out'),
                                     "TO:", str(link[1])+str(Port[1])+str('-In'))
            NoCRG.add_edge(str(link[0])+str(Port[0])+str('O'), str(link[1])+str(Port[1])+str('I'))
        else:
            if DetailedReport:print ("BROKEN LINK:", link)
    if Report: print ("ROUTE GRAPH IS READY... ")
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


def UpdateNoCRouteGraph(NoCRG, FromPort, ToPort, AddOrRemove):
    """
     we would like to eliminate the path or turn that is not working anymore...
    """
    print "ROUTING GRAPH BEING UPDATED..."
    if AddOrRemove == 'REMOVE':
        if (FromPort, ToPort) in NoCRG.edges():
            NoCRG.remove_edge(FromPort, ToPort)
        else:
            print "CONNECTION DIDN'T EXIST IN ROUTE GRAPH"
    if AddOrRemove == 'ADD':
        if (FromPort, ToPort) in NoCRG.edges():
            print "CONNECTION DIDN'T EXIST IN ROUTE GRAPH"
        else:
            NoCRG.add_edge(FromPort, ToPort)
    print "ROUTING GRAPH UPDATED..."
    return None


def FindRouteInRouteGraph(NoCRG, CriticalRG, NonCriticalRG, SourceNode, DestinationNode, Report):
    """
    :param NoCRG: NoC Routing Graph
    :param SourceNode: Source node on AG
    :param DestinationNode: Destination node on AG
    :return: return a path (by name of links) on AG from source to destination if possible, None if not.
    """
    if Config.EnablePartitioning:
        if SourceNode in Config.GateToNonCritical:
            CurrentRG = NonCriticalRG
        elif SourceNode in Config.GateToCritical:
            CurrentRG = CriticalRG
        elif SourceNode in Config.CriticalRegionNodes:
            CurrentRG = CriticalRG
        else:
            CurrentRG = NonCriticalRG
    else:
        CurrentRG = NoCRG
    Source = str(SourceNode)+str('L')+str('I')
    Destination = str(DestinationNode)+str('L')+str('O')
    if networkx.has_path(CurrentRG, Source, Destination):
        if Config.RotingType == 'MinimalPath':
            AllPaths = ReturnMinimalPaths(CurrentRG, SourceNode, DestinationNode)
        elif Config.RotingType == 'NonMinimalPath':
            AllPaths = list(networkx.all_simple_paths(CurrentRG, Source, Destination))
        else:
            raise ValueError("Invalid RotingType")
        AllLinks = []
        for j in range(0, len(AllPaths)):
            Path = AllPaths[j]
            Links = []
            for i in range (0, len(Path)-1):
                if int(re.search(r"\d+", Path[i]).group()) != int(re.search(r"\d+", Path[i+1]).group()):
                    Links.append((int(re.search(r"\d+", Path[i]).group()), int(re.search(r"\d+", Path[i+1]).group())))
            AllLinks.append(Links)
        if Report:print "\t\tFINDING PATH(S) FROM: ", Source, "TO:", Destination, " ==>", \
                            AllLinks

        return AllLinks, len(AllPaths)
    else:
        if Report:print "\t\tNO PATH FOUND FROM: ", Source, "TO:", Destination
        return None, None


def ReturnMinimalPaths(CurrentRG, SourceNode, DestinationNode):
    AllMinimalPaths=[]
    MaxHopCount= AG_Functions.manhattan_distance(SourceNode, DestinationNode)
    Source = str(SourceNode)+str('L')+str('I')
    Destination = str(DestinationNode)+str('L')+str('O')
    AllPaths = list(networkx.all_shortest_paths(CurrentRG, Source, Destination))
    for Path in AllPaths:
        if (len(Path)-2)/2 <= MaxHopCount:
            AllMinimalPaths.append(Path)
    return AllMinimalPaths

