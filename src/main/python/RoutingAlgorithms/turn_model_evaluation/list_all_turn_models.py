# Copyright (C) 2015 Siavoosh Payandeh Azad  and Thilo Kogge

import sys
import copy
import itertools
from random import shuffle, sample
from functools import partial
from multiprocessing import Pool
from statistics import stdev
from scipy.misc import comb
from ConfigAndPackages import PackageFile, Config, all_2d_turn_model_package
from ArchGraphUtilities import AG_Functions
from RoutingAlgorithms import Routing
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from RoutingAlgorithms.Routing_Functions import extended_degree_of_adaptiveness, degree_of_adaptiveness, \
    check_deadlock_freeness, return_turn_model_name
from RoutingAlgorithms.Calculate_Reachability import reachability_metric
from RoutingAlgorithms.turn_model_evaluation.turn_model_viz import viz_all_turn_models_against_each_other
from RoutingAlgorithms.turn_model_evaluation.turn_model_viz import viz_turn_model_evaluation
from ConfigAndPackages.all_odd_even_turn_model import all_odd_even_list


def enumerate_all_2d_turn_models_based_on_df(combination):
    """
    Lists all 2D deadlock free turn models in "deadlock_free_turns" in "Generated_Files"
    folder!
    ---------------------
        We have 256 turns in 2D Mesh NoC!
    ---------------------
    :param combination: number of turns which should be checked for combination!
    :return: None
    """
    counter = 0
    all_turns_file = open('Generated_Files/Turn_Model_Lists/all_2D_turn_models_'+str(combination)+'.txt', 'w')
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    Config.RotingType = 'NonMinimalPath'

    all_turns_file.write("#"+"\t\tDF/D\t"+'%25s' % "turns"+'%20s' % " "+"\t\t"+'%10s' % "c-metric" +
                         "\t\t"+'%10s' % "DoA"+"\t\t"+'%10s' % "DoAx"+"\n")
    all_turns_file.write("--------------"*8+"\n")
    ag = copy.deepcopy(AG_Functions.generate_ag())
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)
    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_2D)

    deadlock_free_counter = 0
    deadlock_counter = 0
    # print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        turns_health = copy.deepcopy(turns_health_2d_network)
        for turn in turns:
            turns_health[turn] = True
        counter += 1
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, list(turns), False,  False))
        if check_deadlock_freeness(noc_rg):
            connectivity_metric = reachability_metric(ag, noc_rg, False)
            doa = degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
            doa_ex = extended_degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
            deadlock_free_counter += 1
            # print counter, "\t \033[92mDF\033[0m \t", list(turns), "\t\t", connectivity_metric
            all_turns_file.write(str(counter)+"\t\tDF\t"+'%51s' % str(list(turns)) +
                                 "\t\t"+'%10s' % str(connectivity_metric) +
                                 "\t\t"+'%10s' % str(round(doa, 2))+"\t\t"+'%10s' % str(round(doa_ex, 2))+"\n")
        else:
            deadlock_counter += 1
            # print counter, "\t \033[31mDL\033[0m   \t", list(turns), "\t\t----"
            all_turns_file.write(str(counter)+"\t\tDL\t"+'%51s' % str(list(turns)) +
                                 "\t\t-----"+"\t\t-----"+"\t\t-----"+"\n")
        del shmu
        del noc_rg
    all_turns_file.write("---------------------------"+"\n")
    all_turns_file.write("Number of turn models with deadlock: "+str(deadlock_counter)+"\n")
    all_turns_file.write("Number of turn models without deadlock: "+str(deadlock_free_counter)+"\n")
    all_turns_file.write("=========================================="+"\n")
    all_turns_file.close()
    return None

