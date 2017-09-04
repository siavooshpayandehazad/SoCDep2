# Copyright (C) Siavoosh Payandeh Azad
# the main idea of reach-ability is from the following paper:
# NoCDepend: A flexible and scalable Dependability Technique for 3D Networks-on-Chip
# how ever, at the moment we only implemented a 2D version of it.

from networkx import has_path, shortest_path_length, all_simple_paths
from copy import deepcopy
from ConfigAndPackages import Config
from Routing import generate_noc_route_graph
from ArchGraphUtilities.AG_Functions import manhattan_distance, return_node_number, return_node_location


def calculate_reachability(ag, noc_rg):
    """
    adds non-reachable nodes from each node's port to that port's unreachable list
    :param ag: Architecture Graph
    :param noc_rg: NoC Routing Graph
    :return: None
    """
    if '3D' in Config.ag.topology:
        port_list = ['U', 'N', 'E', 'W', 'S', 'D']
    else:
        port_list = ['N', 'E', 'W', 'S']

    for source_node in ag.nodes():
        for port in port_list:
            ag.node[source_node]['Router'].unreachable[port] = []
        for destination_node in ag.nodes():
            # if SourceNode != DestinationNode:
                for port in port_list:
                    if not is_destination_reachable_via_port(noc_rg, source_node, port, destination_node, False):
                        # print ("No Path From", SourceNode,Port,"To",DestinationNode)
                        ag.node[source_node]['Router'].unreachable[port].append(destination_node)
    return None


def is_destination_reachable_via_port(noc_rg, source_node, port, destination_node, report):
    """
    checks if there is a path from source node's port to local port of destination node
    :param noc_rg: NoC Routing Graph
    :param source_node: source node ID
    :param port: port from which a path search starts from source node
    :param destination_node: destination node ID
    :param report: boolean, which enables printing reports to console
    :return: True if there is a path from source's port to destination, False, if no path is found
    """
    # the Source port should be output port since this is output of router to other routers
    source = str(source_node)+str(port)+str('O')
    # the destination port should be output port since this is output of router to PE
    # (which will be connected to PE's input port)
    destination = str(destination_node)+str('L')+str('O')
    if has_path(noc_rg, source, destination):
        return True
    else:
        if report:
            print ("\t\tNO PATH FOUND FROM: ", source, "TO:", destination)
        return False


def is_destination_reachable_from_source(noc_rg, source_node, destination_node):
    """
    checks if destination is reachable from the local port of the source node
    the search starts from the local port
    :param noc_rg: NoC routing graph
    :param source_node: source node id
    :param destination_node: destination node id
    :return: True if there is a path else, False
    """
    # the Source port should be input port since this is input of router
    # (which will be connected to PE's output port)
    source = str(source_node)+str('L')+str('I')
    # the destination port should be output port since this is output of router to PE
    # (which will be connected to PE's input port)
    destination = str(destination_node)+str('L')+str('O')
    if has_path(noc_rg, source, destination):
        if Config.RotingType == 'MinimalPath':
            path_length = shortest_path_length(noc_rg, source, destination)
            minimal_hop_count = manhattan_distance(source_node, destination_node)
            if (path_length/2) == minimal_hop_count:
                return True
        else:
            return True
    else:
        return False


def how_many_paths_from_source(noc_rg, source_node, destination_node):
    """
    returns the number of paths from the source's local port to destination
    :param noc_rg: NoC routing graph
    :param source_node: source node
    :param destination_node: destination node
    :return: number of paths from source node to destination
    """
    source = str(source_node)+str('L')+str('I')
    destination = str(destination_node)+str('L')+str('O')
    if has_path(noc_rg, source, destination):
        number_of_paths = len(list(all_simple_paths(noc_rg, source, destination)))
        return number_of_paths
    else:
        return 0


