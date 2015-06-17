# Copyright (C) Siavoosh Payandeh Azad
# the main idea of reach-ability is from the following paper:
# NoCDepend: A flexible and scalable Dependability Technique for 3D Networks-on-Chip
# how ever, at the moment we only implemented a 2D version of it.

import networkx,re,copy
import Config
import Routing

def CalculateReachability(AG, NoCRG):
    PortList = ['N', 'E', 'W', 'S']
    for SourceNode in AG.nodes():
        for Port in PortList:
            AG.node[SourceNode]['Unreachable'][Port]=[]
        for DestinationNode in AG.nodes():
            # if SourceNode != DestinationNode:
                for Port in PortList:
                    if not IsDestinationReachableViaPort(NoCRG, SourceNode, Port, DestinationNode, False, False):
                        # print "No Path From", SourceNode,Port,"To",DestinationNode
                        AG.node[SourceNode]['Unreachable'][Port].append(DestinationNode)


def IsDestinationReachableViaPort(NoCRG, SourceNode, Port, DestinationNode, ReturnAllPaths, Report):
    """
    :param NoCRG: NoC Routing Graph
    :param SourceNode: Source node on AG
    :param DestinationNode: Destination node on AG
    :param ReturnAllPaths: boolean that decides to return shortest path or all the paths between two nodes
    :return: return a path (by name of links) on AG from source to destination if possible, None if not.
    """
    Source = str(SourceNode)+str(Port)+str('O')
    Destination = str(DestinationNode)+str('L')+str('O')
    if networkx.has_path(NoCRG, Source, Destination):
        return True
    else:
        if Report:print "\t\tNO PATH FOUND FROM: ", Source, "TO:", Destination
        return False

def ReportReachability (AG):
    print "====================================="
    for Node in AG.nodes():
        print "NODE", Node, "UNREACHABLE NODES:"
        for Port in AG.node[Node]['Unreachable']:
            print "Port:", Port, " ==>", AG.node[Node]['Unreachable'][Port]

def ReportReachabilityInFile (AG,FileName):
    ReachabilityFile = open('Generated_Files/'+FileName+".txt",'w')
    for Node in AG.nodes():
        ReachabilityFile.write( "=====================================\n")
        ReachabilityFile.write( "NODE "+str(Node)+" UNREACHABLE NODES:\n")
        for Port in AG.node[Node]['Unreachable']:
            ReachabilityFile.write("Port: "+str(Port)+" ==> "+str(AG.node[Node]['Unreachable'][Port])+"\n")
    ReachabilityFile.close()

def ReportGSNoCFriendlyReachabilityInFile (AG):
    ReachabilityFile = open("Generated_Files/GSNoC_RectangleFile.txt",'w')
    for Node in AG.nodes():
        NodeX = Node % Config.Network_X_Size
        NodeY = Node / Config.Network_X_Size
        NodeZ = Node / (Config.Network_Y_Size * Config.Network_X_Size)
        for Port in AG.node[Node]['Unreachable']:
            if Port == "S":
                Direction = "SOUTH"
            elif Port == "N":
                Direction = "NORTH"
            elif Port == "W":
                Direction = "WEST"
            else:
                Direction = "EAST"
            for Entry in AG.node[Node]['Unreachable'][Port]:
                ReachabilityFile.write( "["+str(NodeX)+","+str(NodeY)+","+str(NodeZ)+"] ")
                UnreachableArea = AG.node[Node]['Unreachable'][Port][Entry]
                if UnreachableArea[0] is not None:
                    UnreachableX = UnreachableArea[0] % Config.Network_X_Size
                    UnreachableY = UnreachableArea[0] / Config.Network_X_Size
                    UnreachableZ = UnreachableArea[0] / (Config.Network_Y_Size * Config.Network_X_Size)
                    ReachabilityFile.write(str(Direction)+" NetLocCube(ll=["+str(UnreachableX)+","+str(UnreachableY)+
                                           ","+str(UnreachableZ)+"],")
                    UnreachableX = UnreachableArea[1] % Config.Network_X_Size
                    UnreachableY = UnreachableArea[1] / Config.Network_X_Size
                    UnreachableZ = UnreachableArea[1] / (Config.Network_Y_Size * Config.Network_X_Size)
                    ReachabilityFile.write("ur=["+str(UnreachableX)+","+str(UnreachableY)+
                                           ","+str(UnreachableZ)+"])\n")
                else:
                    ReachabilityFile.write(str(Direction)+" NetLocCube(invalid)\n")

        ReachabilityFile.write("\n")
    ReachabilityFile.close()

def OptimizeReachabilityRectangles(AG, NumberOfRects):
    # the idea of merging is that we make a rectangle with representing 2 vertex of it,
    # namely north-west and south-east vertex.
    # Then we try to generate optimal rectangle set that covers all of the nodes...
    print "====================================="
    print "STARTING RECTANGLE OPTIMIZATION..."
    for Node in AG.nodes():
        for Port in AG.node[Node]['Unreachable']:
            RectangleList = {}
            for i in range(0, NumberOfRects):
                RectangleList[i] = (None, None)
            if len( AG.node[Node]['Unreachable'][Port]) == Config.Network_X_Size * Config.Network_Y_Size:
                RectangleList[0] = ( 0 , Config.Network_X_Size*Config.Network_Y_Size -1)
            else:
                RectangleList = copy.deepcopy(MergeNodeWithRectangles(RectangleList,AG.node[Node]['Unreachable'][Port]))
            AG.node[Node]['Unreachable'][Port] = RectangleList
    print "RECTANGLE OPTIMIZATION FINISHED..."
    return None

