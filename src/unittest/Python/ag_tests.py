# Copyright (C) Siavoosh Payandeh Azad
import unittest
import sys
import os
import re

# Setting up the python path to import the functions
current_path = re.sub('unittest', '', str(os.getcwd()))
sys.path.append(current_path)
# Add Imports here:
from ArchGraphUtilities.AG_Functions import return_node_location, return_node_number, manhattan_distance, generate_ag
from ArchGraphUtilities.AG_Functions import update_ag_regions, max_node_neighbors, return_healthy_nodes
from ArchGraphUtilities.AG_Functions import random_darkness, return_active_nodes, generate_manual_ag
from ArchGraphUtilities.AG_Functions import generate_generic_topology_ag
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from ConfigAndPackages import Config
from math import ceil
import copy
import random


class ArchGraphTesting(unittest.TestCase):

    def test_generate_manual_ag(self):
        for number_of_tests in range(0, 100):
            number_of_nodes = random.randint(10, 30)
            number_of_edges = int(ceil(number_of_nodes*1.5))
            proc_element_list = []
            edge_list = []
            edge_port_list = []
            for i in range(0, number_of_nodes):
                proc_element_list.append(i)

            for j in range(0, number_of_edges):
                link = random.sample(proc_element_list, 2)
                while (link[0], link[1]) in edge_list:
                    link = random.sample(proc_element_list, 2)
                edge_list.append((link[0], link[1]))
                port_1 = random.choice(['W', 'E', 'S', 'N'])
                port_2 = random.choice(['W', 'E', 'S', 'N'])
                edge_port_list.append((port_1, port_2))

            ag = generate_manual_ag(proc_element_list, edge_list, edge_port_list)
            self.assertEqual(len(ag.nodes()), len(proc_element_list))
            self.assertEqual(len(ag.edges()), len(edge_list))
            for node in ag.nodes():
                self.assertTrue(node in proc_element_list)
            for link in ag.edges():
                self.assertTrue(link in edge_list)
                port = ag.edge[link[0]][link[1]]['Port']
                index = edge_list.index(link)
                self.assertEqual(edge_port_list[index], port)
            del ag

    def test_generate_generic_topology_ag(self):
        temp_x = Config.ag.x_size
        temp_y = Config.ag.y_size
        temp_z = Config.ag.z_size
        size_z = 1
        for size_y in range(2, 5):
            for size_x in range(2, 5):
                for topology in ['2DMesh', '2DTorus', '2DRing', '2DLine']:
                    Config.ag.x_size = size_x
                    Config.ag.y_size = size_y
                    Config.ag.z_size = size_z
                    ag_4_test = copy.deepcopy(generate_generic_topology_ag(topology, None))
                    self.assertEqual(len(ag_4_test.nodes()), size_x*size_y*size_z, msg=str(ag_4_test.nodes()))
                    # --------------------------------------------
                    if topology is '2DMesh':
                        link_counter = 0
                        for j in range(0, size_y):
                            for i in range(0, size_x-1):
                                source = return_node_number(i, j, 0)
                                destination = return_node_number(i+1, j, 0)
                                self.assertTrue(ag_4_test.has_edge(source, destination))
                                self.assertTrue(ag_4_test.has_edge(destination, source))
                                link_counter += 2

                        for j in range(0, size_y-1):
                            for i in range(0, size_x):
                                source = return_node_number(i, j, 0)
                                destination = return_node_number(i, j+1, 0)
                                self.assertTrue(ag_4_test.has_edge(source, destination))
                                self.assertTrue(ag_4_test.has_edge(destination, source))
                                link_counter += 2

                        self.assertEqual(link_counter, len(ag_4_test.edges()), msg="link_counter: " +
                                         str(link_counter) + " number of edges: " + str(len(ag_4_test.edges())) +
                                         " topology: "+str(topology))
                    # --------------------------------------------
                    if topology is '2DTorus':
                        link_list = []
                        for j in range(0, size_y):
                            for i in range(0, size_x-1):
                                source = return_node_number(i, j, 0)
                                destination = return_node_number(i+1, j, 0)
                                self.assertTrue(ag_4_test.has_edge(source, destination))
                                self.assertTrue(ag_4_test.has_edge(destination, source))
                                if (source, destination) not in link_list:
                                    link_list.append((source, destination))
                                if (destination, source) not in link_list:
                                    link_list.append((destination, source))

                        for j in range(0, size_y-1):
                            for i in range(0, size_x):
                                source = return_node_number(i, j, 0)
                                destination = return_node_number(i, j+1, 0)
                                self.assertTrue(ag_4_test.has_edge(source, destination),
                                                msg="in topology: "+str(topology)+"\ndid not found path from " +
                                                    str(source) +
                                                    " to "+str(destination) +
                                                    " \nAG nodes: "+str(ag_4_test.nodes()) +
                                                    " \nAG edges: "+str(ag_4_test.edges()))
                                self.assertTrue(ag_4_test.has_edge(destination, source))
                                if (source, destination) not in link_list:
                                    link_list.append((source, destination))
                                if (destination, source) not in link_list:
                                    link_list.append((destination, source))

                        for i in range(0, size_x):
                            source = return_node_number(i, size_y-1, 0)
                            destination = return_node_number(i, 0, 0)
                            self.assertTrue(ag_4_test.has_edge(source, destination))
                            self.assertTrue(ag_4_test.has_edge(destination, source))
                            if (source, destination) not in link_list:
                                link_list.append((source, destination))
                            if (destination, source) not in link_list:
                                link_list.append((destination, source))
                        for j in range(0, size_y):
                            source = return_node_number(size_x-1, j, 0)
                            destination = return_node_number(0, j, 0)
                            self.assertTrue(ag_4_test.has_edge(source, destination))
                            self.assertTrue(ag_4_test.has_edge(destination, source))
                            if (source, destination) not in link_list:
                                link_list.append((source, destination))
                            if (destination, source) not in link_list:
                                link_list.append((destination, source))
                        self.assertEqual(len(link_list), len(ag_4_test.edges()), msg="link_list: "+str(link_list) +
                                         " number of edges: " + str(len(ag_4_test.edges())) + " topology: " +
                                         str(topology))
                    # --------------------------------------------
                    if topology is '2DLine':
                        link_counter = 0
                        for j in range(0, size_y):
                            for i in range(0, size_x-1):
                                source = return_node_number(i, j, 0)
                                destination = return_node_number(i+1, j, 0)
                                self.assertTrue(ag_4_test.has_edge(source, destination))
                                self.assertTrue(ag_4_test.has_edge(destination, source))
                                link_counter += 2
                        self.assertEqual(link_counter, len(ag_4_test.edges()), msg="link_counter: " +
                                         str(link_counter) + " number of edges: " +
                                         str(len(ag_4_test.edges())) + " topology: "+str(topology))
                    # --------------------------------------------
                    if topology is '2DRing':
                        link_list = []
                        for j in range(0, size_y):
                            for i in range(0, size_x-1):
                                source = return_node_number(i, j, 0)
                                destination = return_node_number(i+1, j, 0)
                                self.assertTrue(ag_4_test.has_edge(source, destination))
                                self.assertTrue(ag_4_test.has_edge(destination, source))
                                if (source, destination) not in link_list:
                                    link_list.append((source, destination))
                                if (destination, source) not in link_list:
                                    link_list.append((destination, source))
                        for j in range(0, size_y):
                            source = return_node_number(size_x-1, j, 0)
                            destination = return_node_number(0, j, 0)
                            self.assertTrue(ag_4_test.has_edge(source, destination))
                            self.assertTrue(ag_4_test.has_edge(destination, source))
                            if (source, destination) not in link_list:
                                link_list.append((source, destination))
                            if (destination, source) not in link_list:
                                link_list.append((destination, source))
                        self.assertEqual(len(link_list), len(ag_4_test.edges()), msg="link_list: " +
                                         str(link_list) + " number of edges: " + str(len(ag_4_test.edges())) +
                                         " topology: "+str(topology))
                    del ag_4_test

        # --------------------------------------------
        for size_z in range(2, 5):
            for size_y in range(2, 5):
                for size_x in range(2, 5):
                    for topology in ['3DMesh']:
                        size_x = 2
                        size_y = 2
                        size_z = 2
                        Config.ag.x_size = size_x
                        Config.ag.y_size = size_y
                        Config.ag.z_size = size_z
                        ag_4_test = generate_generic_topology_ag(topology, None)
                        link_counter = 0
                        for k in range(0, size_z):
                            for j in range(0, size_y):
                                for i in range(0, size_x-1):
                                    source = return_node_number(i, j, k)
                                    destination = return_node_number(i+1, j, k)
                                    self.assertTrue(ag_4_test.has_edge(source, destination))
                                    self.assertTrue(ag_4_test.has_edge(destination, source))
                                    link_counter += 2

                        for k in range(0, size_z):
                            for j in range(0, size_y-1):
                                for i in range(0, size_x):
                                    source = return_node_number(i, j, k)
                                    destination = return_node_number(i, j+1, k)
                                    self.assertTrue(ag_4_test.has_edge(source, destination))
                                    self.assertTrue(ag_4_test.has_edge(destination, source))
                                    link_counter += 2

                        for k in range(0, size_z-1):
                            for j in range(0, size_y):
                                for i in range(0, size_x):
                                    source = return_node_number(i, j, k)
                                    destination = return_node_number(i, j, k+1)
                                    self.assertTrue(ag_4_test.has_edge(source, destination))
                                    self.assertTrue(ag_4_test.has_edge(destination, source))
                                    link_counter += 2
                        self.assertEqual(link_counter, len(ag_4_test.edges()), msg="link_counter: " +
                                         str(link_counter) + " number of edges: " + str(len(ag_4_test.edges())) +
                                         " list of edges: "+str(ag_4_test.edges()) + " topology: "+str(topology))
                        del ag_4_test

        Config.ag.x_size = temp_x
        Config.ag.y_size = temp_y
        Config.ag.z_size = temp_z

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

        # return to previous Config
        Config.CriticalRegionNodes = copy.deepcopy(temp_critical_region)
        Config.GateToNonCritical = copy.deepcopy(temp_gnc_region)
        Config.GateToCritical = copy.deepcopy(temp_gc_region)

        Config.ag.x_size = temp_ag_x
        Config.ag.y_size = temp_ag_y
        Config.ag.z_size = temp_ag_z
        del ag_4_test

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
        shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth, False)

        healthy_nodes = copy.deepcopy(ag_4_test.nodes())
        for node in ag_4_test.nodes():
            if random.choice(['Healthy', 'Faulty']) == 'Faulty':
                healthy_nodes.remove(node)
                shmu_4_test.break_node(node, False)

        test_healthy_nodes = return_healthy_nodes(ag_4_test, shmu_4_test.SHM)
        self.assertEqual(test_healthy_nodes, healthy_nodes)
        del ag_4_test
        del shmu_4_test

    def test_random_darkness_return_active_nodes(self):
        # copy the config
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
            active_nodes = return_active_nodes(ag_4_test)
            self.assertEqual(len(ag_4_test.nodes())-num_of_dark_nodes, len(active_nodes))
            # clean the AG
            for node in ag_4_test.nodes():
                ag_4_test.node[node]['PE'].dark = False
        del ag_4_test
        # return to previous config
        Config.DarkSiliconPercentage = config_darkness