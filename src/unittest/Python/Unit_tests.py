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
from ArchGraphUtilities.AG_Functions import update_ag_regions, max_node_neighbors, return_healthy_nodes
from ArchGraphUtilities.AG_Functions import random_darkness
from SystemHealthMonitoring import SystemHealthMonitoringUnit, SHMU_Functions
from RoutingAlgorithms.Calculate_Reachability import is_node_inside_rectangle
from ConfigAndPackages import Config
from math import ceil
import copy
import random

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

    def test_update_ag_regions(self):

        # taking a copy of the Config
        temp_critical_region = copy.deepcopy(Config.CriticalRegionNodes)
        temp_gnc_region = copy.deepcopy(Config.GateToNonCritical)
        temp_gc_region = copy.deepcopy(Config.GateToCritical)
        temp_ag_x = Config.ag.x_size
        temp_ag_y = Config.ag.y_size
        temp_ag_z = Config.ag.z_size

        # setting up the Config
        Config.ag.x_size = 5
        Config.ag.y_size = 5
        Config.ag.z_size = 1

        Config.CriticalRegionNodes = [16, 17, 21, 22, 23, 28, 29]
        Config.GateToNonCritical = [15, 27]
        Config.GateToCritical = [20]

        ag_4_test = copy.deepcopy(generate_ag(logging=None))
        self.assertEqual(len(ag_4_test.nodes()), Config.ag.x_size*Config.ag.y_size*Config.ag.z_size)

        update_ag_regions(ag_4_test)

        for node in ag_4_test.nodes():
            if node in Config.CriticalRegionNodes:
                self.assertEqual(ag_4_test.node[node]['Region'], 'H')
            elif node in Config.GateToCritical:
                self.assertEqual(ag_4_test.node[node]['Region'], 'GH')
            elif node in Config.GateToNonCritical:
                self.assertEqual(ag_4_test.node[node]['Region'], 'GNH')
            else:
                self.assertEqual(ag_4_test.node[node]['Region'], 'L')

        Config.CriticalRegionNodes = copy.deepcopy(temp_critical_region)
        Config.GateToNonCritical = copy.deepcopy(temp_gnc_region)
        Config.GateToCritical = copy.deepcopy(temp_gc_region)

        Config.ag.x_size = temp_ag_x
        Config.ag.y_size = temp_ag_y
        Config.ag.z_size = temp_ag_z

    def test_max_node_neighbors(self):
        number_of_nodes = random.randint(0, 10)
        node_neighbors = {}
        max_neighbors = 0
        for i in range(0, number_of_nodes):
            num_of_neighbors = random.randint(1, number_of_nodes**2)
            node_neighbors[i] = num_of_neighbors
            if num_of_neighbors > max_neighbors:
                max_neighbors = num_of_neighbors
        sorted_node_neighbors = sorted(node_neighbors, key=node_neighbors.get, reverse=True)
        list_of_max_neighbors = max_node_neighbors(node_neighbors, sorted_node_neighbors)
        for node in list_of_max_neighbors:
            self.assertEqual(node_neighbors[node], max_neighbors)

    def test_return_healthy_nodes(self):
        ag_4_test = copy.deepcopy(generate_ag(logging=None))
        shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth)

        healthy_nodes = copy.deepcopy(ag_4_test.nodes())
        for node in ag_4_test.nodes():
            if random.choice(['Healthy', 'Faulty']) == 'Faulty':
                healthy_nodes.remove(node)
                shmu_4_test.break_node(node, False)

        test_healthy_nodes = return_healthy_nodes(ag_4_test, shmu_4_test.SHM)
        self.assertEqual(test_healthy_nodes, healthy_nodes)

    def test_random_darkness(self):
        config_darkness = Config.DarkSiliconPercentage
        ag_4_test = copy.deepcopy(generate_ag(logging=None))
        for i in range(1, 100):
            Config.DarkSiliconPercentage = i
            random_darkness(ag_4_test)
            num_of_dark_nodes = 0
            for node in ag_4_test.nodes():
                if ag_4_test.node[node]['PE'].dark:
                    num_of_dark_nodes += 1
            self.assertEqual(num_of_dark_nodes, ceil(len(ag_4_test.nodes())*i/100))
            # clean the AG
            for node in ag_4_test.nodes():
                ag_4_test.node[node]['PE'].dark = False
        del ag_4_test
        Config.DarkSiliconPercentage = config_darkness

if __name__ == '__main__':
    unittest.main()
