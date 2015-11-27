# Copyright (C) 2015 Siavoosh Payandeh Azad
import SystemHealthMonitoringUnit
from ConfigAndPackages import Config

def TestSHMU(AG):
    print ("===========================================")
    print ("STARTING SYSTEM HEALTH MAP TESTS...")
    SHMU4Test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
    SHMU4Test.SetUp_NoC_SystemHealthMap(AG, Config.TurnsHealth)
    TestBreaking(SHMU4Test)
    TestRestore(SHMU4Test)
    TestAging(SHMU4Test)
    # todo: needs more test etc...
    del SHMU4Test
    print ("ALL SHM TESTS PASSED...")
    return None


def TestBreaking(SHMU):
    for Node in SHMU.SHM.nodes():
        SHMU.BreakNode(Node, False)
        if SHMU.SHM.node[Node]['NodeHealth']:
            raise ValueError('SHM BreakNode DID NOT WORK FOR NODE', Node)
        for Turn in SHMU.SHM.node[Node]['TurnsHealth']:
            SHMU.BreakTurn(Node, Turn, False)
            if SHMU.SHM.node[Node]['TurnsHealth'][Turn]:
                raise ValueError('SHM BreakTurn DID NOT WORK FOR NODE:', Node, 'TURN:', Turn)
    for link in SHMU.SHM.edges():
        SHMU.BreakLink(link, False)
        if SHMU.SHM.edge[link[0]][link[1]]['LinkHealth']:
            raise ValueError('SHM BreakLink DID NOT WORK FOR LINK', link)
    print ("  - BREAKING TESTS PASSED...")


def TestRestore(SHMU):
    for Node in SHMU.SHM.nodes():
        SHMU.RestoreBrokenNode(Node, False)
        if not SHMU.SHM.node[Node]['NodeHealth']:
            raise ValueError('SHM RestoreBrokenNode DID NOT WORK FOR NODE', Node)
        for Turn in SHMU.SHM.node[Node]['TurnsHealth']:
            SHMU.RestoreBrokenTurn(Node, Turn, False)
            if not SHMU.SHM.node[Node]['TurnsHealth'][Turn]:
                raise ValueError('SHM RestoreBrokenTurn DID NOT WORK FOR NODE:', Node, 'TURN:', Turn)
    for link in SHMU.SHM.edges():
        SHMU.RestoreBrokenLink(link, False)
        if not SHMU.SHM.edge[link[0]][link[1]]['LinkHealth']:
            raise ValueError('SHM RestoreBrokenLink DID NOT WORK FOR LINK', link)
    print ("  - RESTORE TESTS PASSED...")


def TestAging(SHMU):
    for Node in SHMU.SHM.nodes():
        SHMU.IntroduceAging(Node, 0.5, False)
        if SHMU.SHM.node[Node]['NodeSpeed'] != 50:
            raise ValueError('SHM IntroduceAging DID NOT WORK FOR NODE', Node)
        SHMU.IntroduceAging(Node, 0.5, False)
        if SHMU.SHM.node[Node]['NodeSpeed'] != 25:
            raise ValueError('SHM IntroduceAging ROUND 2 DID NOT WORK FOR NODE', Node)
    print ("  - AGING TESTS PASSED...")