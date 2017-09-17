# Copyright (C) 2015 Siavoosh Payandeh Azad

import random
import copy
from Scheduler import Scheduler, Scheduling_Functions, Scheduling_Reports
from Mapper import Mapping_Functions
from ConfigAndPackages import Config


def mapping_opt_local_search(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg, shm,
                             iteration_num, report, detailed_report, logging,
                             cost_data_file_name, mapping_process_file_name, random_seed,
                             initial_mapping_string=None):
    random.seed(random_seed)
    if report:
        print ("===========================================")
        print ("STARTING MAPPING OPTIMIZATION...USING LOCAL SEARCH...")
        print ("NUMBER OF ITERATIONS: "+str(iteration_num))

    if type(cost_data_file_name) is str:
        mapping_cost_file = open('Generated_Files/Internal/'+cost_data_file_name+'.txt', 'a')
    else:
        raise ValueError("cost_data_file_name name is not string: "+str(cost_data_file_name))

    if type(mapping_process_file_name) is str:
        mapping_process_file = open('Generated_Files/Internal/'+mapping_process_file_name+'.txt', 'a')
    else:
        raise ValueError("mapping_process_file name is not string: "+str(mapping_process_file_name))

    best_tg = copy.deepcopy(tg)
    best_ag = copy.deepcopy(ag)
    best_ctg = copy.deepcopy(ctg)
    best_cost = Mapping_Functions.mapping_cost_function(tg, ag, shm, False, initial_mapping_string=initial_mapping_string)
    starting_cost = best_cost
    for iteration in range(0, iteration_num):
        logging.info("       ITERATION:"+str(iteration))
        cluster_to_move = random.choice(ctg.nodes())
        current_node = ctg.node[cluster_to_move]['Node']
        Mapping_Functions.remove_cluster_from_node(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg,
                                                   cluster_to_move, current_node, logging)
        destination_node = random.choice(ag.nodes())
        if Config.EnablePartitioning:
            while ctg.node[cluster_to_move]['Criticality'] != ag.node[destination_node]['Region']:
                destination_node = random.choice(ag.nodes())
        # print (ctg.node[cluster_to_move]['Criticality'],AG.node[destination_node]['Region'])

        try_counter = 0
        while not Mapping_Functions.add_cluster_to_node(tg, ctg, ag, shm, noc_rg, critical_rg, noncritical_rg,
                                                        cluster_to_move, destination_node, logging):

            # If add_cluster_to_node fails it automatically removes all the connections...
            # we need to add the cluster to the old place...
            Mapping_Functions.add_cluster_to_node(tg, ctg, ag, shm, noc_rg, critical_rg, noncritical_rg,
                                                  cluster_to_move, current_node, logging)

            # choosing another cluster to move
            cluster_to_move = random.choice(ctg.nodes())
            current_node = ctg.node[cluster_to_move]['Node']
            Mapping_Functions.remove_cluster_from_node(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg,
                                                       cluster_to_move, current_node, logging)
            destination_node = random.choice(ag.nodes())
            if Config.EnablePartitioning:
                while ctg.node[cluster_to_move]['Criticality'] != ag.node[destination_node]['Region']:
                    destination_node = random.choice(ag.nodes())
            # print (ctg.node[cluster_to_move]['Criticality'],AG.node[destination_node]['Region'])

            if try_counter >= 3*len(ag.nodes()):
                if report:
                    print ("CAN NOT FIND ANY FEASIBLE SOLUTION... ABORTING LOCAL SEARCH...")
                logging.info("CAN NOT FIND ANY FEASIBLE SOLUTION... ABORTING LOCAL SEARCH...")
                tg = copy.deepcopy(best_tg)
                ag = copy.deepcopy(best_ag)
                ctg = copy.deepcopy(ctg)
                if report:
                    Scheduling_Reports.report_mapped_tasks(ag, logging)
                    Mapping_Functions.mapping_cost_function(tg, ag, shm, True, initial_mapping_string=initial_mapping_string)
                return best_tg, best_ctg, best_ag
            try_counter += 1

        Scheduling_Functions.clear_scheduling(ag)
        Scheduler.schedule_all(tg, ag, shm, False, logging)

        current_cost = Mapping_Functions.mapping_cost_function(tg, ag, shm, detailed_report, initial_mapping_string= initial_mapping_string)
        mapping_process_file.write(Mapping_Functions.mapping_into_string(tg)+"\n")
        mapping_cost_file.write(str(current_cost)+"\n")
        if current_cost <= best_cost:
            if current_cost < best_cost:
                if report:
                    print ("\033[32m* NOTE::\033[0mBETTER SOLUTION FOUND WITH COST: "+str(current_cost) +
                           "\t ITERATION:"+str(iteration))
                logging.info("NOTE:: MOVED TO SOLUTION WITH COST: "+str(current_cost)+"ITERATION: "+str(iteration))
            else:
                logging.info("NOTE:: MOVED TO SOLUTION WITH COST: "+str(current_cost)+"ITERATION: "+str(iteration))

            best_tg = copy.deepcopy(tg)
            best_ag = copy.deepcopy(ag)
            best_ctg = copy.deepcopy(ctg)
            best_cost = current_cost
        else:
            tg = copy.deepcopy(best_tg)
            ag = copy.deepcopy(best_ag)
            ctg = copy.deepcopy(best_ctg)
            mapping_process_file.write(Mapping_Functions.mapping_into_string(tg)+"\n")

    Scheduling_Functions.clear_scheduling(ag)
    Scheduler.schedule_all(tg, ag, shm, False, logging)
    mapping_process_file.close()
    mapping_cost_file.close()
    if report:
        print ("-------------------------------------")
        print ("STARTING COST: "+str(starting_cost)+"\tFINAL COST: "+str(best_cost) +
               "\tAFTER "+str(iteration_num)+" ITERATIONS")
        print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(starting_cost-best_cost)/starting_cost))+" %")
    return best_tg, best_ctg, best_ag


