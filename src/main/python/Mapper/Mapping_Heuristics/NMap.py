# Copyright (C) 2015 Siavoosh Payandeh Azad

# Acknowledgement This mapping is based on "Bandwidth-Constrained Mapping of Cores onto NoC Architectures"
# paper by Srinivasan Murali and Giovanni De Micheli.

# On November 13th 2015, the following sections were added by Behrad Niazmand
# Swapping phase of NMAP algorithm

import copy, random
from TaskGraphUtilities import TG_Functions
from ArchGraphUtilities import AG_Functions
from Scheduler import Scheduler
from Mapper import Mapping_Functions
from RoutingAlgorithms import Calculate_Reachability
from networkx.classes.function import edges


def NMap (TG, AG, NoCRG, CriticalRG, NonCriticalRG, SHM, logging):
    """
    Performs NMap Mapping algorithm
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param NoCRG: NoC Routing Graph
    :param CriticalRG: NoC Routing Graph for Critical Region
    :param NonCriticalRG: NoC Routing Graph for Non-Critical Region
    :param SHM: System Health Map
    :param logging: logging File
    :return: TG and AG
    """
    print ("===========================================")
    print ("STARTING N-MAP MAPPING...\n")

    if len(TG.nodes()) > len(AG.nodes()):
        raise ValueError("Number of tasks should be smaller or equal to number of PEs")

    MappedTasks = []
    UnmappedTasks = copy.deepcopy(TG.nodes())
    AllocatedNodes =[]
    UnAllocatedNodes = copy.deepcopy(AG.nodes())

    # remove all broken nodes from UnAllocatedNodes list
    for node in UnAllocatedNodes:
        if not SHM.node[node]['NodeHealth']:
            UnAllocatedNodes.remove(node)
            print ("REMOVED BROKEN NODE "+str(node)+" FROM UN-ALLOCATED NODES")

    print ("------------------")
    print ("STEP 1:")
    # step 1: find the task with highest weighted communication volume
    TasksComDict = TG_Functions.tasks_communication_weight(TG)
    SortedTasksCom = sorted(TasksComDict, key=TasksComDict.get, reverse=True)
    print ("\t SORTED TASKS BY COMMUNICATION WEIGHT:\n"+"\t "+str(SortedTasksCom))
    print ("\t -------------")
    ChosenTask = SortedTasksCom[0]
    print ("\t CHOSEN TASK: "+str(ChosenTask))
    MappedTasks.append(ChosenTask)
    print ("\t ADDED TASK "+str(ChosenTask)+"TO MAPPED TASKS LIST")
    UnmappedTasks.remove(ChosenTask)
    print ("\t REMOVED TASK "+str(ChosenTask)+"FROM UN-MAPPED TASKS LIST")

    print ("------------------")
    print ("STEP 2:")
    NodeNeighborsDict = AG_Functions.node_neighbors(AG, SHM)
    SortedNodeNeighbors = sorted(NodeNeighborsDict, key=NodeNeighborsDict.get, reverse=True)
    MaxNeighborsNode = AG_Functions.max_node_neighbors(NodeNeighborsDict, SortedNodeNeighbors)
    print ("\t SORTED NODES BY NUMBER OF NEIGHBOURS:\n"+"\t "+str(SortedNodeNeighbors))
    print ("\t -------------")
    print ("\t NODES WITH MAX NEIGHBOURS:\t"+str(MaxNeighborsNode))
    ChosenNode = random.choice(MaxNeighborsNode)

    print ("\t CHOSEN NODE: "+str(ChosenNode))
    AllocatedNodes.append(ChosenNode)
    print ("\t ADDED NODE "+str(ChosenNode)+" TO ALLOCATED NODES LIST")
    UnAllocatedNodes.remove(ChosenNode)
    print ("\t REMOVED NODE "+str(ChosenNode)+" FROM UN-ALLOCATED NODES LIST")
    # Map Chosen Task on Chosen Node...
    if Mapping_Functions.MapTaskToNode(TG, AG, SHM, NoCRG, CriticalRG,
                                            NonCriticalRG, ChosenTask, ChosenNode, logging):
        print ("\t \033[32m* NOTE::\033[0mTASK "+str(ChosenTask)+" MAPPED ON NODE "+str(ChosenNode))
    else:
        raise ValueError("Mapping task on node failed...")

    print ("------------------")
    print ("STEP 3:")
    while len(UnmappedTasks) > 0:
        print ("\033[33m==>\033[0m  UN-MAPPED TASKS #: "+str(len(UnmappedTasks)))
        print ("\t -------------")
        print ("\t STEP 3.1:")
        # find the unmapped task which communicates most with MappedTasks
        MaxCom = 0
        UnmappedTasksCom = {}
        TasksWithMaxComToMapped = []
        for Task in UnmappedTasks:
            TaskWeight = 0
            for MappedTask in MappedTasks:
                if (Task, MappedTask) in TG.edges():
                    TaskWeight += TG.edge[Task][MappedTask]["ComWeight"]
                if (MappedTask, Task) in TG.edges():
                    TaskWeight += TG.edge[MappedTask][Task]["ComWeight"]
            UnmappedTasksCom[Task] = TaskWeight
            if MaxCom < TaskWeight:
                MaxCom = TaskWeight
                TasksWithMaxComToMapped = [Task]
            elif MaxCom == TaskWeight:
                TasksWithMaxComToMapped.append(Task)
        print ("\t MAX COMMUNICATION WITH THE MAPPED TASKS: "+str(MaxCom))
        print ("\t TASK(S) WITH MAX COMMUNICATION TO MAPPED TASKS: "+str(TasksWithMaxComToMapped))
        if len(TasksWithMaxComToMapped) > 1:
            # multiple tasks with same comm to mapped
            # Find the one that communicate most with Un-mapped takss...
            CandidTaskWithMaxComToUnMapped = []
            MaxCom = 0
            for CandidateTask in TasksWithMaxComToMapped:
                TaskWeight = 0
                for UnMappedTask in UnmappedTasks:
                    if (Task, UnMappedTask) in TG.edges():
                        TaskWeight += TG.edge[Task][UnMappedTask]["ComWeight"]
                    if (UnMappedTask, Task) in TG.edges():
                        TaskWeight += TG.edge[UnMappedTask][Task]["ComWeight"]
                if TaskWeight > MaxCom:
                    CandidTaskWithMaxComToUnMapped = [CandidateTask]
                elif TaskWeight == MaxCom:
                    CandidTaskWithMaxComToUnMapped.append(CandidateTask)
            print ("\t CANDIDATE TASK(S) THAT COMMUNICATE MOST WITH UN_MAPPED: "+str(CandidTaskWithMaxComToUnMapped))
            if len(CandidTaskWithMaxComToUnMapped) > 1:
                # if multiple tasks with the same com to unmmaped also,
                # choose randomly
                ChosenTask = random.choice(CandidTaskWithMaxComToUnMapped)
            else:
                ChosenTask = CandidTaskWithMaxComToUnMapped[0]
        else:
            ChosenTask = TasksWithMaxComToMapped[0]
        print ("\t CHOSEN TASK: "+str(ChosenTask))

        # Find the unallocated tile with lowest communication cost to/from the allocated_tiles_set.
        print ("\t -------------")
        print ("\t STEP 3.2:")
        MinCost = float("inf")
        NodeCandidates=[]
        for UnAllocatedNode in UnAllocatedNodes:
            Cost = 0
            Reachable = True
            for MappedTask in MappedTasks:
                ComWeight = 0
                if (ChosenTask, MappedTask) in TG.edges():
                    # print ("TASK CONNECTED TO MAPPED TASK:", MappedTask)
                    ComWeight += TG.edge[ChosenTask][MappedTask]["ComWeight"]
                    DestNode = TG.node[MappedTask]['Node']
                    # here we check if this node is even reachable from the chosen node?
                    if Calculate_Reachability.IsDestReachableFromSource(NoCRG, UnAllocatedNode, DestNode):
                        ManhatanDistance = AG_Functions.ManhattanDistance(UnAllocatedNode,DestNode)
                        Cost += ManhatanDistance * ComWeight
                    else:
                        Reachable = False
                elif (MappedTask, ChosenTask) in TG.edges():
                    # print ("TASK CONNECTED TO MAPPED TASK:", MappedTask)
                    ComWeight += TG.edge[MappedTask][ChosenTask]["ComWeight"]
                    DestNode = TG.node[MappedTask]['Node']
                    # here we check if this node is even reachable from the chosen node?
                    if Calculate_Reachability.IsDestReachableFromSource(NoCRG, DestNode, UnAllocatedNode):
                        ManhatanDistance = AG_Functions.ManhattanDistance(UnAllocatedNode, DestNode)
                        Cost += ManhatanDistance * ComWeight
                    else:
                        Reachable = False
            if Reachable:
                if Cost < MinCost:
                    NodeCandidates = [UnAllocatedNode]
                    MinCost = Cost
                elif Cost == MinCost:
                    NodeCandidates.append(UnAllocatedNode)
            else:
                print ("\t \033[33m* NOTE::\033[0m NODE "+str(UnAllocatedNode)+" CAN NOT REACH...")
                pass
        print ("\t CANDIDATE NODES: "+str(NodeCandidates)+" MIN COST: "+str(MinCost))

        if len(NodeCandidates) == 0:
            raise ValueError("COULD NOT FIND A REACHABLE CANDIDATE NODE...")
        elif len(NodeCandidates) > 1:
            ChosenNode = random.choice(NodeCandidates)
        elif len(NodeCandidates) == 1:
            ChosenNode = NodeCandidates[0]
        else:
            # this means that the chosen task is not connected to any other task... so its cost is infinity
            ChosenNode = random.choice(UnAllocatedNodes)

        MappedTasks.append(ChosenTask)
        print ("\t ADDED TASK "+str(ChosenTask)+" TO MAPPED TASKS LIST")
        UnmappedTasks.remove(ChosenTask)
        print ("\t REMOVED TASK "+str(ChosenTask)+" FROM UN-MAPPED TASKS LIST")

        AllocatedNodes.append(ChosenNode)
        print ("\t ADDED NODE "+str(ChosenNode)+" TO ALLOCATED NODES LIST")
        UnAllocatedNodes.remove(ChosenNode)
        print ("\t REMOVED NODE "+str(ChosenNode)+" FROM UN-ALLOCATED NODES LIST")

        if Mapping_Functions.MapTaskToNode(TG, AG, SHM, NoCRG, CriticalRG,
                                            NonCriticalRG, ChosenTask, ChosenNode, logging):
            print ("\t \033[32m* NOTE::\033[0mTASK "+str(ChosenTask)+" MAPPED ON NODE "+str(ChosenNode))
        else:
            raise ValueError("Mapping task on node failed...")

    # Added by Behrad (Still under development)
    # Swapping phase
    print "-----------------------"
    print "PHASE ONE IS DONE... STARTING SWAP PROCESS..."
    for node_id_1 in range(0 , len(AG.nodes())-1):
        for node_id_2 in range(node_id_1+1 , len(AG.nodes())-1):
            pass
            # Save current mapping in an array
            # Also save the mapping's csomm_cost in a variable
            CommCost = CalculateComCost(TG)

            # Swap (node_id_1 , node_id_2)
            SawpNodes(TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, node_id_1, node_id_2, logging)
            # Check and calculate communication cost for all communication flows in the task graph (which is equal to the total number of edges in the application graph
                # starting from the communication flow with the largest communication volume first
            CommCost_new = CalculateComCost(TG)
            # If comm_cost of current mapping is the same or bigger than the previous mapping, discard mapping
                # Revert back to previous mapping with better comm_cost
            # Else
                # Save new mapping as better mapping with less comm_cost
            if CommCost_new < CommCost:
                print "\033[32m* NOTE::\033[0m BETTER SOLUTION FOUND WITH COST:", CommCost_new
            else:
                pass
                #print "Reverting to old solution"
                SawpNodes(TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, node_id_2, node_id_1, logging)
            # Reset the comm_cost after each swapping

    # End of Swapping phase
    print "SWAP PROCESS FINISHED..."
    Scheduler.ScheduleAll(TG, AG, SHM, True, False, logging)
    return TG, AG


