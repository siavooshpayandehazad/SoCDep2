# Copyright (C) 2015 Siavoosh Payandeh Azad 

import copy
from Mapper import Mapping_Functions
from ConfigAndPackages import Config
from Scheduler import Scheduler, Scheduling_Functions
import random
from math import exp, log10, log1p
from collections import deque
from scipy import stats
import statistics


def optimize_mapping_sa(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg,
                        shm, cost_data_file, logging):
    print ("===========================================")
    print ("STARTING MAPPING OPTIMIZATION...USING SIMULATED ANNEALING...")
    print ("STARTING TEMPERATURE: "+str(Config.SA_InitialTemp))
    print ("ANNEALING SCHEDULE: "+Config.SA_AnnealingSchedule)
    print ("TERMINATION CRITERIA: "+Config.TerminationCriteria)
    print ("================")

    if type(cost_data_file) is str:
        mapping_cost_file = open('Generated_Files/Internal/'+cost_data_file+'.txt', 'a')
    else:
        raise ValueError("cost_data_file name is not string: "+str(cost_data_file))

    mapping_process_file = open('Generated_Files/Internal/MappingProcess.txt', 'w')
    sa_temperature_file = open('Generated_Files/Internal/SATemp.txt', 'w')
    sa_cost_slop_file = open('Generated_Files/Internal/SACostSlope.txt', 'w')
    sa_huang_race_file = open('Generated_Files/Internal/SAHuangRace.txt', 'w')

    if Config.SA_AnnealingSchedule in ['Adaptive', 'Aart', 'Huang']:
        cost_monitor = deque([])
    else:
        cost_monitor = []

    if Config.DistanceBetweenMapping:
        init_map_string = Mapping_Functions.mapping_into_string(tg)
        if Config.Mapping_CostFunctionType == 'CONSTANT':
            Mapping_Functions.clear_mapping(tg, ctg, ag)
            if not Mapping_Functions.make_initial_mapping(tg, ctg, ag, shm, noc_rg, critical_rg,
                                                          noncritical_rg, True, logging,
                                                          Config.mapping_random_seed):
                raise ValueError("FEASIBLE MAPPING NOT FOUND...")
    else:
        init_map_string = None

    current_tg = copy.deepcopy(tg)
    current_ag = copy.deepcopy(ag)
    current_ctg = copy.deepcopy(ctg)
    current_cost = Mapping_Functions.mapping_cost_function(tg, ag, shm, False, initial_mapping_string=init_map_string)
    starting_cost = current_cost

    best_tg = copy.deepcopy(tg)
    best_ag = copy.deepcopy(ag)
    best_ctg = copy.deepcopy(ctg)
    best_cost = current_cost

    initial_temp = Config.SA_InitialTemp
    sa_temperature_file.write(str(initial_temp)+"\n")
    temperature = initial_temp
    slope = None
    zero_slope_counter = 0
    standard_deviation = None

    # for Huang Annealing schedule
    huang_counter1 = 0
    huang_counter2 = 0
    huang_steady_counter = 0
    iteration_num = Config.SimulatedAnnealingIteration
    # for i in range(0, iteration_num):
    #       move to another solution
    i = 0
    while True:
        i += 1
        new_tg, new_ctg, new_ag = move_to_next_solution(i, current_tg, current_ctg, current_ag,  noc_rg,
                                                        shm, critical_rg, noncritical_rg, logging)
        Scheduling_Functions.clear_scheduling(new_ag)
        Scheduler.schedule_all(new_tg, new_ag, shm, False, logging)

        # calculate the cost of new solution
        new_cost = Mapping_Functions.mapping_cost_function(new_tg, new_ag, shm, False,
                                                           initial_mapping_string=init_map_string)

        if new_cost < best_cost:
            best_tg = copy.deepcopy(new_tg)
            best_ag = copy.deepcopy(new_ag)
            best_ctg = copy.deepcopy(new_ctg)
            best_cost = new_cost
            print ("\033[33m* NOTE::\033[0mFOUND BETTER SOLUTION WITH COST:"+"{0:.2f}".format(new_cost) +
                   "\t ITERATION:"+str(i)+"\tIMPROVEMENT:" +
                   "{0:.2f}".format(100*(starting_cost-new_cost)/starting_cost)+" %")
        # calculate the probability P of accepting the solution
        prob = metropolis(current_cost, new_cost, temperature)
        # print ("prob:", prob)
        # throw the coin with probability P
        random_seed = Config.mapping_random_seed
        random.seed(Config.mapping_random_seed)
        for j in range(0, i):
            random_seed = random.randint(1, 100000)
        random.seed(random_seed)
        logging.info("Throwing Dice: random_seed: "+str(random_seed)+"    iteration: "+str(i))
        if prob > random.random():
            # accept the new solution
            move_accepted = True
            current_tg = copy.deepcopy(new_tg)
            current_ag = copy.deepcopy(new_ag)
            current_ctg = copy.deepcopy(new_ctg)
            current_cost = new_cost
            if Config.SA_ReportSolutions:
                if slope is not None:
                    print ("\033[32m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:", "{0:.2f}".format(current_cost),
                           "\tprob:", "{0:.2f}".format(prob), "\tTemp:", "{0:.2f}".format(temperature),
                           "\t Iteration:", i, "\tSLOPE:", "{0:.2f}".format(slope))
                if standard_deviation is not None:
                    print ("\033[32m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:", "{0:.2f}".format(current_cost),
                           "\tprob:", "{0:.2f}".format(prob), "\tTemp:", "{0:.2f}".format(temperature),
                           "\t Iteration:", i, "\tSTD_DEV:", "{0:.2f}".format(standard_deviation))
                else:
                    print ("\033[32m* NOTE::\033[0mMOVED TO SOLUTION WITH COST:", "{0:.2f}".format(current_cost),
                           "\tprob:", "{0:.2f}".format(prob), "\tTemp:", "{0:.2f}".format(temperature),
                           "\t Iteration:", i)
        else:
            move_accepted = False
            # move back to initial solution
            pass
        # update Temp
        mapping_process_file.write(Mapping_Functions.mapping_into_string(current_tg)+"\n")
        sa_temperature_file.write(str(temperature)+"\n")
        mapping_cost_file.write(str(current_cost)+"\n")

        if Config.SA_AnnealingSchedule == 'Adaptive':
            if len(cost_monitor) > Config.CostMonitorQueSize:
                cost_monitor.appendleft(current_cost)
                cost_monitor.pop()
            else:
                cost_monitor.appendleft(current_cost)
            slope = calculate_slope_of_cost(cost_monitor)
            if slope == 0:
                zero_slope_counter += 1
            else:
                zero_slope_counter = 0
            sa_cost_slop_file.write(str(slope)+"\n")

        if Config.SA_AnnealingSchedule == 'Aart':
            if len(cost_monitor) == Config.CostMonitorQueSize:
                standard_deviation = statistics.stdev(cost_monitor)
                cost_monitor.clear()
                # print (standard_deviation)
            else:
                cost_monitor.appendleft(current_cost)

        # Huang's annealing schedule is very much like Aart's Schedule... how ever, Aart's schedule stays in a fixed
        # temperature for a fixed number of steps, however, Huang's schedule decides about number of steps dynamically

        if Config.SA_AnnealingSchedule == 'Huang':
            cost_monitor.appendleft(current_cost)
            if len(cost_monitor) > 1:
                huang_cost_mean = sum(cost_monitor)/len(cost_monitor)
                huang_cost_sd = statistics.stdev(cost_monitor)
                if move_accepted:
                    if huang_cost_mean - Config.HuangAlpha * huang_cost_sd <= current_cost <= \
                            huang_cost_mean + Config.HuangAlpha * huang_cost_sd:
                        huang_counter1 += 1
                    else:
                        huang_counter2 += 1
            # print (huang_counter1, huang_counter2)
            sa_huang_race_file.write(str(huang_counter1)+" "+str(huang_counter2)+"\n")
            if huang_counter1 == Config.HuangTargetValue1:
                standard_deviation = statistics.stdev(cost_monitor)
                cost_monitor.clear()
                huang_counter1 = 0
                huang_counter2 = 0
                huang_steady_counter = 0
            elif huang_counter2 == Config.HuangTargetValue2:
                huang_counter1 = 0
                huang_counter2 = 0
                standard_deviation = None
            elif huang_steady_counter == Config.CostMonitorQueSize:
                standard_deviation = statistics.stdev(cost_monitor)
                cost_monitor.clear()
                huang_counter1 = 0
                huang_counter2 = 0
                huang_steady_counter = 0
                print ("\033[36m* COOLING::\033[0m REACHED MAX STEADY STATE... PREPARING FOR COOLING...")
            else:
                standard_deviation = None

            huang_steady_counter += 1

        temperature = next_temp(initial_temp, i, iteration_num, temperature, slope, standard_deviation)

        if Config.SA_AnnealingSchedule == 'Adaptive':
            if zero_slope_counter == Config.MaxSteadyState:
                print ("NO IMPROVEMENT POSSIBLE...")
                break
        if Config.TerminationCriteria == 'IterationNum':
            if i == Config.SimulatedAnnealingIteration:
                print ("REACHED MAXIMUM ITERATION NUMBER...")
                break
        elif Config.TerminationCriteria == 'StopTemp':
            if temperature <= Config.SA_StopTemp:
                print ("REACHED STOP TEMPERATURE...")
                break

    mapping_cost_file.close()
    mapping_process_file.close()
    sa_temperature_file.close()
    sa_cost_slop_file.close()
    sa_huang_race_file.close()
    print ("-------------------------------------")
    print ("STARTING COST:"+str(starting_cost)+"\tFINAL COST:"+str(best_cost))
    print ("IMPROVEMENT:"+"{0:.2f}".format(100*(starting_cost-best_cost)/starting_cost)+" %")
    return best_tg, best_ctg, best_ag


