# Copyright (C) Siavoosh Payandeh Azad

from Routing import FindRouteInRouteGraph
import networkx,re

def CalculateReachability (AG,NoCRG):
    PortList = ['N','E','W','S']
    for SourceNode in AG.nodes():
        for Port in PortList:
            AG.node[SourceNode]['Unreachable'][Port]=[]
        for DestinationNode in AG.nodes():
            if SourceNode != DestinationNode:
                for Port in PortList:
                    if IsDestinationReachableViaPort(NoCRG,SourceNode,Port,DestinationNode,False,False) is None:
                        #print "No Path From", SourceNode,Port,"To",DestinationNode
                        AG.node[SourceNode]['Unreachable'][Port].append(DestinationNode)


def ReportReachability (AG):
    for Node in AG.nodes():
        print "NODE",Node,"UNREACHABLE NODES:"
        for Port in AG.node[Node]['Unreachable']:
            print "Port:",Port," ==>",AG.node[Node]['Unreachable'][Port]


def IsDestinationReachableViaPort(NoCRG,SourceNode,Port,DestinationNode,ReturnAllPaths,Report):
    """
    :param NoCRG: NoC Routing Graph
    :param SourceNode: Source node on AG
    :param DestinationNode: Destination node on AG
    :param ReturnAllPaths: boolean that decides to return shortest path or all the paths between two nodes
    :return: return a path (by name of links) on AG from source to destination if possible, None if not.
    """
    Source = str(SourceNode) + str(Port) + str('O')
    Destination = str(DestinationNode) + str('L') + str('O')
    if networkx.has_path(NoCRG,Source,Destination):
        ShortestPath = networkx.shortest_path(NoCRG,Source,Destination)
        AllPaths = list(networkx.all_simple_paths(NoCRG,Source,Destination))
        ShortestLinks = []
        for i in range (0,len(ShortestPath)-1):
            #if ShortestPath[i][0] != ShortestPath[i+1][0]:
            if int(re.search(r'\d+', ShortestPath[i]).group()) != int(re.search(r'\d+', ShortestPath[i+1]).group()):
                ShortestLinks.append((int(re.search(r'\d+', ShortestPath[i]).group()),int(re.search(r'\d+', ShortestPath[i+1]).group())))
        AllLinks = []
        for j in range(0, len(AllPaths)):
            Path = AllPaths[j]
            Links = []
            for i in range (0,len(Path)-1):
                #print Path[i],Path[i+1]
                #print int(re.search(r'\d+', Path[i]).group()), int(re.search(r'\d+', Path[i+1]).group())
                if int(re.search(r'\d+', Path[i]).group()) != int(re.search(r'\d+', Path[i+1]).group()):
                    Links.append((int(re.search(r'\d+', Path[i]).group()),int(re.search(r'\d+', Path[i+1]).group())))
            AllLinks.append(Links)
        if Report:print "\t\tFINDING PATH(S) FROM: ", Source, "TO:", Destination," ==>", AllLinks if ReturnAllPaths else ShortestLinks
        if ReturnAllPaths:
            return AllLinks
        else:
            return ShortestLinks
    else:
        if Report:print "\t\tNO PATH FOUND FROM: ", Source, "TO:", Destination
        return None