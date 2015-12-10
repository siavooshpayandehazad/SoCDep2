# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import Config
import random
import SHMU_Reports
from RoutingAlgorithms import Routing


def ApplyInitialFaults(SHM):
        for BrokenLink in Config.ListOfBrokenLinks:
            SHM.break_link(BrokenLink, True)

        for NodeWithBrokenTurn in Config.ListOfBrokenTurns:
            SHM.break_turn(NodeWithBrokenTurn, Config.ListOfBrokenTurns[NodeWithBrokenTurn], True)

        for AgedPE in Config.ListOfAgedPEs:
            SHM.introduce_aging(AgedPE, Config.ListOfAgedPEs[AgedPE], True)

        for BrokenNode in Config.ListOfBrokenPEs:
            SHM.break_node(BrokenNode, True)


def RandomFaultGeneration(SHM):
    """

    :param SHM: System Health Map
    :return:
    """
    ChosenFault = random.choice(['Link', 'Turn', 'Node'])
    # Todo: fix the distribution of fault types
    # FaultTypes = ['T','T','T','T','T','P']
    FaultTypes = ['T']
    FaultType = random.choice(FaultTypes)
    if ChosenFault == 'Link':
        ChosenLink = random.choice(SHM.edges())
        return ChosenLink, FaultType
    elif ChosenFault == 'Turn':
        ChosenNode = random.choice(SHM.nodes())
        ChosenTurn = random.choice(SHM.node[ChosenNode]['TurnsHealth'].keys())
        while not ChosenTurn in Config.UsedTurnModel:
            ChosenTurn = random.choice(SHM.node[ChosenNode]['TurnsHealth'].keys())
        return {ChosenNode: ChosenTurn}, FaultType
    elif ChosenFault == 'Node':
        ChosenNode = random.choice(SHM.nodes())
        return ChosenNode, FaultType


def GenerateFaultConfig (SHMU):
    """
    Generates a string (FaultConfig) from the configuration of the faults in the SHM
    :return: FaultConfig string
    """
    FaultConfig = ""
    for node in SHMU.SHM.nodes():
        FaultConfig += str(node)
        FaultConfig += "T" if SHMU.SHM.node[node]['NodeHealth'] else "F"
        FaultConfig += str(int(SHMU.SHM.node[node]['NodeSpeed']))
        for Turn in SHMU.SHM.node[node]['TurnsHealth']:
            FaultConfig += "T" if SHMU.SHM.node[node]['TurnsHealth'][Turn] else "F"
    return FaultConfig


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
