# Copyright (C) Siavoosh Payandeh Azad
# the main idea of reach-ability is from the following paper:
# NoCDepend: A flexible and scalable Dependability Technique for 3D Networks-on-Chip
# how ever, at the moment we only implemented a 2D version of it.

import networkx,re,copy
from ConfigAndPackages import Config
import Routing
from ArchGraphUtilities import AG_Functions

def calculate_reachability(AG, NoCRG):
    if '3D' in Config.NetworkTopology:
        PortList = ['U', 'N', 'E', 'W', 'S', 'D']
    else:
        PortList = ['N', 'E', 'W', 'S']

    for SourceNode in AG.nodes():
        for Port in PortList:
            AG.node[SourceNode]['Router'].Unreachable[Port]=[]
        for DestinationNode in AG.nodes():
            # if SourceNode != DestinationNode:
                for Port in PortList:
                    if not IsDestinationReachableViaPort(NoCRG, SourceNode, Port, DestinationNode, False, False):
                        # print ("No Path From", SourceNode,Port,"To",DestinationNode)
                        AG.node[SourceNode]['Router'].Unreachable[Port].append(DestinationNode)


def IsDestinationReachableViaPort(NoCRG, SourceNode, Port, DestinationNode, ReturnAllPaths, Report):

    # the Source port should be output port since this is output of router to other routers
    Source = str(SourceNode)+str(Port)+str('O')
    # the destination port should be output port since this is output of router to PE
    # (which will be connected to PE's input port)
    Destination = str(DestinationNode)+str('L')+str('O')
    if networkx.has_path(NoCRG, Source, Destination):
        return True
    else:
        if Report:print ("\t\tNO PATH FOUND FROM: ", Source, "TO:", Destination)
        return False


def IsDestReachableFromSource(NoCRG, SourceNode, DestinationNode):

    # the Source port should be input port since this is input of router
    # (which will be connected to PE's output port)
    Source = str(SourceNode)+str('L')+str('I')
    # the destination port should be output port since this is output of router to PE
    # (which will be connected to PE's input port)
    Destination = str(DestinationNode)+str('L')+str('O')
    if networkx.has_path(NoCRG, Source, Destination):
        return True
    else:
        return False


def HowManyPathsFromSource(NoCRG, SourceNode, DestinationNode):
    Source = str(SourceNode)+str('L')+str('I')
    Destination = str(DestinationNode)+str('L')+str('O')
    if networkx.has_path(NoCRG, Source, Destination):
        NumberOfPaths = len(list(networkx.all_simple_paths(NoCRG, Source, Destination)))
        return NumberOfPaths
    else:
        return 0


def OptimizeReachabilityRectangles(AG, NumberOfRects):
    # the idea of merging is that we make a rectangle with representing 2 vertex of it,
    # namely north-west and south-east vertex.
    # Then we try to generate optimal rectangle set that covers all of the nodes...
    print ("=====================================")
    print ("STARTING RECTANGLE OPTIMIZATION...")
    for Node in AG.nodes():
        for Port in AG.node[Node]['Router'].Unreachable:
            RectangleList = {}
            for i in range(0, NumberOfRects):
                RectangleList[i] = (None, None)
            if len( AG.node[Node]['Router'].Unreachable[Port]) == Config.Network_X_Size*Config.Network_Y_Size:
                RectangleList[0] = (0, Config.Network_X_Size*Config.Network_Y_Size-1)
            else:
                RectangleList = copy.deepcopy(MergeNodeWithRectangles(RectangleList, AG.node[Node]['Router'].Unreachable[Port]))
            AG.node[Node]['Router'].Unreachable[Port] = RectangleList
    print ("RECTANGLE OPTIMIZATION FINISHED...")
    return None


