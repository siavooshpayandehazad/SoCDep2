# Copyright (C) Siavoosh Payandeh Azad
from re import sub
from os import getcwd
from sys import path
from unittest import TestCase
from copy import deepcopy

# Setting up the python path to import the functions
current_path = sub('unittest', '', str(getcwd()))
path.append(current_path)
# Add Imports here:
from RoutingAlgorithms.Routing import generate_noc_route_graph
from RoutingAlgorithms.Routing_Functions import check_deadlock_freeness, degree_of_adaptiveness, \
    extended_degree_of_adaptiveness, return_turn_model_name
from ArchGraphUtilities.AG_Functions import generate_ag
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from ConfigAndPackages import Config, PackageFile


class RoutingTesting(TestCase):

    def test_routing_functions(self):
        # backing up the original config...
        initial_config_ag = deepcopy(Config.ag)
        initial_turn_model = Config.UsedTurnModel
        initial_routing_type = Config.RotingType
        # -----------------------------------------------------
        Config.ag.type = "Generic"
        Config.ag.topology = "2DMesh"
        Config.RotingType = "MinimalPath"
        Config.ag.x_size = 3
        Config.ag.y_size = 3
        Config.ag.z_size = 1

        for turn_model in PackageFile.routing_alg_list_2d:
            tmName = return_turn_model_name(turn_model)
            Config.UsedTurnModel = deepcopy(turn_model)
            Config.TurnsHealth = deepcopy(Config.setup_turns_health())
            ag_4_test = deepcopy(generate_ag(logging=None))
            shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
            shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth, False)
            noc_rg = generate_noc_route_graph(ag_4_test, shmu_4_test, turn_model, False, False)

            self.assertEqual(check_deadlock_freeness(noc_rg), True, msg=f"TM {tmName} Deadlock freeness failed")
            if turn_model in [PackageFile.XY_TurnModel, PackageFile.YX_TurnModel]:
                if turn_model == PackageFile.XY_TurnModel:
                    self.assertEqual(tmName, '0', msg=f"TM name {tmName} is not 0")
                else:
                    self.assertEqual(tmName, '13',  msg=f"TM name {tmName} is not 13")
                self.assertEqual(degree_of_adaptiveness(ag_4_test, noc_rg, report=False)/72.0, 1.0, msg=f"TM: {tmName} DOA failed")
                self.assertEqual(extended_degree_of_adaptiveness(ag_4_test, noc_rg, report=False)/72.0, 1.0, msg=f"TM: {tmName} DOAex failed")
            del ag_4_test
            del shmu_4_test

        # -----------------------------------------------------
        Config.ag.type = "Generic"
        Config.ag.topology = "3DMesh"
        Config.RotingType = "NonMinimalPath"
        Config.ag.x_size = 3
        Config.ag.y_size = 3
        Config.ag.z_size = 3

        for turn_model in PackageFile.routing_alg_list_3d:
            Config.UsedTurnModel = deepcopy(turn_model)
            Config.TurnsHealth = deepcopy(Config.setup_turns_health())
            ag_4_test = deepcopy(generate_ag(logging=None))
            shmu_4_test = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
            shmu_4_test.setup_noc_shm(ag_4_test, Config.TurnsHealth, False)
            noc_rg = generate_noc_route_graph(ag_4_test, shmu_4_test, turn_model, False, False)
            self.assertEqual(check_deadlock_freeness(noc_rg), True, msg=f"TM: {turn_model} deadlock freeness Failed!")
            if turn_model == PackageFile.XYZ_TurnModel:
                self.assertEqual(return_turn_model_name(turn_model), "3d_XYZ", msg="Turn Model is not 3d_XYZ")
                self.assertEqual(degree_of_adaptiveness(ag_4_test, noc_rg, False)/702, 1, msg="DoA test failed")
                self.assertEqual(extended_degree_of_adaptiveness(ag_4_test, noc_rg, False)/702, 1, msg="ExDoA test failed")
            if turn_model == PackageFile.NegativeFirst3D_TurnModel:
                self.assertEqual(return_turn_model_name(turn_model), "3d_NegFirst", msg="TM name is not 3d_NegFirst")
            del ag_4_test
            del shmu_4_test
            del noc_rg
        # -----------------------------------------------------
        # going back to original config
        Config.ag = deepcopy(initial_config_ag)
        Config.UsedTurnModel = initial_turn_model
        Config.TurnsHealth = deepcopy(Config.setup_turns_health())
        Config.RotingType = initial_routing_type
