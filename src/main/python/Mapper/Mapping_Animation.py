# Copyright (C) 2015 Siavoosh Payandeh Azad

# Here we want to animate the mapping process...

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ConfigAndPackages import Config
from math import log10
from ArchGraphUtilities import AG_Functions
import random


def generate_frames(ag, shm):
    """
    Generates Animation frames for the mapping process.
    :param ag: Architecture Graph
    :param shm: System Health Map
    :return: None
    """
    print ("===========================================")
    print ("GENERATING MAPPING ANIMATION FRAMES...")
    mapping_process_file = open("Generated_Files/Internal/MappingProcess.txt", 'r')
    x_size = float(Config.ag.x_size)
    y_size = float(Config.ag.y_size)
    line = mapping_process_file.readline()

    bound = int(log10(2 * Config.MaxNumberOfIterations)) + 1   # UpperBoundOnFileNumberDigits
    counter = 0
    while line != '':
        fig = plt.figure(figsize=(4*Config.ag.x_size, 4*Config.ag.y_size), dpi=Config.viz.frame_resolution)
        # initialize an empty list of cirlces
        mapped_pe_list = line.split(" ")
        for node in ag.nodes():
            location = AG_Functions.return_node_location(node)
            # print (node, location)
            if shm.node[node]['NodeHealth']:
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
            fig.gca().add_patch(patches.Rectangle((location[0]/x_size, location[1]/y_size),
                                width=0.15, height=0.15, facecolor=color,
                                edgecolor="black", linewidth=3, alpha=0.5))
            if str(node) in mapped_pe_list:
                tasks = [i for i, x in enumerate(mapped_pe_list) if x == str(node)]
                offset_x = 0
                offset_y = 0.02
                task_count = 0
                for task in tasks:
                    task_count += 1
                    offset_x += 0.03
                    if task_count == 5:
                        task_count = 1
                        offset_x = 0.03
                        offset_y += 0.03
                    random.seed(task)
                    r = random.randrange(0, 255)
                    g = random.randrange(0, 255)
                    b = random.randrange(0, 255)
                    color = '#%02X%02X%02X' % (r, g, b)
                    circle = plt.Circle((location[0]/x_size+offset_x, location[1]/y_size+offset_y), 0.01, fc=color)
                    if Config.viz.frame_resolution >= 50:
                        plt.text(location[0]/x_size+offset_x, location[1]/y_size+offset_y-0.001, task)
                    plt.gca().add_patch(circle)
        fig.text(0.25, 0.02, "Iteration:" + str(counter), fontsize=35)
        plt.savefig("GraphDrawings/Mapping_Animation_Material/Mapping_Frame_"+str(counter).zfill(bound) + ".png",
                    dpi=Config.viz.frame_resolution)
        plt.clf()
        plt.close(fig)
        counter += 1
        line = mapping_process_file.readline()
    mapping_process_file.close()
    print ("\033[35m* VIZ::\033[0mMAPPING ANIMATION FRAMES READY AT: GraphDrawings/Mapping_Animation_Material")
    return None