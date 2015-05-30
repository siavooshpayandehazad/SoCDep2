__author__ = 'siavoosh'
import networkx

def GenerateTG(Task_List,TG_Edge_List,Task_Criticality_List,Task_WCET_List,TG_Edge_Weight):
    TG=networkx.DiGraph()
    Edge_Criticality_List=[]
    # IF both sender and receiver are critical then that transaction is critical
    for edge in TG_Edge_List:
        if Task_Criticality_List[Task_List.index(edge[0])]=='H' and Task_Criticality_List[Task_List.index(edge[1])]=='H' :
            Edge_Criticality_List.append('H')
        else:
            Edge_Criticality_List.append('L')

    for i in range(0,len(Task_List)):
        TG.add_node(Task_List[i],WCET=Task_WCET_List[i],Criticality=Task_Criticality_List[i],Cluster=None,Node=None,Priority=None)

    for i in range(0,len(TG_Edge_List)):
        TG.add_edge(TG_Edge_List[i][0],TG_Edge_List[i][1],Criticality=Edge_Criticality_List[i],Link=[],ComWeight=TG_Edge_Weight[i])  # Communication weight
    return TG

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