# Copyright (C) 2015 Siavoosh Payandeh Azad

from RoutingAlgorithms import Routing
from Scheduler import Scheduling_Functions
from ConfigAndPackages import Config
import statistics
import random
from math import ceil



def MakeInitialMapping(TG, CTG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, Report, logging):
    if Report: print ("===========================================")
    if Report: print ("STARTING INITIAL MAPPING...")
    Itteration=0
    for Cluster in CTG.nodes():
        DestNode = random.choice(AG.nodes())
        if Config.EnablePartitioning:
            while(CTG.node[Cluster]['Criticality']!= AG.node[DestNode]['Region']):
                DestNode = random.choice(AG.nodes())
        # print (CTG.node[Cluster]['Criticality'],AG.node[DestNode]['Region'])
        while not AddClusterToNode(TG, CTG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, Cluster, DestNode, logging):
            Itteration += 1
            DestNode = random.choice(AG.nodes())        # try another node
            if Config.EnablePartitioning:
                while(CTG.node[Cluster]['Criticality']!= AG.node[DestNode]['Region']):
                    DestNode = random.choice(AG.nodes())
            # print (CTG.node[Cluster]['Criticality'],AG.node[DestNode]['Region'])
            logging.info("\tMAPPING ATTEMPT: #"+str(Itteration+1)+"FOR CLUSTER:"+str(Cluster))
            if Itteration == 10*len(CTG.nodes()):
                if Report: print ("\033[33mWARNING::\033[0m INITIAL MAPPING FAILED... AFTER "+str(Itteration)+" ITERATIONS")
                logging.warning("INITIAL MAPPING FAILED...")
                ClearMapping(TG,CTG,AG)
                return False
        logging.info("MAPPED CLUSTER "+str(Cluster)+" ON NODE "+str(DestNode))
        Itteration = 0
    if Report: print ("INITIAL MAPPING READY... ")
    return True



def MapTaskToNode(TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, Task, Node, logging):
    if not SHM.SHM.node[Node]['NodeHealth']:
        logging.info("CAN NOT MAP ON BROKEN NODE: "+str(Node))
        return False
    logging.info( "\tADDING TASK:"+str(Task)+"TO NODE:"+str(Node))
    TG.node[Task]['Node'] = Node
    AG.node[Node]['PE'].MappedTasks.append(Task)
    AG.node[Node]['PE'].Utilization += TG.node[Task]['WCET']
    for Edge in TG.edges():
        if Task in Edge: # find all the edges that are connected to Task
            logging.info("\t\tEDGE:"+str(Edge)+"CONTAINS Task:"+str(Task))
            SourceNode=TG.node[Edge[0]]['Node']
            DestNode=TG.node[Edge[1]]['Node']
            if SourceNode is not None and DestNode is not None: # check if both ends of this edge is mapped
                if SourceNode != DestNode:
                    ListOfLinks, NumberOfPaths = Routing.FindRouteInRouteGraph(NoCRG, CriticalRG, NonCriticalRG,
                                                                SourceNode, DestNode, False) # Find the links to be used
                    # print NumberOfPaths, ListOfLinks
                    if ListOfLinks is not None:
                        logging.info("\t\t\tADDING PATH FROM NODE:"+str(SourceNode)+"TO NODE"+str(DestNode))
                        logging.info("\t\t\tLIST OF LINKS:"+str(ListOfLinks))
                        Counter = 0

                        if TG.edge[Edge[0]][Edge[1]]["Criticality"] == 'H':
                            Probability = 1         # we reserve the whole bandwidth for critical packets...
                        else:
                            Probability = 1.0/NumberOfPaths

                        for path in ListOfLinks:
                            for Link in path:
                                if Edge in AG.edge[Link[0]][Link[1]]['MappedTasks'].keys():
                                    AG.edge[Link[0]][Link[1]]['MappedTasks'][Edge].append((Counter, Probability))
                                    AG.node[Link[0]]['Router'].MappedTasks[Edge].append((Counter, Probability))
                                    logging.info("\t\t\t\tAdding Packet "+str(Edge)+" To Router:"+str(Link[0]))
                                else:
                                    AG.edge[Link[0]][Link[1]]['MappedTasks'][Edge] = [(Counter, Probability)]
                                    AG.node[Link[0]]['Router'].MappedTasks[Edge] = [(Counter, Probability)]
                                    logging.info("\t\t\t\tAdding Packet "+str(Edge)+" To Router:"+str(Link[0]))

                                AG.node[path[len(path)-1][1]]['Router'].MappedTasks[Edge] = [(Counter, Probability)]
                                logging.info("\t\t\t\tAdding Packet "+str(Edge)+" To Router:"+str(path[len(path)-1][1]))

                                EdgeListOfLinks = list(batch[1] for batch in TG.edge[Edge[0]][Edge[1]]['Link'])
                                if Link not in EdgeListOfLinks:
                                    TG.edge[Edge[0]][Edge[1]]['Link'].append((Counter, Link, Probability))

                            Counter += 1
                    else:
                        RemoveTaskFromNode(TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, Task, Node, logging)
                        logging.warning("\tNO PATH FOUND FROM "+str(SourceNode)+" TO "+str(DestNode)+"...")
                        print ("NO PATH FOUND FROM "+str(SourceNode)+" TO "+str(DestNode)+" ...")
                        return False
    return True


