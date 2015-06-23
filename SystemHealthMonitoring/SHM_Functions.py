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

def RandomFaultInjection(SHM):
    ChosenFault = random.choice(['Link', 'Turn', 'PE', 'Age'])
    if ChosenFault == 'Link':
        ChosenLink = random.choice(SHM.SHM.edges())
        SHM.BreakLink(ChosenLink,True)
    elif ChosenFault == 'Turn':
        ChosenNode = random.choice(SHM.SHM.nodes())
        ChosenTurn = random.choice(SHM.SHM.node[ChosenNode]['TurnsHealth'].keys())
        SHM.BreakTurn(ChosenNode, ChosenTurn, True)
    elif ChosenFault == 'PE':
        ChosenNode = random.choice(SHM.SHM.nodes())
        SHM.BreakNode(ChosenNode, True)
    elif ChosenFault == 'Age':
        ChosenNode = random.choice(SHM.SHM.nodes())
        RandomSpeedDown = random.choice([0.3, 0.25, 0.2, 0.15, 0.1, 0.05])
        SHM.IntroduceAging(ChosenNode, RandomSpeedDown, True)