def CalculateComCost(TG):
    """
    Calculates the cost of the current mapping
    :param TG: Task Graph
    :return:  cost of the mapping
    """
    Cost = 0
    for Edge in TG.edges():
        T1 = Edge[0]
        T2 = Edge[1]
        Node1 = TG.node[T1]['Node']
        Node2 = TG.node[T2]['Node']
        ComWeight = TG.edge[Edge[0]][Edge[1]]["ComWeight"]
        ManhatanDistance = AG_Functions.ManhattanDistance(Node1, Node2)
        Cost += ManhatanDistance * ComWeight
    return Cost

def SawpNodes(TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, Node1, Node2, logging):
    """
    Swaps tasks of two nodes with each other!
    :param TG:  Task Graph
    :param AG:  Architecture Graph
    :param SHM: System Health Map
    :param NoCRG: NoC Routing Graph
    :param CriticalRG: NoC Routing Graph of Critical Region
    :param NonCriticalRG: NoC routing Graph of NonCritical Region
    :param Node1: first chosen node for swapping
    :param Node2:   2nd Chosen node for swapping
    :param logging: logging file
    :return: True if it successfully swaps two nodes tasks
    """
    if len(AG.node[Node1]['PE'].MappedTasks) == 0 or len(AG.node[Node2]['PE'].MappedTasks) == 0:
        raise ValueError("at least one of selected nodes for swapping doesnt have any tasks on it. ")

    Task_1 = AG.node[Node1]['PE'].MappedTasks[0]
    Task_2 = AG.node[Node2]['PE'].MappedTasks[0]
    Mapping_Functions.RemoveTaskFromNode(TG, AG, NoCRG, CriticalRG, NonCriticalRG, Task_1, Node1, logging)
    Mapping_Functions.RemoveTaskFromNode(TG, AG, NoCRG, CriticalRG, NonCriticalRG, Task_2, Node2, logging)
    if not Mapping_Functions.MapTaskToNode(TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, Task_1, Node2, logging):
        raise ValueError("SawpNodes FAILED WHILE TYING TO MAP FIRST CHOSEN TASK ON SECOND NODE ")
    if not Mapping_Functions.MapTaskToNode(TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, Task_2, Node1, logging):
        raise ValueError("SawpNodes FAILED WHILE TYING TO MAP SECOND CHOSEN TASK ON FIRST NODE ")
    return True