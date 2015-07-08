# Copyright (C) 2015 Siavoosh Payandeh Azad

# Here we want to animate the mapping process...

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ConfigAndPackages import Config
from math import log10
from ArchGraphUtilities import AG_Functions
import random


def GenerateFrames(TG, AG, SHM):
    print "==========================================="
    print "GENERATING MAPPING ANIMATION FRAMES..."
    MappingProcessFile = open("Generated_Files/Internal/MappingProcess.txt", 'r')
    XSize = float(Config.Network_X_Size)
    YSize = float(Config.Network_Y_Size)
    line = MappingProcessFile.readline()

    Bound = int(log10(2 * Config.MaxNumberOfIterations)) + 1   # UpperBoundOnFileNumberDigits
    Counter = 0
    while line != '':
        fig = plt.figure(figsize=(4*Config.Network_X_Size, 4*Config.Network_Y_Size), dpi=Config.FrameResolution)
        # initialize an empty list of cirlces
        MappedPEList = line.split(" ")
        for node in AG.nodes():
            Location = AG_Functions.ReturnNodeLocation(node)
            # print node, Location
            if SHM.SHM.node[node]['NodeHealth']:
                if Config.EnablePartitioning:
                    if node in Config.CriticalRegionNodes:
                        color = '#FF878B'
                    elif node in Config.GateToNonCritical:
                        color = '#928AFF'
                    elif node in Config.GateToCritical:
                        color = '#FFC29C'
                    else:
                        color = 'white'
                else:
                    color = 'white'
            else:   # node is broken
                color = '#7B747B'
            fig.gca().add_patch(patches.Rectangle((Location[0]/XSize, Location[1]/YSize),
                                                   width=0.15, height=0.15, facecolor=color,
                                                   edgecolor="black", linewidth=3, alpha= 0.5))
            if str(node) in MappedPEList:
                Tasks = [i for i,x in enumerate(MappedPEList) if x == str(node)]
                OffsetX = 0
                OffsetY = 0.02
                TaskCount = 0
                for task in Tasks:
                    TaskCount += 1
                    OffsetX += 0.03
                    if TaskCount == 5:
                        TaskCount = 1
                        OffsetX = 0.03
                        OffsetY += 0.03
                    random.seed(task)
                    r = random.randrange(0,255)
                    g = random.randrange(0,255)
                    b = random.randrange(0,255)
                    color = '#%02X%02X%02X' % (r,g,b)
                    circle = plt.Circle((Location[0]/XSize+OffsetX, Location[1]/YSize+OffsetY), 0.01, fc=color)
                    if Config.FrameResolution >= 50:
                        plt.text(Location[0]/XSize+OffsetX, Location[1]/YSize+OffsetY -  0.001,task)
                    plt.gca().add_patch(circle)
        fig.text(0.25, 0.02, "Iteration:" + str(Counter), fontsize=35)
        plt.savefig("GraphDrawings/Mapping_Animation_Material/Mapping_Anim_Fig"+ str(Counter).zfill(Bound) + ".png",
                    dpi=Config.FrameResolution)
        plt.clf()
        plt.close(fig)
        Counter += 1
        line = MappingProcessFile.readline()
    MappingProcessFile.close()
    print "MAPPING ANIMATION FRAMES READY..."
    return None

