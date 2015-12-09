# Copyright (C) 2015 Siavoosh Payandeh Azad 


def FindScheduleMakeSpan(ag):
    """
    Calculates the makespan of the Scheduling
    :param ag: Architecture Graph
    :return: MakeSpan of the Scheduling
    """
    MakeSpan = 0
    for Node in ag.nodes():
        for Task in ag.node[Node]['PE'].MappedTasks:
            MakeSpan = max(ag.node[Node]['PE'].Scheduling[Task][1], MakeSpan)
    return MakeSpan


################################################################
def ClearScheduling(ag, tg):
    """
    Clears scheduling from PEs, Routers and Links
    :param AG: Architecture Graph
    :param tg: Task Graph
    :return: None
    """
    for node in ag.nodes():
        ag.node[node]['PE'].Scheduling = {}
        ag.node[node]['Router'].Scheduling = {}
    for link in ag.edges():
        ag.edge[link[0]][link[1]]['Scheduling'] = {}
    return None


