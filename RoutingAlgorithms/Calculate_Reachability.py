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
                    if not IsDestinationReachableViaPort(NoCRG,SourceNode,Port,DestinationNode,False,False):
                        #print "No Path From", SourceNode,Port,"To",DestinationNode
                        AG.node[SourceNode]['Unreachable'][Port].append(DestinationNode)

def ReportReachability (AG):
    for Node in AG.nodes():
        print "NODE",Node,"UNREACHABLE NODES:"
        for Port in AG.node[Node]['Unreachable']:
            print "Port:",Port," ==>",AG.node[Node]['Unreachable'][Port]

def ReportReachabilityInFile (AG,FileName):
    ReachabilityFile = open('Generated_Files/'+FileName+".txt",'w')
    for Node in AG.nodes():
        ReachabilityFile.write( "=====================================\n")
        ReachabilityFile.write( "NODE "+str(Node)+" UNREACHABLE NODES:\n")
        for Port in AG.node[Node]['Unreachable']:
            ReachabilityFile.write("Port: "+str(Port)+" ==> "+str(AG.node[Node]['Unreachable'][Port])+"\n")
    ReachabilityFile.close()

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
        return True
    else:
        if Report:print "\t\tNO PATH FOUND FROM: ", Source, "TO:", Destination
        return False