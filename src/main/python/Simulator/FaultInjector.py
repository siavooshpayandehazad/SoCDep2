# Copyright (C) 2015 Siavoosh Payandeh Azad


from SystemHealthMonitoring import SHMU_Functions
import random
from ConfigAndPackages import Config
####################################################################
#
#                   Fault event handler
#
####################################################################


def fault_event(env, ag, shmu, noc_rg, fault_time_list, counter_threshold, logging):
    """
    Injects rand fault events (random location and type of fault) at times taken from fault_time_list
    :param env: Simulator Environment
    :param ag: Architecture Graph
    :param shmu: System health Monitoring Unit
    :param noc_rg: NoC routing Graph
    :param fault_time_list: List of faults to happen in future
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    fault = False
    while True:
        for fault_time in fault_time_list:
            # print env.now, fault_time
            if float("{0:.1f}".format(env.now)) == fault_time:
                fault = True
                # print "Fault Location:", FaultLocation, "Type:", FaultType
                pass
            else:
                # print env.now, FaultTime
                pass
        if fault:
            fault_location, fault_type = SHMU_Functions.RandomFaultGeneration(shmu.SHM)
            SHMU_Functions.apply_fault_event(ag, shmu, noc_rg, fault_location, fault_type)
            if random.random() > Config.error_correction_rate:
                counter_threshold.increase_fault_counter(fault_location, logging)
            else:
                counter_threshold.increase_intermittent_counter(fault_location, logging)
            fault = False
        yield env.timeout(0.1)
        pass