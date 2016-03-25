# Copyright (C) 2015 Siavoosh Payandeh Azad  and Thilo Kogge

from ConfigAndPackages import PackageFile, Config
import copy
import itertools
import AG_Functions
from RoutingAlgorithms import Routing
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from RoutingAlgorithms import Calculate_Reachability
import networkx
from statistics import stdev
from random import shuffle


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
    all_turns_file = open('Generated_Files/Turn_Model_Lists/all_turn_models'+str(combination)+'.txt', 'w')
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
        if networkx.is_directed_acyclic_graph(noc_rg):
            connectivity_metric = Calculate_Reachability.reachability_metric(ag, noc_rg, False)
            deadlock_free_counter += 1
            print counter, "\t \033[92mDF\033[0m \t", list(turns), connectivity_metric
            all_turns_file.write(str(counter)+"\t\tDF\t"+str(list(turns))+"\t\t"+str(connectivity_metric)+"\n")
        else:
            deadlock_counter += 1
            print counter, "\t \033[31mDL\033[0m   \t", list(turns), "----"
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
    Config.ag.topology = '3DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 3

    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_3D)

    print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        counter += 1
        print counter, "\t\t", list(turns)
    return None


def report_turn_model_fault_tolerance(turn_model, combination):

    Config.UsedTurnModel = copy.deepcopy(turn_model)
    Config.TurnsHealth = copy.deepcopy(Config.setup_turns_health())

    ag = copy.deepcopy(AG_Functions.generate_ag(report=False))

    if Config.UsedTurnModel == PackageFile.XY_TurnModel:
        turn_model_name = 'XY'
    elif Config.UsedTurnModel == PackageFile.WestFirst_TurnModel:
        turn_model_name = 'West_First'
    elif Config.UsedTurnModel == PackageFile.NorthLast_TurnModel:
        turn_model_name = 'North_Last'
    elif Config.UsedTurnModel == PackageFile.NegativeFirst2D_TurnModel:
        turn_model_name = 'Neg_First'
    elif Config.UsedTurnModel == PackageFile.XYZ_TurnModel:
        turn_model_name = 'XYZ'
    elif Config.UsedTurnModel == PackageFile.NegativeFirst3D_TurnModel:
        turn_model_name = 'Neg_First_3D'
    else:
        turn_model_name = None

    turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+str(turn_model_name) +
                                '_eval_'+str(len(ag.edges())-combination)+'.txt', 'w')
    counter = 0
    metric_sum = 0
    print "here1"
    sub_ag_list = list(itertools.combinations(ag.edges(), combination))
    print "here2"
    shuffle(sub_ag_list)
    print "here3"
    list_of_avg = []
    for sub_ag in sub_ag_list:
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, copy.deepcopy(Config.TurnsHealth), False)
        for link in list(sub_ag):
            shmu.break_link(link, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, Config.UsedTurnModel,
                                                                False,  False))
        connectivity_metric = Calculate_Reachability.reachability_metric(ag, noc_rg, False)
        counter += 1
        metric_sum += connectivity_metric
        std = None
        list_of_avg.append(float(metric_sum)/counter)
        if len(list_of_avg) > 5000:
            list_of_avg.pop(0)
            std = stdev(list_of_avg)
            if std < 0.009:
                turn_model_eval_file.write("STD of the last 5000 average samples is bellow 0.009\n")
                turn_model_eval_file.write("Terminating the search!\n")
                del shmu
                del noc_rg
                break
        turn_model_eval_file.write(str(counter)+"\t\t"+str(connectivity_metric)+"\n")
        print str(counter)+"\t\t"+str(connectivity_metric)+"\t\t", float(metric_sum)/counter, "\t\t", std
        del shmu
        del noc_rg

    if counter > 0:
        avg_connectivity = float(metric_sum)/counter
    else:
        avg_connectivity = 0
    turn_model_eval_file.write("==============================================\n")
    turn_model_eval_file.write("Combination: "+str(len(ag.edges())-combination)+"\n" +
                               "   AVG Connectivity: "+str(avg_connectivity)+"\n")
    return None