def optimize_reachability_rectangles(ag, number_of_rectangles):
    """
    optimizes the rectangles in non-reachable lists of AG to reduce it to number of
    rectangles
    :param ag: Architecture Graph
    :param number_of_rectangles: number of available rectangles
    :return: None
    """
    # the idea of merging is that we make a rectangle with representing 2 vertex of it,
    # namely north-west and south-east vertex.
    # Then we try to generate optimal rectangle set that covers all of the nodes...
    print ("=====================================")
    print ("STARTING RECTANGLE OPTIMIZATION...")
    for node in ag.nodes():
        for port in ag.node[node]['Router'].unreachable:
            rectangle_list = {}
            for i in range(0, number_of_rectangles):
                rectangle_list[i] = (None, None)
            if len(ag.node[node]['Router'].unreachable[port]) == Config.ag.x_size*Config.ag.y_size:
                rectangle_list[0] = (0, Config.ag.x_size*Config.ag.y_size-1)
            else:
                rectangle_list = deepcopy(merge_node_with_rectangles(rectangle_list,
                                                                     ag.node[node]['Router'].unreachable[port]))
            ag.node[node]['Router'].unreachable[port] = deepcopy(rectangle_list)
    print ("RECTANGLE OPTIMIZATION FINISHED...")
    return None


def merge_node_with_rectangles(rectangle_list, unreachable_node_list):
    """

    :param rectangle_list:
    :param unreachable_node_list: un-reachable nodes that are initially populating the unreachable list
    :return: rectangle list
    """
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
                                node_number = return_node_number(network_node_x, network_node_y, network_node_z)
                                if node_number not in unreachable_node_list:
                                    loss_less_merge = False
                                    break
                    # if we are not losing any Node, we perform Merge...
                    if loss_less_merge:
                        #                                            merged X      Merged Y       Merged Z
                        merged_1 = return_node_number(location_1[0], location_1[1], location_1[2])
                        merged_2 = return_node_number(location_2[0], location_2[1], location_2[2])
                        rectangle_list[rectangle] = deepcopy((merged_1, merged_2))
                        covered = True
                        break
        if not covered:
            pass
            # print ("COULD NOT PERFORM ANY LOSS-LESS MERGE FOR:"+str(UnreachableNode))
            # print (RectangleList)
    return rectangle_list


def is_node_inside_rectangle(rect, node):
    """
    Checks if the node id is inside the rectangle
    :param rect: rectangle represented by 2 coordinates lower_left, upper_right
    :param node: node id
    :return: True if node id is inside rectangle else, False
    """
    r1x, r1y, r1z = return_node_location(rect[0])
    r2x, r2y, r2z = return_node_location(rect[1])
    node_x, node_y, node_z = return_node_location(node)
    if r1x <= node_x <= r2x and r1y <= node_y <= r2y and r1z <= node_z <= r2z:
        return True
    else:
        return False


def merge_rectangle_with_node(rect_ll, rect_ur, node):
    """
    Merges a rectangle with a node
    :param rect_ll: rectangle lower left position
    :param rect_ur:  rectangle upper right position
    :param node: ID of the node to be merged
    :return: coordination of final rectangle (rect_ll, rect_ur)
    """
    x1, y1, z1 = return_node_location(rect_ll)
    x2, y2, z2 = return_node_location(rect_ur)
    node_x, node_y, node_z = return_node_location(node)
    merged_x1 = min(x1, node_x)
    merged_y1 = min(y1, node_y)
    merged_z1 = min(z1, node_z)
    merged_x2 = max(x2, node_x)
    merged_y2 = max(y2, node_y)
    merged_z2 = max(z2, node_z)
    location_1 = merged_x1, merged_y1, merged_z1
    location_2 = merged_x2, merged_y2, merged_z2
    return location_1, location_2


def clear_reachability_calculations(ag):
    """
    clears all the unreachable lists in the network
    :param ag: architecture graph
    :return: None
    """
    for node in ag.nodes():
        for port in ag.node[node]['Router'].unreachable:
            ag.node[node]['Router'].unreachable[port] = {}
    return None