def evaluate_actual_odd_even_turn_model():
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    Config.RotingType = 'MinimalPath'
    ag = copy.deepcopy(AG_Functions.generate_ag())
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

    turn_model_odd =  ['E2N', 'E2S', 'W2N', 'W2S', 'S2E', 'N2E']
    turn_model_even = ['E2N', 'E2S', 'S2W', 'S2E', 'N2W', 'N2E']

    if not check_tm_domination(turn_model_odd, turn_model_even):   # taking out the domination!
        turns_health = copy.deepcopy(turns_health_2d_network)
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))

        for node in ag.nodes():
            node_x, node_y, node_z = AG_Functions.return_node_location(node)
            if node_x % 2 == 1:
                for turn in turn_model_odd:
                    shmu.restore_broken_turn(node, turn, False)
                    from_port = str(node)+str(turn[0])+"I"
                    to_port = str(node)+str(turn[2])+"O"
                    Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
            else:
                for turn in turn_model_even:
                    shmu.restore_broken_turn(node, turn, False)
                    from_port = str(node)+str(turn[0])+"I"
                    to_port = str(node)+str(turn[2])+"O"
                    Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
        draw_rg(noc_rg)
        connectivity_metric = reachability_metric(ag, noc_rg, False)
        print "connectivity_metric:", connectivity_metric
        if check_deadlock_freeness(noc_rg):
            print "Deadlock free!"

        doa = degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
        doa_ex = extended_degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
        print "doa:", doa
        print "doa_ex", doa_ex

        sys.stdout.flush()


def enumerate_all_3d_turn_models_based_on_df(combination):
    """
    Lists all 3D deadlock free turn models in "deadlock_free_turns" in "Generated_Files"
    folder!
    ---------------------
        We have 16,777,216 turns in 3D Mesh NoC! if it takes one second to calculate
        deadlock freeness Then it takes almost 194.2 Days (almost 6.4 Months) to
        check all of them. that is the reason we need to make this parallel!
    ---------------------
    :param combination: number of turns which should be checked for combination!
    :return: None
    """
    counter = 0
    all_turns_file = open('Generated_Files/Turn_Model_Lists/all_3D_turn_models_'+str(combination)+'.txt', 'w')
    turns_health_3d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False,
                               "N2U": False, "N2D": False, "S2U": False, "S2D": False,
                               "W2U": False, "W2D": False, "E2U": False, "E2D": False,
                               "U2W": False, "U2E": False, "U2N": False, "U2S": False,
                               "D2W": False, "D2E": False, "D2N": False, "D2S": False}
    Config.ag.topology = '3DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 3

    ag = copy.deepcopy(AG_Functions.generate_ag())
    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_3D)

    deadlock_free_counter = 0
    deadlock_counter = 0
    # print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        turns_health = copy.deepcopy(turns_health_3d_network)
        for turn in turns:
            turns_health[turn] = True
        counter += 1
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, list(turns), False,  False))
        if check_deadlock_freeness(noc_rg):
            connectivity_metric = reachability_metric(ag, noc_rg, False)
            doa = degree_of_adaptiveness(ag, noc_rg, False)
            deadlock_free_counter += 1
            # print counter, "\t \033[92mDF\033[0m \t", list(turns), "\t\t", connectivity_metric
            all_turns_file.write(str(counter)+"\t\tDF\t"+str(list(turns))+"\t\t"+str(connectivity_metric) +
                                 "\t\t"+str(doa)+"\n")
        else:
            deadlock_counter += 1
            # print counter, "\t \033[31mDL\033[0m   \t", list(turns), "\t\t----"
            all_turns_file.write(str(counter)+"\t\tDL\t"+str(list(turns))+"\t\t-----""\n")
        del shmu
        del noc_rg
    all_turns_file.write("---------------------------"+"\n")
    all_turns_file.write("Number of turn models with deadlock: "+str(deadlock_counter)+"\n")
    all_turns_file.write("Number of turn models without deadlock: "+str(deadlock_free_counter)+"\n")
    all_turns_file.write("=========================================="+"\n")
    all_turns_file.close()
    return None


def enumerate_all_3d_turn_models(combination):
    """
    Lists all 3D deadlock free turn models in "deadlock_free_turns"
    ---------------------
        We have 16,777,216 turns in 3D Mesh NoC!
    ---------------------
    :param combination: number of turns which should be checked for combination!
    :return: None
    """
    counter = 0
    Config.ag.topology = '3DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 3
    all_turns_file = open('Generated_Files/Turn_Model_Lists/all_3D_turn_models_'+str(combination)+'.txt', 'w')

    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_3D)

    # print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        counter += 1
        # print counter, "\t\t", list(turns)
        all_turns_file.write(str(counter)+"\t\t"+str(list(turns))+"\n")
    all_turns_file.close()
    return None


