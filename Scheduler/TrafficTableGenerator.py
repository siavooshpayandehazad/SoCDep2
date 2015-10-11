# Copyright (C) 2015 Siavoosh Payandeh Azad
from ArchGraphUtilities import AG_Functions
from ConfigAndPackages import Config


def GenerateNoximTrafficTable (AG, TG):
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
    TrafficTableFile = open('Generated_Files/NoximTrafficTable.txt','w')
    for Node in AG.nodes():
        if len(AG.node[Node]['MappedTasks'])>0:
            for Task in AG.node[Node]['MappedTasks']:
                for Edge in TG.edges():
                    if Edge[0] == Task and (TranslateNodeNumberToNoximSystem(TG.node[Edge[0]]['Node']) != TranslateNodeNumberToNoximSystem(TG.node[Edge[1]]['Node'])):
                        SourceNodeNoxim = TranslateNodeNumberToNoximSystem(TG.node[Edge[0]]['Node'])
                        DestinationNodeNoxim = TranslateNodeNumberToNoximSystem(TG.node[Edge[1]]['Node'])
                        StringToWrite  = str(SourceNodeNoxim) + " " + str(DestinationNodeNoxim)
                        StringToWrite += " 0.01"
                        StringToWrite += " 0.01"
                        StringToWrite += " " + str(int(AG.node[Node]['Scheduling'][Task][0]))
                        StringToWrite += " " + str(int(AG.node[Node]['Scheduling'][Task][1]))
                        TrafficTableFile.write(StringToWrite+"\n")
    TrafficTableFile.close()
    return None

def TranslateNodeNumberToNoximSystem(Node):
    X,Y,Z = AG_Functions.ReturnNodeLocation(Node)
    Z = Config.Network_Z_Size - Z -1
    Y = Config.Network_Y_Size - Y -1
    return AG_Functions.ReturnNodeNumber(X,Y,Z)


def GenerateGSNoCTrafficTable (AG, TG):
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

    TrafficTableFile = open('Generated_Files/GSNoCTrafficTable.txt','w')
    for Node in AG.nodes():
        if len(AG.node[Node]['MappedTasks'])>0:
            for Task in AG.node[Node]['MappedTasks']:
                for Edge in TG.edges():
                    if Edge[0] == Task or Edge[1] == Task:
                        StringToWrite = str(Node)+ "\t" + str(Task) + "\t"+str(TG.node[Task]['WCET']) + "\t"
                        StringToWrite += str(Edge[0]) + str(Edge[1]) + " \t" +  str(TG.edge[Edge[0]][Edge[1]]['ComWeight'])
                        # todo: This should be replaced with BW
                        StringToWrite +=  "\t" + str(TG.edge[Edge[0]][Edge[1]]['ComWeight']) + " \t"
                        StringToWrite += str(Edge[0]) +"\t"+ str(Edge[1]) + "\t"
                        StringToWrite += str(TG.node[Edge[0]]['Node']) + "\t" + str(TG.node[Edge[1]]['Node'])
                        TrafficTableFile.write(StringToWrite+"\n")
    TrafficTableFile.close()
    return None
