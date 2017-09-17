# Copyright (C) 2015 Siavoosh Payandeh Azad
from networkx import all_simple_paths, all_shortest_paths, is_directed_acyclic_graph, find_cycle
from Calculate_Reachability import is_destination_reachable_from_source
from ConfigAndPackages import PackageFile, all_2d_turn_model_package
from ArchGraphUtilities.AG_Functions import manhattan_distance

def extended_degree_of_adaptiveness(ag, noc_rg, report):
    """
    :param ag: architecture graph
    :param noc_rg: NoC routing graph
    :param report: report switch
    :return: reachability metric
    """
    if report:
        print ("=====================================")
        print ("CALCULATING REACH-ABILITY METRIC OF THE CURRENT ROUTING ALGORITHM UNDER CURRENT FAULT CONFIG")
    reachability_counter = 0
    for source_node in ag.nodes():
        for destination_node in ag.nodes():
            if source_node != destination_node:
                if is_destination_reachable_from_source(noc_rg, source_node, destination_node):
                    reachability_counter += len(list(all_simple_paths(noc_rg,
                                                str(source_node)+str('L')+str('I'),
                                                str(destination_node)+str('L')+str('O'))))
    r_metric = float(reachability_counter)
    if report:
        print ("REACH-ABILITY METRIC: "+str(r_metric))
    return r_metric


def degree_of_adaptiveness(ag, noc_rg, report):
    """
    :param ag: architecture graph
    :param noc_rg: NoC routing graph
    :param report: report switch
    :return: reachability metric
    """
    if report:
        print ("=====================================")
        print ("CALCULATING REACH-ABILITY METRIC OF THE CURRENT ROUTING ALGORITHM UNDER CURRENT FAULT CONFIG")
    reachability_counter = 0
    for source_node in ag.nodes():
        for destination_node in ag.nodes():
            if source_node != destination_node:
                if is_destination_reachable_from_source(noc_rg, source_node, destination_node):
                    for path in  all_shortest_paths(noc_rg, str(source_node)+str('L')+str('I'),
                                                    str(destination_node)+str('L')+str('O')):
                        if (len(path)/2)-1 <= manhattan_distance(source_node, destination_node):
                            reachability_counter += 1

    r_metric = float(reachability_counter)
    if report:
        print ("REACH-ABILITY METRIC: "+str(r_metric))
    return r_metric


def check_deadlock_freeness(noc_rg):
    """
    Checks if routing graph is a directed acyclic graph which would result
    in a deadlock-free routing algorithm
    :param noc_rg: NoC Routing Graph
    :return: True if noc_rg is deadlock free else False!
    """
    if is_directed_acyclic_graph(noc_rg):
        return True
    else:
        print  find_cycle(noc_rg, orientation='original')
        return False


def return_turn_model_name(turn_model):
    if turn_model in all_2d_turn_model_package.all_2d_turn_models:
        tm_index = all_2d_turn_model_package.all_2d_turn_models.index(turn_model)
        turn_model_name = str(tm_index)
    elif turn_model == PackageFile.XYZ_TurnModel:
        turn_model_name = '3d_XYZ'
    elif turn_model == PackageFile.NegativeFirst3D_TurnModel:
        turn_model_name = '3d_NegFirst'
    else:
        turn_model_name = None
    return turn_model_name