def next_temp(initial_temp, iteration, max_iteration, current_temp, slope=None, standard_deviation=None):
    if Config.SA_AnnealingSchedule == 'Linear':
        temp = (float(max_iteration-iteration)/max_iteration)*initial_temp
        print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Exponential':
        temp = current_temp * Config.SA_Alpha
        print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Logarithmic':
        # this is based on "A comparison of simulated annealing cooling strategies"
        # by Yaghout Nourani and Bjarne Andresen
        temp = Config.LogCoolingConstant * (1.0/log10(1+(iteration+1)))     # iteration should be > 1 so I added 1
        print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Adaptive':
        temp = current_temp
        if iteration > Config.CostMonitorQueSize:
            if 0 < slope < Config.SlopeRangeForCooling:
                temp = current_temp * Config.SA_Alpha
                print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Markov':
        temp = initial_temp - (iteration/Config.MarkovNum)*Config.MarkovTempStep
        if temp < current_temp:
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
        if temp <= 0:
            temp = current_temp
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Aart':
        # This is coming from the following paper:
        # Job Shop Scheduling by Simulated Annealing Author(s): Peter J. M. van Laarhoven,
        # Emile H. L. Aarts, Jan Karel Lenstra
        if iteration % Config.CostMonitorQueSize == 0 and standard_deviation is not None and standard_deviation != 0:
            temp = float(current_temp)/(1+(current_temp*(log1p(Config.Delta)/standard_deviation)))
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
        elif standard_deviation == 0:
            temp = float(current_temp)*Config.SA_Alpha
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
        else:
            temp = current_temp