def RemoveTaskFromNode(TG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, Task, Node, logging):
    logging.info("\tREMOVING TASK:"+str(Task)+"FROM NODE:"+str(Node))
    for Edge in TG.edges():
        if Task in Edge:
            SourceNode = TG.node[Edge[0]]['Node']
            DestNode = TG.node[Edge[1]]['Node']
            if SourceNode is not None and DestNode is not None:
                if SourceNode != DestNode:
                    ListOfLinks, NumberOfPaths = Routing.FindRouteInRouteGraph(NoCRG, CriticalRG, NonCriticalRG,
                                                                SourceNode, DestNode, False) #Find the links to be used
                    if ListOfLinks is not None:
                        logging.info("\t\t\tREMOVING PATH FROM NODE:"+str(SourceNode)+"TO NODE"+str(DestNode))
                        logging.info("\t\t\tLIST OF LINKS:"+str(ListOfLinks))
                        for path in ListOfLinks:
                            for Link in path:
                                if Edge in AG.edge[Link[0]][Link[1]]['MappedTasks'].keys():
                                    del AG.edge[Link[0]][Link[1]]['MappedTasks'][Edge]
                                    del AG.node[Link[0]]['Router'].MappedTasks[Edge]
                                    logging.info("\t\t\t\tRemoving Packet "+str(Edge)+" To Router:"+str(Link[0]))
                                    for BatchAndLink in TG.edge[Edge[0]][Edge[1]]['Link']:
                                        if BatchAndLink[1] == Link:
                                            TG.edge[Edge[0]][Edge[1]]['Link'].remove(BatchAndLink)
                            del AG.node[path[len(path)-1][1]]['Router'].MappedTasks[Edge]
                            logging.info("\t\t\t\tRemoving Packet "+str(Edge)+" To Router:"+str(path[len(path)-1][1]))
                    else:
                        logging.warning("\tNOTHING TO BE REMOVED...")
    TG.node[Task]['Node'] = None
    AG.node[Node]['PE'].MappedTasks.remove(Task)
    AG.node[Node]['PE'].Utilization -= TG.node[Task]['WCET']
    return True


