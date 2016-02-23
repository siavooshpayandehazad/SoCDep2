# Copyright (C) Siavoosh Payandeh Azad

from ArchGraphUtilities import AG_Functions


def report_gsnoc_friendly_reachability_in_file(ag):
    reachability_file = open("Generated_Files/GSNoC_RectangleFile.txt", 'w')
    for node in ag.nodes():
        node_x, node_y, node_z = AG_Functions.return_node_location(node)
        for port in ag.node[node]['Router'].Unreachable:
            if port == "S":
                direction = "SOUTH"
            elif port == "N":
                direction = "NORTH"
            elif port == "W":
                direction = "WEST"
            elif port == "E":
                direction = "EAST"
            for entry in ag.node[node]['Router'].Unreachable[port]:
                reachability_file.write("["+str(node_x)+","+str(node_y)+","+str(node_z)+"] ")
                unreachable_area = ag.node[node]['Router'].Unreachable[port][entry]
                if unreachable_area[0] is not None:
                    unreachable_x, unreachable_y, unreachable_z = AG_Functions.return_node_location(unreachable_area[0])
                    reachability_file.write(str(direction)+" NetLocCube(ll=["+str(unreachable_x)+"," +
                                            str(unreachable_y)+","+str(unreachable_z)+"],")
                    unreachable_x, unreachable_y, unreachable_z = AG_Functions.return_node_location(unreachable_area[1])
                    reachability_file.write("ur=["+str(unreachable_x)+","+str(unreachable_y) +
                                            ","+str(unreachable_z)+"])\n")
                else:
                    reachability_file.write(str(direction)+" NetLocCube(invalid)\n")
        reachability_file.write("\n")
    reachability_file.close()


def report_reachability(ag):
    """
    reports unreachable nodes for each port of each node
    :param ag: architecture graph
    :return: None
    """
    print ("=====================================")
    for node in ag.nodes():
        print ("NODE", node, "UNREACHABLE NODES:")
        for port in ag.node[node]['Router'].Unreachable:
            print ("Port:"+str(port)+" ==>"+str(ag.node[node]['Router'].Unreachable[port]))
    return None


def report_reachability_in_file(ag, file_name):
    reachability_file = open('Generated_Files/'+file_name+".txt", 'w')
    for node in ag.nodes():
        reachability_file.write("=====================================\n")
        reachability_file.write("NODE "+str(node)+" UNREACHABLE NODES:\n")
        for port in ag.node[node]['Router'].Unreachable:
            reachability_file.write("Port: "+str(port)+" ==> "+str(ag.node[node]['Router'].Unreachable[port])+"\n")
    reachability_file.close()
    return None
