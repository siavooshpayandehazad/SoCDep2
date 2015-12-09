# Copyright (C) 2015 Siavoosh Payandeh Azad


from SystemHealthMonitoring import SHMU_Functions

####################################################################
#
#                   Fault event handler
#
####################################################################


def fault_event(env, ag, SHMU, NoCRG, fault_time_list, counter_threshold, logging):
    """

    :param env: Simulator Environment
    :param ag: Architecture Graph
    :param SHMU: System health Monitoring Unit
    :param NoCRG: NoC routing Graph
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
            fault_location, fault_type = SHMU_Functions.RandomFaultGeneration(SHMU.SHM)
            SHMU_Functions.apply_fault_event(ag, SHMU, NoCRG, fault_location, fault_type)
            counter_threshold.increase_fault_counter(fault_location, logging)
            fault = False
        yield env.timeout(0.1)
        pass