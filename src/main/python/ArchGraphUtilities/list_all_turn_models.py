# Copyright (C) 2015 Siavoosh Payandeh Azad  and Thilo Kogge

from ConfigAndPackages import PackageFile, Config, all_2d_turn_model_package
import copy
import random
import itertools
import AG_Functions
from RoutingAlgorithms import Routing
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from RoutingAlgorithms import Calculate_Reachability
import networkx
from statistics import stdev
import os
from random import shuffle, sample
import matplotlib.pyplot as plt
from scipy.misc import comb
from functools import partial
from RoutingAlgorithms.Routing import return_turn_model_name
from multiprocessing import Pool


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

    ag = copy.deepcopy(AG_Functions.generate_ag())
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
        if networkx.is_directed_acyclic_graph(noc_rg):
            connectivity_metric = Calculate_Reachability.reachability_metric(ag, noc_rg, False)
            deadlock_free_counter += 1
            print counter, "\t \033[92mDF\033[0m \t", list(turns), "\t\t", connectivity_metric
            all_turns_file.write(str(counter)+"\t\tDF\t"+str(list(turns))+"\t\t"+str(connectivity_metric)+"\n")
        else:
            deadlock_counter += 1
            print counter, "\t \033[31mDL\033[0m   \t", list(turns), "\t\t----"
            all_turns_file.write(str(counter)+"\t\tDL\t"+str(list(turns))+"\t\t-----""\n")
        del shmu
        del noc_rg
    all_turns_file.write("---------------------------"+"\n")
    all_turns_file.write("Number of turn models with deadlock: "+str(deadlock_counter)+"\n")
    all_turns_file.write("Number of turn models without deadlock: "+str(deadlock_free_counter)+"\n")
    all_turns_file.write("=========================================="+"\n")
    all_turns_file.close()
    return None


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
        if networkx.is_directed_acyclic_graph(noc_rg):
            connectivity_metric = Calculate_Reachability.reachability_metric(ag, noc_rg, False)
            deadlock_free_counter += 1
            print counter, "\t \033[92mDF\033[0m \t", list(turns), "\t\t", connectivity_metric
            all_turns_file.write(str(counter)+"\t\tDF\t"+str(list(turns))+"\t\t"+str(connectivity_metric)+"\n")
        else:
            deadlock_counter += 1
            print counter, "\t \033[31mDL\033[0m   \t", list(turns), "\t\t----"
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

    print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        counter += 1
        print counter, "\t\t", list(turns)
        all_turns_file.write(str(counter)+"\t\t"+str(list(turns))+"\n")
    all_turns_file.close()
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

    print "Number of Turns:", combination
    for turns in itertools.combinations(turn_model_list, combination):
        counter += 1
        print counter, "\t\t", list(turns)
        all_turns_file.write(str(counter)+"\t\t"+str(list(turns))+"\n")
    all_turns_file.close()
    return None


def check_fault_tolerance_of_routing_algs(dimension, number_of_multi_threads, viz):
    if dimension == '2D':
        Config.ag.topology = '2DMesh'
        Config.ag.z_size = 1
        args = list(range(0, 25))
        turn_model_list = all_2d_turn_model_package.all_2d_turn_models
        viz_2d_turn_model()
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

    Config.UsedTurnModel = copy.deepcopy(turn_model)
    Config.TurnsHealth = copy.deepcopy(Config.setup_turns_health())

    ag = copy.deepcopy(AG_Functions.generate_ag(report=False))

    turn_model_name = Routing.return_turn_model_name(Config.UsedTurnModel)

    file_name = str(turn_model_name)+'_eval'
    turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+file_name+'.txt', 'a+')
    if viz:
        file_name_viz = str(turn_model_name)+'_eval_'+str(len(ag.edges())-combination)
        turn_model_eval_viz_file = open('Generated_Files/Internal/'+file_name_viz+'.txt', 'w')
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
        connectivity_metric = Calculate_Reachability.reachability_metric(ag, noc_rg, False)
        counter += 1
        metric_sum += connectivity_metric
        std = None
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
        print "#:"+str(counter)+"\t\tC.M.:"+str(connectivity_metric)+"\t\t avg:", \
            float(metric_sum)/counter, "\t\tstd:", std
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


def report_3d_turn_model_fault_tolerance(turn_model, combination, viz):

    Config.UsedTurnModel = copy.deepcopy(turn_model)
    Config.TurnsHealth = copy.deepcopy(Config.setup_turns_health())

    ag = copy.deepcopy(AG_Functions.generate_ag(report=False))

    turn_model_name = Routing.return_turn_model_name(Config.UsedTurnModel)

    file_name = str(turn_model_name)+'_eval'
    turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+file_name+'.txt', 'a+')
    if viz:
        file_name_viz = str(turn_model_name)+'_eval_'+str(len(ag.edges())-combination)
        turn_model_eval_viz_file = open('Generated_Files/Internal/'+file_name_viz+'.txt', 'w')
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
        connectivity_metric = Calculate_Reachability.reachability_metric(ag, noc_rg, False)
        counter += 1
        metric_sum += connectivity_metric
        std = None
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
        if counter == number_of_combinations:
            del shmu
            del noc_rg
            break
        if viz:
            turn_model_eval_viz_file.write(str(float(metric_sum)/counter)+"\n")
        print "#:"+str(counter)+"\t\tC.M.:"+str(connectivity_metric)+"\t\t avg:", \
            float(metric_sum)/counter, "\t\tstd:", std
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