def MergeNodeWithRectangles (RectangleList, UnreachableNodeList):
    # todo: in this function if we can not perform any loss-less merge, we terminate the process...
    # which is bad... we need to make sure that this node is covered
    for UnreachableNode in UnreachableNodeList:
        Covered = False
        for Rectangle in RectangleList:
            if RectangleList[Rectangle][0] == None:
                # there is no entry, this is the first node to get in...
                RectangleList[Rectangle] = (UnreachableNode, UnreachableNode)
                Covered = True
                break
            else:
                if is_node_inside_rectangle(RectangleList[Rectangle], UnreachableNode):
                    Covered = True
                    break
                else:
                    MergedX1, MergedY1, MergedZ1, MergedX2, MergedY2, MergedZ2 = MergeRectangleWithNode(RectangleList[Rectangle][0],
                                                                                   RectangleList[Rectangle][1],
                                                                                   UnreachableNode)
                    # print ("Merged:" ,MergedY1 * Config.Network_X_Size + MergedX1,
                    #        MergedY2 * Config.Network_X_Size + MergedX2)
                    LossLessMerge = True
                    for NetworkNode_X in range(MergedX1, MergedX2+1):
                        for NetworkNode_Y in range(MergedY1, MergedY2+1):
                            for NetworkNode_Z in range(MergedZ1, MergedZ2+1):
                                NodeNumber = AG_Functions.return_node_number(NetworkNode_X,NetworkNode_Y, NetworkNode_Z)
                                if NodeNumber not in UnreachableNodeList:
                                    LossLessMerge = False
                                    break
                    # if we are not losing any Node, we perform Merge...
                    if LossLessMerge:
                        Merged1 = AG_Functions.return_node_number(MergedX1,MergedY1, MergedZ1)
                        Merged2 = AG_Functions.return_node_number(MergedX2,MergedY2, MergedZ2)
                        RectangleList[Rectangle] = copy.deepcopy((Merged1, Merged2))
                        Covered = True
                        break
        if not Covered:
            pass
            # print ("COULD NOT PERFORM ANY LOSS-LESS MERGE FOR:"+str(UnreachableNode))
            # print (RectangleList)
    return RectangleList


def is_node_inside_rectangle(Rect,Node):
    RX1, RY1, RZ1 = AG_Functions.return_node_location(Rect[0])
    RX2, RY2, RZ2 = AG_Functions.return_node_location(Rect[1])
    NodeX, NodeY, NodeZ = AG_Functions.return_node_location(Node)
    if RX1 <= NodeX <= RX2 and RY1 <= NodeY <= RY2 and RZ1 <= NodeZ <= RZ2:
        return True
    else:
        return False


def MergeRectangleWithNode(Rect_ll, Rect_ur, Node):
    x1, y1, z1 = AG_Functions.return_node_location(Rect_ll)
    x2, y2, z2 = AG_Functions.return_node_location(Rect_ur)
    NodeX, NodeY, NodeZ = AG_Functions.return_node_location(Node)
    MergedX1 = min(x1, NodeX)
    MergedY1 = min(y1, NodeY)
    MergedZ1 = min(z1, NodeZ)
    MergedX2 = max(x2, NodeX)
    MergedY2 = max(y2, NodeY)
    MergedZ2 = max(z2, NodeZ)
    return MergedX1, MergedY1, MergedZ1, MergedX2, MergedY2, MergedZ2


def ClearReachabilityCalculations(ag):
    for node in ag.nodes():
        for port in ag.node[node]['Router'].Unreachable:
            ag.node[node]['Router'].Unreachable[port] = {}
    return None


