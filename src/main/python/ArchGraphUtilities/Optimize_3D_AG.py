# Copyright (C) Siavoosh Payandeh Azad

from ConfigAndPackages import Config
from AG_Functions import return_node_number, return_node_location
from RoutingAlgorithms import Routing, Calculate_Reachability, RoutingGraph_Reports
import random
import copy
from Arch_Graph_Reports import draw_ag


def optimize_ag_vertical_links(ag, shmu, logging):
    if Config.Network_Z_Size < 2:
        raise ValueError("Can not optimize VL placement with 1 layer... (NOC is still 2D)")
    if Config.VL_OptAlg == "LocalSearch":
        return opt_ag_vertical_link_local_search(ag, shmu, logging)
    elif Config.VL_OptAlg == "IterativeLocalSearch":
        return opt_ag_vertical_link_iterative_local_search(ag, shmu, logging)
    else:
        raise ValueError("VL_OptAlg parameter is not valid")


def opt_ag_vertical_link_iterative_local_search(ag, shmu, logging):
    best_vertical_link_list = []
    starting_cost = None
    for j in range(0, Config.AG_Opt_Iterations_ILS):
        remove_all_vertical_links(shmu, ag)
        vertical_link_list_init = copy.deepcopy(find_feasible_ag_vertical_link_placement(ag, shmu))
        routing_graph = copy.deepcopy(Routing.GenerateNoCRouteGraph(ag, shmu,
                                                                    Config.UsedTurnModel, False, False))
        cost = Calculate_Reachability.ReachabilityMetric(ag, routing_graph, False)
        current_best_cost = cost
        if j == 0:
            print ("=====================================")
            print ("STARTING AG VERTICAL LINK PLACEMENT OPTIMIZATION")
            print ("NUMBER OF LINKS: "+str(Config.VerticalLinksNum))
            print ("NUMBER OF ITERATIONS: "+str(Config.AG_Opt_Iterations_ILS*Config.AG_Opt_Iterations_LS))
            print ("INITIAL REACHABILITY METRIC: "+str(cost))
            starting_cost = cost
            best_cost = cost
            best_vertical_link_list = vertical_link_list_init[:]
            ag_temp = copy.deepcopy(ag)
            cleanup_ag(ag_temp, shmu)
            draw_ag(ag_temp, "AG_VLOpt_init")
            del ag_temp
        else:
            print ("\033[33m* NOTE::\033[0m STARITNG NEW ROUND: "+str(j+1)+"\t STARTING COST:"+str(cost))
            if cost > best_cost:
                best_vertical_link_list = vertical_link_list_init[:]
                best_cost = cost
                print ("\033[32m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:" +
                       str(cost) + "\t ITERATION: "+str(j*Config.AG_Opt_Iterations_LS))
        vertical_link_list = vertical_link_list_init[:]
        for i in range(0, Config.AG_Opt_Iterations_LS):
            new_vertical_link_list = copy.deepcopy(move_to_new_vertical_link_configuration(ag, shmu,
                                                                                           vertical_link_list))
            new_routing_graph = Routing.GenerateNoCRouteGraph(ag, shmu, Config.UsedTurnModel,
                                                              False, False)
            cost = Calculate_Reachability.ReachabilityMetric(ag, new_routing_graph, False)

            if cost >= current_best_cost:
                vertical_link_list = new_vertical_link_list[:]
                if cost > current_best_cost:
                    current_best_cost = cost
                    print ("\t \tMOVED TO SOLUTION WITH COST:" + str(cost)
                           + "\t ITERATION: "+str(j*Config.AG_Opt_Iterations_LS+i))
            else:
                return_to_solution(ag, shmu, vertical_link_list)

            if cost > best_cost:
                best_vertical_link_list = vertical_link_list[:]
                best_cost = cost
                print ("\033[32m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:" +
                       str(cost) + "\t ITERATION: "+str(j*Config.AG_Opt_Iterations_LS+i))

    return_to_solution(ag, shmu, best_vertical_link_list)
    print ("-------------------------------------")
    print ("STARTING COST:"+str(starting_cost)+"\tFINAL COST:"+str(best_cost))
    print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(best_cost-starting_cost)/starting_cost))+" %")
    return shmu


