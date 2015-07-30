# Copyright (C) 2015 Siavoosh Payandeh Azad 

import networkx
import random
from ConfigAndPackages import Config

def GenerateManualTG(Task_List,TG_Edge_List,Task_Criticality_List,Task_WCET_List,TG_Edge_Weight):
    print("PREPARING TASK GRAPH (TG)...")
    TG=networkx.DiGraph()
    Edge_Criticality_List=[]
    # IF both sender and receiver are critical then that transaction is critical
    for i in range(0,len(Task_List)):
        TG.add_node(Task_List[i], WCET=Task_WCET_List[i], Criticality=Task_Criticality_List[i],
                    Cluster=None, Node=None, Priority=None, Distance=None , Release=0)

    print "\tCALCULATING THE CRITICALITY OF LINKS..."
    GateWayEdges = []
    GatewayCounter = 0
    for edge in TG_Edge_List:
        if Task_Criticality_List[Task_List.index(edge[0])] == 'H' and Task_Criticality_List[Task_List.index(edge[1])] == 'H':
            Edge_Criticality_List.append('H')
        elif Task_Criticality_List[Task_List.index(edge[0])]=='H' and Task_Criticality_List[Task_List.index(edge[1])]=='L' :
            # gateway to Low
            GatewayNumber = len(Task_List)+GatewayCounter
            TG.add_node(GatewayNumber, WCET=1, Criticality= 'GNH',
                    Cluster=None, Node=None, Priority=None, Distance=None , Release=0)
            TG.add_edge(edge[0],GatewayNumber,Criticality = 'H', Link=[], ComWeight = TG_Edge_Weight[TG_Edge_List.index(edge)])
            TG.add_edge(GatewayNumber,edge[1],Criticality = 'L', Link=[], ComWeight = TG_Edge_Weight[TG_Edge_List.index(edge)])
            GateWayEdges.append(edge)
            GatewayCounter += 1

        elif Task_Criticality_List[Task_List.index(edge[0])]=='L' and Task_Criticality_List[Task_List.index(edge[1])]=='H' :
            # gateway to high
            GatewayNumber = len(Task_List)+GatewayCounter
            TG.add_node(GatewayNumber, WCET=1, Criticality= 'GH',
                    Cluster=None, Node=None, Priority=None, Distance=None , Release=0)
            TG.add_edge(edge[0],GatewayNumber, Criticality = 'L', Link=[], ComWeight = TG_Edge_Weight[TG_Edge_List.index(edge)])
            TG.add_edge(GatewayNumber,edge[1], Criticality = 'H', Link=[], ComWeight = TG_Edge_Weight[TG_Edge_List.index(edge)])
            GateWayEdges.append(edge)
            GatewayCounter += 1

        else:
            Edge_Criticality_List.append('L')
    print "\tLINKS CRITICALITY CALCULATED!"

    for edge in GateWayEdges:
        TG_Edge_List.remove(edge)

    for i in range(0,len(TG_Edge_List)):
        TG.add_edge(TG_Edge_List[i][0], TG_Edge_List[i][1], Criticality=Edge_Criticality_List[i], Link=[], ComWeight=TG_Edge_Weight[i])  # Communication weight
    AssignDistance(TG)
    print("TASK GRAPH (TG) IS READY...")
    return TG

