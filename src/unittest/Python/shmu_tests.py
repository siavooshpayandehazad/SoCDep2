# Copyright (C) Siavoosh Payandeh Azad

import unittest
import sys
import os
import re

# Setting up the python path to import the functions
current_path = re.sub('unittest', '', str(os.getcwd()))
sys.path.append(current_path)
# Add Imports here:
from ArchGraphUtilities.AG_Functions import generate_ag
from SystemHealthMonitoring import SystemHealthMonitoringUnit, SHMU_Functions
from ConfigAndPackages import Config
import copy


class SystemHealthMonitoringUnitTesting(unittest.TestCase):

    def test_shmu_breaking_and_restore(self):
        ag_4_test = copy.deepcopy(generate_ag(logging=None))
        shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth)
        for node in shmu_4_test.SHM.nodes():
            shmu_4_test.break_node(node, False)
            self.assertEqual(shmu_4_test.SHM.node[node]['NodeHealth'], False)

            for Turn in shmu_4_test.SHM.node[node]['TurnsHealth']:
                shmu_4_test.break_turn(node, Turn, False)
                self.assertEqual(shmu_4_test.SHM.node[node]['TurnsHealth'][Turn], False)

        for link in shmu_4_test.SHM.edges():
            shmu_4_test.break_link(link, False)
            self.assertEqual(shmu_4_test.SHM.edge[link[0]][link[1]]['LinkHealth'], False)
        # testing Restore
        for node in shmu_4_test.SHM.nodes():
            shmu_4_test.restore_broken_node(node, False)
            self.assertEqual(shmu_4_test.SHM.node[node]['NodeHealth'], True)

            for turn in shmu_4_test.SHM.node[node]['TurnsHealth']:
                shmu_4_test.restore_broken_turn(node, turn, False)
                self.assertEqual(shmu_4_test.SHM.node[node]['TurnsHealth'][turn], True)

        for link in shmu_4_test.SHM.edges():
            shmu_4_test.restore_broken_link(link, False)
            self.assertEqual(shmu_4_test.SHM.edge[link[0]][link[1]]['LinkHealth'], True)
        del ag_4_test
        del shmu_4_test

    def test_shmu_aging(self):
        ag_4_test = copy.deepcopy(generate_ag(logging=None))
        shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth)
        for Node in shmu_4_test.SHM.nodes():
            shmu_4_test.introduce_aging(Node, 0.5, False)
            self.assertEqual(shmu_4_test.SHM.node[Node]['NodeSpeed'], 50)
            shmu_4_test.introduce_aging(Node, 0.5, False)
            self.assertEqual(shmu_4_test.SHM.node[Node]['NodeSpeed'], 25)
        del ag_4_test
        del shmu_4_test

    def test_apply_initial_faults(self):
        # todo: generate some random faults and put them in Config and then return to normal
        ag_4_test = copy.deepcopy(generate_ag(logging=None))
        shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth)
        SHMU_Functions.apply_initial_faults(shmu_4_test)
        for broken_link in Config.ListOfBrokenLinks:
            self.assertEqual(shmu_4_test.SHM.edge[broken_link[0]][broken_link[1]]['LinkHealth'], False)
        for router_with_broken_turn in Config.ListOfBrokenTurns:
            broken_turn = Config.ListOfBrokenTurns[router_with_broken_turn]
            self.assertEqual(shmu_4_test.SHM.node[router_with_broken_turn]['TurnsHealth'][broken_turn], False)
        for broken_node in Config.ListOfBrokenPEs:
            self.assertEqual(shmu_4_test.SHM.node[broken_node]['NodeHealth'], False)
        for aged_pe in Config.ListOfAgedPEs:
            self.assertEqual(shmu_4_test.SHM.node[aged_pe]['NodeSpeed'],  Config.ListOfAgedPEs[aged_pe])
        del ag_4_test
        del shmu_4_test