def check_tm_domination(turn_model_1, turn_model_2):
    domination_1_2 = True
    domination_2_1 = True
    for turn in turn_model_1:
        if turn not in turn_model_2:
            domination_1_2 = False
            break

    for turn in turn_model_2:
        if turn not in turn_model_1:
            domination_2_1 = False
            break
    if domination_1_2 or domination_2_1:
        return True
    else:
        return False


def enumerate_all_odd_even_turn_models():
    all_odd_evens_file = open('Generated_Files/Turn_Model_Lists/odd_even_tm_list_dl_free.txt', 'w')
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 6
    Config.ag.y_size = 6
    Config.ag.z_size = 1
    Config.RotingType = 'MinimalPath'
    ag = copy.deepcopy(AG_Functions.generate_ag())
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

    turn_model_list = []
    for length in range(0, len(turns_health_2d_network.keys())+1):
        for item in list(itertools.combinations(turns_health_2d_network.keys(), length)):
            if len(item) > 0:
                turn_model_list.append(list(item))

    connected_counter = 0
    deadlock_free_counter = 0
    tm_counter = 0
    for turn_model_odd in turn_model_list:
        for turn_model_even in turn_model_list:
            if not check_tm_domination(turn_model_odd, turn_model_even):   # taking out the domination!
                turns_health = copy.deepcopy(turns_health_2d_network)
                shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
                shmu.setup_noc_shm(ag, turns_health, False)
                noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))

                for node in ag.nodes():
                    node_x, node_y, node_z = AG_Functions.return_node_location(node)
                    if node_x % 2 == 1:
                        for turn in turn_model_odd:
                            shmu.restore_broken_turn(node, turn, False)
                            from_port = str(node)+str(turn[0])+"I"
                            to_port = str(node)+str(turn[2])+"O"
                            Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                    else:
                        for turn in turn_model_even:
                            shmu.restore_broken_turn(node, turn, False)
                            from_port = str(node)+str(turn[0])+"I"
                            to_port = str(node)+str(turn[2])+"O"
                            Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                connectivity_metric = reachability_metric(ag, noc_rg, False)
                if connectivity_metric == number_of_pairs:
                    connected_counter += 1
                    if check_deadlock_freeness(noc_rg):
                        deadlock_free_counter += 1
                        all_odd_evens_file.write("["+str(turn_model_odd)+","+str(turn_model_even)+"],\n")

                tm_counter += 1
                sys.stdout.write("\rchecked TM: %i " % tm_counter +
                                 " number of fully connected TM: %i" % connected_counter +
                                 " number of deadlock free connected TM: %i" % deadlock_free_counter)
                sys.stdout.flush()
    all_odd_evens_file.close()
    return None