def viz_turn_model_evaluation(cost_file_name):
    """
    Visualizes the cost of solutions during local search mapping optimization process
    :param cost_file_name: Name of the Cost File (Holds values of cost function for different mapping steps)
    :return: None
    """
    print ("===========================================")
    print ("GENERATING TURN MODEL EVALUATION VISUALIZATIONS...")
    print 'READING Generated_Files/Internal/'+cost_file_name+'.txt'
    fig, ax1 = plt.subplots()
    try:
        viz_file = open('Generated_Files/Internal/'+cost_file_name+'.txt', 'r')
        con_metric = []
        line = viz_file.readline()
        con_metric.append(float(line))
        while line != "":
            con_metric.append(float(line))
            line = viz_file.readline()
        solution_num = range(0, len(con_metric))
        viz_file.close()

        ax1.set_ylabel('Connectivity Metric')
        ax1.set_xlabel('time')
        ax1.plot(solution_num, con_metric, '#5095FD')

    except IOError:
        print ('CAN NOT OPEN', cost_file_name+'.txt')

    plt.savefig("GraphDrawings/"+str(cost_file_name)+".png", dpi=300)
    print ("\033[35m* VIZ::\033[0m Turn Model Evaluation " +
           "GRAPH CREATED AT: GraphDrawings/"+str(cost_file_name)+".png")
    plt.clf()
    plt.close(fig)
    return None


def viz_all_turn_models_against_each_other():
    print ("===========================================")
    print ("GENERATING TURN MODEL EVALUATION VISUALIZATIONS...")
    fig = plt.figure()

    ax1 = plt.subplot(111)
    turn_model_eval_directory = "Generated_Files/Turn_Model_Eval"
    file_list = [txt_file for txt_file in os.listdir(turn_model_eval_directory) if txt_file.endswith(".txt")]
    counter = 0
    for txt_file in file_list:
        viz_file = open(turn_model_eval_directory+"/"+txt_file, 'r')
        line = viz_file.readline()
        value_list = []
        while line != "":
            value = line.split()
            value_list.append(float(value[1]))
            line = viz_file.readline()
        index_list = range(0, len(value_list))
        viz_file.close()
        value_list = sorted(value_list)
        random.seed(counter)
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        color = '#%02X%02X%02X' % (r, g, b)
        file_name = txt_file.split("_")
        ax1.plot(index_list, value_list, color, label=str(file_name[1]))
        counter += 1
    lgd = ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=3)
    ax1.grid('on')
    plt.savefig("GraphDrawings/Turn_Models_Fault_Tolerance_Eval.png", bbox_extra_artists=(lgd,),
                bbox_inches='tight', dpi=300)
    plt.clf()
    plt.close(fig)
    print ("\033[35m* VIZ::\033[0m Turn Model Evaluation " +
           "GRAPH CREATED AT: GraphDrawings/Turn_Models_Fault_Tolerance_Eval.png")
    return None


def viz_2d_turn_model():
    fig = plt.figure(figsize=(19, 12))
    count = 1
    for turn_model in all_2d_turn_model_package.all_2d_turn_models:
        ax1 = plt.subplot(7, 8, count)
        if "E2S" in turn_model:
            ax1.annotate("",
                         xy=(0, 0.5), xycoords='data',
                         xytext=(0.2, 0.7), textcoords='data',
                         size=20,
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="angle, angleA=0, angleB=90, rad=0")
                         )
        if "S2W" in turn_model:
            ax1.annotate("",
                         xy=(0.2, 0.7), xycoords='data',
                         xytext=(0.4, 0.5), textcoords='data',
                         size=20,
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="angle, angleA=90, angleB=0, rad=0")
                         )
        if "N2E" in turn_model:
            ax1.annotate("",
                         xy=(0.2, 0.3), xycoords='data',
                         xytext=(0.0, 0.5), textcoords='data',
                         size=20,
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="angle, angleA=90, angleB=0, rad=0")
                         )
        if "W2N" in turn_model:
            ax1.annotate("",
                         xy=(0.4, 0.5), xycoords='data',
                         xytext=(0.2, 0.3), textcoords='data',
                         size=20,
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="angle, angleA=0, angleB=90, rad=0")
                         )
        # #######################
        if "S2E" in turn_model:
            ax1.annotate("",
                         xy=(0.75, 0.7), xycoords='data',
                         xytext=(0.55, 0.5), textcoords='data',
                         size=20,
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="angle, angleA=90, angleB=0, rad=0")
                         )
        if "W2S" in turn_model:
            ax1.annotate("",
                         xy=(0.95, 0.5), xycoords='data',
                         xytext=(0.75, 0.7), textcoords='data',
                         size=20,
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="angle, angleA=0, angleB=90, rad=0")
                         )
        if "E2N" in turn_model:
            ax1.annotate("",
                         xy=(0.55, 0.5), xycoords='data',
                         xytext=(0.75, 0.3), textcoords='data',
                         size=20,
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="angle, angleA=180, angleB=90, rad=0")
                         )
        if "N2W" in turn_model:
            ax1.annotate("",
                         xy=(0.75, 0.3), xycoords='data',
                         xytext=(0.95, 0.5), textcoords='data',
                         size=20,
                         arrowprops=dict(arrowstyle="->",
                                         connectionstyle="angle, angleA=90, angleB=0, rad=0")
                         )
        ax1.text(0, 0.8, str(turn_model), fontsize=5)
        count += 1
        ax1.axis('off')
    plt.axis('off')
    plt.savefig("GraphDrawings/Turn_Model.png", dpi=300, bbox_inches='tight')
    plt.clf()
    plt.close(fig)
    # print ("\033[35m* VIZ::\033[0m Turn Model viz " +
    #       "TURN MODEL VIZ CREATED AT: GraphDrawings/Turn_Model_"+turn_model_name+".png")
    return None