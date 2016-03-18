# Copyright (C) 2015 Siavoosh Payandeh Azad  and Thilo Kogge

from ConfigAndPackages import PackageFile, Config
import copy
import itertools
import AG_Functions
from RoutingAlgorithms import Routing
from SystemHealthMonitoring import SystemHealthMonitoringUnit
import networkx


def list_all_3d_turn_models():
    """
    Lists all 3D deadlock free turn models in "deadlock_free_turns" in "Generated_Files"
    folder!
    :return: None
    """
    counter = 0
    all_turns_file = open('Generated_Files/deadlock_free_turns.txt', 'w')

    Config.ag.topology = '3DMesh'
    Config.ag.x_size = 10
    Config.ag.y_size = 10
    Config.ag.z_size = 10

    ag = copy.deepcopy(AG_Functions.generate_ag())
    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_3D)

    print "=========================================="
    print "list of 3D deadlock free turn models:"

    for combination in range(1, len(turn_model_list)):
        for turns in itertools.combinations(turn_model_list, combination):

            counter += 1
            shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
            shmu.setup_noc_shm(ag, Config.TurnsHealth, False)
            noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, list(turns), False,  False))
            if networkx.is_directed_acyclic_graph(noc_rg):
                print counter, "\t", list(turns)
                all_turns_file.write(str(counter)+"   "+str(list(turns))+"\n")

            del shmu
            del noc_rg
        print "---------------------------"

    all_turns_file.close()
    return None