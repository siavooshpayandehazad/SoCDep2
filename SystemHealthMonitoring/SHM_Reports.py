# Copyright (C) 2015 Siavoosh Payandeh Azad


import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ConfigAndPackages import Config
from ArchGraphUtilities import AG_Functions

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

def DrawSHM(SHM):
    print "==========================================="
    print "GENERATING SYSTEM HEALTH MAP DRAWING..."
    fig = plt.figure(figsize=(4*Config.Network_X_Size, 4*Config.Network_Y_Size))
    XSize = float(Config.Network_X_Size)
    YSize = float(Config.Network_Y_Size)

    for node in SHM.SHM.nodes():
        Location = AG_Functions.ReturnNodeLocation(node)
        X = Location[0]/XSize
        Y = Location[1]/YSize
        CircleRouter = plt.Circle((X+0.1, Y+0.1), 0.05, facecolor='w')
        plt.gca().add_patch(CircleRouter)
        if SHM.SHM.node[node]['NodeHealth']:
            color = 'w'
        else:
            color = 'r'
        CircleNode = plt.Circle((X+0.14, Y+0.06), 0.01, facecolor=color)
        plt.gca().add_patch(CircleNode)

        for turn in SHM.SHM.node[node]['TurnsHealth']:
            if SHM.SHM.node[node]['TurnsHealth'][turn]:
                color = 'black'
            else:
                color = 'r'

            if turn == 'S2E':
                plt.gca().add_patch(patches.Arrow(X+0.11, Y+0.075, 0.015, 0.015, width=0.01, color= color))
            elif turn == 'E2S':
                plt.gca().add_patch(patches.Arrow(X+0.135, Y+0.09, -0.015, -0.015, width=0.01, color= color))
            elif turn == 'W2N':
                plt.gca().add_patch(patches.Arrow(X+0.065, Y+0.105, 0.015, 0.015, width=0.01, color= color))
            elif turn == 'N2W':
                plt.gca().add_patch(patches.Arrow(X+0.09, Y+0.12, -0.015, -0.015, width=0.01, color= color))
            elif turn == 'N2E':
                plt.gca().add_patch(patches.Arrow(X+0.12, Y+0.12, 0.015, -0.015, width=0.01, color= color))
            elif turn == 'E2N':
                plt.gca().add_patch(patches.Arrow(X+0.125, Y+0.105, -0.015, 0.015, width=0.01, color= color))
            elif turn == 'W2S':
                plt.gca().add_patch(patches.Arrow(X+0.075, Y+0.09, 0.015, -0.015, width=0.01, color= color))
            elif turn == 'S2W':
                plt.gca().add_patch(patches.Arrow(X+0.080, Y+0.075, -0.015, 0.015, width=0.01, color= color))

    for link in SHM.SHM.edges():
        if SHM.SHM.edge[link[0]][link[1]]['LinkHealth']:
            color = 'black'
        else:
            color = 'r'
        SourceLoc = AG_Functions.ReturnNodeLocation(link[0])
        DestinLoc = AG_Functions.ReturnNodeLocation(link[1])

        dx = ((DestinLoc[0] - SourceLoc [0])/XSize)
        dy = ((DestinLoc[1] - SourceLoc [1])/YSize)
        if dx == 0:
            if dy < 0:
                X = SourceLoc[0]/XSize + 0.09
                Y = SourceLoc[1]/YSize + 0.0
                plt.gca().add_patch(patches.Arrow(X, Y, 0, 0.05, width=0.01, color= color))
            else:
                X = SourceLoc[0]/XSize + 0.11
                Y = SourceLoc[1]/YSize + 0.2
                plt.gca().add_patch(patches.Arrow(X, Y, 0, -0.05, width=0.01, color= color))

        elif dy == 0:
            if dx < 0:
                X = SourceLoc[0]/XSize -0.01
                Y = SourceLoc[1]/YSize + 0.09
                plt.gca().add_patch(patches.Arrow(X, Y, 0.05, 0, width=0.01, color= color))
            else:
                X = SourceLoc[0]/XSize + 0.21
                Y = SourceLoc[1]/YSize + 0.11
                plt.gca().add_patch(patches.Arrow(X, Y, -0.05, 0, width=0.01, color= color))

        else:
            raise ValueError("Can not draw link", link)

    fig.text(0.25, 0.02, "System Health Map", fontsize=35)
    plt.savefig("GraphDrawings/SHM.png")
    plt.clf()
    plt.close(fig)
    return None

