# Copyright (C) Siavoosh Payandeh Azad

from ArchGraphUtilities import AG_Functions

def ReportGSNoCFriendlyReachabilityInFile (AG):
    ReachabilityFile = open("Generated_Files/GSNoC_RectangleFile.txt",'w')
    for Node in AG.nodes():
        NodeX, NodeY, NodeZ = AG_Functions.ReturnNodeLocation(Node)
        for Port in AG.node[Node]['Unreachable']:
            if Port == "S":
                Direction = "SOUTH"
            elif Port == "N":
                Direction = "NORTH"
            elif Port == "W":
                Direction = "WEST"
            elif Port == "E":
                Direction = "EAST"
            for Entry in AG.node[Node]['Unreachable'][Port]:
                ReachabilityFile.write( "["+str(NodeX)+","+str(NodeY)+","+str(NodeZ)+"] ")
                UnreachableArea = AG.node[Node]['Unreachable'][Port][Entry]
                if UnreachableArea[0] is not None:
                    UnreachableX, UnreachableY, UnreachableZ = AG_Functions.ReturnNodeLocation(UnreachableArea[0])
                    ReachabilityFile.write(str(Direction)+" NetLocCube(ll=["+str(UnreachableX)+","+str(UnreachableY)+
                                           ","+str(UnreachableZ)+"],")
                    UnreachableX, UnreachableY, UnreachableZ = AG_Functions.ReturnNodeLocation(UnreachableArea[1])
                    ReachabilityFile.write("ur=["+str(UnreachableX)+","+str(UnreachableY)+
                                           ","+str(UnreachableZ)+"])\n")
                else:
                    ReachabilityFile.write(str(Direction)+" NetLocCube(invalid)\n")
        ReachabilityFile.write("\n")
    ReachabilityFile.close()

def ReportReachability (AG):
    print "====================================="
    for Node in AG.nodes():
        print "NODE", Node, "UNREACHABLE NODES:"
        for Port in AG.node[Node]['Unreachable']:
            print "Port:", Port, " ==>", AG.node[Node]['Unreachable'][Port]

def ReportReachabilityInFile (AG,FileName):
    ReachabilityFile = open('Generated_Files/'+FileName+".txt",'w')
    for Node in AG.nodes():
        ReachabilityFile.write( "=====================================\n")
        ReachabilityFile.write( "NODE "+str(Node)+" UNREACHABLE NODES:\n")
        for Port in AG.node[Node]['Unreachable']:
            ReachabilityFile.write("Port: "+str(Port)+" ==> "+str(AG.node[Node]['Unreachable'][Port])+"\n")
    ReachabilityFile.close()