__author__ = 'siavoosh'

from TaskGraphUtilities import TG_Functions
import copy
#Todo: move sub functions out of the file


def ScheduleAll(TG,AG,Report):
    print "\t\tSTARTING SCHEDULING PROCESS..."
    TaskToSchedule=TG_Functions.FindSourceNodes(TG)
    SuccessorsList=[]
    priority=0
    #first schedule the high critical tasks and their high critical transactions
    while len(TaskToSchedule)>0:
        for Task in TG.nodes():
            if TG.node[Task]['Priority']==priority:
                if TG.node[Task]['Criticality']=='H':
                    Node = TG.node[Task]['Node']
                    if Report:print "\tSCHEDULING TASK",Task,"ON NODE:",Node
                    Add_TG_TaskToNode(TG,AG,Task,Node,Report)
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                            if TG.edge[Edge[0]][Edge[1]]['Criticality']=='H':
                                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                    for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                        if Report:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                        Add_TG_EdgeTo_link(TG,AG,Edge,Link,Report)
            if TG.node[Task]['Priority']==priority+1:
                SuccessorsList.append(Task)
        TaskToSchedule = copy.deepcopy(SuccessorsList)
        SuccessorsList=[]
        priority+=1

    TaskToSchedule=TG_Functions.FindSourceNodes(TG)
    SuccessorsList=[]
    priority=0
    #schedule the low critical transactions of high critical tasks
    while len(TaskToSchedule)>0:
        for Task in TG.nodes():
            if TG.node[Task]['Priority']==priority:
                if TG.node[Task]['Criticality']=='H':
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                            if TG.edge[Edge[0]][Edge[1]]['Criticality']=='L':
                                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                    for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                        if Report:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                        Add_TG_EdgeTo_link(TG,AG,Edge,Link,Report)
            if TG.node[Task]['Priority']==priority+1:
                SuccessorsList.append(Task)
        TaskToSchedule = copy.deepcopy(SuccessorsList)
        SuccessorsList=[]
        priority+=1
    #schedule low critical tasks and their transactions
    TaskToSchedule=TG_Functions.FindSourceNodes(TG)
    SuccessorsList=[]
    priority=0
    while len(TaskToSchedule)>0:
        for Task in TG.nodes():
            if TG.node[Task]['Priority']==priority:
                if TG.node[Task]['Criticality']=='L':
                    Node = TG.node[Task]['Node']
                    if Report:print "\tSCHEDULING TASK",Task,"ON NODE:",Node
                    Add_TG_TaskToNode(TG,AG,Task,Node,Report)
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                            if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                    if Report:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                    Add_TG_EdgeTo_link(TG,AG,Edge,Link,Report)
            if TG.node[Task]['Priority']==priority+1:
                SuccessorsList.append(Task)
        TaskToSchedule = copy.deepcopy(SuccessorsList)
        SuccessorsList=[]
        priority+=1
    print "\t\tDONE SCHEDULING..."
    return None

def FindScheduleMakeSpan(AG):
    MakeSpan=0
    for Node in AG.nodes():
        for Task in AG.node[Node]['MappedTasks']:
            if AG.node[Node]['Scheduling'][Task][1]>MakeSpan:
                MakeSpan=AG.node[Node]['Scheduling'][Task][1]
    return MakeSpan

def Add_TG_TaskToNode(TG,AG,Task,Node,Report):
    if Report: "\t\tADDING TASK:",Task," TO NODE:",Node
    CriticalityLevel=TG.node[Task]['Criticality']
    StartTime=max(FindLastAllocatedTimeOnNode(TG,AG,Node,Report),FindTaskPredecessorsFinishTime(TG,AG,Task,CriticalityLevel))
    EndTime=StartTime+TG.node[Task]['WCET']
    if Report:print "\t\tSTARTING TIME:",StartTime,"ENDING TIME:",EndTime
    AG.node[Node]['Scheduling'][Task]=[StartTime,EndTime]
    TG.node[Task]['Node']=Node
    return True


def FindTaskPredecessorsFinishTime(TG,AG,Task,CriticalityLevel):
    FinishTime=0
    if len(TG.predecessors(Task))>0:
        for Predecessor in TG.predecessors(Task):
            if TG.node[Predecessor]['Node'] is not None: #predecessor is mapped
                if TG.node[Predecessor]['Criticality']==CriticalityLevel: #this is not quit right...
                    Node = TG.node[Predecessor]['Node']
                    if  Predecessor in AG.node[Node]['Scheduling']:
                        if AG.node[Node]['Scheduling'][Predecessor][1]>FinishTime:
                            FinishTime=AG.node[Node]['Scheduling'][Predecessor][1]
    for Edge in TG.edges():
        if Edge[1]==Task:
            if TG.edge[Edge[0]][Edge[1]]['Criticality']==CriticalityLevel:
                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                    for Link in  TG.edge[Edge[0]][Edge[1]]['Link']: #for each link that this edge goes through
                        if len(AG.edge[Link[0]][Link[1]]['Scheduling'])>0:
                            if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']: #if this edge is scheduled
                                if AG.edge[Link[0]][Link[1]]['Scheduling'][Edge][1]>FinishTime:
                                    FinishTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Edge][1]
    return FinishTime



