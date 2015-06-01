__author__ = 'siavoosh'
import networkx

def GenerateNoCRouteGraph(AG,SystemHealthMap,TurnModel,Report):
    """
    This function takes the Architecture graph and the health status of the Architecture
    and generates the route graph... route graph is a graph that has all the paths available
    and we can find graph algorithms to find paths...
    :param AG: Architecture Graph
    :param SystemHealthMap: System Health Map
    :return: RouteGraph
    """

    # ACKNOWLEDGEMENT The Routing Graph is based on the idea from Thilo Kogge's Master Thesis

    # all the links that go inside the router are called in
    #
    #              _______|____|______
    #             |       O    I      |
    #             |                  O|----> E out
    # W in ---->  |I                  |
    #             |                  I|<---- E in
    #             |                   |
    # W out <---- |O                  |
    #             |                 O/
    #             |_____I___O______I/
    #                   |   |
    #
    # the turns should be named with port 2 port naming convention...
    # E2N is a turn that connects input of East port of the router to
    # output of north

    print "STARTING BUILDING ROUTING ARCHITECTURE..."
    ReportTurnModel(TurnModel)
    PortList=['N','W','L','E','S'] #the order is crucial... do not change
    NoCRG= networkx.DiGraph()
    for node in AG.nodes():
        if Report:print "GENERATING PORTS:"
        for port in PortList:
            if Report:print "\t",str(node)+str(port)+str('I'),"&",str(node)+str(port)+str('O')
            NoCRG.add_node(str(node)+str(port)+str('I'),Node=node,Port=port,Dir='I')
            NoCRG.add_node(str(node)+str(port)+str('O'),Node=node,Port=port,Dir='O')
        if Report:print "CONNECTING LOCAL PATHS:"
        for port in PortList:   #connect local to every output port
            if port != 'L':
                NoCRG.add_edge(str(node)+str('L')+str('I'),str(node)+str(port)+str('O'))
                if Report:print "\t",'L',"--->",port
                NoCRG.add_edge(str(node)+str(port)+str('I'),str(node)+str('L')+str('O'))
                if Report:print "\t",port,"--->",'L'
        if Report:print "CONNECTING DIRECT PATHS:"
        for i in range(0,int(len(PortList))): #connect direct paths
            if PortList[i] != 'L':
                if Report:print "\t",PortList[i],"--->",PortList[len(PortList)-1-i]
                inID= str(node)+str(PortList[i])+str('I')
                outID=str(node)+str(PortList[len(PortList)-1-i])+str('O')
                NoCRG.add_edge(inID,outID)

        if Report:print "CONNECTING TURNS:"
        for turn in TurnModel:
            if turn in SystemHealthMap.SHM.node[node]['TurnsHealth']:
                if SystemHealthMap.SHM.node[node]['TurnsHealth'][turn]:
                    InPort=turn[0]
                    OutPort=turn[2]
                    if InPort != OutPort:
                        NoCRG.add_edge(str(node)+str(InPort)+str('I'),str(node)+str(OutPort)+str('O'))
                    else: #just for defensive programming reasons...
                        print "\033[31mERROR::\033[0m U-TURN DETECTED!"
                        print "TERMINATING THE PROGRAM..."
                        print "HINT: CHECK YOUR TURN MODEL!"
                        return False
                    if Report:print "\t",InPort,"--->",OutPort
        if Report:print "------------------------"

    for link in AG.edges(): # here we should connect connections between routers
        Port=AG.edge[link[0]][link[1]]['Port']
        if SystemHealthMap.SHM[link[0]][link[1]]['LinkHealth']:
            if Report:print "CONNECTING LINK:",link,"BY CONNECTING:",str(link[0])+str(Port[0])+str('-Out'),"TO:",\
                str(link[1])+str(Port[1])+str('-In')
            NoCRG.add_edge(str(link[0])+str(Port[0])+str('O'),str(link[1])+str(Port[1])+str('I'))
        else:
            if Report:print "BROKEN LINK:",link
    print "ROUTE GRAPH IS READY... "
    return NoCRG

def ReportTurnModel(TurnModel):
    print "\tUSING TURN MODE: ",TurnModel
    print "\tPREPARING VISUALIZATION OF TURN MODEL..."
    print  "\t",unichr(0x2197) if "S2E" in TurnModel else "\033[31m"+unichr(0x2197)+"\033[0m",\
           unichr(0x2198) if "W2S" in TurnModel else "\033[31m"+unichr(0x2198)+"\033[0m","\t"\
           ,unichr(0x2199) if "E2S" in TurnModel else "\033[31m"+unichr(0x2199)+"\033[0m",\
           unichr(0x2196) if "S2W" in TurnModel else "\033[31m"+unichr(0x2196)+"\033[0m"

    print   "\t",unichr(0x2196) if "E2N" in TurnModel else "\033[31m"+unichr(0x2196)+"\033[0m"\
            ,unichr(0x2199) if "N2W" in TurnModel else "\033[31m"+unichr(0x2199)+"\033[0m","\t"\
            ,unichr(0x2198) if "N2E" in TurnModel else "\033[31m"+unichr(0x2198)+"\033[0m"\
            ,unichr(0x2197) if "W2N" in TurnModel else "\033[31m"+unichr(0x2197)+"\033[0m"
    print "\t","---------------------------"
    return None

def UpdateNoCRouteGraph(SystemHealthMap,NewEvent):
    """
     we would like to eliminate the path that is not working anymore...
    :param SystemHealthMap: System Health Map
    :param NewEvent: new fault that has happened...
    :return:
    """
    #ToDo
    return None


def FindRouteInRouteGraph(NoCRG,SourceNode,DestinationNode,Report):
    """
    :param NoCRG:
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
        if Report:print "\t\tFINDING PATH FROM: ",Source,"TO:", Destination," ==>",links
        return links
    else:
        if Report:print "\t\tNO PATH FOUND FROM: ",Source,"TO:", Destination
        return None