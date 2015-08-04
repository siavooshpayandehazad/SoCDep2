# Copyright (C) 2015 Siavoosh Payandeh Azad


import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ConfigAndPackages import Config
from ArchGraphUtilities import AG_Functions



def Report_NoC_SystemHealthMap(SHM):
        print ("===========================================")
        print ("      REPORTING SYSTEM HEALTH MAP")
        print ("===========================================")
        for Node in SHM.SHM.nodes():
            print ("\tNODE:", Node)
            print ("\t\tNODE HEALTH:", SHM.SHM.node[Node]['NodeHealth'])
            print ("\t\tNODE SPEED:", SHM.SHM.node[Node]['NodeSpeed'])
            print ("\t\tTURNS:", SHM.SHM.node[Node]['TurnsHealth'])
            print ("\t==============")
        for Edge in SHM.SHM.edges():
            print ("\tLINK:", Edge, "\t", SHM.SHM.edge[Edge[0]][Edge[1]]['LinkHealth'])


def ReportTheEvent(FaultLocation, FaultType):
    print ("===========================================")
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
    print (StringToPrint)
    return None


def ReportMPM(SHM):
        print ("===========================================")
        print ("      REPORTING MOST PROBABLE MAPPING ")
        print ("===========================================")
        for item in SHM.MPM:
            print ("KEY:", item, "\t\tMAPPING:", SHM.MPM[item])
        return None