def AddClusterToNode(TG, CTG, AG, SHM, NoCRG, CriticalRG, NonCriticalRG, Cluster, Node, logging):
    if not SHM.SHM.node[Node]['NodeHealth']:
        logging.info("CAN NOT MAP ON BROKEN NODE: "+str(Node))
        return False

    # Adding The cluster to Node...
    logging.info( "\tADDING CLUSTER:"+str(Cluster)+"TO NODE:"+str(Node))
    CTG.node[Cluster]['Node'] = Node
    for Task in CTG.node[Cluster]['TaskList']:
        TG.node[Task]['Node'] = Node
        AG.node[Node]['PE'].MappedTasks.append(Task)
    AG.node[Node]['PE'].Utilization += CTG.node[Cluster]['Utilization']

    for Edge in CTG.edges():
        if Cluster in Edge: # find all the edges that are connected to Cluster
            logging.info("\t\tEDGE:"+str(Edge)+"CONTAINS CLUSTER:"+str(Cluster))
            SourceNode=CTG.node[Edge[0]]['Node']
            DestNode=CTG.node[Edge[1]]['Node']
            if SourceNode is not None and DestNode is not None: # check if both ends of this edge is mapped
                if SourceNode != DestNode:
                    ListOfLinks, NumberOfPaths = Routing.FindRouteInRouteGraph(NoCRG, CriticalRG, NonCriticalRG,
                                                                               SourceNode, DestNode,
                                                                               False) # Find the links to be used
                    ListOfEdges = []
                    # print ("NumberOfPaths:", NumberOfPaths)
                    # print NumberOfPaths, ListOfLinks
                    if ListOfLinks is not None:
                            #find all the edges in TaskGraph that contribute to this edge in CTG
                            for edge in TG.edges():
                                if TG.node[edge[0]]['Cluster'] == Edge[0] and TG.node[edge[1]]['Cluster'] == Edge[1]:
                                    ListOfEdges.append(edge)

                    #print ("LIST OF LINKS:", ListOfLinks)
                    # add edges from list of edges to all links from list of links
                    # todo: I have to think more... this is not enough to add all the links there...
                    if ListOfLinks is not None and len(ListOfEdges) > 0:
                        logging.info("\t\t\tADDING PATH FROM NODE:"+str(SourceNode)+"TO NODE"+str(DestNode))
                        logging.info("\t\t\tLIST OF LINKS:"+str(ListOfLinks))
                        logging.info("\t\t\tLIST OF EDGES:"+str(ListOfEdges))
                        Counter = 0
                        for path in ListOfLinks:
                            for Link in path:
                                for Edge in ListOfEdges:
                                    if TG.edge[Edge[0]][Edge[1]]["Criticality"] == 'H':
                                        Probability = 1         # we reserve the whole bandwidth for critical packets...
                                    else:
                                        Probability = 1.0/NumberOfPaths

                                    if Edge in AG.edge[Link[0]][Link[1]]['MappedTasks'].keys():
                                        AG.edge[Link[0]][Link[1]]['MappedTasks'][Edge].append((Counter, Probability))
                                        AG.node[Link[0]]['Router'].MappedTasks[Edge].append((Counter, Probability))
                                        logging.info("\t\t\t\tAdding Packet "+str(Edge)+" To Router:"+str(Link[0]))
                                    else:
                                        AG.edge[Link[0]][Link[1]]['MappedTasks'][Edge] = [(Counter, Probability)]
                                        AG.node[Link[0]]['Router'].MappedTasks[Edge] = [(Counter, Probability)]
                                        logging.info("\t\t\t\tAdding Packet "+str(Edge)+" To Router:"+str(Link[0]))
                                    EdgeListOfLinks = list(batch[1] for batch in TG.edge[Edge[0]][Edge[1]]['Link'])
                                    if Link not in EdgeListOfLinks:
                                        TG.edge[Edge[0]][Edge[1]]['Link'].append((Counter, Link, Probability))

                            for Edge in ListOfEdges:
                                if TG.edge[Edge[0]][Edge[1]]["Criticality"] == 'H':
                                    Probability = 1         # we reserve the whole bandwidth for critical packets...
                                else:
                                    Probability = 1.0/NumberOfPaths
                                AG.node[path[len(path)-1][1]]['Router'].MappedTasks[Edge] = [(Counter, Probability)]
                                logging.info("\t\t\t\tAdding Packet "+str(Edge)+" To Router:"+str(path[len(path)-1][1]))

                            Counter += 1
                    else:
                        logging.warning( "\tNO PATH FOUND FROM SOURCE TO DESTINATION...")
                        logging.info("REMOVING ALL THE MAPPED CONNECTIONS FOR CLUSTER "+str(Cluster))
                        RemoveClusterFromNode(TG, CTG, AG, NoCRG, CriticalRG, NonCriticalRG, Cluster, Node, logging)
                        return False
    return True


