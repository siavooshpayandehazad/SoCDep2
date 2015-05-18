__author__ = 'siavoosh'
import networkx

def GenerateNoCRouteGraph(AG,SystemHealthMap,TurnModel):
    """
    This function takes the Architecture graph and the health status of the Architecture
    and generates the route graph... route graph is a graph that has all the paths available
    and we can find graph algorithms to find paths...
    :param AG: Architecture Graph
    :param SystemHealthMap: System Health Map
    :return: RouteGraph
    """

    # all the links that go inside the router are called in
    #              ___________________
    #             |       O    O      |
    #             |                  O|----> E out
    # W out <---- |O                  |
    #             |                  O|<---- E in
    #             |                   |
    #  W in ----> |O                  |
    #             |                 O/
    #             |_____O___O______O/


    print "STARTING BUILDING ROUTING ARCHITECTURE..."
    print "USING TURN MODE: ",TurnModel
    PortList=['N','W','L','E','S'] #the order is crucial... do not change
    NoCRG= networkx.DiGraph()
    for node in AG.nodes():
        print "GENERATING PORTS:"
        for port in PortList:
            print "\t",str(node)+str(port)+str('I'),"&",str(node)+str(port)+str('O')
            NoCRG.add_node(str(node)+str(port)+str('I'),Node=node,Port=port,Dir='I')
            NoCRG.add_node(str(node)+str(port)+str('O'),Node=node,Port=port,Dir='O')
        print "CONNECTING LOCAL PATHS:"
        for port in PortList:   #connect local to every output port
            if port != 'L':
                NoCRG.add_edge(str(node)+str('L')+str('I'),str(node)+str(port)+str('O'))
                print "\t",'L',"--->",port
                NoCRG.add_edge(str(node)+str(port)+str('I'),str(node)+str('L')+str('O'))
                print "\t",port,"--->",'L'
        print "CONNECTING DIRECT PATHS:"
        for i in range(0,int(len(PortList))): #connect direct paths
            if PortList[i] != 'L':
                print "\t",PortList[i],"--->",PortList[len(PortList)-1-i]
                inID= str(node)+str(PortList[i])+str('I')
                outID=str(node)+str(PortList[len(PortList)-1-i])+str('O')
                NoCRG.add_edge(inID,outID)

        print "CONNECTING TURNS:"
        for turn in TurnModel:
            if turn in SystemHealthMap.SHM.node[node]['TurnsHealth']:
                if SystemHealthMap.SHM.node[node]['TurnsHealth'][turn]:
                    InPort=turn[0]
                    OutPort=turn[2]
                    NoCRG.add_edge(str(node)+str(InPort)+str('I'),str(node)+str(OutPort)+str('O'))
                    print "\t",InPort,"--->",OutPort
        print "------------------------"

    for link in AG.edges(): # here we should connect connections between routers
        Port=AG.edge[link[0]][link[1]]['Port']
        if SystemHealthMap.SHM[link[0]][link[1]]['LinkHealth']:
            print "CONNECTING LINK:",link,"BY CONNECTING:",str(link[0])+str(Port[0])+str('-Out'),"TO:",\
                str(link[1])+str(Port[1])+str('-In')
            NoCRG.add_edge(str(link[0])+str(Port[0])+str('O'),str(link[1])+str(Port[1])+str('I'))
        else:
            print "BROKEN LINK:",link
    print "ROUTE GRAPH IS READY... "
    return NoCRG



def UpdateNoCRouteGraph(SystemHealthMap,NewEvent):
    """
     we would like to eliminate the path that is not working anymore...
    :param SystemHealthMap: System Health Map
    :param NewEvent: new fault that has happened...
    :return:
    """
    #ToDo
    return None


def FindRouteInRouteGraph(NoCRG,SourceNode,DestinationNode):
    """
    :param AG: Architecture graph
    :param SourceNode: Source node on AG
    :param DestinationNode: Destination node on AG
    :return: return a path (by name of links) on AG from source to destination if possible, None if not.
    """
    Source=str(SourceNode)+str('L')+str('I')
    Destination=str(DestinationNode)+str('L')+str('O')

    if networkx.has_path(NoCRG,Source,Destination):
        paths=networkx.shortest_path(NoCRG,Source,Destination)
        links=[]
        for i in range (0,len(paths)-1):
            if paths[i][0] != paths[i+1][0]:
                links.append((int(paths[i][0]),int(paths[i+1][0])))
        print "FINDIGN PATH FROM: ",Source,"TO:", Destination," ==>",links
        return links
    else:
        print "NO PATH FOUND FROM: ",Source,"TO:", Destination
        return None

