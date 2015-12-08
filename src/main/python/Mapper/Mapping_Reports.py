# Copyright (C) 2015 Siavoosh Payandeh Azad
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ConfigAndPackages import Config
from ArchGraphUtilities import AG_Functions
import random, networkx

def ReportMapping(AG, logging):
    """
    Reports mapping into log file
    :param AG: Architecture Graph
    :param logging: logging file
    :return: None
    """
    logging.info("===========================================")
    logging.info("      REPORTING MAPPING RESULT")
    logging.info("===========================================")
    for Node in AG.nodes():
        logging.info("NODE: "+str(Node)+" CONTAINS: "+str(AG.node[Node]['PE'].MappedTasks))
        logging.info("NODE: "+str(Node)+"'s Router CONTAINS: "+str(AG.node[Node]['Router'].MappedTasks))
    for link in AG.edges():
         logging.info("LINK: "+str(link)+" CONTAINS: "+str(AG.edge[link[0]][link[1]]['MappedTasks']))
    return None


def DrawMappingDistribution(AG, SHMU):
    """
    Draws mapping Task Number and Utilization Distribution
    :param AG: Architecture Graph
    :param SHMU: System health Monitoring Unit
    :return: None
    """
    print ("===========================================")
    print ("GENERATING MAPPING DISTRIBUTIONS VISUALIZATION...")
    fig_Num = plt.figure(figsize=(4*Config.Network_X_Size, 4*Config.Network_Y_Size))
    fig_Util = plt.figure(figsize=(4*Config.Network_X_Size, 4*Config.Network_Y_Size))
    MaxNumberOfTasks = 0
    MaxUtilization = 0
    for node in AG.nodes():
        MaxNumberOfTasks = max(len(AG.node[node]['PE'].MappedTasks), MaxNumberOfTasks)
        MaxUtilization = max(AG.node[node]['PE'].Utilization, MaxUtilization)

    for node in AG.nodes():
        Location = AG_Functions.return_node_location(node)
        XSize = float(Config.Network_X_Size)
        YSize = float(Config.Network_Y_Size)
        ZSize = float(Config.Network_Y_Size)
        Num = 255*len(AG.node[node]['PE'].MappedTasks)/float(MaxNumberOfTasks)
        Util = 255*AG.node[node]['PE'].Utilization/float(MaxUtilization)
        if SHMU.SHM.node[node]['NodeHealth']:
            if not AG.node[node]['PE'].Dark:
                color = '#%02X%02X%02X' % (255, 255-Num, 255-Num)
            else:
                color = 'gray'
        else:   # node is broken
            color = '#7B747B'
        fig_Num.gca().add_patch(patches.Rectangle((Location[0]/XSize+Location[2]/(ZSize*XSize**2),
                                                   Location[1]/YSize+Location[2]/(ZSize*YSize**2)),
                                                   width=0.15, height=0.15, facecolor=color,
                                                   edgecolor="black", linewidth=3, zorder=ZSize-Location[2]))
        if SHMU.SHM.node[node]['NodeHealth']:
            if not AG.node[node]['PE'].Dark:
                color = '#%02X%02X%02X' % (255, 255-Util, 255-Util)
            else:
                color = 'gray'
        else:   # node is broken
            color = '#7B747B'
        fig_Util.gca().add_patch(patches.Rectangle((Location[0]/XSize+Location[2]/(ZSize*XSize**2),
                                                    Location[1]/YSize+Location[2]/(ZSize*YSize**2)),
                                                    width=0.15, height=0.15, facecolor=color,
                                                    edgecolor="black", linewidth=3, zorder=ZSize-Location[2]))

    fig_Num.text(0.25, 0.03, 'Distribution of number of the tasks on the network', fontsize=15)
    fig_Util.text(0.25, 0.03, 'Distribution of utilization of network nodes', fontsize=15)
    fig_Num.savefig("GraphDrawings/Mapping_Num.png")
    fig_Util.savefig("GraphDrawings/Mapping_Util.png")
    fig_Num.clf()
    fig_Util.clf()
    plt.close(fig_Num)
    plt.close(fig_Util)
    print ("\033[35m* VIZ::\033[0mMAPPING UTILIZATION DISTRIBUTION DRAWING CREATED AT: GraphDrawings/Mapping_Util.png")
    print ("\033[35m* VIZ::\033[0mMAPPING TASK NUMBER DISTRIBUTION DRAWING CREATED AT: GraphDrawings/Mapping_Num.png")

    return None