def calculate_reachability_with_regions(AG, SHMU):
    # first Add the VirtualBrokenLinksForNonCritical
    AlreadyBrokenLinks= []
    for VirtualBrokenLink in Config.VirtualBrokenLinksForNonCritical:
        if SHMU.SHM.edge[VirtualBrokenLink[0]][VirtualBrokenLink[1]]['LinkHealth']:
            SHMU.break_link(VirtualBrokenLink,True)
        else:
            AlreadyBrokenLinks.append(VirtualBrokenLink)
    # Construct The RoutingGraph
    NonCriticalRG = copy.deepcopy(Routing.GenerateNoCRouteGraph(AG, SHMU, Config.UsedTurnModel, False, False))
    # calculate the rectangles for Non-Critical
    calculate_reachability(AG, NonCriticalRG)
    # save Non Critical rectangles somewhere
    NonCriticalRect={}
    GateWayRect={}
    for Node in Config.GateToNonCritical:
        GateWayRect[Node] = copy.deepcopy(AG.node[Node]['Router'].Unreachable)
    for Node in AG.nodes():
        if Node not in Config.CriticalRegionNodes:
            NonCriticalRect[Node] = copy.deepcopy(AG.node[Node]['Router'].Unreachable)
    # Restore the VirtualBrokenLinksForNonCritical
    for VirtualBrokenLink in Config.VirtualBrokenLinksForNonCritical:
        if VirtualBrokenLink not in AlreadyBrokenLinks:
            SHMU.restore_broken_link(VirtualBrokenLink,True)

    AlreadyBrokenLinks = []
    # Add VirtualBrokenLinksForCritical
    for VirtualBrokenLink in Config.VirtualBrokenLinksForCritical:
        if SHMU.SHM.edge[VirtualBrokenLink[0]][VirtualBrokenLink[1]]['LinkHealth']:
            SHMU.break_link(VirtualBrokenLink, True)
        else:
            AlreadyBrokenLinks.append(VirtualBrokenLink)
    ClearReachabilityCalculations(AG)
    # Construct The RoutingGraph
    CriticalRG = copy.deepcopy(Routing.GenerateNoCRouteGraph(AG, SHMU, Config.UsedTurnModel, False, False))
    # calculate the rectangles for Critical
    calculate_reachability(AG, CriticalRG)
    # save Critical rectangles somewhere
    CriticalRect={}
    for Node in Config.CriticalRegionNodes:
        CriticalRect[Node] = copy.deepcopy(AG.node[Node]['Router'].Unreachable)
    for Node in Config.GateToCritical:
        GateWayRect[Node] = copy.deepcopy(AG.node[Node]['Router'].Unreachable)
    # Restore the VirtualBrokenLinksForNonCritical
    for VirtualBrokenLink in Config.VirtualBrokenLinksForCritical:
        if VirtualBrokenLink not in AlreadyBrokenLinks:
            SHMU.restore_broken_link(VirtualBrokenLink, True)

    # Combine Lists
    for Node in AG.nodes():
        if Node in CriticalRect:
            AG.node[Node]['Router'].Unreachable = copy.deepcopy(CriticalRect[Node])
        elif Node in Config.GateToCritical:
            AG.node[Node]['Router'].Unreachable = copy.deepcopy(GateWayRect[Node])
        elif Node in Config.GateToNonCritical:
            AG.node[Node]['Router'].Unreachable = copy.deepcopy(GateWayRect[Node])
        else:
            AG.node[Node]['Router'].Unreachable = copy.deepcopy(NonCriticalRect[Node])
    # optimize the results
    OptimizeReachabilityRectangles(AG, Config.NumberOfRects)
    return CriticalRG, NonCriticalRG



def ReachabilityMetric(ag, noc_rg, report):
    """
    returns the ratio of sum of number of number of paths
    to each nodes for each node to all possible reachable case (where each node can reach all other nodes)
    :param ag: architecture graph
    :param noc_rg: NoC routing graph
    :param report: report switch
    :return: reachability metric
    """
    if report:
        print ("=====================================")
        print ("CALCULATING REACH-ABILITY METRIC OF THE CURRENT ROUTING ALGORITHM UNDER CURRENT FAULT CONFIG")
    reachability_counter = 0
    for source_node in ag.nodes():
        for destination_node in ag.nodes():
            if source_node != destination_node:
                if IsDestReachableFromSource(noc_rg, source_node, destination_node):
                    reachability_counter += 1
    r_metric = float(reachability_counter)
    if report:
        print ("REACH-ABILITY METRIC: "+str(r_metric))
    return r_metric