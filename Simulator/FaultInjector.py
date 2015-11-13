__author__ = 'siavoosh'


from SystemHealthMonitoring import SHM_Functions
####################################################################
#
#                   Fault event handler
#
####################################################################




"""
def FaultEvent(SystemStartingTime,AG,SHM,NoCRG):
    global timer
    TimeAfterSystemStart = time.time() - SystemStartingTime
    print ("\033[92mTIME::\033[0m FAULT OCCURRED"+str("%.2f" % TimeAfterSystemStart)+" SECONDS AFTER SYSTEM START...")
    # Should we reset the timer or the next fault falls out of the program run time?
    TimeUntilNextFault = numpy.random.normal(Config.MTBF,Config.SD4MTBF)
    if TimeAfterSystemStart + TimeUntilNextFault <= Config.ProgramRunTime:
        print ("TIME UNTIL NEXT FAULT:"+str("%.2f" % TimeUntilNextFault)+" Sec")
        # reset the timer
        timer = threading.Timer(TimeUntilNextFault, FaultEvent, args=[SystemStartingTime, AG, SHM, NoCRG])
        timer.start()

    # we generate some random fault to be inserted in the system
    FaultLocation, FaultType = SHM_Functions.RandomFaultGeneration(SHM)
    # here we actually insert the fault in the system
    SHM_Functions.ApplyFaultEvent(AG, SHM, NoCRG, FaultLocation, FaultType)
    # here we have to check what actions should we take?
    # 1-  Should we update the NoC-Depend rectangles? these are the cases:
    #       - permanently broken Link
    #       - permanently broken Turn
    # 2- Should we change the mapping?


def FaultInjector(SystemStartingTime,AG,SHM,NoCRG):
    if Config.EventDrivenFaultInjection:
        TimeUntilNextFault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
        print ("TIME UNTIL NEXT FAULT:"+str("%.2f" % TimeUntilNextFault)+" Sec")
        timer = threading.Timer(TimeUntilNextFault, FaultEvent, args=[SystemStartingTime, AG, SHM, NoCRG])
        timer.start()

        while True:
            if time.time() - SystemStartingTime > Config.ProgramRunTime:
                break

        timer.cancel()
        timer.join()
"""""