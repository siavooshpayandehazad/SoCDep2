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
    all_turns_file = open('Generated_Files/all_turn_models.txt', 'w')
    TurnsHealth_3DNetwork = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                             "W2N": False, "W2S": False, "E2N": False, "E2S": False,
                             "N2U": False, "N2D": False, "S2U": False, "S2D": False,
                             "W2U": False, "W2D": False, "E2U": False, "E2D": False,
                             "U2W": False, "U2E": False, "U2N": False, "U2S": False,
                             "D2W": False, "D2E": False, "D2N": False, "D2S": False}
    Config.ag.topology = '3DMesh'
    Config.ag.x_size = 10
    Config.ag.y_size = 10
    Config.ag.z_size = 10

    ag = copy.deepcopy(AG_Functions.generate_ag())
    turn_model_list = copy.deepcopy(PackageFile.FULL_TurnModel_3D)

    print "=========================================="
    print "list of 3D deadlock free turn models:"

    for combination in range(1, len(turn_model_list)):
        print "Number of Turns:", combination
        for turns in itertools.combinations(turn_model_list, combination):
            TurnsHealth = copy.deepcopy(TurnsHealth_3DNetwork)
            for turn in  turns:
                TurnsHealth[turn] = True
            counter += 1
            shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()


            shmu.setup_noc_shm(ag, TurnsHealth, False)
            noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, list(turns), False,  False))
            if networkx.is_directed_acyclic_graph(noc_rg):
                print counter, "\t \033[92mDF\033[0m \t", list(turns)
                all_turns_file.write(str(counter)+"\t DF \t"+str(list(turns))+"\n")
            else:
                print counter, "\t \033[31mDL\033[0m   \t", list(turns)
                all_turns_file.write(str(counter)+"\t  DL  \t"+str(list(turns))+"\n")
            del shmu
            del noc_rg
        print "---------------------------"

    all_turns_file.close()
    return None