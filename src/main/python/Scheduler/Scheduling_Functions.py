# Copyright (C) 2015 Siavoosh Payandeh Azad 


def FindScheduleMakeSpan(AG):
    """
    Calculates the makespan of the Scheduling
    :param AG: Architecture Graph
    :return: MakeSpan of the Scheduling
    """
    MakeSpan = 0
    for Node in AG.nodes():
        for Task in AG.node[Node]['PE'].MappedTasks:
            MakeSpan = max(AG.node[Node]['PE'].Scheduling[Task][1], MakeSpan)
    return MakeSpan


################################################################
def ClearScheduling(AG, TG):
    """
    Clears scheduling from PEs, Routers and Links
    :param AG: Architecture Graph
    :param TG: Task Graph
    :return: None
    """
    for Node in AG.nodes():
        AG.node[Node]['PE'].Scheduling = {}
        AG.node[Node]['Router'].Scheduling = {}
    for Link in AG.edges():
        AG.edge[Link[0]][Link[1]]['Scheduling'] = {}
    return None


