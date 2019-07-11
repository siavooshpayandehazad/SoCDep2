# Copyright (C) Siavoosh Payandeh Azad
import unittest
import sys
import os
import re

# Setting up the python path to import the functions

# Add Imports here:
from copy import deepcopy
from RoutingAlgorithms.Calculate_Reachability import is_node_inside_rectangle, how_many_paths_from_source, \
    is_destination_reachable_from_source, is_destination_reachable_via_port, clear_reachability_calculations
from ConfigAndPackages import Config, PackageFile
from ArchGraphUtilities.AG_Functions import generate_ag, return_node_location
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from RoutingAlgorithms.Routing import generate_noc_route_graph


class ReachabilityTesting(unittest.TestCase):

    def test_is_node_inside_rectangle(self):
        # test that every node in network is inside a cube with size of network
        rectangle = (0, Config.ag.x_size*Config.ag.y_size*Config.ag.z_size-1)
        for node in range(0, Config.ag.x_size*Config.ag.y_size*Config.ag.z_size-1):
            self.assertEqual(is_node_inside_rectangle(rectangle, node), True)

        node = Config.ag.x_size * Config.ag.y_size * Config.ag.z_size
        self.assertEqual(is_node_inside_rectangle(rectangle, node), False)

    def test_how_many_paths_from_source(self):
        initial_config_ag = deepcopy(Config.ag)
        initial_turn_model = Config.UsedTurnModel
        initial_routing_type = Config.RotingType

        Config.ag.type = "Generic"
        Config.ag.topology = "2DMesh"
        Config.ag.x_size = 3
        Config.ag.y_size = 3
        Config.ag.z_size = 1

        turn_model = PackageFile.XY_TurnModel
        Config.UsedTurnModel = deepcopy(turn_model)
        Config.TurnsHealth = deepcopy(Config.setup_turns_health())
        ag_4_test = deepcopy(generate_ag(logging=None))
        shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth, False)
        noc_rg = generate_noc_route_graph(ag_4_test, shmu_4_test, turn_model, False, False)
        for source_node in ag_4_test.nodes():
            for destination_node in ag_4_test.nodes():
                if source_node != destination_node:
                    self.assertEqual(how_many_paths_from_source(noc_rg, source_node, destination_node), 1)

        Config.ag = deepcopy(initial_config_ag)
        Config.UsedTurnModel = initial_turn_model
        Config.TurnsHealth = deepcopy(Config.setup_turns_health())
        Config.RotingType = initial_routing_type

    def test_is_destination_reachable_from_source(self):
        initial_config_ag = deepcopy(Config.ag)
        initial_turn_model = Config.UsedTurnModel
        initial_routing_type = Config.RotingType

        Config.ag.type = "Generic"
        Config.ag.topology = "2DMesh"
        Config.ag.x_size = 3
        Config.ag.y_size = 3
        Config.ag.z_size = 1

        for turn_model in PackageFile.routing_alg_list_2d:
            Config.UsedTurnModel = deepcopy(turn_model)
            Config.TurnsHealth = deepcopy(Config.setup_turns_health())
            ag_4_test = deepcopy(generate_ag(logging=None))
            shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
            shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth, False)
            noc_rg = generate_noc_route_graph(ag_4_test, shmu_4_test, turn_model, False, False)
            for source_node in ag_4_test.nodes():
                for destination_node in ag_4_test.nodes():
                    if source_node != destination_node:
                        self.assertEqual(is_destination_reachable_from_source(noc_rg, source_node, destination_node),
                                         True)
                        s_x, s_y, s_z = return_node_location(source_node)
                        d_x, d_y, d_z = return_node_location(destination_node)
                        # is_destination_reachable_via_port checks output ports only
                        self.assertEqual(is_destination_reachable_via_port(noc_rg, source_node, 'L',
                                                                           destination_node, False), False)
                        if turn_model == PackageFile.XY_TurnModel:
                            if s_x > d_x:
                                self.assertEqual(is_destination_reachable_via_port(noc_rg, source_node, 'W',
                                                                                   destination_node, False), True)
                            if s_x < d_x:
                                self.assertEqual(is_destination_reachable_via_port(noc_rg, source_node, 'E',
                                                                                   destination_node, False), True)
                            if s_x == d_x:
                                if s_y < d_y:
                                    self.assertEqual(is_destination_reachable_via_port(noc_rg, source_node, 'N',
                                                                                       destination_node, False), True)
                                else:
                                    self.assertEqual(is_destination_reachable_via_port(noc_rg, source_node, 'S',
                                                                                       destination_node, False), True)
            del ag_4_test
            del shmu_4_test
            del noc_rg

        Config.ag.type = "Generic"
        Config.ag.topology = "3DMesh"
        Config.ag.x_size = 3
        Config.ag.y_size = 3
        Config.ag.z_size = 3
        Config.RotingType = "MinimalPath"

        for turn_model in PackageFile.routing_alg_list_3d:
            Config.UsedTurnModel = deepcopy(turn_model)
            Config.TurnsHealth = deepcopy(Config.setup_turns_health())
            ag_4_test = deepcopy(generate_ag(logging=None))
            shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
            shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth, False)
            noc_rg = generate_noc_route_graph(ag_4_test, shmu_4_test, turn_model, False, False)
            for source_node in ag_4_test.nodes():
                for destination_node in ag_4_test.nodes():
                    if source_node != destination_node:
                        self.assertEqual(is_destination_reachable_from_source(noc_rg, source_node, destination_node),
                                         True)
                    # todo: check is_destination_reachable_via_port
            del ag_4_test
            del shmu_4_test
            del noc_rg

        Config.ag = deepcopy(initial_config_ag)
        Config.UsedTurnModel = initial_turn_model
        Config.TurnsHealth = deepcopy(Config.setup_turns_health())
        Config.RotingType = initial_routing_type

    def test_clear_reachability_calculations(self):
        initial_config_ag = deepcopy(Config.ag)
        initial_turn_model = Config.UsedTurnModel
        initial_routing_type = Config.RotingType

        Config.ag.type = "Generic"
        Config.ag.topology = "2DMesh"
        Config.ag.x_size = 3
        Config.ag.y_size = 3
        Config.ag.z_size = 1

        ag_4_test = deepcopy(generate_ag(logging=None))
        clear_reachability_calculations(ag_4_test)
        for node in ag_4_test.nodes():
            for port in ag_4_test.node[node]['Router'].unreachable:
                self.assertEqual(ag_4_test.node[node]['Router'].unreachable[port], {})
        del ag_4_test

        Config.ag = deepcopy(initial_config_ag)
        Config.UsedTurnModel = initial_turn_model
        Config.TurnsHealth = deepcopy(Config.setup_turns_health())
        Config.RotingType = initial_routing_type