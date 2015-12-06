# Copyright (C) 2015 Siavoosh Payandeh Azad


from SystemHealthMonitoring import SHMU_Functions

####################################################################
#
#                   Fault event handler
#
####################################################################

def FaultEvent(env, AG, SHMU, NoCRG, FaultTimeList):
    Fault = False
    while True:
        for FaultTime in FaultTimeList:
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
            Fault = False
        yield env.timeout(0.1)
        pass