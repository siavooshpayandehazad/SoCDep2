# Copyright (C) 2015 Siavoosh Payandeh Azad 

import random
import copy
from ConfigAndPackages import Config
import networkx
# from Clustering_Functions import remove_task_from_ctg
from Clustering_Functions import add_task_to_ctg, clear_clustering, \
    ctg_cost_function, remove_empty_clusters, ctg_opt_move
from Clustering_Test import double_check_ctg
from Clustering_Reports import report_ctg


def generate_ctg(num_of_clusters):
    """
    Generates a clustered task graph without any edges or tasks assigned to clusters.
    the number of clusters should be the same as the number of nodes in Architecture graph.
    :param num_of_clusters: Number of clusters to be generated
    :return: Empty Clustered Task Graph
    """
    print ("===========================================")
    print ("PREPARING FOR CLUSTERING THE TASK GRAPH...")
    print ("   NUMBER OF CLUSTERS: "+str(num_of_clusters))
    ctg = networkx.DiGraph()
    for i in range(0, num_of_clusters):
        ctg.add_node(i, TaskList=[], Node=None, Utilization=0, Criticality='L')
    print ("CLUSTERS GENERATED...")
    return ctg


def gen_transparent_clusters(tg):
    print ("===========================================")
    print ("PREPARING FOR CLUSTERING THE TASK GRAPH...")
    print ("   NUMBER OF CLUSTERS: "+str(len(tg.nodes())))
    ctg = networkx.DiGraph()
    for i in range(0, len(tg.nodes())):
        ctg.add_node(i, TaskList=[], Node=None, Utilization=0,
                     Criticality='L')
    for task_id in tg.nodes():
        add_task_to_ctg(tg, ctg, task_id, task_id)
    report_ctg(ctg, "CTG.png")
    return ctg



def initial_clustering(tg, ctg):
    """
    Randomly assign the tasks to clusters to make the initial solution for optimization...
    :param tg: Task Graph
    :param ctg: Clustered Task Graph
    :return: True if successful, False otherwise
    """
    print ("===========================================")
    print ("STARTING INITIAL CLUSTERING...")

    if Config.clustering.random_seed is not None:
        print "RANDOM SEED: ", Config.clustering.random_seed
        random.seed(Config.clustering.random_seed)
    else:
        print "RANDOM SEED SET TO NONE!"
        random.seed(None)

    for task in tg.nodes():
        iteration = 0
        destination_cluster = random.choice(ctg.nodes())
        while not add_task_to_ctg(tg, ctg, task, destination_cluster):
            # remove_task_from_ctg(TG,CTG,Task)
            iteration += 1
            destination_cluster = random.choice(ctg.nodes())
            if iteration == 10*len(ctg.nodes()):
                clear_clustering(tg, ctg)
                return False
    # double_check_ctg(TG,CTG)
    print ("INITIAL CLUSTERED TASK GRAPH (CTG) READY...")
    report_ctg(ctg, "CTG_Initial.png")
    return True


def ctg_opt_local_search(tg, ctg, num_of_iter, logging):
    """
    Local Search optimization for reducing the cost of a clustering solution
    :param tg: Task Graph
    :param ctg: Clustered Task Graph
    :param num_of_iter: Number of iterations for local search
    :return: best answer (CTG) found by the search
    """
    clustering_cost_file = open('Generated_Files/Internal/ClusteringCost.txt', 'w')
    print ("===========================================")
    print ("STARTING LOCAL SEARCH OPTIMIZATION FOR CTG...")
    cost = ctg_cost_function(ctg)
    starting_cost = cost
    clustering_cost_file.write(str(cost)+"\n")
    best_solution = copy.deepcopy(ctg)
    best_tg = copy.deepcopy(tg)
    print ("\tINITIAL COST: "+str(cost))
    # choose a random task from TG
    for i in range(0, num_of_iter):

        # print ("\tITERATION:",i)
        if Config.TestMode:
            double_check_ctg(tg, ctg)
        # Make a move!
        ctg_opt_move(tg, ctg, i, logging)
        new_cost = ctg_cost_function(ctg)
        clustering_cost_file.write(str(new_cost)+"\n")
        if new_cost <= cost:
            if new_cost < cost:
                print ("\033[32m* NOTE::\033[0mBETTER SOLUTION FOUND WITH COST:\t" +
                       str(new_cost)+"\t\tIteration #:"+str(i))
            best_solution = copy.deepcopy(ctg)
            best_tg = copy.deepcopy(tg)
            cost = new_cost
        else:
            ctg = copy.deepcopy(best_solution)
            tg = copy.deepcopy(best_tg)
    clustering_cost_file.close()
    remove_empty_clusters(best_solution)
    # double_check_ctg(best_tg, best_solution)
    print ("-------------------------------------")
    print ("STARTING COST:"+str(starting_cost)+"\tFINAL COST: "+str(cost)+"\tAFTER "+str(num_of_iter)+" ITERATIONS")
    print ("IMPROVEMENT:"+str("{0:.2f}".format(100*(starting_cost-cost)/starting_cost))+" %")
    return best_solution, best_tg