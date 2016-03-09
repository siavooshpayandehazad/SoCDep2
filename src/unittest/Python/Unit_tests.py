# Copyright (C) Siavoosh Payandeh Azad
import unittest
import sys
import os
import re

# Setting up the python path to import the functions
CurrentPath = re.sub('UnitTest', '', str(os.getcwd()))
sys.path.append(CurrentPath)
# Add Imports here:
from ArchGraphUtilities.AG_Functions import return_node_location, return_node_number, manhattan_distance, generate_ag
from SystemHealthMonitoring import SystemHealthMonitoringUnit, SHMU_Functions
from RoutingAlgorithms.Calculate_Reachability import is_node_inside_rectangle
from ConfigAndPackages import Config
import copy


class UnitTesting(unittest.TestCase):

    def test_return_node_number(self):
        self.assertEqual(return_node_number(0, 0, 0), 0)
        for k in range(0, Config.ag.z_size):
            for j in range(0, Config.ag.y_size):
                for i in range(0, Config.ag.x_size):
                    self.assertEqual(return_node_number(i, j, k),
                                     i + j*Config.ag.x_size+k*Config.ag.y_size*Config.ag.x_size)
        self.assertEqual(return_node_number(Config.ag.x_size-1, Config.ag.y_size-1, Config.ag.z_size-1),
                         Config.ag.x_size * Config.ag.y_size * Config.ag.z_size - 1)

    def test_return_node_location(self):
        for k in range(0, Config.ag.z_size):
            for j in range(0, Config.ag.y_size):
                for i in range(0, Config.ag.x_size):
                    # we have the assumption that return_node_number is fully tested...
                    self.assertEqual(return_node_location(return_node_number(i, j, k)), (i, j, k))

    def test_manhattan_distance(self):
        self.assertEqual(manhattan_distance(0, 0), 0)
        last_node_number = return_node_number(Config.ag.x_size-1, Config.ag.y_size-1, Config.ag.z_size-1)
        self.assertEqual(manhattan_distance(0, last_node_number),
                         Config.ag.x_size+Config.ag.y_size+Config.ag.z_size-3)

    def test_is_node_inside_rectangle(self):
        # test that every node in network is inside a cube with size of network
        rectangle = (0, Config.ag.x_size*Config.ag.y_size*Config.ag.z_size-1)
        for node in range(0, Config.ag.x_size*Config.ag.y_size*Config.ag.z_size-1):
            self.assertEqual(is_node_inside_rectangle(rectangle, node), True)

        node = Config.ag.x_size * Config.ag.y_size * Config.ag.z_size
        self.assertEqual(is_node_inside_rectangle(rectangle, node), False)

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

if __name__ == '__main__':
    unittest.main()