def calculate_reachability_with_regions(ag, shmu):
    """
    calculates the routing graph for different regions of partitioned network
    :param ag: architecture graph
    :param shmu: system health monitoring unit
    :return: routing graph of critical partition and non-critical partition
    """
    # first Add the VirtualBrokenLinksForNonCritical
    already_broken_links = []
    for virtual_broken_link in Config.VirtualBrokenLinksForNonCritical:
        if shmu.SHM.edge[virtual_broken_link[0]][virtual_broken_link[1]]['LinkHealth']:
            shmu.break_link(virtual_broken_link, True)
        else:
            already_broken_links.append(virtual_broken_link)
    # Construct The RoutingGraph
    non_critical_rg = deepcopy(generate_noc_route_graph(ag, shmu, Config.UsedTurnModel, False, False))
    # calculate the rectangles for Non-Critical
    calculate_reachability(ag, non_critical_rg)
    # save Non Critical rectangles somewhere
    non_critical_rect = {}
    gate_way_rect = {}
    for node in Config.GateToNonCritical:
        gate_way_rect[node] = deepcopy(ag.node[node]['Router'].unreachable)
    for node in ag.nodes():
        if node not in Config.CriticalRegionNodes:
            non_critical_rect[node] = deepcopy(ag.node[node]['Router'].unreachable)
    # Restore the VirtualBrokenLinksForNonCritical
    for virtual_broken_link in Config.VirtualBrokenLinksForNonCritical:
        if virtual_broken_link not in already_broken_links:
            shmu.restore_broken_link(virtual_broken_link, True)

    already_broken_links = []
    # Add VirtualBrokenLinksForCritical
    for virtual_broken_link in Config.VirtualBrokenLinksForCritical:
        if shmu.SHM.edge[virtual_broken_link[0]][virtual_broken_link[1]]['LinkHealth']:
            shmu.break_link(virtual_broken_link, True)
        else:
            already_broken_links.append(virtual_broken_link)
    clear_reachability_calculations(ag)
    # Construct The RoutingGraph
    critical_rg = deepcopy(generate_noc_route_graph(ag, shmu, Config.UsedTurnModel, False, False))
    # calculate the rectangles for Critical
    calculate_reachability(ag, critical_rg)
    # save Critical rectangles somewhere
    critical_rect = {}
    for node in Config.CriticalRegionNodes:
        critical_rect[node] = deepcopy(ag.node[node]['Router'].unreachable)
    for node in Config.GateToCritical:
        gate_way_rect[node] = deepcopy(ag.node[node]['Router'].unreachable)
    # Restore the VirtualBrokenLinksForNonCritical
    for virtual_broken_link in Config.VirtualBrokenLinksForCritical:
        if virtual_broken_link not in already_broken_links:
            shmu.restore_broken_link(virtual_broken_link, True)

    # Combine Lists
    for node in ag.nodes():
        if node in critical_rect:
            ag.node[node]['Router'].unreachable = deepcopy(critical_rect[node])
        elif node in Config.GateToCritical:
            ag.node[node]['Router'].unreachable = deepcopy(gate_way_rect[node])
        elif node in Config.GateToNonCritical:
            ag.node[node]['Router'].unreachable = deepcopy(gate_way_rect[node])
        else:
            ag.node[node]['Router'].unreachable = deepcopy(non_critical_rect[node])
    # optimize the results
    optimize_reachability_rectangles(ag, Config.NumberOfRects)
    return critical_rg, non_critical_rg


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
                if is_destination_reachable_from_source(noc_rg, source_node, destination_node):
                    reachability_counter += 1
    r_metric = float(reachability_counter)
    if report:
        print ("REACH-ABILITY METRIC: "+str(r_metric))
    return r_metric
