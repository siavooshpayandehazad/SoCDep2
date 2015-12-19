# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import Config
import random
import SHMU_Reports
from RoutingAlgorithms import Routing


def ApplyInitialFaults(shm):
        for broken_link in Config.ListOfBrokenLinks:
            shm.break_link(broken_link, True)

        for router_with_broken_turn in Config.ListOfBrokenTurns:
            shm.break_turn(router_with_broken_turn, Config.ListOfBrokenTurns[router_with_broken_turn], True)

        for aged_pe in Config.ListOfAgedPEs:
            shm.introduce_aging(aged_pe, Config.ListOfAgedPEs[aged_pe], True)

        for broken_node in Config.ListOfBrokenPEs:
            shm.break_node(broken_node, True)


def RandomFaultGeneration(shm):
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

    ChosenFault = random.choice(location_choices)
    # Todo: fix the distribution of fault types
    # FaultTypes = ['T','T','T','T','T','P']
    FaultTypes = ['T']
    random.seed(None)
    FaultType = random.choice(FaultTypes)
    if ChosenFault == 'Link':
        ChosenLink = random.choice(shm.edges())
        return ChosenLink, FaultType
    elif ChosenFault == 'Turn':
        ChosenNode = random.choice(shm.nodes())
        ChosenTurn = random.choice(shm.node[ChosenNode]['TurnsHealth'].keys())
        while not ChosenTurn in Config.UsedTurnModel:
            ChosenTurn = random.choice(shm.node[ChosenNode]['TurnsHealth'].keys())
        return {ChosenNode: ChosenTurn}, FaultType
    elif ChosenFault == 'Node':
        ChosenNode = random.choice(shm.nodes())
        return ChosenNode, FaultType


def GenerateFaultConfig(shmu):
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


def apply_fault_event(AG, SHMU, NoCRG, FaultLocation, FaultType):
        SHMU_Reports.ReportTheEvent(FaultLocation, FaultType)
        if type(FaultLocation) is tuple:      # its a Link fault
            if FaultType == 'T':    # Transient Fault
                if SHMU.SHM.edge[FaultLocation[0]][FaultLocation[1]]['LinkHealth']:
                    SHMU.break_link(FaultLocation, True)
                    SHMU.restore_broken_link(FaultLocation, True)
                else:
                    print ("\033[33mSHM:: NOTE:\033[0mLINK ALREADY BROKEN")
            elif FaultType == 'P':   # Permanent Fault
                Port = AG.edge[FaultLocation[0]][FaultLocation[1]]['Port']
                FromPort = str(FaultLocation[0])+str(Port[0])+str('O')
                ToPort = str(FaultLocation[1])+str(Port[1])+str('I')
                Routing.UpdateNoCRouteGraph(NoCRG, FromPort, ToPort, 'REMOVE')
                SHMU.break_link(FaultLocation, True)
        elif type(FaultLocation) is dict:   # its a Turn fault
            CurrentNode = FaultLocation.keys()[0]
            CurrentTurn = FaultLocation[CurrentNode]
            if FaultType == 'T':    # Transient Fault
                if SHMU.SHM.node[CurrentNode]['TurnsHealth'][CurrentTurn]:   # check if the turn is actually working
                    SHMU.break_turn(CurrentNode, CurrentTurn, True)
                    SHMU.restore_broken_turn(CurrentNode, CurrentTurn, True)
                else:
                    print ("\033[33mSHM:: NOTE:\033[0mTURN ALREADY BROKEN")
            elif FaultType == 'P':   # Permanent Fault
                FromPort = str(CurrentNode)+str(CurrentTurn[0])+str('I')
                ToPort = str(CurrentNode)+str(CurrentTurn[2])+str('O')
                Routing.UpdateNoCRouteGraph(NoCRG, FromPort, ToPort, 'REMOVE')
                SHMU.break_turn(CurrentNode, CurrentTurn, True)
        else:           # its a Node fault
            if FaultType == 'T':    # Transient Fault
                if SHMU.SHM.node[FaultLocation]['NodeHealth']:
                    SHMU.break_node(FaultLocation, True)
                    SHMU.restore_broken_node(FaultLocation, True)
                else:
                    print ("\033[33mSHM:: NOTE:\033[0m NODE ALREADY BROKEN")
            elif FaultType == 'P':   # Permanent Fault
                SHMU.break_node(FaultLocation, True)
        return None
