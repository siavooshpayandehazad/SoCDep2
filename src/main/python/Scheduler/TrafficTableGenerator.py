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
                    if Edge[0] == Task and (translate_node_number_to_noxim_system(tg.node[Edge[0]]['task'].node) !=
                                            translate_node_number_to_noxim_system(tg.node[Edge[1]]['task'].node)):
                        # in Noxim's traffic table, since each router has only one IP core connected
                        # to it, Node(i) cannot send data to Node(i)
                        source_node_noxim = translate_node_number_to_noxim_system(tg.node[Edge[0]]['task'].node)
                        destination_node_noxim = translate_node_number_to_noxim_system(tg.node[Edge[1]]['task'].node)
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
    z = Config.ag.z_size - z - 1
    y = Config.ag.y_size - y - 1
    return AG_Functions.return_node_number(x, y, z)