def RemoveClusterFromNode(TG, CTG, AG, NoCRG, CriticalRG, NonCriticalRG, Cluster, Node, logging):
    logging.info("\tREMOVING CLUSTER:"+str(Cluster)+"FROM NODE:"+str(Node))
    for Edge in CTG.edges():
        if Cluster in Edge: # find all the edges that are connected to Cluster
            SourceNode = CTG.node[Edge[0]]['Node']
            DestNode = CTG.node[Edge[1]]['Node']
            if SourceNode is not None and DestNode is not None: #check if both ends of this edge is mapped
                if SourceNode != DestNode:
                    #Find the links to be used
                    ListOfLinks, NumberOfPaths = Routing.FindRouteInRouteGraph(NoCRG, CriticalRG, NonCriticalRG,
                                                                               SourceNode, DestNode, False)
                    ListOfEdges = []
                    if ListOfLinks is not None:
                        for edge in TG.edges(): #find all the edges in TaskGraph that contribute to this edge in CTG
                            if TG.node[edge[0]]['Cluster'] == Edge[0] and TG.node[edge[1]]['Cluster'] == Edge[1]:
                                ListOfEdges.append(edge)

                    # remove edges from list of edges to all links from list of links
                    if ListOfLinks is not None and len(ListOfEdges) > 0:
                        logging.info("\t\t\tREMOVING PATH FROM NODE:"+str(SourceNode)+"TO NODE"+str(DestNode))
                        logging.info("\t\t\tLIST OF LINKS:"+str(ListOfLinks))
                        logging.info("\t\t\tLIST OF EDGES:"+str(ListOfEdges))
                        for path in ListOfLinks:
                            for Link in path:
                                for Edge in ListOfEdges:
                                    if Edge in AG.edge[Link[0]][Link[1]]['MappedTasks'].keys():
                                        del AG.edge[Link[0]][Link[1]]['MappedTasks'][Edge]
                                        del AG.node[Link[0]]['Router'].MappedTasks[Edge]
                                        logging.info("\t\t\t\tRemoving Packet "+str(Edge)+" To Router:"+str(Link[0]))
                                        for LinkAndBatch in TG.edge[Edge[0]][Edge[1]]['Link']:
                                            if LinkAndBatch[1] == Link:
                                                TG.edge[Edge[0]][Edge[1]]['Link'].remove(LinkAndBatch)
                            for Edge in ListOfEdges:
                                del AG.node[path[len(path)-1][1]]['Router'].MappedTasks[Edge]
                                logging.info("\t\t\t\tRemoving Packet "+str(Edge)+" To Router:"+str(path[len(path)-1][1]))
                    else:
                        logging.warning("\tNOTHING TO BE REMOVED...")
    CTG.node[Cluster]['Node'] = None
    for Task in CTG.node[Cluster]['TaskList']:
        TG.node[Task]['Node'] = None
        AG.node[Node]['PE'].MappedTasks.remove(Task)
    AG.node[Node]['PE'].Utilization -= CTG.node[Cluster]['Utilization']
    return True


def ClearMapping(TG, CTG, AG):
    for node in TG.nodes():
        TG.node[node]['Node'] = None
    for Edge in TG.edges():
        TG.edge[Edge[0]][Edge[1]]['Link'] = []
    for cluster in CTG.nodes():
        CTG.node[cluster]['Node'] = None
    for node in AG.nodes():
        AG.node[node]['PE'].MappedTasks = []
        AG.node[node]['PE'].Utilization = 0
        AG.node[node]['PE'].Scheduling = {}

        AG.node[node]['Router'].Scheduling = {}
        AG.node[node]['Router'].MappedTasks = {}

    for link in AG.edges():
        AG.edge[link[0]][link[1]]['MappedTasks'] = {}
        AG.edge[link[0]][link[1]]['Scheduling'] = {}
    return True


