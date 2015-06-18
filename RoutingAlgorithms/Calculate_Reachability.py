# Copyright (C) Siavoosh Payandeh Azad
# the main idea of reach-ability is from the following paper:
# NoCDepend: A flexible and scalable Dependability Technique for 3D Networks-on-Chip
# how ever, at the moment we only implemented a 2D version of it.

import networkx,re,copy
import Config
import Routing
from ArchGraphUtilities import AG_Functions

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
                RectangleList[0] = (0, Config.Network_X_Size*Config.Network_Y_Size -1)
            else:
                RectangleList = copy.deepcopy(MergeNodeWithRectangles(RectangleList, AG.node[Node]['Unreachable'][Port]))
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
                if IsNodeInsideRectangle(RectangleList[Rectangle],UnreachableNode):
                    Covered = True
                    break
                else:
                    MergedX1, MergedY1, MergedZ1, MergedX2, MergedY2, MergedZ2 = MergeRectangleWithNode(RectangleList[Rectangle][0],
                                                                                   RectangleList[Rectangle][1],
                                                                                   UnreachableNode)
                    # print "Merged:" ,MergedY1 * Config.Network_X_Size + MergedX1, MergedY2 * Config.Network_X_Size + MergedX2
                    LossLessMerge = True
                    for NetworkNode_X in range(MergedX1, MergedX2+1):
                        for NetworkNode_Y in range(MergedY1, MergedY2+1):
                            for NetworkNode_Z in range(MergedZ1, MergedZ2+1):
                                NodeNumber = AG_Functions.ReturnNodeNumber(NetworkNode_X,NetworkNode_Y, NetworkNode_Z)
                                if NodeNumber not in UnreachableNodeList:
                                    LossLessMerge = False
                                    break
                    # if we are not losing any Node, we perform Merge...
                    if LossLessMerge:
                        Merged1 = AG_Functions.ReturnNodeNumber(MergedX1,MergedY1, MergedZ1)
                        Merged2 = AG_Functions.ReturnNodeNumber(MergedX2,MergedY2, MergedZ2)
                        RectangleList[Rectangle] = copy.deepcopy((Merged1, Merged2))
                        Covered = True
                        break
        if not Covered:
            print "COULD NOT PERFORM ANY LOSS_LESS MERGE FOR:", UnreachableNode
            print RectangleList
    return RectangleList


def IsNodeInsideRectangle(Rect,Node):
    RX1, RY1, RZ1 = AG_Functions.ReturnNodeLocation(Rect[0])
    RX2, RY2, RZ2 = AG_Functions.ReturnNodeLocation(Rect[1])
    NodeX, NodeY, NodeZ = AG_Functions.ReturnNodeLocation(Node)
    if NodeX >= RX1 and NodeX <= RX2 and NodeY >= RY1 and NodeY <= RY2 and NodeZ >= RZ1 and NodeZ <= RZ2:
        return True
    else:
        return False


def MergeRectangleWithNode(Rect_ll, Rect_ur, Node):
    X1, Y1, Z1 = AG_Functions.ReturnNodeLocation(Rect_ll)
    X2, Y2, Z2 = AG_Functions.ReturnNodeLocation(Rect_ur)
    NodeX, NodeY, NodeZ = AG_Functions.ReturnNodeLocation(Node)
    MergedX1 = min(X1, NodeX)
    MergedY1 = min(Y1, NodeY)
    MergedZ1 = min(Z1, NodeZ)
    MergedX2 = max(X2, NodeX)
    MergedY2 = max(Y2, NodeY)
    MergedZ2 = max(Z2, NodeZ)
    return MergedX1,MergedY1,MergedZ1, MergedX2, MergedY2, MergedZ2


def ClearReachabilityCalculations(AG):
    for Node in AG.nodes():
        for Port in AG.node[Node]['Unreachable']:
            AG.node[Node]['Unreachable'][Port] = {}
    return None


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
    for Node in Config.GateToNonCritical:
        GateWayRect[Node] = copy.deepcopy(AG.node[Node]['Unreachable'])
    for Node in AG.nodes():
        if Node not in Config.CriticalRegionNodes:
            NonCriticalRect[Node] = copy.deepcopy(AG.node[Node]['Unreachable'])
    # Restore the VirtualBrokenLinksForNonCritical
    for VirtualBrokenLink in Config.VirtualBrokenLinksForNonCritical:
        SHM.RestoreBrokenLink(VirtualBrokenLink,True)

    # Add VirtualBrokenLinksForCritical
    for VirtualBrokenLink in Config.VirtualBrokenLinksForCritical:
        SHM.BreakLink(VirtualBrokenLink,True)
    ClearReachabilityCalculations(AG)
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