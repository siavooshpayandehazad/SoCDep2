# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import Config
import random

def ApplyInitialFaults(SHM):
        for BrokenLink in Config.ListOfBrokenLinks:
            SHM.BreakLink(BrokenLink, True)

        for NodeWithBrokenTurn in Config.ListOfBrokenTurns:
            SHM.BreakTurn(NodeWithBrokenTurn, Config.ListOfBrokenTurns[NodeWithBrokenTurn], True)

        for AgedPE in Config.ListOfAgedPEs:
            SHM.IntroduceAging(AgedPE, Config.ListOfAgedPEs[AgedPE], True)

        for BrokenNode in Config.ListOfBrokenPEs:
            SHM.BreakNode(BrokenNode, True)

def RandomFaultGeneration(SHM):
    ChosenFault = random.choice(['Link', 'Turn', 'Node'])
    FaultTypes = ['T','P']
    FaultType = random.choice(FaultTypes)
    if ChosenFault == 'Link':
        ChosenLink = random.choice(SHM.SHM.edges())
        return ChosenLink, FaultType
    elif ChosenFault == 'Turn':
        ChosenNode = random.choice(SHM.SHM.nodes())
        ChosenTurn = random.choice(SHM.SHM.node[ChosenNode]['TurnsHealth'].keys())
        return {ChosenNode: ChosenTurn}, FaultType
    elif ChosenFault == 'Node':
        ChosenNode = random.choice(SHM.SHM.nodes())
        return ChosenNode, FaultType


def GenerateFaultConfig (SHM):
    """
    Generates a string (FaultConfig) from the configuration of the faults in the SHM
    :return: FaultConfig string
    """
    FaultConfig = ""
    for node in SHM.SHM.nodes():
        FaultConfig += str(node)
        FaultConfig += "T" if SHM.SHM.node[node]['NodeHealth'] else "F"
        FaultConfig += str(int(SHM.SHM.node[node]['NodeSpeed']))
        for Turn in SHM.SHM.node[node]['TurnsHealth']:
            FaultConfig += "T" if SHM.SHM.node[node]['TurnsHealth'][Turn] else "F"
    return FaultConfig