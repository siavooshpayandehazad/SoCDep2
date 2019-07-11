# Copyright (C) 2015 Siavoosh Payandeh Azad
import networkx
from ConfigAndPackages import Config
import random
from math import ceil
# todo: add virtual channel support AG...


class Router():
    def __init__(self):
        self.unreachable = {}
        self.mapped_tasks = {}
        self.scheduling = {}


class PE():     # PROCESSING ELEMENT
    def __init__(self):
        self.utilization = 0
        self.dark = False
        self.mapped_tasks = []
        self.scheduling = {}
        self.type = 'Processor'       # Can be accelerator or something else


def generate_manual_ag(proc_element_list, ag_edge_list, ag_edge_port_list, report = False):
    """
    Generates an architecture graph from manually defined AG in  Config file
    :param proc_element_list:  List of Processing Elements
    :param ag_edge_list: List of Edges between PEs
    :param ag_edge_port_list:  Port connection for each of the links between PEs
    :return: ag
    """
    if report:
        print("===========================================")
        print("PREPARING AN ARCHITECTURE GRAPH (AG)...")
    ag = networkx.DiGraph()
    for processing_element in proc_element_list:
        ag.add_node(processing_element, PE=PE(), Router=Router(), Region='L')
    for i in range(0, len(ag_edge_list)):
        edge = ag_edge_list[i]
        ag.add_edge(edge[0], edge[1], Port=ag_edge_port_list[i], MappedTasks={}, Scheduling={})
    if report:
        print("\tNODES: "+str(ag.nodes(data=False)))
        print("\tEDGES: "+str(ag.edges(data=False)))
        print("ARCHITECTURE GRAPH (AG) IS READY...")
    return ag