def FindEdgePredecessorsFinishTime(TG,AG,Edge):
    FinishTime=0
    Node = TG.node[Edge[0]]['Node']
    if Edge[0] in AG.node[Node]['Scheduling']:
        if AG.node[Node]['Scheduling'][Edge[0]][1]>FinishTime:
            FinishTime=AG.node[Node]['Scheduling'][Edge[0]][1]
    for Link in AG.edges():
        if Edge in AG.edge[Link[0]][Link[1]]['Scheduling']:
            if AG.edge[Link[0]][Link[1]]['Scheduling'][Edge][1]>FinishTime:
                FinishTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Edge][1]

    return FinishTime

def Add_TG_EdgeTo_link(TG,AG,Edge,Link,Report):
    if Report:print "\t\tADDING EDGE:",Edge," TO LINK:",Link
    StartTime=max(FindLastAllocatedTimeOnLink(TG,AG,Link,Report),FindEdgePredecessorsFinishTime(TG,AG,Edge))
    EndTime=StartTime+(TG.edge[Edge[0]][Edge[1]]['ComWeight'])
    if Report:print "\t\tSTARTING TIME:",StartTime,"ENDING TIME:",EndTime
    AG.edge[Link[0]][Link[1]]['Scheduling'][Edge]=[StartTime,EndTime]
    return True

def ReportMappedTasks(AG):
    print "==========================================="
    print "          REPORTING SCHEDULING "
    print "==========================================="
    for Node in AG.nodes():
        print "NODE", Node,"CONTAINS THE FOLLOWING TASKS:",AG.node[Node]['MappedTasks'],\
            "\tWITH SCHEDULING:",AG.node[Node]['Scheduling']
    for Link in AG.edges():
        print "LINK", Link,"CONTAINS THE FOLLOWING TG's Edges:",AG.edge[Link[0]][Link[1]]['MappedTasks'],\
            "\tWITH SCHEDULING:",AG.edge[Link[0]][Link[1]]['Scheduling']
    return None

def ClearScheduling(AG,TG):
    for Node in AG.nodes():
        AG.node[Node]['Scheduling']={}
    for Link in AG.edges():
        AG.edge[Link[0]][Link[1]]['Scheduling']={}
    return None

def FindLastAllocatedTimeOnLink(TG,AG,Link,Report):
    if Report:print "\t\tFINDING LAST ALLOCATED TIME ON LINK", Link
    LastAllocatedTime=0
    if len(AG.edge[Link[0]][Link[1]]['MappedTasks'])>0:
        for Task in AG.edge[Link[0]][Link[1]]['MappedTasks']:
            if Task in AG.edge[Link[0]][Link[1]]['Scheduling']:
                StartTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][0]
                EndTime=AG.edge[Link[0]][Link[1]]['Scheduling'][Task][1]
                if StartTime is not None and EndTime is not None:
                    if Report:print "\t\t\tTASK STARTS AT:",StartTime,"AND ENDS AT:",EndTime
                    if EndTime > LastAllocatedTime:
                        LastAllocatedTime = EndTime
    else:
        if Report:print "\t\t\tNO SCHEDULED TASK FOUND"
        return 0
    if Report:print "\t\t\tLAST ALLOCATED TIME:",LastAllocatedTime
    return LastAllocatedTime

def FindLastAllocatedTimeOnNode(TG,AG,Node,Report):
    if Report:print "\t\tFINDING LAST ALLOCATED TIME ON NODE", Node
    LastAllocatedTime=0
    if len(AG.node[Node]['MappedTasks'])>0:
        if Report:print "\t\t\tMAPPED TASKS ON THE NODE:",AG.node[Node]['MappedTasks']
        for Task in AG.node[Node]['MappedTasks']:
            if Task in AG.node[Node]['Scheduling']:
                StartTime=AG.node[Node]['Scheduling'][Task][0]
                EndTime=AG.node[Node]['Scheduling'][Task][1]
                if StartTime is not None and EndTime is not None:
                    if Report:print "\t\t\tTASK STARTS AT:",StartTime,"AND ENDS AT:",EndTime
                    if EndTime > LastAllocatedTime:
                        LastAllocatedTime = EndTime
    else:
        if Report:print "\t\t\tNO SCHEDULED TASK FOUND"
        return 0
    if Report:print "\t\t\tLAST ALLOCATED TIME:",LastAllocatedTime
    return LastAllocatedTime