def evaluate_doa_for_all_odd_even_turn_model_list():
    all_odd_evens_file = open('Generated_Files/Turn_Model_Lists/all_odd_evens_doa.txt', 'w')
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    Config.RotingType = 'MinimalPath'
    ag = copy.deepcopy(AG_Functions.generate_ag())
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

    turn_model_list = []
    for length in range(0, len(turns_health_2d_network.keys())+1):
        for item in list(itertools.combinations(turns_health_2d_network.keys(), length)):
            if len(item) > 0:
                turn_model_list.append(list(item))

    classes_of_doa = {}
    classes_of_doax = {}
    tm_counter = 0

    all_odd_evens_file.write("    #  |                  "+'%51s' % " "+" \t|")
    all_odd_evens_file.write(" DoA    |   DoAx | \tC-metric\n")
    all_odd_evens_file.write("-------|--------------------------------------------" +
                             "----------------------------|--------|--------|-------------"+"\n")
    for turn_model in all_odd_even_list:
        turn_model_odd = turn_model[0]
        turn_model_even = turn_model[1]

        turns_health = copy.deepcopy(turns_health_2d_network)
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))

        for node in ag.nodes():
            node_x, node_y, node_z = AG_Functions.return_node_location(node)
            if node_x % 2 == 1:
                for turn in turn_model_odd:
                    shmu.restore_broken_turn(node, turn, False)
                    from_port = str(node)+str(turn[0])+"I"
                    to_port = str(node)+str(turn[2])+"O"
                    Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
            else:
                for turn in turn_model_even:
                    shmu.restore_broken_turn(node, turn, False)
                    from_port = str(node)+str(turn[0])+"I"
                    to_port = str(node)+str(turn[2])+"O"
                    Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
        doa = degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
        doa_ex = extended_degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)

        if round(doa, 2) not in classes_of_doa.keys():
            classes_of_doa[round(doa, 2)] = [tm_counter]
        else:
            classes_of_doa[round(doa, 2)].append(tm_counter)

        if round(doa_ex, 2) not in classes_of_doax.keys():
            classes_of_doax[round(doa_ex, 2)] = [tm_counter]
        else:
            classes_of_doax[round(doa_ex, 2)].append(tm_counter)

        all_odd_evens_file.write('%5s' % str(tm_counter)+"  | even turn model:"+'%53s' % str(turn_model_even)+"\t|")
        all_odd_evens_file.write("        |        |\n")
        all_odd_evens_file.write("       | odd turn model: "+'%53s' % str(turn_model_odd)+" \t|")

        all_odd_evens_file.write('%8s' % str(round(doa, 2)) + "|" + '%8s' % str(round(doa_ex, 2)) +
                                 "|\n")     # +'%8s' % str(round(connectivity_metric,2))+"\n")
        all_odd_evens_file.write("-------|--------------------------------------------" +
                                 "----------------------------|--------|--------|-------------"+"\n")
        tm_counter += 1
        sys.stdout.write("\rchecked TM: %i " % tm_counter)
        sys.stdout.flush()
    print
    print "----------------------------------------"
    print "classes of DOA:", sorted(classes_of_doa.keys())
    for item in sorted(classes_of_doa.keys()):
        print item,  sorted(classes_of_doa[item])
        # print
    print "------------------------------"
    print "classes of DOA_ex:", sorted(classes_of_doax.keys())
    for item in sorted(classes_of_doax.keys()):
        print item,  sorted(classes_of_doax[item])

    all_odd_evens_file.close()
    return None


def enumerate_all_2d_turn_models(combination):
    """
    Lists all 2D deadlock free turn models in "deadlock_free_turns"
    :param combination: number of turns which should be checked for combination!
    :return: None
    """
    counter = 0
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    all_turns_file = open('Generated_Files/Turn_Model_Lists/all_2D_turn_models_'+str(combination)+'.txt', 'w')
    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_2D)

    # print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        counter += 1
        # print counter, "\t\t", list(turns)
        all_turns_file.write(str(counter)+"\t\t"+str(list(turns))+"\n")
    all_turns_file.close()
    return None


def check_fault_tolerance_of_routing_algs(dimension, number_of_multi_threads, viz):
    """
    runs appropriate functions for checking fault tolerance of the network according to the topology,
    on number_of_multi_threads parallel threads
    :param dimension: defines the topology of the network, either "2D" or "3D"
    :param number_of_multi_threads: number of threads for running the program
    :param viz: boolean, if True, generates visualization of convergence of the connectivity metirc
    :return: False if the Dimension is wrong, other wise True
    """
    if dimension == '2D':
        Config.ag.topology = '2DMesh'
        Config.ag.z_size = 1
        args = list(range(0, 25))
        turn_model_list = all_2d_turn_model_package.all_2d_turn_models
    elif dimension == '3D':
        Config.ag.topology = '3DMesh'
        Config.ag.z_size = 3
        args = list(range(0, 108, 4))
        turn_model_list = PackageFile.routing_alg_list_3d
    else:
        print "Please choose a valid dimension!"
        return False
    for turn_model in turn_model_list:
        if dimension == '2D':
            p = Pool(number_of_multi_threads)
            function = partial(report_2d_turn_model_fault_tolerance, turn_model, viz)
            p.map(function, args)
            p.terminate()
        elif dimension == '3D':
            p = Pool(number_of_multi_threads)
            function = partial(report_3d_turn_model_fault_tolerance, turn_model, viz)
            p.map(function, args)
            p.terminate()
    if viz:
        for turn_model in turn_model_list:
            for arg in args:
                turn_model_name = return_turn_model_name(turn_model)
                file_name = None
                if dimension == '2D':
                    file_name = str(turn_model_name) + "_eval_" + str(24-arg)
                elif dimension == '3D':
                    file_name = str(turn_model_name) + "_eval_" + str(108-arg)
                viz_turn_model_evaluation(file_name)
    if dimension == '2D':
        viz_all_turn_models_against_each_other()
    return True


