# Copyright (C) 2015 Siavoosh Payandeh Azad 


def FindScheduleMakeSpan(AG):
    MakeSpan = 0
    for Node in AG.nodes():
        for Task in AG.node[Node]['PE'].MappedTasks:
            MakeSpan = max(AG.node[Node]['PE'].Scheduling[Task][1], MakeSpan)
    return MakeSpan


################################################################
def ClearScheduling(AG, TG):
    for Node in AG.nodes():
        AG.node[Node]['PE'].Scheduling = {}
    for Link in AG.edges():
        AG.edge[Link[0]][Link[1]]['Scheduling'] = {}
    return None