def generate_generic_topology_ag(topology, logging=None, report=False):
    """
    Takes a generic topology: 2DTorus, 2DMesh, 2DLine, 2DRing etc. and returns AG
    :param topology: a string with topology name
    :param logging: logging file
    :return: AG
    """
    size_x = Config.ag.x_size
    size_y = Config.ag.y_size
    size_z = Config.ag.z_size
    supported_topologies = ['2DTorus', '2DMesh', '2DRing', '2DLine', '3DMesh']
    if report:
        print("===========================================")
        print("PREPARING AN ARCHITECTURE GRAPH (AG)...")
        print("TOPOLOGY: "+topology)
        print("X SIZE:"+str(size_x))
        print("Y SIZE:"+str(size_y))
        print("Z SIZE:"+str(size_z))
    ag = networkx.DiGraph()

    if topology not in supported_topologies:
        if logging is not None:
            logging.error("TOPOLOGY NOT SUPPORTED...")
        raise ValueError('TOPOLOGY ', topology, ' is NOT SUPPORTED...')
    if logging is not None:
        logging.info("GENERATING ARCHITECTURE GRAPH (AG)...")
    if topology == '2DSpidergon':
        if size_x == size_y:
            # Todo: write spidergon
            pass
    if topology == '2DTorus':
        for i in range(0, size_x*size_y):
            ag.add_node(i, PE=PE(), Router=Router(), Region='N')
        for i in range(0, size_x):
            current_node = return_node_number(i, 0, 0)
            next_node = return_node_number(i, size_y-1, 0)
            if logging is not None:
                logging.info("CONNECTING  "+str(current_node)+" TO "+str(next_node))
                logging.info("CONNECTING  "+str((size_y-1)*size_x+i)+" TO "+str(current_node))
            ag.add_edge(current_node, (size_y-1)*size_x+i, Port=('S', 'N'), MappedTasks={}, Scheduling={})
            ag.add_edge(next_node, current_node, Port=('N', 'S'), MappedTasks={}, Scheduling={})
        for j in range(0, size_y):
            current_node = return_node_number(0, j, 0)
            next_node = return_node_number(size_x-1, j, 0)
            if logging is not None:
                logging.info("CONNECTING  "+str(current_node)+" TO "+str(next_node))
                logging.info("CONNECTING  "+str(next_node)+" TO "+str(current_node))
            ag.add_edge(current_node, next_node, Port=('W', 'E'), MappedTasks={}, Scheduling={})
            ag.add_edge(next_node, current_node, Port=('E', 'W'), MappedTasks={}, Scheduling={})
            for i in range(0, size_x-1):
                current_node = return_node_number(i, j, 0)
                next_node = return_node_number(i+1, j, 0)
                if logging is not None:
                    logging.info("CONNECTING  " + str(current_node) + " TO " + str(next_node))
                    logging.info("CONNECTING  "+str(next_node)+" TO "+str(current_node))
                ag.add_edge(current_node, next_node, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                ag.add_edge(next_node, current_node, Port=('W', 'E'), MappedTasks={}, Scheduling={})
        for j in range(0, size_y-1):
            for i in range(0, size_x):
                current_node = return_node_number(i, j, 0)
                next_node = return_node_number(i, j+1, 0)
                if logging is not None:
                    logging.info("CONNECTING  "+str(current_node)+" TO "+str(next_node))
                    logging.info("CONNECTING  "+str(next_node)+" TO "+str(current_node))
                ag.add_edge(current_node, next_node, Port=('N', 'S'), MappedTasks={}, Scheduling={})
                ag.add_edge(next_node, current_node, Port=('S', 'N'), MappedTasks={}, Scheduling={})
    ##############################################################
    if topology == '2DMesh':
        for i in range(0, size_x*size_y):
            ag.add_node(i, PE=PE(), Router=Router(),  Region='N')
        for j in range(0, size_y):
            for i in range(0, size_x-1):
                current_node = return_node_number(i, j, 0)
                next_node = return_node_number(i+1, j, 0)
                if logging is not None:
                    logging.info("CONNECTING  "+str(current_node)+" TO "+str(next_node))
                    logging.info("CONNECTING  "+str(next_node)+" TO "+str(current_node))
                ag.add_edge(current_node, next_node, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                ag.add_edge(next_node, current_node, Port=('W', 'E'), MappedTasks={}, Scheduling={})
        for j in range(0, size_y-1):
            for i in range(0, size_x):
                current_node = return_node_number(i, j, 0)
                next_node = return_node_number(i, j+1, 0)
                if logging is not None:
                    logging.info("CONNECTING  "+str(current_node)+" TO "+str(next_node))
                    logging.info("CONNECTING  "+str(next_node)+" TO "+str(current_node))
                ag.add_edge(current_node, next_node, Port=('N', 'S'), MappedTasks={}, Scheduling={})
                ag.add_edge(next_node, current_node, Port=('S', 'N'), MappedTasks={}, Scheduling={})
    ##############################################################
    if topology == '3DMesh':
        for i in range(0, size_x*size_y*size_z):
            ag.add_node(i, PE=PE(), Router=Router(), Region='N')
        for z in range(0, size_z):
            # connect the connections in each layer
            for y in range(0, size_y):
                for x in range(0, size_x-1):
                    current_node = return_node_number(x, y, z)
                    next_node = return_node_number(x+1, y, z)
                    ag.add_edge(current_node, next_node, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                    ag.add_edge(next_node, current_node, Port=('W', 'E'), MappedTasks={}, Scheduling={})
            for y in range(0, size_y-1):
                for x in range(0, size_x):
                    current_node = return_node_number(x, y, z)
                    next_node = return_node_number(x, y+1, z)
                    ag.add_edge(current_node, next_node, Port=('N', 'S'), MappedTasks={}, Scheduling={})
                    ag.add_edge(next_node, current_node, Port=('S', 'N'), MappedTasks={}, Scheduling={})
        for z in range(0, size_z-1):
            # connect routers between layers.
            for y in range(0, size_y):
                for x in range(0, size_x):
                    current_node = return_node_number(x, y, z)
                    next_node = return_node_number(x, y, z+1)
                    ag.add_edge(current_node, next_node, Port=('U', 'D'), MappedTasks={}, Scheduling={})
                    ag.add_edge(next_node, current_node, Port=('D', 'U'), MappedTasks={}, Scheduling={})
    ##############################################################
    elif topology == '2DRing':
        for i in range(0, size_x*size_y):
            ag.add_node(i, PE=PE(), Router=Router(), Region='N')
        for j in range(0, size_y):
            current_node = return_node_number(0, j, 0)
            next_node = return_node_number(size_x-1, j, 0)
            if logging is not None:
                logging.info("CONNECTING  "+str(current_node)+" TO "+str(next_node))
                logging.info("CONNECTING  "+str(next_node)+" TO "+str(current_node))
            ag.add_edge(current_node, j*size_x+size_x-1, Port=('W', 'E'), MappedTasks={}, Scheduling={})
            ag.add_edge(next_node, current_node, Port=('E', 'W'), MappedTasks={}, Scheduling={})
            for i in range(0, size_x-1):
                current_node = return_node_number(i, j, 0)
                next_node = return_node_number(i+1, j, 0)
                if logging is not None:
                    logging.info("CONNECTING  "+str(current_node)+" TO "+str(next_node))
                    logging.info("CONNECTING  "+str(next_node)+" TO "+str(current_node))
                ag.add_edge(current_node, next_node, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                ag.add_edge(next_node, current_node, Port=('W', 'E'), MappedTasks={}, Scheduling={})
    ##############################################################
    elif topology == '2DLine':
        for i in range(0, size_x*size_y):
            ag.add_node(i, PE=PE(), Router=Router(), Region='N')
        for j in range(0, size_y):
            for i in range(0, size_x-1):
                current_node = return_node_number(i, j, 0)
                next_node = return_node_number(i+1, j, 0)
                if logging is not None:
                    logging.info("CONNECTING  "+str(current_node)+" TO "+str(next_node))
                    logging.info("CONNECTING  "+str(next_node)+" TO "+str(current_node))
                ag.add_edge(current_node, next_node, Port=('E', 'W'), MappedTasks={}, Scheduling={})
                ag.add_edge(next_node, current_node, Port=('W', 'E'), MappedTasks={}, Scheduling={})
    if report:
        print("ARCHITECTURE GRAPH (AG) IS READY...")
    return ag


def generate_ag(logging=None, report=False):
    """
    This function generates the architecture graph based on the configuration in Config File
    :param logging: logging file
    :return: returns the generated Architecture Graph
    """
    if Config.ag.type == 'Generic':
        return generate_generic_topology_ag(Config.ag.topology, logging, report=report)
    elif Config.ag.type == 'Manual':
        return generate_manual_ag(Config.PE_List, Config.AG_Edge_List, Config.AG_Edge_Port_List)
    else:
        raise ValueError('AG TYPE DOESNT EXIST...!!!')


def update_ag_regions(ag):
    """
    Takes an architecture graph and updates the node's Regions according to config file
    :param ag: Architecture graph
    :return: None
    """
    print("===========================================")
    print("UPDATING ARCHITECTURE GRAPH (AG) REGIONS...")
    for node_id in ag.nodes():
        if node_id in Config.CriticalRegionNodes:
            ag.node[node_id]['Region'] = 'H'
        elif node_id in Config.GateToCritical:
            ag.node[node_id]['Region'] = 'GH'
        elif node_id in Config.GateToNonCritical:
            ag.node[node_id]['Region'] = 'GNH'
        else:
            ag.node[node_id]['Region'] = 'L'
    print("ARCHITECTURE GRAPH (AG) REGIONS UPDATED...")
    return None


def return_node_location(node_number):
    """
    calculates the Cartesian location of the node
    Examples:
    return_node_location(0) = (0,0,0)
    return_node_location(Config.ag.x_size * Config.ag.y_size * Config.ag.z_size - 1) =
            (Config.ag.x_size -1, Config.ag.y_size - 1, Config.ag.z_size -1)
    :param node_number: The node id used in AG
    :return: Cartesian location of the node in the form of (x,y,z)
    """
    node_x = node_number % Config.ag.x_size
    node_y = (node_number // Config.ag.x_size) % Config.ag.y_size
    node_z = node_number // (Config.ag.y_size * Config.ag.x_size)
    return node_x, node_y, node_z


def return_node_number(node_x, node_y, node_z):
    """
    Takes cartesian location of a node and returns node id
    :param node_x: Location of the node on X axis
    :param node_y:  Location of the node on Y axis
    :param node_z: Location of the node on Z axis
    :return: ID of the node as an integer
    """
    return node_z * Config.ag.x_size * Config.ag.y_size + node_y * Config.ag.x_size + node_x


def node_neighbors(ag, system_health_map):
    """
    :param ag: Architecture graph (directed graph)
    :param system_health_map: System Health Map
    :return: A dictionary with node number as the key and the number of neighbors as values
    """
    node_neighbor = {}
    for Node in ag.nodes():
        number_of_neighbours = 0
        for Link in ag.edges():
            if Node in Link:
                if system_health_map.edges[Link]['LinkHealth']:
                    number_of_neighbours += 1
        node_neighbor[Node] = number_of_neighbours
    return node_neighbor


def max_node_neighbors(node_neighbors_dict, sorted_node_neighbors):
    """
    :param node_neighbors_dict: dictionary with nodes as keys and number of neighbors as values
    :param sorted_node_neighbors: sorted list of nodes by number of neighbors
    :return: returns a list of nodes with maximum number of neighbors
    """
    max_neighbour_num = 0
    for node in sorted_node_neighbors:
        if node_neighbors_dict[node] > max_neighbour_num:
            max_neighbour_num = node_neighbors_dict[node]
    max_neighbour_nodes = []
    for node in sorted_node_neighbors:
        if node_neighbors_dict[node] == max_neighbour_num:
            max_neighbour_nodes.append(node)
    return max_neighbour_nodes


def manhattan_distance(node_1, node_2):
    """
    Takes the node id of two nodes and returns the manhattan distance of those nodes
    :param node_1: Node id of 1st node
    :param node_2: Node id of 2nd node
    :return: returns manhattan distance between two nodes
    """
    x1, y1, z1 = return_node_location(node_1)
    x2, y2, z2 = return_node_location(node_2)

    return abs(x2-x1)+abs(y2-y1)+abs(z2-z1)


def setup_network_partitioning(ag):
    """
    Takes Architecture Graph as parameter and different regions from
    Config File and Sets up the partitioning for different regions
    :param ag: Architecture Graph
    :return: None
    """
    # Todo: This needs to be tested...
    print("===========================================")
    print("SETTING UP NETWORK PARTITIONING...")
    non_critical_nodes = []
    for node in ag.nodes():
        if node not in Config.CriticalRegionNodes:
            if node not in Config.GateToNonCritical:
                if node not in Config.GateToCritical:
                    non_critical_nodes.append(node)

    for link in ag.edges():
        # ListOfBrokenLinks
        if link[0] in Config.CriticalRegionNodes and link[1] in non_critical_nodes:
            Config.ListOfBrokenLinks.append(link)
        if link[0] in non_critical_nodes and link[1] in Config.CriticalRegionNodes:
            Config.ListOfBrokenLinks.append(link)

        if link[0] in Config.GateToCritical and link[1] in non_critical_nodes:
            Config.ListOfBrokenLinks.append(link)
        if link[0] in non_critical_nodes and link[1] in Config.GateToNonCritical:
            Config.ListOfBrokenLinks.append(link)

        # VirtualBrokenLinksForNonCritical
        if link[0] in Config.GateToCritical and link[1] in Config.CriticalRegionNodes:
            Config.VirtualBrokenLinksForNonCritical.append(link)
        if link[0] in Config.GateToCritical and link[1] in Config.GateToNonCritical:
            Config.VirtualBrokenLinksForNonCritical.append(link)
        if link[0] in Config.GateToNonCritical and link[1] in Config.CriticalRegionNodes:
            Config.VirtualBrokenLinksForNonCritical.append(link)

        #  VirtualBrokenLinksForCritical
        if link[0] in Config.GateToNonCritical and link[1] in non_critical_nodes:
            Config.VirtualBrokenLinksForCritical.append(link)

    print("ListOfBrokenLinks:", Config.ListOfBrokenLinks)
    print("VirtualBrokenLinksForNonCritical:", Config.VirtualBrokenLinksForNonCritical)
    print("VirtualBrokenLinksForCritical:", Config.VirtualBrokenLinksForCritical)
    return None


def random_darkness(ag):
    """
    randomly sets Config.DarkSiliconPercentage percent of the nodes to dark
    Takes the percentage of dark nodes form the Config File and turns of some Nodes.
    :param ag: Architecture Graph
    :return: None
    """
    number_of_dark_nodes = int(ceil(len(ag.nodes())*Config.DarkSiliconPercentage/100))
    list_of_dark_node = random.sample(ag.nodes(), number_of_dark_nodes)
    for node in list_of_dark_node:
        ag.node[node]['PE'].dark = True
    return None


def return_active_nodes(ag):
    """
    Returns Nodes in AG which are active (Not falling in dark areas)
    :param ag: Architecture Graph
    :return: list of active nodes.
    """
    active_nodes = []
    for node in ag.nodes():
        if not ag.node[node]['PE'].dark:
            active_nodes.append(node)
    return active_nodes


def return_node_util(tg, ag, node):
    """
    Returns the total utilization of mapped tasks on a given node.
    :param tg: task graph
    :param ag: architecture graph
    :param node: node id in ag
    :return: utilization
    """
    utilization = 0
    if len(ag.node[node]['PE'].mapped_tasks) > 0:
        for task in ag.node[node]['PE'].mapped_tasks:
            utilization += tg.node[task]['task'].wcet
    return utilization


def return_link_util(tg, ag, link):
    utilization = 0
    for task in ag.edges[link]['MappedTasks']:
        utilization += tg.edges[task]['ComWeight']
    return utilization

def return_healthy_nodes(ag, system_health_map):
    """
    Returns Nodes in AG which are tagged Healthy in SHM
    :param ag: Architecture Graph
    :param system_health_map: System Health Map
    :return: List of healthy Nodes in AG
    """
    healthy_nodes = []
    for node in ag.nodes():
        if system_health_map.node[node]['NodeHealth']:
            healthy_nodes.append(node)
    return healthy_nodes


def return_healthy_active_nodes(ag, system_health_map):
    """
    Returns Nodes in AG which are tagged Healthy in SHM and are active
    :param ag: Architecture Graph
    :param system_health_map: System Health Map
    :return: list of Healthy Active nodes
    """
    healthy_active_nodes = []
    for node in ag.nodes():
        if system_health_map.node[node]['NodeHealth']:
            if not ag.node[node]['PE'].dark:
                healthy_active_nodes.append(node)
    return healthy_active_nodes