def CostFunction(TG, AG, SHM, Report, InitialMappingString = None):
    NodeMakeSpanList = []
    LinkMakeSpanList = []
    for Node in AG.nodes():
        if SHM.SHM.node[Node]['NodeHealth']:
            NodeMakeSpanList.append(Scheduling_Functions.FindLastAllocatedTimeOnNode(TG, AG, Node, logging=None))
    for link in AG.edges():
        if SHM.SHM.edge[link[0]][link[1]]['LinkHealth']:
            LinkMakeSpanList.append(Scheduling_Functions.FindLastAllocatedTimeOnLink(TG, AG, link, logging=None))
    NodeMakeSpan_Stdev = statistics.stdev(NodeMakeSpanList)
    NodeMakeSpan_Max = max(NodeMakeSpanList)
    LinkMakeSpan_Stdev = statistics.stdev(LinkMakeSpanList)
    LinkMakeSpan_Max = max(LinkMakeSpanList)

    if Config.Mapping_CostFunctionType == 'SD':
        Cost = NodeMakeSpan_Stdev + LinkMakeSpan_Stdev
    elif Config.Mapping_CostFunctionType == 'SD+MAX' :
        Cost = NodeMakeSpan_Max + NodeMakeSpan_Stdev + LinkMakeSpan_Stdev + LinkMakeSpan_Max
    elif Config.Mapping_CostFunctionType == 'MAX' :
        Cost = NodeMakeSpan_Max + LinkMakeSpan_Max
    elif Config.Mapping_CostFunctionType == 'CONSTANT':
        Cost = 1
    else:
        raise ValueError("Mapping_CostFunctionType is not valid")

    Distance = None
    if InitialMappingString is not None:
        Distance = HammingDistanceOfMapping(InitialMappingString,MappingIntoString(TG))
        Cost += Distance
    if Report:
        print ("===========================================")
        print ("      REPORTING MAPPING COST")
        print ("===========================================")
        print ("NODES MAKE SPAN MAX:"+str(NodeMakeSpan_Max))
        print ("NODES MAKE SPAN STANDARD DEVIATION:"+str(NodeMakeSpan_Stdev))
        print ("LINKS MAKE SPAN MAX:"+str(LinkMakeSpan_Max))
        print ("LINKS MAKE SPAN STANDARD DEVIATION:"+str(LinkMakeSpan_Stdev))
        if Distance is not None:
            print ("DISTANCE FROM STARTING SOLUTION:"+str(Distance))
        print ("MAPPING SCHEDULING COST:"+str(Cost))

    if Cost == 0:
            raise ValueError("Mapping with 0 cost... Something is wrong here...")
    return Cost


def CalculateReliabilityCost(TG, NoCRG, logging):
    # todo...
    Cost = 0
    for edge in TG.edges():
        Node1 = TG.node[edge[0]]['Node']
        Node2 = TG.node[edge[1]]['Node']
        logging.info("PACKET FROM NODE "+str(Node1)+"TO NODE "+str(Node2))

    return Cost

def FindUnMappedTaskWithSmallestWCET(TG, logging):
    ShortestTasks = []
    SmallestWCET = Config.WCET_Range
    for Node in TG.nodes():
        if TG.node[Node]['Node'] is None:
            if TG.node[Node]['WCET'] < SmallestWCET:
                SmallestWCET= TG.node[Node]['WCET']
    logging.info("THE SHORTEST WCET OF UNMAPPED TASKS IS:"+str(SmallestWCET))
    for Nodes in TG.nodes():
        if TG.node[Nodes]['Node'] is None:
            if TG.node[Nodes]['WCET'] == SmallestWCET:
                ShortestTasks.append(Nodes)
    logging.info("THE LIST OF SHORTEST UNMAPPED TASKS:"+str(ShortestTasks))
    return ShortestTasks


def FindUnMappedTaskWithBiggestWCET(TG, logging):
    LongestTasks = []
    BiggestWCET = 0
    for Node in TG.nodes():
        if TG.node[Node]['Node'] is None:
            if TG.node[Node]['WCET'] > BiggestWCET:
                BiggestWCET= TG.node[Node]['WCET']
    logging.info("THE LONGEST WCET OF UNMAPPED TASKS IS:"+str(BiggestWCET))
    for Nodes in TG.nodes():
        if TG.node[Nodes]['Node'] is None:
            if TG.node[Nodes]['WCET'] == BiggestWCET:
                LongestTasks.append(Nodes)
    logging.info("THE LIST OF LONGEST UNMAPPED TASKS:"+str(LongestTasks))
    return LongestTasks


