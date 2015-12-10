# Copyright (C) 2015 Siavoosh Payandeh Azad
import SystemHealthMonitoringUnit
from ConfigAndPackages import Config


def test_shmu(ag):
    print ("===========================================")
    print ("STARTING SYSTEM HEALTH MAP TESTS...")
    shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
    shmu_4_test.setup_noc_shm(ag, Config.TurnsHealth)
    TestBreaking(shmu_4_test)
    TestRestore(shmu_4_test)
    TestAging(shmu_4_test)
    # todo: needs more test etc...
    del shmu_4_test
    print ("ALL SHM TESTS PASSED...")
    return None


def TestBreaking(shmu):
    for node in shmu.SHM.nodes():
        shmu.BreakNode(node, False)
        if shmu.SHM.node[node]['NodeHealth']:
            raise ValueError('SHM BreakNode DID NOT WORK FOR NODE', node)
        for Turn in shmu.SHM.node[node]['TurnsHealth']:
            shmu.break_turn(node, Turn, False)
            if shmu.SHM.node[node]['TurnsHealth'][Turn]:
                raise ValueError('SHM break_turn DID NOT WORK FOR NODE:', node, 'TURN:', Turn)
    for link in shmu.SHM.edges():
        shmu.break_link(link, False)
        if shmu.SHM.edge[link[0]][link[1]]['LinkHealth']:
            raise ValueError('SHM break_link DID NOT WORK FOR LINK', link)
    print ("  - BREAKING TESTS PASSED...")


def TestRestore(shmu):
    for node in shmu.SHM.nodes():
        shmu.RestoreBrokenNode(node, False)
        if not shmu.SHM.node[node]['NodeHealth']:
            raise ValueError('SHM RestoreBrokenNode DID NOT WORK FOR NODE', node)
        for turn in shmu.SHM.node[node]['TurnsHealth']:
            shmu.RestoreBrokenTurn(node, turn, False)
            if not shmu.SHM.node[node]['TurnsHealth'][turn]:
                raise ValueError('SHM RestoreBrokenTurn DID NOT WORK FOR NODE:', node, 'TURN:', turn)
    for link in shmu.SHM.edges():
        shmu.restore_broken_link(link, False)
        if not shmu.SHM.edge[link[0]][link[1]]['LinkHealth']:
            raise ValueError('SHM restore_broken_link DID NOT WORK FOR LINK', link)
    print ("  - RESTORE TESTS PASSED...")


def TestAging(shmu):
    for Node in shmu.SHM.nodes():
        shmu.IntroduceAging(Node, 0.5, False)
        if shmu.SHM.node[Node]['NodeSpeed'] != 50:
            raise ValueError('SHM IntroduceAging DID NOT WORK FOR NODE', Node)
        shmu.IntroduceAging(Node, 0.5, False)
        if shmu.SHM.node[Node]['NodeSpeed'] != 25:
            raise ValueError('SHM IntroduceAging ROUND 2 DID NOT WORK FOR NODE', Node)
    print ("  - AGING TESTS PASSED...")