# Copyright (C) 2017 Siavoosh Payandeh Azad
import copy
from networkx import has_path, all_shortest_paths, all_simple_paths
from ArchGraphUtilities import AG_Functions
from ArchGraphUtilities.AG_Functions import manhattan_distance
from ConfigAndPackages import Config
from RoutingAlgorithms import Routing
from RoutingAlgorithms.Calculate_Reachability import is_destination_reachable_from_source
from RoutingAlgorithms.Routing import return_minimal_paths
from RoutingAlgorithms.Routing_Functions import check_deadlock_freeness
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from RoutingAlgorithms import RoutingGraph_Reports


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
    reconf_file = open("Generated_Files/MC_reconfigration_bits.txt","a")
    print()
    print("-"*23)
    print("reconfiguration bits for :")

    node_turn_dict = {}
    for i in range(0, size**2):

        node_turn_dict[i] = []
        temp_list = []
        for edge in noc_rg.edges():
            if int(edge[0][:-2]) == i and int(edge[1][:-2]) == i:
                turn_1 = edge[0][-2]
                turn_2 =  edge[1][-2]
                #print("\t", turn_1, "--->", turn_2)
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
        print("\tRxy_reconf_"+str(i)+" <=\""+str(string[::-1])+"\";"+"--"+str(int(string[::-1][12:],2)))
        reconf_file.write("\tRxy_reconf_"+str(i)+" <=\""+str(string[::-1])+"\";"+"--"+str(int(string[::-1][12:],2))+"\n")
    reconf_file.close()
    return None

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


def mixed_critical_rg(network_size, routing_type, critical_nodes, critical_rg_nodes, broken_links,
                      turn_model, viz, report):

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
    copy_rg =copy.deepcopy(noc_rg)

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
        if (int(edge[0][:-2]), int(edge[1][:-2]))in broken_links:
            edges_to_be_removed.append(edge)
        # removing edges that go from non-critical ports to ports used by critical ports
        if noc_rg.node[edge[0]]["criticality"] != noc_rg.node[edge[1]]["criticality"]:
            edges_to_be_removed.append(edge)
        else:
            if noc_rg.node[edge[0]]["criticality"] == "L":
                if edge[0][:-2] == edge[1][:-2]:
                    # remove the links that do not follow the turn model rules!
                    if str(edge[0][-2])+"2"+str(edge[1][-2]) not in turn_model:
                        if edge[0][-2] == "L" or edge[1][-2] == "L":
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

    reachability_counter = 0
    connectivity_counter = 0
    print("deadlock freeness:", check_deadlock_freeness(noc_rg))
    for node_1 in ag.nodes():
        for node_2 in ag.nodes():
            if node_1 != node_2:
                if node_1 in critical_nodes or node_2 in critical_nodes:
                    pass
                else:

                    if is_destination_reachable_from_source(noc_rg, node_1, node_2):
                        connectivity_counter += 1
                        if routing_type == "MinimalPath":
                            paths = return_minimal_paths(noc_rg, node_1, node_2)
                            all_minimal_paths = return_minimal_paths(copy_rg, node_1, node_2)
                            valid_path = True
                            for path in paths:
                                for node in path:
                                    successors = noc_rg.successors(node)
                                    if str(node_2)+str('L')+str('O') in successors:
                                        #print(node_2, successors)
                                        break
                                    else:
                                        for successor in successors:
                                            valid_successor = False

                                            for path_1 in all_minimal_paths:
                                                if successor in path_1:
                                                    valid_successor = True
                                                    break
                                            if valid_successor:
                                                sucessor_paths = []
                                                max_hop_count = manhattan_distance(int(successor[:-2]), node_2)
                                                if has_path(noc_rg, successor, str(node_2)+str('L')+str('O')):
                                                    all_paths_from_sucessor = list(all_shortest_paths(noc_rg, successor, str(node_2)+str('L')+str('O')))
                                                    for Path in all_paths_from_sucessor:
                                                        if (len(Path)-2)/2 <= max_hop_count:
                                                            sucessor_paths.append(Path)
                                                if len(sucessor_paths)==0:
                                                    valid_path = False
                                                    #print(path, node, node_2, successor, "FALSE")
                                                    break
                                                else:
                                                    pass
                                                    #print(path, node, node_2, successor, "TRUE")


                            if valid_path:
                                reachability_counter += 1
                            else:
                                if report:
                                    print(node_1,"can not reach  ", node_2)
                        else:
                            reachability_counter += 1
                    else:
                        if report:
                            print(node_1,"can not connect", node_2)
    print("average connectivity for non-critical nodes:", float(connectivity_counter)/(len(ag.nodes())-len(critical_nodes)))
    print("average reachability for non-critical nodes:", float(reachability_counter)/(len(ag.nodes())-len(critical_nodes)))
    return float(connectivity_counter)/(len(ag.nodes())-len(critical_nodes)), noc_rg


def generate_routing_table(size, noc_rg, routing_type):
    routing_table_file = open("Generated_Files/MC_routing_table.txt", 'a')
    for current_node in range(0, size**2):


        routing_table_file.write("-- Node "+str(current_node)+"\n")
        routing_table_file.write("constant routing_table_bits_"+str(current_node)+": t_tata_long := (\n")


        counter = 0
        for dir in ["L", "S", "E", "W", "N"]:
            if dir == "L":
                routing_table_file.write("\t-- local\n")
            elif dir == "S":
                routing_table_file.write("\t-- north\n")
            elif dir == "E":
                routing_table_file.write("\t-- east\n")
            elif dir == "W":
                routing_table_file.write("\t-- west\n")
            else:
                routing_table_file.write("\t-- south\n")
            for destination_node in range(0, size**2):

                current_port = str(current_node)+dir+"I"
                if current_node == destination_node:
                    if counter == size**2*5-1:
                        routing_table_file.write("\t\t"+str(counter)+" => \"0000\"\n")
                    else:
                        routing_table_file.write("\t\t"+str(counter)+" => \"0000\",\n")
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
                                if path[1][-2] == "N":
                                    all_ports.append("S")
                                elif path[1][-2] == "S":
                                    all_ports.append("N")
                                else:
                                    all_ports.append(path[1][-2])
                        string = ""
                        if "N" in all_ports:
                            string += "1"
                        else:
                            string += "0"
                        if "E" in all_ports:
                            string += "1"
                        else:
                            string += "0"
                        if "W" in all_ports:
                            string += "1"
                        else:
                            string += "0"
                        if "S" in all_ports:
                            string += "1"
                        else:
                            string += "0"
                        if counter == size**2*5-1:
                            routing_table_file.write("\t\t"+str(counter)+" => \""+string+"\"\n")
                        else:
                            routing_table_file.write("\t\t"+str(counter)+" => \""+string+"\",\n")
                    else:
                        if counter == size**2*5-1:
                            routing_table_file.write("\t\t"+str(counter)+" => \"0000\"\n")
                        else:
                            routing_table_file.write("\t\t"+str(counter)+" => \"0000\",\n")
                        pass

                counter += 1
        routing_table_file.write(" );\n")
    routing_table_file.close()
    return None
