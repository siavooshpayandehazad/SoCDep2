# Copyright (C) 2015 Siavoosh Payandeh Azad

def Report_NoC_SystemHealthMap(SHM):
        print "==========================================="
        print "      REPORTING SYSTEM HEALTH MAP"
        print "==========================================="
        for Node in SHM.SHM.nodes():
            print "\tNODE:", Node
            print "\t\tNODE HEALTH:", SHM.SHM.node[Node]['NodeHealth']
            print "\t\tNODE SPEED:", SHM.SHM.node[Node]['NodeSpeed']
            print "\t\tTURNS:", SHM.SHM.node[Node]['TurnsHealth']
            print "\t=============="
        for Edge in SHM.SHM.edges():
            print "\tLINK:", Edge, "\t", SHM.SHM.edge[Edge[0]][Edge[1]]['LinkHealth']


def ReportTheEvent(FaultLocation, FaultType):
    print "==========================================="
    if FaultType == 'T':    # Transient Fault
            StringToPrint = "\033[33mSHM:: Event:\033[0m Transient Fault happened at "
    else:   # Permanent Fault
            StringToPrint = "\033[33mSHM:: Event:\033[0m Permanent Fault happened at "
    if type(FaultLocation) is tuple:
            StringToPrint += 'Link ' + str(FaultLocation)
    elif type(FaultLocation) is dict:
            Turn = FaultLocation[FaultLocation.keys()[0]]
            Node = FaultLocation.keys()[0]
            StringToPrint += 'Turn ' + str(Turn) + ' of Node ' + str(Node)
    else:
            StringToPrint += 'Node ' + str(FaultLocation)
    print StringToPrint
    return None

def ReportMPM(SHM):
        print "==========================================="
        print "      REPORTING MOST PROBABLE MAPPING "
        print "==========================================="
        for item in SHM.MPM:
            print "KEY:",item,"\t\tMAPPING:",SHM.MPM[item]
        return None