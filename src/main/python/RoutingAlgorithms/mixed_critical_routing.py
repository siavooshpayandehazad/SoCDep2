# Copyright (C) 2017 Siavoosh Payandeh Azad
import copy
from networkx import has_path, all_shortest_paths, all_simple_paths
from ArchGraphUtilities import AG_Functions
from ArchGraphUtilities.AG_Functions import manhattan_distance
from ConfigAndPackages import Config, PackageFile
from ConfigAndPackages.all_2d_turn_model_package import all_2d_turn_models
from RoutingAlgorithms import Routing
from RoutingAlgorithms.Calculate_Reachability import reachability_metric, is_destination_reachable_from_source, \
    is_destination_reachable_via_port
from RoutingAlgorithms.Routing import return_minimal_paths
from RoutingAlgorithms.Routing_Functions import check_deadlock_freeness
from SystemHealthMonitoring import SystemHealthMonitoringUnit
import RoutingGraph_Reports
from SystemHealthMonitoring.SHMU_Reports import draw_shm
from Utilities import misc


def find_all_roots(noc_rg):
    """
    Returns all non-local roots that have outgoing edges
    :param noc_rg: network routing graph
    :return: list of node ids of all non-local roots with outgoing edges
    """
    roots = []
    for node in noc_rg.nodes():
        if len(noc_rg.successors(node)) == 0:
            if "L" not in node:
                if len(noc_rg.predecessors(node))>0:
                    roots.append(node)
    return roots


def find_all_leaves(noc_rg):
    """
    Returns all non-local leaves that have incoming edges
    :param noc_rg: network routing graph
    :return: list of node ids of all non-local leaves with incoming edges
    """
    leaves = []
    for node in noc_rg.nodes():
        if len(noc_rg.predecessors(node)) == 0:
            if "L" not in node:
                if len(noc_rg.successors(node))>0:
                    leaves.append(node)
    return leaves


