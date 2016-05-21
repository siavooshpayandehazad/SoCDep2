# Copyright (C) Siavoosh Payandeh Azad

from vl_opt_functions import *
from ArchGraphUtilities import Arch_Graph_Reports
from RoutingAlgorithms import Routing
import copy
from ConfigAndPackages import Config


def opt_ag_vertical_link_local_search(ag, shmu, cost_file_name, logging):
    """
    optimizes vertical link placement using greedy local search algorithm
    :param ag: architecture graph
    :param shmu: system health monitoring unit
    :param cost_file_name: name of the file for dumping the cost values during the process
    :param logging: logging file
    :return: None
    """
    logging.info("STARTING LS FOR VL PLACEMENT...")
    if type(cost_file_name) is str:
        ag_cost_file = open('Generated_Files/Internal/'+cost_file_name+'.txt', 'a')
    else:
        raise ValueError("ag_cost_file name is not string: "+str(cost_file_name))

    remove_all_vertical_links(shmu, ag)
    vertical_link_list = find_feasible_ag_vertical_link_placement(ag, shmu)
    routing_graph = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                   Config.DebugInfo, Config.DebugDetails))
    cost = vl_cost_function(ag, routing_graph)
    print ("=====================================")
    print ("STARTING AG VERTICAL LINK PLACEMENT OPTIMIZATION")
    print ("NUMBER OF LINKS: "+str(Config.vl_opt.vl_num))
    print ("NUMBER OF ITERATIONS: "+str(Config.vl_opt.ls_iteration))
    print ("INITIAL REACHABILITY METRIC: "+str(cost))
    starting_cost = cost
    best_cost = cost

    ag_temp = copy.deepcopy(ag)
    cleanup_ag(ag_temp, shmu)
    Arch_Graph_Reports.draw_ag(ag_temp, "AG_VLOpt_init")
    del ag_temp

    ag_cost_file.write(str(cost)+"\n")

    for i in range(0, Config.vl_opt.ls_iteration):
        new_vertical_link_list = copy.deepcopy(move_to_new_vertical_link_configuration(ag, shmu,
                                                                                       vertical_link_list))
        new_routing_graph = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                           False, False))
        cost = vl_cost_function(ag, new_routing_graph)
        ag_cost_file.write(str(cost)+"\n")
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
    ag_cost_file.close()
    print ("-------------------------------------")
    print ("STARTING COST:"+str(starting_cost)+"\tFINAL COST:"+str(best_cost))
    print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(best_cost-starting_cost)/starting_cost))+" %")
    logging.info("LS FOR VL PLACEMENT FINISHED...")
    return None


def opt_ag_vertical_link_iterative_local_search(ag, shmu, cost_file_name, logging):
    """
    Runs iterative local search optimization on vertical link placement
    :param ag: architecture graph
    :param shmu: system health map
    :param cost_file_name: file name to dump cost values during the process
    :param logging: logging file
    :return:  None
    """
    logging.info("STARTING ILS FOR VL PLACEMENT...")
    if type(cost_file_name) is str:
        ag_cost_file = open('Generated_Files/Internal/'+cost_file_name+'.txt', 'a')
    else:
        raise ValueError("ag_cost_file name is not string: "+str(cost_file_name))

    best_vertical_link_list = []
    starting_cost = None
    for j in range(0, Config.vl_opt.ils_iteration):
        remove_all_vertical_links(shmu, ag)
        vertical_link_list_init = copy.deepcopy(find_feasible_ag_vertical_link_placement(ag, shmu))
        routing_graph = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu,
                                                                       Config.UsedTurnModel, False, False))
        cost = vl_cost_function(ag, routing_graph)
        ag_cost_file.write(str(cost)+"\n")
        current_best_cost = cost
        if j == 0:
            print ("=====================================")
            print ("STARTING AG VERTICAL LINK PLACEMENT OPTIMIZATION")
            print ("NUMBER OF LINKS: "+str(Config.vl_opt.vl_num))
            print ("NUMBER OF ITERATIONS: "+str(Config.vl_opt.ils_iteration*Config.vl_opt.ls_iteration))
            print ("INITIAL REACHABILITY METRIC: "+str(cost))
            starting_cost = cost
            best_cost = cost
            best_vertical_link_list = vertical_link_list_init[:]
            ag_temp = copy.deepcopy(ag)
            cleanup_ag(ag_temp, shmu)
            Arch_Graph_Reports.draw_ag(ag_temp, "AG_VLOpt_init")
            del ag_temp
        else:
            print("\033[33m* NOTE::\033[0m STARITNG NEW ROUND: "+str(j+1)+"\t STARTING COST:"+str(cost))
            if cost > best_cost:
                best_vertical_link_list = vertical_link_list_init[:]
                best_cost = cost
                print("\033[32m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:" +
                      str(cost) + "\t ITERATION: "+str(j*Config.vl_opt.ls_iteration))
        vertical_link_list = vertical_link_list_init[:]
        for i in range(0, Config.vl_opt.ls_iteration):
            new_vertical_link_list = copy.deepcopy(move_to_new_vertical_link_configuration(ag, shmu,
                                                                                           vertical_link_list))
            new_routing_graph = Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                 False, False)
            cost = vl_cost_function(ag, new_routing_graph)
            ag_cost_file.write(str(cost)+"\n")
            if cost >= current_best_cost:
                vertical_link_list = new_vertical_link_list[:]
                if cost > current_best_cost:
                    current_best_cost = cost
                    print ("\t \tMOVED TO SOLUTION WITH COST:" + str(cost)
                           + "\t ITERATION: "+str(j*Config.vl_opt.ls_iteration+i))
            else:
                return_to_solution(ag, shmu, vertical_link_list)

            if cost > best_cost:
                best_vertical_link_list = vertical_link_list[:]
                best_cost = cost
                print ("\033[32m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:" +
                       str(cost) + "\t ITERATION: "+str(j*Config.vl_opt.ls_iteration+i))

    return_to_solution(ag, shmu, best_vertical_link_list)
    ag_cost_file.close()
    print("-------------------------------------")
    print("STARTING COST:"+str(starting_cost)+"\tFINAL COST:"+str(best_cost))
    print("IMPROVEMENT:"+str("{0:.2f}".format(100*(best_cost-starting_cost)/starting_cost))+" %")
    logging.info("ILS FOR VL PLACEMENT FINISHED...")
    return None
