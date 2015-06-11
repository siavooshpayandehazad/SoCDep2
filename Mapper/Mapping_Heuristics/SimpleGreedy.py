
__author__ = 'siavoosh'
from Mapper import Mapping_Functions
from Scheduler import Scheduling_Functions
import copy
import random

def Min_Min_Mapping (TG,AG,NoCRG,SHM,logging):
    # this function finds the task with the smallest WCET and
    # maps it on the machine that can offer smallest completion time...
    # this means that the mapping algorithm has to take into account the mapping
    # of the edges of the task graph on the links.
    # Note:: this is a heuristic for independent tasks... so we are not going to
    # schedule any link
    print "==========================================="
    print "STARTING MIN-MIN MAPPING"
    ShortestTasks = Mapping_Functions.FindUnMappedTaskWithSmallestWCET(TG,logging)
    while len(ShortestTasks)>0 :
        TaskToBeMapped = ShortestTasks.pop()
        # map the task on the Node that yields smallest Completion time
        CandidateNodes=Mapping_Functions.FindNodeWithSmallestCompletionTime(AG,TG,SHM,TaskToBeMapped)
        print "\tCANDIDATE NODES FOR MAPPING:",CandidateNodes
        if len(CandidateNodes)>0:
            ChosenNode=random.choice(CandidateNodes)
            print "\t\tMAPPING TASK",TaskToBeMapped,"WITH RELEASE:",TG.node[TaskToBeMapped]['Release'], "---> NODE:",ChosenNode
            TG.node[TaskToBeMapped]['Node'] = ChosenNode
            AG.node[ChosenNode]['MappedTasks'].append(TaskToBeMapped)
            Scheduling_Functions.Add_TG_TaskToNode(TG,AG,SHM,TaskToBeMapped,ChosenNode,False)
        if len(ShortestTasks) == 0:
            ShortestTasks = Mapping_Functions.FindUnMappedTaskWithSmallestWCET(TG,logging)
    print "MIN-MIN MAPPING FINISHED..."
    Scheduling_Functions.ReportMappedTasks(AG)
    return TG, AG


def Max_Min_Mapping (TG,AG,NoCRG,SHM,logging):
    # this function finds the task with the biggest WCET and
    # maps it on the machine that can offer smallest completion time...
    # this means that the mapping algorithm has to take into account the mapping
    # of the edges of the task graph on the links.
    # Note:: this is a heuristic for independent tasks... so we are not going to
    # schedule any link
    print "==========================================="
    print "STARTING MIN-MAX MAPPING"
    LongestTasks = Mapping_Functions.FindUnMappedTaskWithBiggestWCET(TG,logging)
    while len(LongestTasks)>0 :
        TaskToBeMapped = LongestTasks.pop()
        # map the task on the Node that yields smallest Completion time
        CandidateNodes=Mapping_Functions.FindNodeWithSmallestCompletionTime(AG,TG,SHM,TaskToBeMapped)
        print "CANDIDATE NODES FOR MAPPING:",CandidateNodes
        if len(CandidateNodes)>0:
            ChosenNode=random.choice(CandidateNodes)
            if len(CandidateNodes)>1:
                print "\tMAPPING TASK",TaskToBeMapped,"WITH RELEASE:",TG.node[TaskToBeMapped]['Release']\
                    , "---> NODE:",ChosenNode,"(RANDOMLY CHOSEN FROM CANDIDATES)"
            else:
                print "\tMAPPING TASK",TaskToBeMapped,"WITH RELEASE:",TG.node[TaskToBeMapped]['Release'], "---> NODE:",ChosenNode
            TG.node[TaskToBeMapped]['Node'] = ChosenNode
            AG.node[ChosenNode]['MappedTasks'].append(TaskToBeMapped)
            Scheduling_Functions.Add_TG_TaskToNode(TG,AG,SHM,TaskToBeMapped,ChosenNode,False)
        if len(LongestTasks) == 0:
            LongestTasks = Mapping_Functions.FindUnMappedTaskWithBiggestWCET(TG,logging)
    print "MIN-MAX MAPPING FINISHED..."
    Scheduling_Functions.ReportMappedTasks(AG)
    return TG, AG

def MinExecutionTime(TG,AG,SHM):
    # this sounds a little stupid because there are no job specific machines...
    # we can Add Specific Accelerators or define different run time on different
    # PEs so this becomes more interesting...
    print "==========================================="
    print "STARTING MIN EXECUTION TIME MAPPING"
    for TaskToBeMapped in TG.nodes():
        ChosenNode=random.choice(Mapping_Functions.FindFastestNodes(AG,SHM,TaskToBeMapped))
        TG.node[TaskToBeMapped]['Node'] = ChosenNode
        AG.node[ChosenNode]['MappedTasks'].append(TaskToBeMapped)
        Scheduling_Functions.Add_TG_TaskToNode(TG,AG,SHM,TaskToBeMapped,ChosenNode,False)
        print "\tTASK",TaskToBeMapped,"MAPPED ON NODE:",ChosenNode
    print "MIN EXECUTION TIME MAPPING FINISHED..."
    Scheduling_Functions.ReportMappedTasks(AG)
    return TG,AG

def MinimumCompletionTime(TG,AG,SHM):
    # The difference with Min Min or Max Min is that we don't add priorities to
    # tasks based on their WCET but we randomly choose a task and schedule it...
    print "==========================================="
    print "STARTING MIN COMPLETION TIME MAPPING"
    for TaskToBeMapped in TG.nodes():
        ChosenNode=random.choice(Mapping_Functions.FindNodeWithSmallestCompletionTime(AG,TG,SHM,TaskToBeMapped))
        TG.node[TaskToBeMapped]['Node'] = ChosenNode
        AG.node[ChosenNode]['MappedTasks'].append(TaskToBeMapped)
        Scheduling_Functions.Add_TG_TaskToNode(TG,AG,SHM,TaskToBeMapped,ChosenNode,False)
        print "\tTASK",TaskToBeMapped,"MAPPED ON NODE:",ChosenNode
    print "MIN COMPLETION TIME MAPPING FINISHED..."
    Scheduling_Functions.ReportMappedTasks(AG)
    return TG,AG

def FirstFree(TG,AG,SHM):
    print "==========================================="
    print "STARTING FIRST FREE MAPPING"
    # Todo: to write the function

    print "FIRST FREE MAPPING FINISHED..."
    Scheduling_Functions.ReportMappedTasks(AG)
    return TG,AG