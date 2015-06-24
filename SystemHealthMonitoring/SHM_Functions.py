# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import Config
import random
import SHM_Reports

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
    # Todo: fix the distribution of fault types
    FaultTypes = ['T','T','T','T','T','P']
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

def ApplyFaultEvent(SHM, FaultLocation, FaultType):
        SHM_Reports.ReportTheEvent(FaultLocation, FaultType)
        if type(FaultLocation) is tuple:      # its a Link fault
            if FaultType == 'T':    # Transient Fault
                if SHM.SHM.edge[FaultLocation[0]][FaultLocation[1]]['LinkHealth']:
                    SHM.BreakLink(FaultLocation, True)
                    SHM.RestoreBrokenLink(FaultLocation, True)
                else:
                    print "\033[33mSHM:: NOTE:\033[0mLINK ALREADY BROKEN"
            elif FaultType == 'P':   # Permanent Fault
                SHM.BreakLink(FaultLocation, True)
        elif type(FaultLocation) is dict:   # its a Turn fault
            if FaultType == 'T':    # Transient Fault
                if SHM.SHM.node[FaultLocation.keys()[0]]['TurnsHealth'][FaultLocation[FaultLocation.keys()[0]]]:
                    SHM.BreakTurn(FaultLocation.keys()[0], FaultLocation[FaultLocation.keys()[0]], True)
                    SHM.RestoreBrokenTurn(FaultLocation.keys()[0], FaultLocation[FaultLocation.keys()[0]], True)
                else:
                    print "\033[33mSHM:: NOTE:\033[0mTURN ALREADY BROKEN"
            elif FaultType == 'P':   # Permanent Fault
                SHM.BreakTurn(FaultLocation.keys()[0], FaultLocation[FaultLocation.keys()[0]], True)
        else:           # its a Node fault
            if FaultType == 'T':    # Transient Fault
                if SHM.SHM.node[FaultLocation]['NodeHealth']:
                    SHM.BreakNode(FaultLocation, True)
                    SHM.RestoreBrokenNode(FaultLocation, True)
                else:
                    print "\033[33mSHM:: NOTE:\033[0m NODE ALREADY BROKEN"
            elif FaultType == 'P':   # Permanent Fault
                SHM.BreakNode(FaultLocation, True)
        return None