def GenerateRandomTG(NumberOfTasks,NumberOfCriticalTasks,NumberOfEdges,WCET_Range,EdgeWeightRange):
    TG=networkx.DiGraph()
    print("PREPARING RANDOM TASK GRAPH (TG)...")

    Task_List=[]
    Task_Criticality_List=[]
    Task_WCET_List=[]
    TG_Edge_List=[]
    Edge_Criticality_List=[]
    TG_Edge_Weight=[]

    for i in range(0,NumberOfTasks):
        Task_List.append(i)
        Task_Criticality_List.append('L')
        Task_WCET_List.append(random.randrange(1,WCET_Range))

    Counter = 0
    while Counter < NumberOfCriticalTasks:
        ChosenTask = random.choice(Task_List)
        if Task_Criticality_List[ChosenTask] == 'L':
            Task_Criticality_List[ChosenTask] = 'H'
            Counter +=1

    for j in range(0,NumberOfEdges):
        SourceTask = random.choice(Task_List)
        DestTask = random.choice(Task_List)
        while SourceTask==DestTask:
            DestTask = random.choice(Task_List)

        if (SourceTask,DestTask) not in TG_Edge_List:
            TG_Edge_List.append((SourceTask,DestTask))
            TG_Edge_Weight.append(random.randrange(1,EdgeWeightRange))

    for i in range(0,len(Task_List)):
        TG.add_node(Task_List[i], WCET = Task_WCET_List[i], Criticality = Task_Criticality_List[i],
                    Cluster = None, Node = None, Priority = None, Distance=None ,Release = 0)

    print "\tCALCULATING THE CRITICALITY OF LINKS..."
    GateWayEdges = []
    GatewayCounter = 0
    for edge in TG_Edge_List:

        if Task_Criticality_List[Task_List.index(edge[0])] == 'H' and Task_Criticality_List[Task_List.index(edge[1])] == 'H':
            Edge_Criticality_List.append('H')
        elif Task_Criticality_List[Task_List.index(edge[0])]=='H' and Task_Criticality_List[Task_List.index(edge[1])]=='L' :
            # gateway to Low
            GatewayNumber = len(Task_List)+GatewayCounter
            TG.add_node(GatewayNumber, WCET=1, Criticality= 'GNH',
                    Cluster=None, Node=None, Priority=None, Distance=None , Release=0)
            if not networkx.has_path(TG,GatewayNumber,edge[0]):
                TG.add_edge(edge[0],GatewayNumber,Criticality = 'H', Link=[], ComWeight = TG_Edge_Weight[TG_Edge_List.index(edge)])
            if not networkx.has_path(TG,edge[1],GatewayNumber):
                TG.add_edge(GatewayNumber,edge[1],Criticality = 'L', Link=[], ComWeight = TG_Edge_Weight[TG_Edge_List.index(edge)])
            GateWayEdges.append(edge)
            GatewayCounter += 1
        elif Task_Criticality_List[Task_List.index(edge[0])]=='L' and Task_Criticality_List[Task_List.index(edge[1])]=='H' :
            # gateway to high
            GatewayNumber = len(Task_List)+GatewayCounter
            TG.add_node(GatewayNumber, WCET=1, Criticality= 'GH',
                    Cluster=None, Node=None, Priority=None, Distance=None , Release=0)
            if not networkx.has_path(TG,GatewayNumber,edge[0]):
                TG.add_edge(edge[0],GatewayNumber, Criticality = 'L', Link=[], ComWeight = TG_Edge_Weight[TG_Edge_List.index(edge)])
            if not networkx.has_path(TG,edge[1],GatewayNumber):
                TG.add_edge(GatewayNumber,edge[1], Criticality = 'H', Link=[], ComWeight = TG_Edge_Weight[TG_Edge_List.index(edge)])
            GateWayEdges.append(edge)
            GatewayCounter += 1
        else:
            Edge_Criticality_List.append('L')
    print "\tLINKS CRITICALITY CALCULATED!"

    for edge in GateWayEdges:
        TG_Edge_List.remove(edge)

    for i in range(0,len(TG_Edge_List)):
        # making sure that the graph is still acyclic
        if not networkx.has_path(TG,TG_Edge_List[i][1],TG_Edge_List[i][0]):
            TG.add_edge(TG_Edge_List[i][0],TG_Edge_List[i][1],Criticality=Edge_Criticality_List[i],
                        Link=[],ComWeight=TG_Edge_Weight[i])  # Communication weight
    AssignDistance(TG)
    print("TASK GRAPH (TG) IS READY...")
    return TG

