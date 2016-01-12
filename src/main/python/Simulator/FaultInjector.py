# Copyright (C) 2015 Siavoosh Payandeh Azad


from SystemHealthMonitoring import SHMU_Functions
import random
from ConfigAndPackages import Config
####################################################################
#
#                   Fault event handler
#
####################################################################


def fault_event(env, ag, shmu, noc_rg, schedule_length, fault_time_list, counter_threshold, logging):
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

            if type(fault_location) is int:
                for scheduling_item in ag.node[fault_location]['PE'].Scheduling:
                    start_time = ag.node[fault_location]['PE'].Scheduling[scheduling_item][0]
                    end_time = ag.node[fault_location]['PE'].Scheduling[scheduling_item][1]
                    if start_time < env.now % schedule_length < end_time:
                        SHMU_Functions.apply_fault_event(ag, shmu, noc_rg, fault_location, fault_type)
                        if random.random() > Config.error_correction_rate:
                            counter_threshold.increase_fault_counter(fault_location, logging)
                        else:
                            counter_threshold.increase_intermittent_counter(fault_location, logging)

            elif type(fault_location) is tuple:
                for scheduling_item in ag.edge[fault_location[0]][fault_location[1]]["Scheduling"]:
                    start_time = ag.edge[fault_location[0]][fault_location[1]]["Scheduling"][scheduling_item][0][0]
                    end_time = ag.edge[fault_location[0]][fault_location[1]]["Scheduling"][scheduling_item][0][1]
                    if start_time < env.now % schedule_length < end_time:
                        SHMU_Functions.apply_fault_event(ag, shmu, noc_rg, fault_location, fault_type)
                        if random.random() > Config.error_correction_rate:
                            counter_threshold.increase_fault_counter(fault_location, logging)
                        else:
                            counter_threshold.increase_intermittent_counter(fault_location, logging)

            elif type(fault_location) is dict:
                for scheduling_item in ag.node[fault_location.keys()[0]]['Router'].Scheduling:
                    start_time = ag.node[fault_location.keys()[0]]['Router'].Scheduling[scheduling_item][0][0]
                    end_time = ag.node[fault_location.keys()[0]]['Router'].Scheduling[scheduling_item][0][1]
                    if start_time < env.now % schedule_length < end_time:
                        SHMU_Functions.apply_fault_event(ag, shmu, noc_rg, fault_location, fault_type)
                        if random.random() > Config.error_correction_rate:
                            counter_threshold.increase_fault_counter(fault_location, logging)
                        else:
                            counter_threshold.increase_intermittent_counter(fault_location, logging)

            fault = False
        yield env.timeout(0.1)
        pass