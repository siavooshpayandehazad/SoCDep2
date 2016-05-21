# Copyright (C) Siavoosh Payandeh Azad


from vl_opt_functions import *
from RoutingAlgorithms import Routing
from ArchGraphUtilities import Arch_Graph_Reports
import copy
from ConfigAndPackages import Config
from math import exp, log10


def opt_ag_vertical_link_sa(ag, shmu, cost_file_name, logging):
    """
    Optimises the vertical link placement using simulated annealing!
    :param ag: architecture graph
    :param shmu: system health monitoring unit
    :param cost_file_name: name of the file for dumping the cost values during the process
    :param logging: logging file
    :return: None
    """
    logging.info("STARTING SA FOR VLP OPT")
    print "==========================================="
    print "VL PLACEMENT OPTIMIZATION USING SIMULATED ANNEALING..."
    print "STARTING TEMPERATURE:", Config.vl_opt.sa_initial_temp
    print "ANNEALING SCHEDULE: ", Config.vl_opt.sa_annealing_schedule
    print "TERMINATION CRITERIA: ", Config.vl_opt.termination_criteria
    if Config.vl_opt.termination_criteria == 'IterationNum':
        print "NUMBER OF ITERATIONS: ", Config.vl_opt.sa_iteration
    print "================"
    if type(cost_file_name) is str:
        ag_cost_file = open('Generated_Files/Internal/'+cost_file_name+'.txt', 'a')
    else:
        raise ValueError("ag_cost_file name is not string: "+str(cost_file_name))

    temperature_file = open('Generated_Files/Internal/vlp_sa_temp.txt', 'w')

    remove_all_vertical_links(shmu, ag)
    vertical_link_list = find_feasible_ag_vertical_link_placement(ag, shmu)
    routing_graph = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                   Config.DebugInfo, Config.DebugDetails))
    cost = vl_cost_function(ag, routing_graph)
    print ("STARTING AG VL PLACEMENT OPTIMIZATION")
    print ("NUMBER OF AVAILABLE V-LINKS: "+str(Config.vl_opt.vl_num))
    print ("INITIAL REACHABILITY METRIC: "+str(cost))
    starting_cost = cost
    current_cost = cost
    best_cost = cost
    best_vertical_link_list = vertical_link_list[:]

    ag_temp = copy.deepcopy(ag)
    cleanup_ag(ag_temp, shmu)
    Arch_Graph_Reports.draw_ag(ag_temp, "AG_VLOpt_init")
    del ag_temp

    ag_cost_file.write(str(cost)+"\n")

    temperature = Config.vl_opt.sa_initial_temp
    initial_temp = temperature
    iteration_num = Config.vl_opt.sa_iteration
    temperature_file.write(str(temperature)+"\n")

    i = 0
    while True:
        i += 1
        new_vertical_link_list = copy.deepcopy(move_to_new_vertical_link_configuration(ag, shmu,
                                                                                       vertical_link_list))
        new_routing_graph = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                           False, False))
        new_cost = vl_cost_function(ag, new_routing_graph)
        ag_cost_file.write(str(new_cost)+"\n")

        prob = metropolis(current_cost, new_cost, temperature)
        if prob > random.random():
            # accept the new solution
            vertical_link_list = new_vertical_link_list[:]
            current_cost = new_cost
            if new_cost > best_cost:
                best_cost = new_cost
                best_vertical_link_list = new_vertical_link_list[:]
                print ("\033[32m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:" +
                       str(cost) + "\t ITERATION: "+str(i))
        else:
            # move back to initial solution
            return_to_solution(ag, shmu, vertical_link_list)
        temperature = next_temp(initial_temp, i, iteration_num, temperature)
        temperature_file.write(str(temperature)+"\n")

        if Config.vl_opt.termination_criteria == 'IterationNum':
            if i == Config.vl_opt.sa_iteration:
                print ("REACHED MAXIMUM ITERATION NUMBER...")
                break
        elif Config.vl_opt.termination_criteria == 'StopTemp':
            if temperature <= Config.vl_opt.sa_stop_temp:
                print ("REACHED STOP TEMPERATURE...")
                break

    ag_cost_file.close()
    temperature_file.close()
    return_to_solution(ag, shmu, best_vertical_link_list)
    print ("-------------------------------------")
    print ("STARTING COST:"+str(starting_cost)+"\tFINAL COST:"+str(best_cost))
    print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(best_cost-starting_cost)/starting_cost))+" %")
    logging.info("SA FOR VL PLACEMENT FINISHED...")
    return None


def metropolis(current_cost, new_cost, temperature):
    """
    returns Metropolis function for finding the probability of the next move
    in Simulated Annealing
    :param current_cost: cost of the current solution
    :param new_cost: cost of the chosen neighbor solution
    :param temperature: current temperature of the process
    :return: Metropolis probability
    """
    if new_cost < current_cost:
        probability = exp((new_cost-current_cost)/temperature)
    else:
        probability = 1.0
    return probability


def next_temp(initial_temp, iteration, max_iteration, current_temp):
    """
    Temperature calculator for simulated annealing
    :param initial_temp: starting temperature of the process
    :param iteration: current iteration number
    :param max_iteration: max number of iterations
    :param current_temp: current temperature of the process
    :return: temperature chosen for next iteration
    """
    if Config.vl_opt.sa_annealing_schedule == 'Linear':
        temp = (float(max_iteration-iteration)/max_iteration)*initial_temp
        print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
    #   ----------------------------------------------------------------
    elif Config.vl_opt.sa_annealing_schedule == 'Exponential':
        temp = current_temp * Config.vl_opt.sa_alpha
        print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
    #   ----------------------------------------------------------------
    elif Config.vl_opt.sa_annealing_schedule == 'Logarithmic':
        # this is based on "A comparison of simulated annealing cooling strategies"
        # by Yaghout Nourani and Bjarne Andresen
        # iteration should be > 1 so I added 1
        temp = Config.vl_opt.sa_log_cooling_constant * (1.0/log10(1+(iteration+1)))
        print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
    else:
        raise ValueError('Invalid Cooling Method for SA...')
    return temp