def report_2d_turn_model_fault_tolerance(turn_model, viz, combination):
    """
    generates 2D architecture graph with all combinations C(len(ag.nodes), combination)
    of links and writes the average connectivity metric in a file.
    :param turn_model: list of allowed turns for generating the routing graph
    :param viz: if true, generates the visualization files
    :param combination: number of links to be present in the network
    :return: None
    """
    Config.UsedTurnModel = copy.deepcopy(turn_model)
    Config.TurnsHealth = copy.deepcopy(Config.setup_turns_health())

    ag = copy.deepcopy(AG_Functions.generate_ag(report=False))

    turn_model_name = return_turn_model_name(Config.UsedTurnModel)

    file_name = str(turn_model_name)+'_eval'
    turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+file_name+'.txt', 'a+')
    if viz:
        file_name_viz = str(turn_model_name)+'_eval_'+str(len(ag.edges())-combination)
        turn_model_eval_viz_file = open('Generated_Files/Internal/'+file_name_viz+'.txt', 'w')
    else:
        turn_model_eval_viz_file = None
    counter = 0
    metric_sum = 0

    sub_ag_list = list(itertools.combinations(ag.edges(), combination))
    shuffle(sub_ag_list)

    list_of_avg = []
    for sub_ag in sub_ag_list:
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, copy.deepcopy(Config.TurnsHealth), False)
        for link in list(sub_ag):
            shmu.break_link(link, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                False,  False))
        connectivity_metric = reachability_metric(ag, noc_rg, False)
        counter += 1
        metric_sum += connectivity_metric
        # std = None
        list_of_avg.append(float(metric_sum)/counter)
        if len(list_of_avg) > 5000:
            list_of_avg.pop(0)
            std = stdev(list_of_avg)
            if std < 0.009:
                # turn_model_eval_file.write("STD of the last 5000 average samples is bellow 0.009\n")
                # turn_model_eval_file.write("Terminating the search!\n")
                del shmu
                del noc_rg
                break
        if viz:
            turn_model_eval_viz_file.write(str(float(metric_sum)/counter)+"\n")
        # print "#:"+str(counter)+"\t\tC.M.:"+str(connectivity_metric)+"\t\t avg:", \
        #     float(metric_sum)/counter, "\t\tstd:", std
        del shmu
        del noc_rg

    if counter > 0:
        avg_connectivity = float(metric_sum)/counter
    else:
        avg_connectivity = 0
    turn_model_eval_file.write(str(len(ag.edges())-combination)+"\t\t"+str(avg_connectivity)+"\n")
    if viz:
        turn_model_eval_viz_file.close()
    turn_model_eval_file.close()
    return None


