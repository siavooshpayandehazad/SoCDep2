__author__ = 'siavoosh'


from SystemHealthMonitoring import SHM_Functions

####################################################################
#
#                   Fault event handler
#
####################################################################

def FaultEvent(env, AG, SHM, NoCRG, FaultTimeList):
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
            FaultLocation, FaultType = SHM_Functions.RandomFaultGeneration(SHM)
            SHM_Functions.ApplyFaultEvent(AG, SHM, NoCRG, FaultLocation, FaultType)
            Fault = False
        yield env.timeout(0.1)
        pass