def report_router_links(size, noc_rg):
    print
    print "-----------------------"
    print "reconfiguration bits for :"

    node_turn_dict = {}
    for i in range(0, size**2):

        node_turn_dict[i] = []
        """
        x,y,z = AG_Functions.return_node_location(i)

        if x+1 < size:
            node = AG_Functions.return_node_number(x+1, y, z)
            west_in = str(node)+"WI"
            north_out = str(node)+"NO"
            edge=(west_in,north_out)
            if edge in noc_rg.edges():
                 node_turn_dict[i].append("W2S")
            sout_out = str(node)+"SO"
            edge=(west_in,sout_out)
            if edge in noc_rg.edges():
                node_turn_dict[i].append("W2N")
            east_out = str(node)+"EO"
            edge=(west_in,east_out)
            if edge in noc_rg.edges():
                node_turn_dict[i].append("W2E")

        if x-1 > 0:
            node = AG_Functions.return_node_number(x+1, y, z)
            east_in = str(node)+"EI"
            north_out = str(node)+"NO"
            edge=(east_in,north_out)
            if edge in noc_rg.edges():
                 node_turn_dict[i].append("E2S")
            sout_out = str(node)+"SO"
            edge=(east_in,sout_out)
            if edge in noc_rg.edges():
                node_turn_dict[i].append("E2N")
            west_out = str(node)+"WO"
            edge=(east_in,west_out)
            if edge in noc_rg.edges():
                node_turn_dict[i].append("E2W")

        if y-1 > 0:
            node = AG_Functions.return_node_number(x+1, y, z)
            north_in = str(node)+"NI"
            west_out = str(node)+"WO"
            edge=(north_in,west_out)
            if edge in noc_rg.edges():
                 node_turn_dict[i].append("S2W")
            east_out = str(node)+"EO"
            edge=(north_in,east_out)
            if edge in noc_rg.edges():
                node_turn_dict[i].append("S2E")
            south_out = str(node)+"SO"
            edge=(north_in,south_out)
            if edge in noc_rg.edges():
                node_turn_dict[i].append("S2N")

        if y+1 < size:
            node = AG_Functions.return_node_number(x+1, y, z)
            south_in = str(node)+"SI"
            west_out = str(node)+"WO"
            edge=(south_in,north_out)
            if edge in noc_rg.edges():
                 node_turn_dict[i].append("N2W")
            east_out = str(node)+"EO"
            edge=(south_in,east_out)
            if edge in noc_rg.edges():
                node_turn_dict[i].append("N2E")
            north_out = str(node)+"NO"
            edge=(south_in,north_out)
            if edge in noc_rg.edges():
                node_turn_dict[i].append("N2S")

        local_in = str(i)+"LI"
        north_out = str(i)+"NO"
        east_out = str(i)+"EO"
        wast_out = str(i)+"WO"
        south_out = str(i)+"SO"
        if (local_in,north_out) in noc_rg.edges():
            node_turn_dict[i].append("L2S")
        if (local_in,east_out) in noc_rg.edges():
            node_turn_dict[i].append("L2E")
        if (local_in,wast_out) in noc_rg.edges():
            node_turn_dict[i].append("L2W")
        if (local_in,south_out) in noc_rg.edges():
            node_turn_dict[i].append("L2N")

        local_out = str(i)+"LO"
        north_in = str(i)+"NI"
        east_in = str(i)+"EI"
        wast_in = str(i)+"WI"
        south_in = str(i)+"SI"
        if (north_in, local_out) in noc_rg.edges():
            node_turn_dict[i].append("S2L")
        if (east_in, local_out) in noc_rg.edges():
            node_turn_dict[i].append("E2L")
        if (wast_in, local_out) in noc_rg.edges():
            node_turn_dict[i].append("W2L")
        if (south_in, local_out) in noc_rg.edges():
            node_turn_dict[i].append("N2L")

        """
        temp_list = []
        for edge in noc_rg.edges():
            if int(edge[0][:-2]) == i and int(edge[1][:-2]) == i:
                turn_1 = edge[0][-2]
                turn_2 =  edge[1][-2]
                #print "\t", turn_1, "--->", turn_2
                if turn_1 == "N":
                    turn_1 = "S"
                elif turn_1 == "S":
                    turn_1 = "N"

                if turn_2 == "N":
                    turn_2 = "S"
                elif turn_2 == "S":
                    turn_2 = "N"


                node_turn_dict[i].append(turn_1+"2"+turn_2)

        string = ""
        if "S2E" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "S2W" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "W2N" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "W2S" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "E2N" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "E2S" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "N2E" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "N2W" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"

        if "N2S" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "S2N" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "E2W" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "W2E" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "L2N" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "N2L" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"

        if "L2E" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "E2L" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"

        if "L2W" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        if "W2L" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"

        if "L2S" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"

        if "S2L" in node_turn_dict[i]:
            string += "1"
        else:
            string += "0"
        print "\tRxy_reconf_"+str(i)+" <=\""+str(string[::-1])+"\";"+"--"+str(int(string[::-1][12:],2))


def cleanup_routing_graph(ag, noc_rg):
    """
    removes un-used edges from noc routing graph
    :param ag: network architecture graph
    :param noc_rg: network routing graph
    :return: noc_rg with the applied removals
    """
    while(len(find_all_roots(noc_rg))>0):
        for node in noc_rg.nodes():
            if len(noc_rg.successors(node)) == 0:
                if "L" not in node:
                    for node_2 in noc_rg.predecessors(node):
                        if (node_2, node) in noc_rg.edges():
                            noc_rg.remove_edge(node_2, node)
    while(len(find_all_leaves(noc_rg))>0):
        for node in noc_rg.nodes():
            if len(noc_rg.predecessors(node)) == 0:
                if "L" not in node:
                    for node_2 in noc_rg.successors(node):
                        if (node, node_2) in noc_rg.edges():
                            noc_rg.remove_edge(node, node_2)
    return noc_rg