def DrawMapping(TG, AG, SHMU):
    """
    This function draws the tasks on tiles of network. this would be very useful to check how our
    mapping optimization is acting...
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param SHMU: System Health Management Unit
    :return: None
    """
    print ("===========================================")
    print ("GENERATING MAPPING VISUALIZATION...")
    fig = plt.figure(figsize=(4*Config.Network_X_Size, 4*Config.Network_Y_Size))
    ColorList = []
    POS = {}
    XSize = float(Config.Network_X_Size)
    YSize = float(Config.Network_Y_Size)
    ZSize = float(Config.Network_Z_Size)
    NodeSize = 0.3
    StepSize = NodeSize * 1.08
    distance = StepSize * ZSize * 1.2
    for node in AG.nodes():
        Location = AG_Functions.return_node_location(node)
        if SHMU.SHM.node[node]['NodeHealth']:
            if not AG.node[node]['PE'].Dark:
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
            else:
                color = 'gray'
        else:   # node is broken
            color = '#7B747B'

        fig.gca().add_patch(patches.Rectangle(((distance*Location[0])+Location[2]*StepSize,
                                               (distance*Location[1])+Location[2]*StepSize),
                                                width=NodeSize, height=NodeSize, facecolor=color,
                                                linewidth=3, alpha=0.5))

        plt.text((distance*Location[0])+Location[2]*StepSize,
                 (distance*Location[1])+Location[2]*StepSize+NodeSize, str(node), fontsize=15)
        if Location[0] < XSize-1:
            X = distance*(Location[0])+Location[2]*StepSize+NodeSize
            Y = distance*(Location[1])+Location[2]*StepSize+(NodeSize/2)
            plt.plot([X, X+distance-NodeSize], [Y, Y], color='black', lw=3)
            # plt.gca().add_patch(patches.Arrow(X, Y, 1.0/XSize - 0.1, 0, width=0.01))
        if Location[1] < YSize-1:
            X = distance*(Location[0])+Location[2]*StepSize+(NodeSize/2)
            Y = distance*(Location[1])+Location[2]*StepSize+NodeSize
            # plt.plot([Y, Y], [X, X+1.0/XSize - 0.1], color ='black')
            plt.plot([X, X], [Y, Y+distance-NodeSize], color='black', lw=3)

        NumberOfTaskInRow = 4
        OffsetX = -(NodeSize/(2*NumberOfTaskInRow))
        OffsetY = NodeSize / (NumberOfTaskInRow+1)
        TaskCount = 0
        for task in AG.node[node]['PE'].MappedTasks:
            OffsetX += NodeSize / NumberOfTaskInRow
            if TaskCount == NumberOfTaskInRow:
                TaskCount = 0
                OffsetX = (NodeSize/(2*NumberOfTaskInRow))
                OffsetY += NodeSize / NumberOfTaskInRow
            random.seed(task)
            r = random.randrange(0, 255)
            g = random.randrange(0, 255)
            b = random.randrange(0, 255)
            color = '#%02X%02X%02X' % (r, g, b)
            ColorList.append(color)
            POS[task] = (distance*Location[0]+Location[2]*StepSize+OffsetX,
                         distance*Location[1]+Location[2]*StepSize+OffsetY)
            TaskCount += 1
    Tasksize = 800/Config.Network_Z_Size
    networkx.draw(TG, POS, with_labels=True, node_size=Tasksize, node_color=ColorList, width=0, alpha=0.5)
    fig.text(0.25, 0.02, 'Mapping visualization for network nodes', fontsize=15)

    plt.text(0, -NodeSize*2/3, 'X', fontsize=15)
    plt.text(-NodeSize*2/3, 0, 'Y', fontsize=15)
    plt.text(-NodeSize*2/3 + NodeSize/3, -NodeSize*2/3 + NodeSize/3, 'Z', fontsize=15)

    plt.gca().add_patch(patches.Arrow(-NodeSize*2/3, -NodeSize*2/3, NodeSize, 0, width=NodeSize/10))
    plt.gca().add_patch(patches.Arrow(-NodeSize*2/3, -NodeSize*2/3, NodeSize/3, NodeSize/3, width=NodeSize/10))
    plt.gca().add_patch(patches.Arrow(-NodeSize*2/3, -NodeSize*2/3, 0, NodeSize, width=NodeSize/10))

    fig.savefig("GraphDrawings/Mapping.png")
    plt.clf()
    plt.close(fig)
    print ("\033[35m* VIZ::\033[0mMAPPING DRAWING CREATED AT: GraphDrawings/Mapping.png")
    return None