def MergeNodeWithRectangles (RectangleList,UnreachableNodeList):
    # todo: in this function if we can not perform any loss-less merge, we terminate the process...
    # which is bad... we need to make sure that this node is covered
    for UnreachableNode in UnreachableNodeList:
        Covered = False
        for Rectangle in RectangleList:
            if RectangleList[Rectangle][0] == None:
                # there is no entry, this is the first node to get in...
                RectangleList[Rectangle] = (UnreachableNode,UnreachableNode)
                Covered = True
                break
            else:
                RX1 = RectangleList[Rectangle][0] % Config.Network_X_Size
                RY1 = RectangleList[Rectangle][0] / Config.Network_X_Size
                RX2 = RectangleList[Rectangle][1] % Config.Network_X_Size
                RY2 = RectangleList[Rectangle][1] / Config.Network_X_Size
                NodeX = UnreachableNode % Config.Network_X_Size
                NodeY = UnreachableNode / Config.Network_X_Size
                if NodeX >= RX1 and NodeX <= RX2 and NodeY >= RY1 and NodeY <= RY2:
                    # node is contained inside the rectangle
                    Covered = True
                    break
                else:
                    MergedX1 = min(RX1, NodeX)
                    MergedY1 = min(RY1, NodeY)
                    MergedX2 = max(RX2, NodeX)
                    MergedY2 = max(RY2, NodeY)
                    # print "Merged:" ,MergedY1 * Config.Network_X_Size + MergedX1, MergedY2 * Config.Network_X_Size + MergedX2
                    LossLessMerge = True
                    for NetworkNode_X in range(MergedX1, MergedX2+1):
                        for NetworkNode_Y in range(MergedY1, MergedY2+1):       # MergedY2 < MergedY1
                            NodeNumber = NetworkNode_Y*Config.Network_X_Size+NetworkNode_X
                            if NodeNumber not in UnreachableNodeList:
                                LossLessMerge = False
                                break
                    # if we are not losing any Node, we perform Merge...
                    if LossLessMerge:
                        Merged1 = MergedY1*Config.Network_X_Size+MergedX1
                        Merged2 = MergedY2*Config.Network_X_Size+MergedX2
                        RectangleList[Rectangle] = copy.deepcopy((Merged1, Merged2))
                        Covered = True
                        break
        if not Covered:
            print "COULD NOT PERFORM ANY LOSS_LESS MERGE FOR:", UnreachableNode
            print RectangleList
    return RectangleList

def CalculateReachabilityWithRegions(AG,SHM, NoCRG):
    # first Add the VirtualBrokenLinksForNonCritical
    for VirtualBrokenLink in Config.VirtualBrokenLinksForNonCritical:
        SHM.BreakLink(VirtualBrokenLink,True)
    # Construct The RoutingGraph
    NonCriticalRG = copy.deepcopy(Routing.GenerateNoCRouteGraph(AG, SHM, Config.WestFirst_TurnModel, False, False))
    # calculate the rectangles for Non-Critical
    CalculateReachability(AG, NonCriticalRG)
    # save Non Critical rectangles somewhere
    NonCriticalRect={}
    GateWayRect={}
    for Node in AG.nodes():
        if Node not in Config.CriticalRegionNodes:
            NonCriticalRect[Node] = copy.deepcopy(AG.node[Node]['Unreachable'])
    for Node in Config.GateToNonCritical:
        GateWayRect[Node] = copy.deepcopy(AG.node[Node]['Unreachable'])
    # Restore the VirtualBrokenLinksForNonCritical
    for VirtualBrokenLink in Config.VirtualBrokenLinksForNonCritical:
        SHM.RestoreBrokenLink(VirtualBrokenLink,True)

    # Add VirtualBrokenLinksForCritical
    for VirtualBrokenLink in Config.VirtualBrokenLinksForCritical:
        SHM.BreakLink(VirtualBrokenLink,True)
    # Construct The RoutingGraph
    CriticalRG = copy.deepcopy(Routing.GenerateNoCRouteGraph(AG, SHM, Config.WestFirst_TurnModel, False, False))
    # calculate the rectangles for Critical
    CalculateReachability(AG, CriticalRG)
    # save Critical rectangles somewhere
    CriticalRect={}

    for Node in Config.CriticalRegionNodes:
        CriticalRect[Node] = copy.deepcopy(AG.node[Node]['Unreachable'])
    for Node in Config.GateToCritical:
        GateWayRect[Node] = copy.deepcopy(AG.node[Node]['Unreachable'])
    # Restore the VirtualBrokenLinksForNonCritical
    for VirtualBrokenLink in Config.VirtualBrokenLinksForCritical:
        SHM.RestoreBrokenLink(VirtualBrokenLink,True)

    # Combine Lists
    for Node in AG.nodes():
        if Node in CriticalRect:
            AG.node[Node]['Unreachable'] = copy.deepcopy(CriticalRect[Node])
        elif Node in Config.GateToCritical:
            AG.node[Node]['Unreachable'] = copy.deepcopy(GateWayRect[Node])
        elif Node in Config.GateToNonCritical:
            AG.node[Node]['Unreachable'] = copy.deepcopy(GateWayRect[Node])
        else:
            AG.node[Node]['Unreachable'] = copy.deepcopy(NonCriticalRect[Node])
    # optimize the results
    OptimizeReachabilityRectangles(AG, Config.NumberOfRects)
    return None