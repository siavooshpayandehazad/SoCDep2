# Copyright (C) 2015 Siavoosh Payandeh Azad


from SystemHealthMonitoring import SHMU_Functions

####################################################################
#
#                   Fault event handler
#
####################################################################


def FaultEvent(env, AG, SHMU, NoCRG, fault_time_list, counter_threshold, logging):
    """

    :param env: Simulator Environment
    :param AG: Architecture Graph
    :param SHMU: System health Monitoring Unit
    :param NoCRG: NoC routing Graph
    :param fault_time_list: List of faults to happen in future
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    Fault = False
    while True:
        for FaultTime in fault_time_list:
            #print env.now, FaultTime
            if float("{0:.1f}".format(env.now)) == FaultTime:
                Fault = True
                # print "Fault Location:", FaultLocation, "Type:", FaultType
                pass
            else:
                # print env.now, FaultTime
                pass

        if Fault:
            FaultLocation, FaultType = SHMU_Functions.RandomFaultGeneration(SHMU.SHM)
            SHMU_Functions.ApplyFaultEvent(AG, SHMU, NoCRG, FaultLocation, FaultType)

            counter_threshold.increase_counter(FaultLocation, logging)
            Fault = False
        yield env.timeout(0.1)
        pass