# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import Config
import random
import SHMU_Reports
from RoutingAlgorithms import Routing


def apply_initial_faults(shm):
        for broken_link in Config.ListOfBrokenLinks:
            shm.break_link(broken_link, True)

        for router_with_broken_turn in Config.ListOfBrokenTurns:
            shm.break_turn(router_with_broken_turn, Config.ListOfBrokenTurns[router_with_broken_turn], True)

        for aged_pe in Config.ListOfAgedPEs:
            shm.introduce_aging(aged_pe, Config.ListOfAgedPEs[aged_pe], True)

        for broken_node in Config.ListOfBrokenPEs:
            shm.break_node(broken_node, True)


def random_fault_generation(shm):
    """

    :param shm: System Health Map
    :return:
    """
    location_choices = []
    if Config.enable_link_counters:
        location_choices.append('Link')
    if Config.enable_pe_counters:
        location_choices.append('Node')
    if Config.enable_router_counters:
        location_choices.append('Turn')

    chosen_fault = random.choice(location_choices)
    # Todo: fix the distribution of fault types
    # FaultTypes = ['T','T','T','T','T','P']
    fault_types = ['T']
    random.seed(None)
    fault_type = random.choice(fault_types)
    if chosen_fault == 'Link':
        chosen_link = random.choice(shm.edges())
        while not shm.edge[chosen_link[0]][chosen_link[1]]['LinkHealth']:
            chosen_link = random.choice(shm.edges())
        return chosen_link, fault_type

    elif chosen_fault == 'Turn':
        chosen_node = random.choice(shm.nodes())
        chosen_turn = random.choice(shm.node[chosen_node]['TurnsHealth'].keys())
        while chosen_turn not in Config.UsedTurnModel:
            chosen_turn = random.choice(shm.node[chosen_node]['TurnsHealth'].keys())
        return {chosen_node: chosen_turn}, fault_type
    elif chosen_fault == 'Node':
        chosen_node = random.choice(shm.nodes())
        return chosen_node, fault_type


def generate_fault_config(shmu):
    """
    Generates a string (fault_config) from the configuration of the faults in the SHM
    :param shmu: System Health Monitoring Unit
    :return: fault_config string
    """
    fault_config = ""
    for node in shmu.SHM.nodes():
        fault_config += str(node)
        fault_config += "T" if shmu.SHM.node[node]['NodeHealth'] else "F"
        fault_config += str(int(shmu.SHM.node[node]['NodeSpeed']))
        for Turn in shmu.SHM.node[node]['TurnsHealth']:
            fault_config += "T" if shmu.SHM.node[node]['TurnsHealth'][Turn] else "F"
    return fault_config


def apply_fault_event(ag, shmu, noc_rg, fault_location, fault_type):
        SHMU_Reports.report_the_event(fault_location, fault_type)
        if type(fault_location) is tuple:      # its a Link fault
            if fault_type == 'T':    # Transient Fault
                if shmu.SHM.edge[fault_location[0]][fault_location[1]]['LinkHealth']:
                    shmu.break_link(fault_location, True)
                    shmu.restore_broken_link(fault_location, True)
                else:
                    print ("\033[33mSHM:: NOTE:\033[0mLINK ALREADY BROKEN")
            elif fault_type == 'P':   # Permanent Fault
                port = ag.edge[fault_location[0]][fault_location[1]]['Port']
                from_port = str(fault_location[0])+str(port[0])+str('O')
                to_port = str(fault_location[1])+str(port[1])+str('I')
                shmu.break_link(fault_location, True)
                Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'REMOVE')
        elif type(fault_location) is dict:   # its a Turn fault
            current_node = fault_location.keys()[0]
            current_turn = fault_location[current_node]
            if fault_type == 'T':    # Transient Fault
                if shmu.SHM.node[current_node]['TurnsHealth'][current_turn]:   # check if the turn is actually working
                    shmu.break_turn(current_node, current_turn, True)
                    shmu.restore_broken_turn(current_node, current_turn, True)
                else:
                    print ("\033[33mSHM:: NOTE:\033[0mTURN ALREADY BROKEN")
            elif fault_type == 'P':   # Permanent Fault
                from_port = str(current_node)+str(current_turn[0])+str('I')
                to_port = str(current_node)+str(current_turn[2])+str('O')
                Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'REMOVE')
                shmu.break_turn(current_node, current_turn, True)
        else:           # its a Node fault
            if fault_type == 'T':    # Transient Fault
                if shmu.SHM.node[fault_location]['NodeHealth']:
                    shmu.break_node(fault_location, True)
                    shmu.restore_broken_node(fault_location, True)
                else:
                    print ("\033[33mSHM:: NOTE:\033[0m NODE ALREADY BROKEN")
            elif fault_type == 'P':   # Permanent Fault
                shmu.break_node(fault_location, True)
        return None