def FindNodeWithSmallestCompletionTime(AG, TG, SHM, Task):
    """
    THIS FUNCTION CAN BE STRICTLY USED FOR INDEPENDENT TGs
    :param AG: Arch Graph
    :param TG: Task Graph
    :param SHM: System Health Monitor
    :param Task: Task number
    :return: list of nodes with smallest completion time for Task
    """
    NodesWithSmallestCT = []
    RandomNode = random.choice(AG.nodes())
    while not SHM.SHM.node[RandomNode]['NodeHealth']:
        RandomNode = random.choice(AG.nodes())
    NodeSpeedDown = 1+((100.0-SHM.SHM.node[RandomNode]['NodeSpeed'])/100)
    TaskExecutionOnNode = TG.node[Task]['WCET']*NodeSpeedDown
    LastAllocatedTimeOnNode = Scheduling_Functions.FindLastAllocatedTimeOnNode(TG, AG, RandomNode, False)
    if LastAllocatedTimeOnNode < TG.node[Task]['Release']:
        SmallestCompletionTime = TG.node[Task]['Release'] + TaskExecutionOnNode
    else:
        SmallestCompletionTime = LastAllocatedTimeOnNode + TaskExecutionOnNode
    for Node in AG.nodes():
        if SHM.SHM.node[Node]['NodeHealth']:
            NodeSpeedDown = 1+((100.0-SHM.SHM.node[Node]['NodeSpeed'])/100)
            TaskExecutionOnNode = TG.node[Task]['WCET']*NodeSpeedDown
            LastAllocatedTimeOnNode = Scheduling_Functions.FindLastAllocatedTimeOnNode(TG, AG, Node, False)
            if LastAllocatedTimeOnNode < TG.node[Task]['Release']:
                CompletionOnNode = TG.node[Task]['Release'] + TaskExecutionOnNode
            else:
                CompletionOnNode = LastAllocatedTimeOnNode + TaskExecutionOnNode

            if ceil(CompletionOnNode) < SmallestCompletionTime:
                SmallestCompletionTime = CompletionOnNode
    for Node in AG.nodes():
        if SHM.SHM.node[Node]['NodeHealth']:
            NodeSpeedDown = 1+((100.0-SHM.SHM.node[Node]['NodeSpeed'])/100)
            LastAllocatedTimeOnNode = Scheduling_Functions.FindLastAllocatedTimeOnNode(TG, AG, Node, False)
            TaskExecutionOnNode = TG.node[Task]['WCET']*NodeSpeedDown
            CompletionOnNode = 0
            if LastAllocatedTimeOnNode < TG.node[Task]['Release']:
                CompletionOnNode = TG.node[Task]['Release']+TaskExecutionOnNode
            else:
                CompletionOnNode = LastAllocatedTimeOnNode+TaskExecutionOnNode
            if CompletionOnNode == SmallestCompletionTime:
                NodesWithSmallestCT.append(Node)
    return NodesWithSmallestCT


def FindFastestNodes(AG, SHM, TaskToBeMapped):
    # todo: we need to add some accelerator nodes which have some specific purpose and
    # enable different tasks to behave differently on them.
    FastestNodes = []
    MaxSpeedup = 0
    for Node in AG.nodes():
        if SHM.SHM.node[Node]['NodeSpeed'] > MaxSpeedup:
            MaxSpeedup = SHM.SHM.node[Node]['NodeSpeed']
    for Node in AG.nodes():
        if SHM.SHM.node[Node]['NodeSpeed'] == MaxSpeedup:
            FastestNodes.append(Node)
    return FastestNodes


def MappingIntoString(TG):
    """
    Takes a Mapped Task Graph and returns a string which contains the mapping information
    :param TG: Task Graph
    :return: A string containing mapping information
    """
    MappingString = ""
    for Task in TG.nodes():
        MappingString += str(TG.node[Task]['Node']) + " "
    return MappingString


def HammingDistanceOfMapping(MappingString1, MappingString2):
    if type(MappingString1) is str and type(MappingString2) is str:
        Str1_List = MappingString1.split()
        Str2_List = MappingString2.split()

        if len(Str1_List) == len(Str2_List):
            distance = 0
            for i in range(0, len(Str1_List)):
                if Str2_List[i] != Str1_List[i]:
                    distance += 1
            return distance
        else:
            raise ValueError("Mapping strings are from different length")
    else:
        raise ValueError("The input mapping strings are of wrong types")