#   ----------------------------------------------------------------
    elif Config.SA_AnnealingSchedule == 'Huang':
        if standard_deviation is not None and standard_deviation != 0:
            temp = float(current_temp)/(1+(current_temp*(log1p(Config.Delta)/standard_deviation)))
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
        elif standard_deviation == 0:
            temp = float(current_temp)*Config.SA_Alpha
            print ("\033[36m* COOLING::\033[0m CURRENT TEMP: "+str(temp))
        else:
            temp = current_temp
#   ----------------------------------------------------------------
    else:
        raise ValueError('Invalid Cooling Method for SA...')
    return temp


def calculate_slope_of_cost(cost_monitor):
    slope = 0
    if len(cost_monitor) > 2:
        x = range(0, len(cost_monitor))
        y = list(cost_monitor)
        slope = stats.linregress(x, y)[0]
    if len(cost_monitor) == 2:
        slope = list(cost_monitor)[1]-list(cost_monitor)[0]
    return slope


def metropolis(current_cost, new_cost, temperature):
    if new_cost > current_cost:
        probability = exp((current_cost-new_cost)/temperature)
    else:
        probability = 1.0
    return probability


def move_to_next_solution(iteration, tg, ctg, ag, noc_rg, shm, critical_rg, noncritical_rg, logging):

    random_seed = Config.mapping_random_seed
    random.seed(Config.mapping_random_seed)
    for i in range(0, iteration):
        random_seed = random.randint(1, 100000)
    random.seed(random_seed)
    logging.info("Moving to next solution: random_seed: "+str(random_seed)+"    iteration: "+str(iteration))

    cluster_to_move = random.choice(ctg.nodes())
    current_node = ctg.node[cluster_to_move]['Node']
    Mapping_Functions.remove_cluster_from_node(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg,
                                               cluster_to_move, current_node, logging)
    destination_node = random.choice(ag.nodes())
    if Config.EnablePartitioning:
        while ctg.node[cluster_to_move]['Criticality'] != ag.node[destination_node]['Region']:
            destination_node = random.choice(ag.nodes())
    try_counter = 0
    while not Mapping_Functions.add_cluster_to_node(tg, ctg, ag, shm, noc_rg, critical_rg, noncritical_rg,
                                                    cluster_to_move, destination_node, logging):

            # If add_cluster_to_node fails it automatically removes all the connections...
            # we need to add the cluster to the old place...
            Mapping_Functions.add_cluster_to_node(tg, ctg, ag, shm, noc_rg, critical_rg, noncritical_rg,
                                                  cluster_to_move, current_node, logging)
            try_counter += 1
            if try_counter >= 3*len(ag.nodes()):
                print ("CAN NOT FIND ANY FEASIBLE SOLUTION... ABORTING LOCAL SEARCH...")
                return tg, ctg, ag

            # choosing another cluster to move
            cluster_to_move = random.choice(ctg.nodes())
            current_node = ctg.node[cluster_to_move]['Node']
            Mapping_Functions.remove_cluster_from_node(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg,
                                                       cluster_to_move, current_node, logging)
            destination_node = random.choice(ag.nodes())
            if Config.EnablePartitioning:
                while ctg.node[cluster_to_move]['Criticality'] != ag.node[destination_node]['Region']:
                    destination_node = random.choice(ag.nodes())
    return tg, ctg, ag