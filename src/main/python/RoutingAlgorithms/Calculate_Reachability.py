# Copyright (C) Siavoosh Payandeh Azad
# the main idea of reach-ability is from the following paper:
# NoCDepend: A flexible and scalable Dependability Technique for 3D Networks-on-Chip
# how ever, at the moment we only implemented a 2D version of it.

import networkx,re,copy
from ConfigAndPackages import Config
import Routing
from ArchGraphUtilities import AG_Functions

def calculate_reachability(ag, NoCRG):
    if '3D' in Config.NetworkTopology:
        port_list = ['U', 'N', 'E', 'W', 'S', 'D']
    else:
        port_list = ['N', 'E', 'W', 'S']

    for source_node in ag.nodes():
        for port in port_list:
            ag.node[source_node]['Router'].Unreachable[port] = []
        for destination_node in ag.nodes():
            # if SourceNode != DestinationNode:
                for port in port_list:
                    if not IsDestinationReachableViaPort(NoCRG, source_node, port, destination_node, False, False):
                        # print ("No Path From", SourceNode,Port,"To",DestinationNode)
                        ag.node[source_node]['Router'].Unreachable[port].append(destination_node)


def IsDestinationReachableViaPort(noc_rg, source_node, port, destination_node, return_all_paths, report):

    # the Source port should be output port since this is output of router to other routers
    source = str(source_node)+str(port)+str('O')
    # the destination port should be output port since this is output of router to PE
    # (which will be connected to PE's input port)
    destination = str(destination_node)+str('L')+str('O')
    if networkx.has_path(noc_rg, source, destination):
        return True
    else:
        if report:print ("\t\tNO PATH FOUND FROM: ", source, "TO:", destination)
        return False


def IsDestReachableFromSource(noc_rg, source_node, destination_node):

    # the Source port should be input port since this is input of router
    # (which will be connected to PE's output port)
    source = str(source_node)+str('L')+str('I')
    # the destination port should be output port since this is output of router to PE
    # (which will be connected to PE's input port)
    destination = str(destination_node)+str('L')+str('O')
    if networkx.has_path(noc_rg, source, destination):
        return True
    else:
        return False


def HowManyPathsFromSource(noc_rg, source_node, destination_node):
    source = str(source_node)+str('L')+str('I')
    destination = str(destination_node)+str('L')+str('O')
    if networkx.has_path(noc_rg, source, destination):
        number_of_paths = len(list(networkx.all_simple_paths(noc_rg, source, destination)))
        return number_of_paths
    else:
        return 0


def OptimizeReachabilityRectangles(ag, number_of_rectangles):
    # the idea of merging is that we make a rectangle with representing 2 vertex of it,
    # namely north-west and south-east vertex.
    # Then we try to generate optimal rectangle set that covers all of the nodes...
    print ("=====================================")
    print ("STARTING RECTANGLE OPTIMIZATION...")
    for node in ag.nodes():
        for port in ag.node[node]['Router'].Unreachable:
            rectangle_list = {}
            for i in range(0, number_of_rectangles):
                rectangle_list[i] = (None, None)
            if len(ag.node[node]['Router'].Unreachable[port]) == Config.Network_X_Size*Config.Network_Y_Size:
                rectangle_list[0] = (0, Config.Network_X_Size*Config.Network_Y_Size-1)
            else:
                rectangle_list = copy.deepcopy(MergeNodeWithRectangles(rectangle_list,
                                                                      ag.node[node]['Router'].Unreachable[port]))
            ag.node[node]['Router'].Unreachable[port] = rectangle_list
    print ("RECTANGLE OPTIMIZATION FINISHED...")
    return None


def MergeNodeWithRectangles(rectangle_list, unreachable_node_list):
    # todo: in this function if we can not perform any loss-less merge, we terminate the process...
    # which is bad... we need to make sure that this node is covered
    for unreachable_node in unreachable_node_list:
        covered = False
        for rectangle in rectangle_list:
            if rectangle_list[rectangle][0] is None:
                # there is no entry, this is the first node to get in...
                rectangle_list[rectangle] = (unreachable_node, unreachable_node)
                covered = True
                break
            else:
                if is_node_inside_rectangle(rectangle_list[rectangle], unreachable_node):
                    covered = True
                    break
                else:

                    location_1, location_2 = merge_rectangle_with_node(rectangle_list[rectangle][0],
                                                                       rectangle_list[rectangle][1],
                                                                       unreachable_node)
                    # print ("Merged:" location_1, location_2)
                    loss_less_merge = True
                    for network_node_x in range(location_1[0], location_2[0]+1):        # (merged_x_1, merged_x_2+1)
                        for network_node_y in range(location_1[1], location_2[1]+1):
                            for network_node_z in range(location_1[2], location_2[2]+1):
                                node_number = AG_Functions.return_node_number(network_node_x, network_node_y,
                                                                              network_node_z)
                                if node_number not in unreachable_node_list:
                                    loss_less_merge = False
                                    break
                    # if we are not losing any Node, we perform Merge...
                    if loss_less_merge:
                        #                                            merged X      Merged Y       Merged Z
                        merged_1 = AG_Functions.return_node_number(location_1[0],location_1[1], location_1[2])
                        merged_2 = AG_Functions.return_node_number(location_2[0],location_2[1], location_2[2])
                        rectangle_list[rectangle] = copy.deepcopy((merged_1, merged_2))
                        covered = True
                        break
        if not covered:
            pass
            # print ("COULD NOT PERFORM ANY LOSS-LESS MERGE FOR:"+str(UnreachableNode))
            # print (RectangleList)
    return rectangle_list


def is_node_inside_rectangle(Rect,Node):
    r1x, r1y, r1z = AG_Functions.return_node_location(Rect[0])
    r2x, r2y, r2z = AG_Functions.return_node_location(Rect[1])
    NodeX, NodeY, NodeZ = AG_Functions.return_node_location(Node)
    if r1x <= NodeX <= r2x and r1y <= NodeY <= r2y and r1z <= NodeZ <= r2z:
        return True
    else:
        return False


def merge_rectangle_with_node(rect_ll, rect_ur, node):
    x1, y1, z1 = AG_Functions.return_node_location(rect_ll)
    x2, y2, z2 = AG_Functions.return_node_location(rect_ur)
    node_x, node_y, node_z = AG_Functions.return_node_location(node)
    merged_x1 = min(x1, node_x)
    merged_y1 = min(y1, node_y)
    merged_z1 = min(z1, node_z)
    merged_x2 = max(x2, node_x)
    merged_y2 = max(y2, node_y)
    merged_z2 = max(z2, node_z)
    location_1 = merged_x1, merged_y1, merged_z1
    location_2 = merged_x2, merged_y2, merged_z2
    return location_1, location_2


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



def reachability_metric(ag, noc_rg, report):
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