def report_3d_turn_model_fault_tolerance(turn_model, viz, combination):
    """
    generates 3D architecture graph with all combinations C(len(ag.nodes), combination)
    of links and writes the average connectivity metric in a file.
    :param turn_model: list of allowed turns for generating the routing graph
    :param combination: number of links to be present in the network
    :param viz: if true, generates the visualization files
    :return: None
    """
    if combination == 108:
        raise ValueError("breaking 108 edges out of 108 edges is not possible your connectivity is 0!")

    Config.UsedTurnModel = copy.deepcopy(turn_model)
    Config.TurnsHealth = copy.deepcopy(Config.setup_turns_health())

    ag = copy.deepcopy(AG_Functions.generate_ag(report=False))

    turn_model_name = return_turn_model_name(Config.UsedTurnModel)

    file_name = str(turn_model_name)+'_eval'
    turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+file_name+'.txt', 'a+')
    if viz:
        file_name_viz = str(turn_model_name)+'_eval_'+str(len(ag.edges())-combination)
        turn_model_eval_viz_file = open('Generated_Files/Internal/'+file_name_viz+'.txt', 'w')
    else:
        turn_model_eval_viz_file = None
    counter = 0
    metric_sum = 0

    list_of_avg = []
    number_of_combinations = comb(108, combination)
    while True:
        sub_ag = sample(ag.edges(), combination)
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, copy.deepcopy(Config.TurnsHealth), False)
        for link in list(sub_ag):
            shmu.break_link(link, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                False,  False))
        connectivity_metric = reachability_metric(ag, noc_rg, False)
        counter += 1
        metric_sum += connectivity_metric
        # std = None
        list_of_avg.append(float(metric_sum)/counter)
        if len(list_of_avg) > 5000:
            list_of_avg.pop(0)
            std = stdev(list_of_avg)
            if std < 0.009:
                # turn_model_eval_file.write("STD of the last 5000 average samples is bellow 0.009\n")
                # turn_model_eval_file.write("Terminating the search!\n")
                del shmu
                del noc_rg
                break
        if viz:
            turn_model_eval_viz_file.write(str(float(metric_sum)/counter)+"\n")

        if counter >= number_of_combinations:
            del shmu
            del noc_rg
            break

        # print "#:"+str(counter)+"\t\tC.M.:"+str(connectivity_metric)+"\t\t avg:", \
        #    float(metric_sum)/counter, "\t\tstd:", std
        del shmu
        del noc_rg

    if counter > 0:
        avg_connectivity = float(metric_sum)/counter
    else:
        avg_connectivity = 0
    turn_model_eval_file.write(str(len(ag.edges())-combination)+"\t\t"+str(avg_connectivity)+"\n")
    turn_model_eval_file.close()
    if viz:
        turn_model_eval_viz_file.close()
    return None


def report_odd_even_turn_model_fault_tolerance(viz, routing_type, combination):
    """
    generates 2D architecture graph with all combinations C(len(ag.nodes), combination)
    of links and writes the average connectivity metric in a file.
    :param viz: if true, generates the visualization files
    :param routing_type: can be "minimal" or "nonminimal"
    :param combination: number of links to be present in the network
    :return: None
    """
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    tm_counter = 0
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1

    selected_turn_models = [677, 678, 697, 699, 717, 718, 737, 739, 757, 759, 778, 779, 797,
                            799, 818, 819, 679, 738, 777, 798]
    #selected_turn_models = [677, 798]
    if routing_type == "minimal":
        Config.RotingType = 'MinimalPath'
    else:
        Config.RotingType = 'NonMinimalPath'

    for turn_id in selected_turn_models:
        counter = 0
        metric_sum = 0
        turn_model = all_odd_even_list[turn_id]

        ag = copy.deepcopy(AG_Functions.generate_ag(report=False))
        turn_model_odd = turn_model[0]
        turn_model_even = turn_model[1]

        file_name = str(tm_counter)+'_eval'
        turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+file_name+'.txt', 'a+')
        if viz:
            file_name_viz = str(tm_counter)+'_eval_'+str(len(ag.edges())-counter)
            turn_model_eval_viz_file = open('Generated_Files/Internal/odd_even'+file_name_viz+'.txt', 'w')
        else:
            turn_model_eval_viz_file = None

        sub_ag_list = list(itertools.combinations(ag.edges(), combination))
        turns_health = copy.deepcopy(turns_health_2d_network)
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)

        for sub_ag in sub_ag_list:
            for link in list(sub_ag):
                shmu.break_link(link, False)

            noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))
            for node in ag.nodes():
                node_x, node_y, node_z = AG_Functions.return_node_location(node)
                if node_x % 2 == 1:
                    for turn in turn_model_odd:
                        shmu.restore_broken_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                else:
                    for turn in turn_model_even:
                        shmu.restore_broken_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')

            connectivity_metric = reachability_metric(ag, noc_rg, False)
            counter += 1
            metric_sum += connectivity_metric
            if viz:
                turn_model_eval_viz_file.write(str(float(metric_sum)/counter)+"\n")
            # print "#:"+str(counter)+"\t\tC.M.:"+str(connectivity_metric)+"\t\t avg:", \
            #     float(metric_sum)/counter, "\t\tstd:", std
            for link in list(sub_ag):
                shmu.restore_broken_link(link, False)
            del noc_rg

        shuffle(sub_ag_list)

        if counter > 0:
            avg_connectivity = float(metric_sum)/counter
        else:
            avg_connectivity = 0
        turn_model_eval_file.write(str(len(ag.edges())-combination)+"\t\t"+str(avg_connectivity)+"\n")
        if viz:
            turn_model_eval_viz_file.close()
        turn_model_eval_file.close()
        sys.stdout.write("\rchecked TM: %i " % tm_counter+"\t\t\tnumber of healthy links: %i " % combination)
        sys.stdout.flush()
        tm_counter += 1
    return None