def opt_ag_vertical_link_local_search(ag, shmu, logging):
    remove_all_vertical_links(shmu, ag)
    vertical_link_list = find_feasible_ag_vertical_link_placement(ag, shmu)
    routing_graph = copy.deepcopy(Routing.GenerateNoCRouteGraph(ag, shmu, Config.UsedTurnModel,
                                                                Config.DebugInfo, Config.DebugDetails))
    cost = Calculate_Reachability.ReachabilityMetric(ag, routing_graph, False)
    print ("=====================================")
    print ("STARTING AG VERTICAL LINK PLACEMENT OPTIMIZATION")
    print ("NUMBER OF LINKS: "+str(Config.VerticalLinksNum))
    print ("NUMBER OF ITERATIONS: "+str(Config.AG_Opt_Iterations_LS))
    print ("INITIAL REACHABILITY METRIC: "+str(cost))
    starting_cost = cost
    best_cost = cost
    ag_temp = copy.deepcopy(ag)
    cleanup_ag(ag_temp, shmu)
    draw_ag(ag_temp, "AG_VLOpt_init")
    del ag_temp
    for i in range(0, Config.AG_Opt_Iterations_LS):
        new_vertical_link_list = copy.deepcopy(move_to_new_vertical_link_configuration(ag, shmu,
                                                                                       vertical_link_list))
        new_routing_graph = copy.deepcopy(Routing.GenerateNoCRouteGraph(ag, shmu,
                                                                        Config.UsedTurnModel, False, False))
        cost = Calculate_Reachability.ReachabilityMetric(ag, new_routing_graph, False)
        if cost >= best_cost:
            vertical_link_list = copy.deepcopy(new_vertical_link_list)
            if cost > best_cost:
                best_cost = cost
                print ("\033[32m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:" + str(cost) + "\t ITERATION: "+str(i))
            else:
                # print ("\033[33m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:" + str(Cost) + "\t ITERATION: "+str(i))
                pass
        else:
            return_to_solution(ag, shmu, vertical_link_list)
            vertical_link_list = copy.deepcopy(vertical_link_list)
    print ("-------------------------------------")
    print ("STARTING COST:"+str(starting_cost)+"\tFINAL COST:"+str(best_cost))
    print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(best_cost-starting_cost)/starting_cost))+" %")
    return shmu


def find_all_vertical_links(ag):
    vertical_link_list = []
    for link in ag.edges():
        # if these nodes are on different layers
        if return_node_location(link[0])[2] != return_node_location(link[1])[2]:
            if link not in vertical_link_list:
                vertical_link_list.append(link)
    return vertical_link_list


def remove_all_vertical_links(shm, ag):
    vertical_link_list = find_all_vertical_links(ag)
    for VLink in vertical_link_list:
        shm.break_link(VLink, False)
    return None


def find_feasible_ag_vertical_link_placement(ag, shmu):
    new_vertical_link_lists = []
    for i in range(0, Config.VerticalLinksNum):
        source_x = random.randint(0, Config.Network_X_Size-1)
        source_y = random.randint(0, Config.Network_Y_Size-1)
        source_z = random.randint(0, Config.Network_Z_Size-1)
        source_node = return_node_number(source_x, source_y, source_z)
        possible_z = []
        if source_z+1 <= Config.Network_Z_Size-1:
            possible_z.append(source_z+1)
        if 0 <= source_z-1:
            possible_z.append(source_z-1)
        destination_node = return_node_number(source_x, source_y, random.choice(possible_z))
        while shmu.SHM.edge[source_node][destination_node]['LinkHealth']:
            source_x = random.randint(0, Config.Network_X_Size-1)
            source_y = random.randint(0, Config.Network_Y_Size-1)
            source_z = random.randint(0, Config.Network_Z_Size-1)
            source_node = return_node_number(source_x, source_y, source_z)
            possible_z = []
            if source_z + 1 <= Config.Network_Z_Size-1:
                possible_z.append(source_z+1)
            if 0 <= source_z-1:
                possible_z.append(source_z-1)
            destination_node = return_node_number(source_x, source_y, random.choice(possible_z))

        # here we have a candidate to restore
        shmu.restore_broken_link((source_node, destination_node), False)
        new_vertical_link_lists.append((source_node, destination_node))
    return new_vertical_link_lists


def return_to_solution(ag, shm, vertical_link_list):
    remove_all_vertical_links(shm, ag)
    for link in vertical_link_list:
        shm.restore_broken_link(link, False)
    return None


def move_to_new_vertical_link_configuration(ag, shmu, vertical_link_lists):
    new_vertical_link_lists = copy.deepcopy(vertical_link_lists)
    chosen_link_to_fix = random.choice(new_vertical_link_lists)
    new_vertical_link_lists.remove(chosen_link_to_fix)
    shmu.break_link(chosen_link_to_fix, False)

    source_x = random.randint(0, Config.Network_X_Size-1)
    source_y = random.randint(0, Config.Network_Y_Size-1)
    source_z = random.randint(0, Config.Network_Z_Size-1)
    source_node = return_node_number(source_x, source_y, source_z)
    possible_z = []
    if source_z + 1 <= Config.Network_Z_Size-1:
        possible_z.append(source_z + 1)
    if 0 <= source_z - 1:
        possible_z.append(source_z - 1)
    destination_node = return_node_number(source_x, source_y, random.choice(possible_z))

    while source_node == destination_node or \
            shmu.SHM.edge[source_node][destination_node]['LinkHealth']:
        source_x = random.randint(0, Config.Network_X_Size-1)
        source_y = random.randint(0, Config.Network_Y_Size-1)
        source_z = random.randint(0, Config.Network_Z_Size-1)
        source_node = return_node_number(source_x, source_y, source_z)
        possible_z = []
        if source_z+1 <= Config.Network_Z_Size-1:
            possible_z.append(source_z+1)
        if 0 <= source_z-1:
            possible_z.append(source_z-1)
        destination_node = return_node_number(source_x, source_y, random.choice(possible_z))
    # here we have a candidate to restore
    shmu.restore_broken_link((source_node, destination_node), False)
    new_vertical_link_lists.append((source_node, destination_node))
    return new_vertical_link_lists


def cleanup_ag(ag, shmu):
    for link in shmu.SHM.edges():
        if not shmu.SHM.edge[link[0]][link[1]]['LinkHealth']:
            ag.remove_edge(link[0], link[1])
    return None