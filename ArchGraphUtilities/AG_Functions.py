__author__ = 'siavoosh'
import networkx
import Config
#todo: add virtual channel support AG...

def GenerateManualAG(PE_List,AG_Edge_List,AG_Edge_Port_List):
    print "==========================================="
    print "PREPARING AN ARCHITECTURE GRAPH (AG)..."
    AG=networkx.DiGraph()
    for PE in PE_List:
        AG.add_node(PE,MappedTasks = [],Scheduling={},Utilization=0)
    for i in range(0,len(AG_Edge_List)):
        EDGE = AG_Edge_List[i]
        AG.add_edge(EDGE[0],EDGE[1],Port=AG_Edge_Port_List[i],MappedTasks = [],Scheduling={})
    print "\tNODES: ",AG.nodes(data=False)
    print "\tEDGES: ",AG.edges(data=False)
    print("ARCHITECTURE GRAPH (AG) IS READY...")
    return AG

def GenerateGenericTopologyAG(Topology,SizeX,SizeY,SizeZ,logging):
    """
    Takes a generic topology: 2DTorus, 2DMesh, 2DLine, 2DRing etc. and returns AG
    :param Topology: a string with topology name
    :return: AG
    """
    SupportedTopologies=['2DSpidergon','2DTorus','2DMesh','2DRing','2DLine']
    print "==========================================="
    print "PREPARING AN ARCHITECTURE GRAPH (AG)..."
    print "TOPOLOGY:",Topology
    print "X SIZE:",SizeX
    print "Y SIZE:",SizeY
    print "Z SIZE:",SizeZ
    AG=networkx.DiGraph()


    if Topology not in SupportedTopologies:
        logging.error("TOPOLOGY NOT SUPPORTED...")
        raise ValueError('TOPOLOGY ',Topology,' is NOT SUPPORTED...')

    logging.info("GENERATING ARCHITECTURE GRAPH (AG)...")
    if Topology=='2DSpidergon':
        if SizeX == SizeY:
            # Todo: write spidergon
            None
    if Topology=='2DTorus':
        for i in range(0,SizeX*SizeY):
            AG.add_node(i,MappedTasks = [],Scheduling={},Utilization=0,Speed=100)
        for i in range(0,SizeX):
            logging.info( "CONNECTING  "+str(i)+" TO "+str((SizeY-1)*(SizeX)+i))
            logging.info( "CONNECTING  "+str((SizeY-1)*SizeX+i)+" TO "+str(i))
            AG.add_edge(i ,(SizeY-1)*SizeX+i,Port=('S','N'),MappedTasks = [],Scheduling={})
            AG.add_edge((SizeY-1)*SizeX+i,i,Port=('N','S'),MappedTasks = [],Scheduling={})
        for j in range(0,SizeY):
            logging.info("CONNECTING  "+str(j*(SizeX))+" TO "+str(j*(SizeX)+SizeX-1))
            logging.info("CONNECTING  "+str(j*(SizeX)+SizeX-1)+" TO "+str(j*(SizeX)))
            AG.add_edge(j*(SizeX),j*(SizeX)+SizeX-1,Port=('W','E'),MappedTasks = [],Scheduling={})
            AG.add_edge(j*(SizeX)+SizeX-1,j*(SizeX),Port=('E','W'),MappedTasks = [],Scheduling={})
            for i in range(0,SizeX-1):
                logging.info("CONNECTING  "+str(j*(SizeX)+i)+" TO "+str(j*(SizeX)+i+1))
                logging.info( "CONNECTING  "+str(j*(SizeX)+i+1)+" TO "+str(j*(SizeX)+i))
                AG.add_edge(j*(SizeX)+i,j*(SizeX)+i+1,Port=('E','W'),MappedTasks = [],Scheduling={})
                AG.add_edge(j*(SizeX)+i+1,j*(SizeX)+i,Port=('W','E'),MappedTasks = [],Scheduling={})
        for j in range(0,SizeY-1):
            for i in range(0,SizeX):
                logging.info( "CONNECTING  "+str(j*(SizeX)+i)+" TO "+str((j+1)*(SizeX)+i))
                logging.info( "CONNECTING  "+str((j+1)*SizeX+i)+" TO "+str(j*SizeX+i))
                AG.add_edge(j*SizeX+i ,(j+1)*SizeX+i,Port=('N','S'),MappedTasks = [],Scheduling={})
                AG.add_edge((j+1)*SizeX+i,j*SizeX+i,Port=('S','N'),MappedTasks = [],Scheduling={})
    if Topology=='2DMesh':
        for i in range(0,SizeX*SizeY):
            AG.add_node(i,MappedTasks = [],Scheduling={},Utilization=0,Speed=100)
        for j in range(0,SizeY):
            for i in range(0,SizeX-1):
                logging.info( "CONNECTING  "+str(j*(SizeX)+i)+" TO "+str(j*(SizeX)+i+1))
                logging.info( "CONNECTING  "+str(j*(SizeX)+i+1)+" TO "+str(j*(SizeX)+i))
                AG.add_edge(j*(SizeX)+i,j*(SizeX)+i+1,Port=('E','W'),MappedTasks = [],Scheduling={})
                AG.add_edge(j*(SizeX)+i+1,j*(SizeX)+i,Port=('W','E'),MappedTasks = [],Scheduling={})
        for j in range(0,SizeY-1):
            for i in range(0,SizeX):
                logging.info( "CONNECTING  "+str(j*(SizeX)+i)+" TO "+str((j+1)*(SizeX)+i))
                logging.info( "CONNECTING  "+str((j+1)*SizeX+i)+" TO "+str(j*SizeX+i))
                AG.add_edge(j*SizeX+i ,(j+1)*SizeX+i,Port=('N','S'),MappedTasks = [],Scheduling={})
                AG.add_edge((j+1)*SizeX+i,j*SizeX+i,Port=('S','N'),MappedTasks = [],Scheduling={})
    elif Topology=='2DRing':
        for i in range(0,SizeX*SizeY):
            AG.add_node(i,MappedTasks = [],Scheduling={},Utilization=0,Speed=100)
        for j in range(0,SizeY):
            logging.info( "CONNECTING  "+str(j*(SizeX))+" TO "+str(j*(SizeX)+SizeX-1))
            logging.info( "CONNECTING  "+str(j*(SizeX)+SizeX-1)+" TO "+str(j*(SizeX)))
            AG.add_edge(j*(SizeX),j*(SizeX)+SizeX-1,Port=('W','E'),MappedTasks = [],Scheduling={})
            AG.add_edge(j*(SizeX)+SizeX-1,j*(SizeX),Port=('E','W'),MappedTasks = [],Scheduling={})
            for i in range(0,SizeX-1):
                logging.info("CONNECTING  "+str(j*(SizeX)+i)+" TO "+str(j*(SizeX)+i+1))
                logging.info( "CONNECTING  "+str(j*(SizeX)+i+1)+" TO "+str(j*(SizeX)+i))
                AG.add_edge(j*(SizeX)+i,j*(SizeX)+i+1,Port=('E','W'),MappedTasks = [],Scheduling={})
                AG.add_edge(j*(SizeX)+i+1,j*(SizeX)+i,Port=('W','E'),MappedTasks = [],Scheduling={})
    elif Topology=='2DLine':
        for i in range(0,SizeX*SizeY):
            AG.add_node(i,MappedTasks = [],Scheduling={},Utilization=0,Speed=100)
        for j in range(0,SizeY):
            for i in range(0,SizeX-1):
                logging.info("CONNECTING  "+str(j*(SizeX)+i)+" TO "+str(j*(SizeX)+i+1))
                logging.info( "CONNECTING  "+str(j*(SizeX)+i+1)+" TO "+str(j*(SizeX)+i))
                AG.add_edge(j*(SizeX)+i,j*(SizeX)+i+1,Port=('E','W'),MappedTasks = [],Scheduling={})
                AG.add_edge(j*(SizeX)+i+1,j*(SizeX)+i,Port=('W','E'),MappedTasks = [],Scheduling={})
    print("ARCHITECTURE GRAPH (AG) IS READY...")
    return AG

def GenerateAG(logging):
    if Config.AG_Type=='Generic':
        return GenerateGenericTopologyAG(Config.NetworkTopology,Config.Network_X_Size,
                                                          Config.Network_Y_Size,Config.Network_Z_Size,logging)
    elif Config.AG_Type=='Manual':
        return GenerateManualAG(Config.PE_List,Config.AG_Edge_List,Config.AG_Edge_Port_List)
    else:
        raise ValueError('AG TYPE DOESNT EXIST...!!!')
