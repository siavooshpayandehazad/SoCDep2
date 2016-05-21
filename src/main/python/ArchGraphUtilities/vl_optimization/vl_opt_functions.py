# Copyright (C) Siavoosh Payandeh Azad

from ConfigAndPackages import Config
from ArchGraphUtilities.AG_Functions import return_node_location
from RoutingAlgorithms import Calculate_Reachability
import random
import copy


def find_all_vertical_links(ag):
    """
    returns a list of all the vertical links possible in AG
    :param ag: architecture graph
    :return: list of all vertical links
    """
    vertical_link_list = []
    for link in ag.edges():
        # if these nodes are on different layers
        if return_node_location(link[0])[2] != return_node_location(link[1])[2]:
            if link not in vertical_link_list:
                vertical_link_list.append(link)
    return vertical_link_list


def remove_all_vertical_links(shmu, ag):
    """
    Finds all vertical links and sets them as faulty in shm
    :param shmu: system health monitoring unit
    :param ag: architecture graph
    :return: None
    """
    vertical_link_list = find_all_vertical_links(ag)
    for v_link in vertical_link_list:
        shmu.break_link(v_link, False)
    return None


def find_feasible_ag_vertical_link_placement(ag, shmu):
    """
    generates a feasible vertical link placement
    :param ag: architecture graph
    :param shmu: system health monitoring unit
    :return: list of vertical links
    """
    new_vertical_link_lists = []
    for i in range(0, Config.vl_opt.vl_num):
        source_node, destination_node = place_a_random_vl(ag, shmu)
        new_vertical_link_lists.append((source_node, destination_node))
    return new_vertical_link_lists


def place_a_random_vl(ag, shmu):
    """
    finds a random vl to restore
    :param ag: architecture graph
    :param shmu: system health monitoring unit
    :return: tuple of source node and destination node of the chosen vertical link
    """

    all_broken_vls = find_all_broken_vls(ag, shmu.SHM)
    if len(all_broken_vls) > 0:
        random.shuffle(all_broken_vls)
        link = random.choice(all_broken_vls)
    else:
        raise ValueError("no broken link to restore!")
    if shmu.SHM.edge[link[0]][link[1]]['LinkHealth']:
        raise ValueError("can not restore healthy link")
    shmu.restore_broken_link(link, False)

    return link[0], link[1]


def find_all_broken_vls(ag, shm):
    """
    Returns a list of all broken VLs in the Architecture Graph
    :param ag: architecture graph
    :param shm: system health map
    :return: list of broken vertical links
    """
    list_of_broken_vls = []
    all_vertical_links = find_all_vertical_links(ag)
    for link in all_vertical_links:
        if not shm.edge[link[0]][link[1]]['LinkHealth']:
            list_of_broken_vls.append(link)
    # print len(list_of_broken_vls)
    return list_of_broken_vls


def return_to_solution(ag, shmu, vertical_link_list):
    """
    Takes a list of vertical links and applies this configuration to the system. used for moving back
    to an old solution
    :param ag: architecture graph
    :param shmu: system health monitoring unit
    :param vertical_link_list: list of vertical links to be placed
    :return: None
    """
    remove_all_vertical_links(shmu, ag)
    for link in vertical_link_list:
        shmu.restore_broken_link(link, False)
    return None


def move_to_new_vertical_link_configuration(ag, shmu, vertical_link_lists):
    """
    Takes a vertical link configuration and moves to a neighbor solution
    :param ag: architecture graph
    :param shmu: systme health monitoring unit
    :param vertical_link_lists: current list of vertical links
    :return: new list of vertical links
    """
    new_vertical_link_lists = copy.deepcopy(vertical_link_lists)
    chosen_link_to_fix = random.choice(new_vertical_link_lists)
    new_vertical_link_lists.remove(chosen_link_to_fix)
    shmu.break_link(chosen_link_to_fix, False)

    source_node, destination_node = place_a_random_vl(ag, shmu)
    new_vertical_link_lists.append((source_node, destination_node))
    return new_vertical_link_lists


def cleanup_ag(ag, shmu):
    """
    removes the physical links in AG based on information in SHM
    :param ag: architecture graph
    :param shmu: system health monitoring unit
    :return:
    """
    for link in shmu.SHM.edges():
        if not shmu.SHM.edge[link[0]][link[1]]['LinkHealth']:
            ag.remove_edge(link[0], link[1])
    return None


def vl_cost_function(ag, routing_graph):
    """
    returns cost of the current vertical link placement
    :param ag: architecture graph
    :param routing_graph: routing graph
    :return: cost of the current vl placement
    """
    return Calculate_Reachability.reachability_metric(ag, routing_graph, False)