def mixed_critical_rg(network_size, routing_type, critical_nodes, critical_rg_nodes, turn_model, viz, report):

    turns_health_2d_network = {"N2W": True, "N2E": True, "S2W": True, "S2E": True,
                               "W2N": True, "W2S": True, "E2N": True, "E2S": True}

    Config.ag.topology = '2DMesh'
    Config.ag.x_size = network_size
    Config.ag.y_size = network_size
    Config.ag.z_size = 1
    Config.RotingType = routing_type

    ag = copy.deepcopy(AG_Functions.generate_ag())
    shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
    shmu.setup_noc_shm(ag, turns_health_2d_network, False)
    noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, turns_health_2d_network.keys(), False,  False))

    for node in critical_rg_nodes:
        if node not in noc_rg.nodes():
            raise ValueError(str(node)+" doesnt exist in noc_rg")

    for node in noc_rg.nodes():
        if node in critical_rg_nodes:
            noc_rg.node[node]["criticality"] = "H"
        else:
            noc_rg.node[node]["criticality"] = "L"

    edges_to_be_removed = []
    for edge in noc_rg.edges():
        if noc_rg.node[edge[0]]["criticality"] != noc_rg.node[edge[1]]["criticality"]:
            edges_to_be_removed.append(edge)
        else:
            if noc_rg.node[edge[0]]["criticality"] == "L":
                if edge[0][:-2] == edge[1][:-2]:
                    if str(edge[0][-2])+"2"+str(edge[1][-2]) not in turn_model:
                        if edge[0][-2] == "L" or  edge[1][-2] == "L":
                            pass
                        elif edge[0][-2] == "E" and edge[1][-2] == "W":
                            pass
                        elif edge[0][-2] == "W" and edge[1][-2] == "E":
                            pass
                        elif edge[0][-2] == "S" and edge[1][-2] == "N":
                            pass
                        elif edge[0][-2] == "N" and edge[1][-2] == "S":
                            pass
                        else:
                            edges_to_be_removed.append(edge)

    for edge in edges_to_be_removed:
        noc_rg.remove_edge(edge[0], edge[1])
    if viz:
        noc_rg = copy.deepcopy(cleanup_routing_graph(ag, noc_rg))
        RoutingGraph_Reports.draw_rg(noc_rg)
    counter = 0
    print "its deadlock free:", check_deadlock_freeness(noc_rg)
    for node_1 in ag.nodes():
        for node_2 in ag.nodes():
            if node_1 != node_2:
                if node_1 in critical_nodes or node_2 in critical_nodes:
                    pass
                else:
                    if is_destination_reachable_from_source(noc_rg, node_1, node_2):
                        counter += 1
                    else:
                        if report:
                            print node_1,"can not reach", node_2
    print "average connectivity for non-critical nodes:", float(counter)/(len(ag.nodes())-len(critical_nodes))
    return float(counter)/(len(ag.nodes())-len(critical_nodes)), noc_rg



def generate_routing_table(size, noc_rg, routing_type):
    for current_node in range(0, size**2):
        print "===="*10
        print "node:", current_node
        print "               "*3+"input direction"
        print "              "*3+"  -----------------"
        print '%5s' % "dest",
        for id in ["N", "E", "W", "S", "L"]:
            print '%20s' % id,
        print
        print " ","------"*18

        for destination_node in range(0, size**2):
            print '%5s' % destination_node,
            for dir in ["N", "E", "W", "S", "L"]:
                current_port = str(current_node)+dir+"I"
                if current_node == destination_node:
                    print '%20s' % 0,
                else:
                    destination_port = str(destination_node)+"LO"
                    if has_path(noc_rg, current_port, destination_port):
                        all_paths = []
                        if routing_type == "MinimalPath":
                            max_hop_count = manhattan_distance(current_node, destination_node)
                            all_found_paths = list(all_shortest_paths(noc_rg, current_port, destination_port))
                            for Path in all_found_paths:
                                if (len(Path)-2)/2 <= max_hop_count:
                                    all_paths.append(Path)
                        else:
                            all_paths = list(all_simple_paths(noc_rg, current_port, destination_port))
                        all_ports = []

                        for path in all_paths:
                            if path[1][-2] not in all_ports:
                                all_ports.append(path[1][-2])
                        print '%20s' % all_ports,
                    else:
                        print '%20s' % 0,
            print