def mapping_opt_iterative_local_search(tg, ctg, ag, noc_rg, critical_rg, noncritical_rg, shm, iteration_num,
                                       sub_iteration, report, detailed_report, logging):
    if report:
        print ("===========================================")
        print ("STARTING MAPPING OPTIMIZATION...USING ITERATIVE LOCAL SEARCH...")

    best_tg = copy.deepcopy(tg)
    best_ag = copy.deepcopy(ag)
    best_ctg = copy.deepcopy(ctg)
    best_cost = Mapping_Functions.mapping_cost_function(tg, ag, shm, False)
    starting_cost = best_cost
    if report:
        print ("INITIAL COST:"+str(starting_cost))
    mapping_cost_file = open('Generated_Files/Internal/LocalSearchMappingCost.txt', 'w')
    mapping_cost_file.close()
    mapping_process_file = open('Generated_Files/Internal/MappingProcess.txt', 'w')
    mapping_process_file.close()
    for Iteration in range(0, iteration_num):
        logging.info("        ITERATION:"+str(Iteration))
        random_seed = Config.mapping_random_seed
        random.seed(Config.mapping_random_seed)
        for i in range(0, Iteration):
            random_seed = random.randint(1, 100000)
        (current_tg, current_ctg, current_ag) = mapping_opt_local_search(tg, ctg, ag, noc_rg, critical_rg,
                                                                         noncritical_rg, shm, sub_iteration,
                                                                         False, detailed_report, logging,
                                                                         "LocalSearchMappingCost",
                                                                         "mapping_process_file_name", random_seed)
        if current_tg is not False:
            current_cost = Mapping_Functions.mapping_cost_function(current_tg, current_ag, shm, False)
            if current_cost <= best_cost:
                if current_cost < best_cost:
                    if report:
                        print ("\033[32m* NOTE::\033[0mBETTER SOLUTION FOUND WITH COST: "+str(current_cost) +
                               "\t ITERATION: "+str(Iteration))
                    logging.info("NOTE:: MOVED TO SOLUTION WITH COST: "+str(current_cost)+"ITERATION: "+str(Iteration))
                else:
                    logging.info("NOTE:: MOVED TO SOLUTION WITH COST: "+str(current_cost)+"ITERATION: "+str(Iteration))
                best_tg = copy.deepcopy(current_tg)
                best_ag = copy.deepcopy(current_ag)
                best_ctg = copy.deepcopy(current_ctg)
                best_cost = current_cost
        del current_tg
        del current_ag
        del current_ctg
        Mapping_Functions.clear_mapping(tg, ctg, ag)
        counter = 0
        schedule = True
        random_seed = Config.mapping_random_seed
        random.seed(Config.mapping_random_seed)
        for i in range(0, Iteration):
            random_seed = random.randint(1, 100000)
        while not Mapping_Functions.make_initial_mapping(tg, ctg, ag, shm, noc_rg, critical_rg,
                                                         noncritical_rg, False, logging, random_seed):
            if counter == 10:   # we try 10 times to find some initial solution... how ever if it fails...
                schedule = False
                break
            counter += 1
        if schedule:
            Scheduling_Functions.clear_scheduling(ag)
            Scheduler.schedule_all(tg, ag, shm, False, logging)
        else:
            if report:
                print ("\033[33mWARNING::\033[0m CAN NOT FIND ANOTHER FEASIBLE SOLUTION... ",
                       "ABORTING ITERATIVE LOCAL SEARCH...")
            logging.info("CAN NOT FIND ANOTHER FEASIBLE SOLUTION... ABORTING ITERATIVE LOCAL SEARCH...")
            if report:
                print ("-------------------------------------")
                print ("STARTING COST: "+str(starting_cost)+"\tFINAL COST: "+str(best_cost))
                print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(starting_cost-best_cost)/starting_cost))+" %")
            return best_tg, best_ctg, best_ag

    if report:
        print ("-------------------------------------")
        print ("STARTING COST:"+str(starting_cost)+"\tFINAL COST:"+str(best_cost))
        print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(starting_cost-best_cost)/starting_cost))+" %")
    return best_tg, best_ctg, best_ag
