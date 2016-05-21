# Copyright (C) 2015 Siavoosh Payandeh Azad
import Config
import PackageFile


def check_config_file():
    """
    Checks parts of the config file for sanity check before running the tool. for finding obvious
    mistakes before running the tool. how ever, tests should be expanded.
    :return: True if all tests are passed
    """
    check_tg_config()
    check_ag_config()
    check_routing_config()
    print "\033[33m* INFO::\033[0m ALL CHECKS FOR CONFIG FILE PASSED..."
    return True


def check_tg_config():
    if Config.tg.num_of_critical_tasks > Config.tg.num_of_tasks:
        raise ValueError("Number of critical tasks is bigger than the number of tasks... sorry, cant be done!")


def check_ag_config():
    if '2D' in Config.ag.topology:
            if Config.ag.z_size > 1:
                raise ValueError("Number of layers is bigger than 1 for a 2D topology... sorry, cant be done!")


def check_routing_config():
    if '2D' in Config.ag.topology:
        if Config.UsedTurnModel not in PackageFile.routing_alg_list_2d:
            raise ValueError(" Turn Model Not Valid... please choose a 2D turn model")
    if '3D' in Config.ag.topology:
        if Config.UsedTurnModel not in PackageFile.routing_alg_list_3d:
            raise ValueError(" Turn Model Not Valid... please choose a 3D turn model")