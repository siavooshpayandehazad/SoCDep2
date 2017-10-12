# Copyright (C) 2017 Siavoosh Payandeh Azad
import copy
from ArchGraphUtilities import AG_Functions
from ConfigAndPackages import Config, PackageFile
from ConfigAndPackages.all_2d_turn_model_package import all_2d_turn_models
from RoutingAlgorithms import Routing
from RoutingAlgorithms.Calculate_Reachability import reachability_metric, is_destination_reachable_from_source
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


def mixed_critical_rg(network_size, routing_type, critical_nodes, critical_rg_nodes, turn_model, viz):

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
                        print node_1,"can not reach", node_2
    print "average reachability for non-critical nodes:", float(counter)/(len(ag.nodes())-len(critical_nodes))
    return float(counter)/(len(ag.nodes())-len(critical_nodes))
