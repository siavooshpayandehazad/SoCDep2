# Copyright (C) Siavoosh Payandeh Azad

from ConfigAndPackages import Config
from ArchGraphUtilities.AG_Functions import return_node_number, return_node_location
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


def find_feasible_ag_vertical_link_placement(shmu):
    """
    generates a feasible vertical link placement
    :param shmu: system health monitoring unit
    :return: list of vertical links
    """
    new_vertical_link_lists = []
    for i in range(0, Config.vl_opt.vl_num):
        source_node, destination_node = place_a_random_vl(shmu)
        new_vertical_link_lists.append((source_node, destination_node))
    return new_vertical_link_lists


def place_a_random_vl(shmu):
    """
    finds a random vl to restore
    :param shmu: system health monitoring unit
    :return: tuple of source node and destination node of the chosen vertical link
    """
    # todo: we can make this function better by finding all broken VLs and choosing randomly one from the list
    # the function is: find_all_broken_vls it has to be integrated

    # choose a random source node
    source_x = random.randint(0, Config.ag.x_size-1)
    source_y = random.randint(0, Config.ag.y_size-1)
    source_z = random.randint(0, Config.ag.z_size-1)
    source_node = return_node_number(source_x, source_y, source_z)
    # find possibility of having up or down link
    possible_z = []
    if source_z+1 <= Config.ag.z_size-1:
        possible_z.append(source_z+1)
    if 0 <= source_z-1:
        possible_z.append(source_z-1)
    # find destination node
    destination_node = return_node_number(source_x, source_y, random.choice(possible_z))
    # check if the chosen node is HEALTHY, meaning that it is in place! if so, find another link
    while shmu.SHM.edge[source_node][destination_node]['LinkHealth']:
        source_x = random.randint(0, Config.ag.x_size-1)
        source_y = random.randint(0, Config.ag.y_size-1)
        source_z = random.randint(0, Config.ag.z_size-1)
        source_node = return_node_number(source_x, source_y, source_z)
        possible_z = []
        if source_z + 1 <= Config.ag.z_size-1:
            possible_z.append(source_z+1)
        if 0 <= source_z-1:
            possible_z.append(source_z-1)
        destination_node = return_node_number(source_x, source_y, random.choice(possible_z))
    # here we have a candidate to restore
    shmu.restore_broken_link((source_node, destination_node), False)
    return source_node, destination_node


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


def move_to_new_vertical_link_configuration(shmu, vertical_link_lists):
    """
    Takes a vertical link configuration and moves to a neighbor solution
    :param shmu: systme health monitoring unit
    :param vertical_link_lists: current list of vertical links
    :return: new list of vertical links
    """
    new_vertical_link_lists = copy.deepcopy(vertical_link_lists)
    chosen_link_to_fix = random.choice(new_vertical_link_lists)
    new_vertical_link_lists.remove(chosen_link_to_fix)
    shmu.break_link(chosen_link_to_fix, False)

    source_node, destination_node = place_a_random_vl(shmu)
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