def VizMappingOpt(CostFileName):
    """
    Visualizes the cost of solutions during local search mapping optimization process
    :param CostFileName: Name of the Cost File (Holds values of cost function for different mapping steps)
    :return: None
    """
    print ("===========================================")
    print ("GENERATING MAPPING OPTIMIZATION VISUALIZATIONS...")

    fig, ax1 = plt.subplots()

    try:
        MappingCostFile = open('Generated_Files/Internal/'+CostFileName+'.txt', 'r')
        Cost = []
        line = MappingCostFile.readline()
        MinCost = float(line)
        MinCostList = []
        MinCostList.append(MinCost)
        Cost.append(float(line))
        while line != "":
            Cost.append(float(line))
            if float(line) < MinCost:
                MinCost = float(line)
            MinCostList.append(MinCost)
            line = MappingCostFile.readline()
        SolutionNum = range(0,len(Cost))
        MappingCostFile.close()

        ax1.set_ylabel('Mapping Cost')
        ax1.set_xlabel('Iteration #')
        ax1.plot(SolutionNum, Cost, 'b', SolutionNum, MinCostList, 'r')

        if Config.Mapping_Function == 'IterativeLocalSearch':
            for Iteration in range(1, Config.IterativeLocalSearchIterations+1):
                x1 = x2 = Iteration * Config.LocalSearchIteration
                y1 = 0
                y2 = max(Cost)
                ax1.plot((x1, x2), (y1, y2), 'g')

    except IOError:
        print ('CAN NOT OPEN', CostFileName+'.txt')

    if Config.Mapping_Function == 'SimulatedAnnealing':
        try:
            SATempFile = open('Generated_Files/Internal/SATemp.txt', 'r')
            Temp = []
            line = SATempFile.readline()
            while line != '':
                Temp.append(float(line))
                line = SATempFile.readline()
            SATempFile.close()
            # print (len(Temp), len(SolutionNum))
            ax2 = ax1.twinx()
            ax2.plot(SolutionNum, Temp, 'g')
            ax2.set_ylabel('Temperature')
            for tl in ax2.get_yticklabels():
                tl.set_color('g')
        except IOError:
            print ('CAN NOT OPEN SATemp.txt')

    plt.savefig("GraphDrawings/Mapping_Opt_Process.png")
    plt.clf()
    plt.close(fig)
    print ("\033[35m* VIZ::\033[0mMAPPING OPTIMIZATION PROCESS GRAPH CREATED AT: GraphDrawings/Mapping_Opt_Process.png")
    return None


def VizCostSlope():
    """
    Visualises the mapping Cost slope for Simulated Annealing. This is like derivative of the cost graph.
    :return: None
    """
    print ("===========================================")
    print ("GENERATING MAPPING OPTIMIZATION COST SLOPE VISUALIZATION...")

    fig, ax1 = plt.subplots()
    try:
        CostSlopeFile = open('Generated_Files/Internal/SACostSlope.txt', 'r')
        CostSlope = []
        line = CostSlopeFile.readline()
        while line != '':
            CostSlope.append(float(line))
            line = CostSlopeFile.readline()
        CostSlopeFile.close()
        # print (len(Temp), len(SolutionNum))

        ax1.plot(range(0, len(CostSlope)), CostSlope)
        ax1.set_ylabel('Cost Slope')
        plt.savefig("GraphDrawings/Mapping_Cost_Slope.png")
        plt.clf()
        plt.close(fig)
        print ("\033[35m* VIZ::\033[0mSA COST SLOPE GRAPH CREATED AT: GraphDrawings/Mapping_Cost_Slope.png")
    except IOError:
            print ('CAN NOT OPEN SACostSlope.txt')

    return None


def VizHuangRace():
    """
    Visualizes The progress of Huang's cooling scheduling counters progress
    :return:    None
    """
    print ("===========================================")
    print ("GENERATING HUANG COUNTERS STATES VISUALIZATION...")
    fig, ax1 = plt.subplots()
    try:
        HuangRaceFile = open('Generated_Files/Internal/SAHuangRace.txt', 'r')
        Counter1 = []
        Counter2 = []
        line = HuangRaceFile.readline()
        while line != '':
            Counterlist = line.split()
            Counter1.append(Counterlist[0])
            Counter2.append(Counterlist[1])
            line = HuangRaceFile.readline()
        HuangRaceFile.close()

        ax1.plot(range(0, len(Counter1)), Counter1, 'b', range(0, len(Counter2)), Counter2, 'g')
        ax1.set_ylabel('Huang counters')
        plt.savefig("GraphDrawings/Mapping_HuangCounters.png", dpi=300)
        plt.clf()
        plt.close(fig)
        print ("\033[35m* VIZ::\033[0mSA HUANG COUNTERS GRAPH CREATED AT: GraphDrawings/Mapping_HuangCounters.png")
    except IOError:
            print ('CAN NOT OPEN SAHuangRace.txt')

    return None