def GenerateRandomIndependentTG(NumberOfTasks,WCET_Range,Release_Range):
    TG=networkx.DiGraph()
    print("PREPARING RANDOM TASK GRAPH (TG) WITH INDEPENDENT TASKS...")

    Task_List=[]
    Task_Criticality_List=[]
    Task_WCET_List=[]
    TG_Release_List= []
    for i in range(0,NumberOfTasks):
        Task_List.append(i)
        Task_Criticality_List.append('L')
        Counter = 0
        while Counter < Config.NumberOfCriticalTasks:
            ChosenTask = random.choice(Task_List)
            if Task_Criticality_List[ChosenTask] == 'L':
                Task_Criticality_List[ChosenTask] = 'H'
                Counter +=1
        Task_WCET_List.append(random.randrange(1,WCET_Range))
        TG_Release_List.append(random.randrange(0,Release_Range))
    for i in range(0,len(Task_List)):
        TG.add_node(Task_List[i], WCET=Task_WCET_List[i], Criticality=Task_Criticality_List[i],
                    Cluster=None, Node=None, Priority=None, Distance=None, Release=TG_Release_List[i])

    print("RANDOM TASK GRAPH (TG) WITH INDEPENDENT TASKS IS READY...")
    return TG

def FindSourceNodes(TG):
    """
    Takes a Task Graph and returns the source nodes of it in a list
    :param TG: Task Graph
    :return: List of source nodes
    """
    SourceNode=[]
    for Task in TG.nodes():
        if len(TG.predecessors(Task))==0:
            SourceNode.append(Task)
    return SourceNode

def AssignDistance(TG):
    print("ASSIGNING PRIORITIES TO TASK GRAPH (TG)...")
    SourceNodes=FindSourceNodes(TG)
    for Task in SourceNodes:
        TG.node[Task]['Distance']=0

    for Task in TG.nodes():
        distance=[]
        if Task not in SourceNodes:
            for Source in SourceNodes:
                if networkx.has_path(TG,Source,Task):
                    #ShortestPaths=networkx.shortest_path(TG,Source,Task)
                    #distance.append(len(ShortestPaths)-1)
                    for path in networkx.all_simple_paths(TG,Source,Task):
                        distance.append(len(path))
            TG.node[Task]['Distance']=max(distance)-1

########################################################
def GenerateTG():
    if Config.TG_Type=='RandomDependent':
        return GenerateRandomTG(Config.NumberOfTasks,Config.NumberOfCriticalTasks,Config.NumberOfEdges,
                                                     Config.WCET_Range,Config.WCET_Range)
    elif Config.TG_Type=='RandomIndependent':
        return GenerateRandomIndependentTG(Config.NumberOfTasks,Config.WCET_Range,Config.Release_Range)
    elif Config.TG_Type=='Manual':
        return GenerateManualTG(Config.Task_List,Config.TG_Edge_List,
                                                     Config.Task_Criticality_List,Config.Task_WCET_List,
                                                     Config.TG_Edge_Weight)
    else:
        raise ValueError('TG TYPE DOESNT EXIST...!!!')


########################################################

def CalculateMaxDistance(TG):
    MaxDistance = 0
    for Task in TG:
        if TG.node[Task]['Distance']> MaxDistance :
            MaxDistance = TG.node[Task]['Distance']
    return MaxDistance


def TasksCommunicationWeight(TG):
    """

    :param TG: Task graph
    :return: Returns a dictionary with task numbers as keys and total communication relevant to that task as value
    """
    TasksCom = {}
    for task in TG.nodes():
        TaskCom = 0
        for links in TG.edges():
            if task in links:
                TaskCom += TG.edge[links[0]][links[1]]["ComWeight"]
        TasksCom[task] = TaskCom

    return TasksCom