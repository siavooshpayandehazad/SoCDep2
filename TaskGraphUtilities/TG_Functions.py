__author__ = 'siavoosh'
import networkx
def FindSourceNodes(TG):
    SourceNode=[]
    for Task in TG.nodes():
        if len(TG.predecessors(Task))==0:
            SourceNode.append(Task)
    return SourceNode


def AssignPriorities(TG):
    SourceNodes=FindSourceNodes(TG)
    for Task in SourceNodes:
        TG.node[Task]['Priority']=0

    for Task in TG.nodes():
        distance=[]
        if Task not in SourceNodes:
            for Source in SourceNodes:
                if networkx.has_path(TG,Source,Task):
                    ShortestPaths=networkx.shortest_path(TG,Source,Task)
                    distance.append(len(ShortestPaths)-1)
            TG.node[Task]['Priority']=min(distance)