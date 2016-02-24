# Copyright (C) 2015 Siavoosh Payandeh Azad
# "generate_noxim_traffic_table" and "TranslateNodeNumberToNoximSystem" Functions were
# written in 2015 by Behrad Niazmand

from ArchGraphUtilities import AG_Functions
from ConfigAndPackages import Config


def generate_noxim_traffic_table(ag, tg):
    # here we should generate a traffic Table for Noxim Simulator to double
    # check our experiments with it.

    # Note that the node numbering in Noxim is as follows:
    #      X ---------->
    #   Y
    #
    #   |   ? ? ?
    #   |
    #   |
    #   V
    #
    #  For Noxim the coordinates of the nodes in AG would be different, the following conversion formula can be used
    #  to transform from GSNoC to Noxim :
    #  GSNoC: (x,y,z) -----> Noxim: (x, |y - dim_y - 1|, |z - dim_z - 1|) (using absolute function)
    #
    # ---------------------------------------------------
    # The file format is:
    # src   dst     pir    por	    t_on    t_off   t_period
    # where:
    #   src:		ID of the source node (PE)
    #   dst:		ID of the destination node (PE)
    #   pir:	Packet Injection Rate for the link
    #   por:    Probability Of Retransmission for the link
    #   t_on:		Time (in cycles) at which activity begins
    #   t_off:    Time (in cycles) at which activity ends
    #   t_period:	Period after which activity starts again
    # ---------------------------------------------------
    traffic_table_file = open('Generated_Files/NoximTrafficTable.txt', 'w')
    for Node in ag.nodes():
        if len(ag.node[Node]['PE'].mapped_tasks) > 0:
            for Task in ag.node[Node]['PE'].mapped_tasks:
                for Edge in tg.edges():
                    if Edge[0] == Task and (translate_node_number_to_noxim_system(tg.node[Edge[0]]['Node']) !=
                                            translate_node_number_to_noxim_system(tg.node[Edge[1]]['Node'])):
                        # in Noxim's traffic table, since each router has only one IP core connected
                        # to it, Node(i) cannot send data to Node(i)
                        source_node_noxim = translate_node_number_to_noxim_system(tg.node[Edge[0]]['Node'])
                        destination_node_noxim = translate_node_number_to_noxim_system(tg.node[Edge[1]]['Node'])
                        # StringToWrite: source + destination
                        string_to_write = str(source_node_noxim) + " " + str(destination_node_noxim)
#                       StringToWrite += " 0" # Region ID (used for bLBDR/Virtualization)
                        string_to_write += " 0.01"  # pir (packet injection rate)
                        string_to_write += " 0.01"  # por (probability of retransmission)
                        # t_on:
                        string_to_write += " " + str(int(ag.node[Node]['PE'].scheduling[Task][0]))
                        # t_off:
                        string_to_write += " " + str(int(ag.node[Node]['PE'].scheduling[Task][1]))
                        # t_period:
                        string_to_write += " " + str(int(ag.node[Node]['PE'].scheduling[Task][1]) + 1)
                        traffic_table_file.write(string_to_write+"\n")
    traffic_table_file.close()
    return None


def translate_node_number_to_noxim_system(node):
    """
    Translates the numbering system of Schedule and Depend to Noxim system
    :param node: Node ID in AG
    :return: Node coordination in Noxim System
    """
    x, y, z = AG_Functions.return_node_location(node)
    z = Config.Network_Z_Size - z - 1
    y = Config.Network_Y_Size - y - 1
    return AG_Functions.return_node_number(x, y, z)


def generate_gsnoc_traffic_table(ag, tg):
    # here we should generate a traffic Table for GSNoC Simulator to double
    # check our experiments with it.
    # This is the format of the application file called GSPA:
    # n.N. | n.T | T.exe. | N.e | w |  bw | St | Dt | Sn |  Dn
    # Where:
    #   n.N.: Node Number
    #   n.T: Task Number
    #   T.exe.: Task Execution Time
    #   N.e: Edge Number
    #   w: Weight counted as number of NoC flits
    #   bw: counted as the percentage number of the maximum NoC physical channel bandwidth capability
    #   St: Source Task
    #   Dt: Destination Task
    #   Sn: Source Node
    #   Dn :Destination Node
    # Note that the node numbering in GSNoC is as follows:
    #   Y
    #   ^
    #   |   7   8   9
    #   |   4   5   6
    #   |   1   2   3
    #       ----------> X
    # which is similar to our numbering system. same Node number can be used for
    # GSNoC as well

    traffic_table_file = open('Generated_Files/GSNoCTrafficTable.txt', 'w')
    for Node in ag.nodes():
        if len(ag.node[Node]['PE'].mapped_tasks) > 0:
            for Task in ag.node[Node]['PE'].mapped_tasks:
                for Edge in tg.edges():
                    if Edge[0] == Task or Edge[1] == Task:
                        string_to_write = str(Node) + "\t" + str(Task) + "\t"+str(tg.node[Task]['WCET']) + "\t"
                        string_to_write += str(Edge[0]) + str(Edge[1]) + " \t" + \
                            str(tg.edge[Edge[0]][Edge[1]]['ComWeight'])
                        # todo: This should be replaced with BW
                        string_to_write += "\t" + str(tg.edge[Edge[0]][Edge[1]]['ComWeight']) + " \t"
                        string_to_write += str(Edge[0]) + "\t" + str(Edge[1]) + "\t"
                        string_to_write += str(tg.node[Edge[0]]['Node']) + "\t" + \
                            str(tg.node[Edge[1]]['Node'])
                        traffic_table_file.write(string_to_write+"\n")
    traffic_table_file.close()
    return None