def test():
    all_odd_evens_file = open('Generated_Files/Turn_Model_Lists/all_odd_evens_doa.txt', 'w')
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    Config.RotingType = 'MinimalPath'
    ag = copy.deepcopy(AG_Functions.generate_ag())
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

    max_ratio = 0
    for turn_model in all_odd_even_list:
    #for item in selected_turn_models:
        #print item
        #turn_model = all_odd_even_list[item]
        #print turn_model
        turn_model_index = all_odd_even_list.index(turn_model)
        turn_model_odd = turn_model[0]
        turn_model_even = turn_model[1]

        turns_health = copy.deepcopy(turns_health_2d_network)
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))

        for node in ag.nodes():
                node_x, node_y, node_z = AG_Functions.return_node_location(node)
                if node_x % 2 == 1:
                    for turn in turn_model_odd:
                        shmu.restore_broken_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                else:
                    for turn in turn_model_even:
                        shmu.restore_broken_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
        #draw_rg(noc_rg)
        number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)
        doa = degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
        sum_of_paths = 0
        sum_of_sim_ratio = 0
        for source_node in ag.nodes():
                for destination_node in ag.nodes():
                    if source_node != destination_node:
                        if is_destination_reachable_from_source(noc_rg, source_node, destination_node):
                                #print source_node, "--->", destination_node
                                paths = list(all_shortest_paths(noc_rg, str(source_node)+str('L')+str('I'), str(destination_node)+str('L')+str('O')))
                                sum_of_paths += len(paths)
                                #for path in paths:
                                #    print path
                                local_sim_ratio = 0
                                counter = 0
                                if len(paths) > 1:
                                    for i in range(0, len(paths)):
                                        for j in range(i, len(paths)):
                                            if paths[i] != paths[j]:
                                                sm=difflib.SequenceMatcher(None,paths[i],paths[j])
                                                simmilarity_ratio =  sm.ratio()
                                                counter += 1
                                                #print "\t", i, "->", j, "\tsimilarity:", simmilarity_ratio
                                                local_sim_ratio += simmilarity_ratio
                                    local_sim_ratio = local_sim_ratio/counter
                                    local_sim_ratio = local_sim_ratio
                                    sum_of_sim_ratio += local_sim_ratio
                                else:

                                    sum_of_sim_ratio += 1
                                #print "average similarity ratio:", local_sim_ratio
                                #print "--------------------------------------------"
        #print "number of paths", sum_of_paths
        doa_ratio = float(doa)/sum_of_sim_ratio
        if max_ratio < doa_ratio:
            max_ratio = doa_ratio
        print "Turn Model ", '%5s' %turn_model_index, "\tdoa:", "{:3.3f}".format(doa), "\tsimilarity ratio:", "{:3.3f}".format(sum_of_sim_ratio), "\t\tfault tolerance metric:","{:3.3f}".format(doa_ratio)
        #print "--------------------------------------------"
        del noc_rg
    print "max doa_ratio", max_ratio
    return None