def DrawSHM(SHM):
    print ("===========================================")
    print ("GENERATING SYSTEM HEALTH MAP DRAWING...")

    XSize = float(Config.Network_X_Size)
    YSize = float(Config.Network_Y_Size)
    ZSize = float(Config.Network_Z_Size)

    fig = plt.figure(figsize=(10*XSize, 10*YSize))
    if ZSize == 1:
        plt.ylim([0, 1])
        plt.xlim([0, 1])
    else:
        plt.ylim([0, ZSize])
        plt.xlim([0, ZSize])

    for node in SHM.SHM.nodes():
        Location = AG_Functions.ReturnNodeLocation(node)
        X = (Location[0]/XSize)*ZSize
        Y = (Location[1]/YSize)*ZSize
        Z = (Location[2]/ZSize)
        X_offset = Z
        Y_offset = Z

        fontsize = 35 /ZSize
        plt.text(X+0.095+X_offset, Y+0.095+Y_offset, str(node), fontsize=fontsize)
        CircleRouter = plt.Circle((X+0.1+X_offset, Y+0.1+Y_offset), 0.05, facecolor='w')
        plt.gca().add_patch(CircleRouter)
        if SHM.SHM.node[node]['NodeHealth']:
            color = 'w'
        else:
            color = 'r'
        CircleNode = plt.Circle((X+0.14+X_offset, Y+0.06 +Y_offset), 0.01, facecolor=color)
        plt.gca().add_patch(CircleNode)

        for turn in SHM.SHM.node[node]['TurnsHealth']:
            if SHM.SHM.node[node]['TurnsHealth'][turn]:
                color = 'black'
            else:
                color = 'r'

            if turn == 'S2E':
                plt.gca().add_patch(patches.Arrow(X + 0.11+X_offset, Y + 0.075 +Y_offset, 0.015, 0.015, width=0.01, color=color))
            elif turn == 'E2S':
                plt.gca().add_patch(patches.Arrow(X + 0.135+X_offset, Y + 0.09+Y_offset, -0.015, -0.015, width=0.01, color=color))
            elif turn == 'W2N':
                plt.gca().add_patch(patches.Arrow(X + 0.065+X_offset, Y + 0.105+Y_offset, 0.015, 0.015, width=0.01, color=color))
            elif turn == 'N2W':
                plt.gca().add_patch(patches.Arrow(X + 0.09+X_offset, Y + 0.12+Y_offset, -0.015, -0.015, width=0.01, color=color))
            elif turn == 'N2E':
                plt.gca().add_patch(patches.Arrow(X + 0.12+X_offset, Y + 0.12+Y_offset, 0.015, -0.015, width=0.01, color=color))
            elif turn == 'E2N':
                plt.gca().add_patch(patches.Arrow(X + 0.125+X_offset, Y + 0.105+Y_offset, -0.015, 0.015, width=0.01, color=color))
            elif turn == 'W2S':
                plt.gca().add_patch(patches.Arrow(X + 0.075+X_offset, Y + 0.09+Y_offset, 0.015, -0.015, width=0.01, color=color))
            elif turn == 'S2W':
                plt.gca().add_patch(patches.Arrow(X + 0.080+X_offset, Y + 0.075+Y_offset, -0.015, 0.015, width=0.01, color=color))

            if SHM.SHM.node[node]['TurnsHealth'][turn]:
                color = 'w'
            else:
                color = 'r'

            if turn == 'N2U':
                CircleNode = plt.Circle((X+0.09+X_offset, Y+0.14 +Y_offset), 0.005, facecolor=color)
                plt.gca().add_patch(CircleNode)
                CircleNode = plt.Circle((X+0.09+X_offset, Y+0.14 +Y_offset), 0.001, facecolor='b')
                plt.gca().add_patch(CircleNode)

            elif turn == 'N2D':
                CircleNode = plt.Circle((X+0.11+X_offset, Y+0.14 +Y_offset), 0.005, facecolor=color)
                plt.gca().add_patch(CircleNode)


            elif turn == 'S2U':
                CircleNode = plt.Circle((X+0.11+X_offset, Y+0.06 +Y_offset), 0.005, facecolor=color)
                plt.gca().add_patch(CircleNode)
                CircleNode = plt.Circle((X+0.11+X_offset, Y+0.06 +Y_offset), 0.001, facecolor='b')
                plt.gca().add_patch(CircleNode)

            elif turn == 'S2D':
                CircleNode = plt.Circle((X+0.09+X_offset, Y+0.06 +Y_offset), 0.005, facecolor=color)
                plt.gca().add_patch(CircleNode)

            elif turn == 'E2U':
                CircleNode = plt.Circle((X+0.142+X_offset, Y+0.11 +Y_offset), 0.005, facecolor=color)
                plt.gca().add_patch(CircleNode)
                CircleNode = plt.Circle((X+0.142+X_offset, Y+0.11 +Y_offset), 0.001, facecolor='b')
                plt.gca().add_patch(CircleNode)

            elif turn == 'E2D':
                CircleNode = plt.Circle((X+0.142+X_offset, Y+0.09 +Y_offset), 0.005, facecolor=color)
                plt.gca().add_patch(CircleNode)

            elif turn == 'W2U':
                CircleNode = plt.Circle((X+0.057+X_offset, Y+0.09+Y_offset), 0.005, facecolor=color)
                plt.gca().add_patch(CircleNode)
                CircleNode = plt.Circle((X+0.057+X_offset, Y+0.09+Y_offset), 0.001, facecolor='b')
                plt.gca().add_patch(CircleNode)
            elif turn == 'W2D':
                CircleNode = plt.Circle((X+0.057+X_offset, Y+0.11+Y_offset), 0.005, facecolor=color)
                plt.gca().add_patch(CircleNode)

    for link in SHM.SHM.edges():
        if SHM.SHM.edge[link[0]][link[1]]['LinkHealth']:
            color = 'black'
        else:
            color = 'r'
        SourceLoc = AG_Functions.ReturnNodeLocation(link[0])
        DestinLoc = AG_Functions.ReturnNodeLocation(link[1])

        X = (SourceLoc[0]/XSize)*ZSize
        Y = (SourceLoc[1]/YSize)*ZSize
        Z = SourceLoc[2]/ZSize
        X_offset = Z
        Y_offset = Z

        dx = ((DestinLoc[0] - SourceLoc[0])/XSize)
        dy = ((DestinLoc[1] - SourceLoc[1])/YSize)
        dz = ((DestinLoc[2] - SourceLoc[2])/ZSize)
        if dz == 0:
            if dx == 0:
                if dy > 0:
                    plt.gca().add_patch(patches.Arrow(X+ 0.11 + X_offset, Y+ 0.15 + Y_offset, 0, dy*ZSize - 0.1, width=0.01, color=color))
                else:
                    plt.gca().add_patch(patches.Arrow(X+ 0.09 + X_offset, Y+ 0.05 + Y_offset, 0, dy*ZSize + 0.1, width=0.01, color=color))

            elif dy == 0:
                if dx > 0:
                    plt.gca().add_patch(patches.Arrow(X+ 0.15 + X_offset, Y+ 0.11 + Y_offset, dx*ZSize - 0.1, 0, width=0.01, color=color))
                else:
                    plt.gca().add_patch(patches.Arrow(X+ 0.05 + X_offset, Y+ 0.09 + Y_offset, dx*ZSize + 0.1, 0, width=0.01, color=color))
            else:
                raise ValueError("Can not draw link", link)
        elif dz > 0:
                Z_offset = 1.4/ZSize
                plt.gca().add_patch(patches.Arrow(X + 0.130 + X_offset, Y + 0.140 + Y_offset, dz*Z_offset, dz*Z_offset, width=0.01, color=color))
        elif dz <0:
                plt.gca().add_patch(patches.Arrow(X + 0.07 + X_offset, Y+ 0.06 + Y_offset, dz*Z_offset, dz*Z_offset, width=0.01, color=color))


    fig.text(0.25, 0.02, "System Health Map", fontsize=35)
    plt.savefig("GraphDrawings/SHM.png", dpi =100)
    plt.clf()
    plt.close(fig)
    print ("\033[35m* VIZ::\033[0mSYSTEM HEALTH MAP DRAWING CREATED AT: GraphDrawings/SHM.png")
    return None

