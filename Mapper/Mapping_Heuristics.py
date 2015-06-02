__author__ = 'siavoosh'
import Mapping_Functions
from Scheduler import Scheduling_Functions
import copy
import random
def Min_Min_Mapping (TG,AG,NoCRG,Report):
    # this function finds the task with the smallest WCET and
    # maps it on the machine that can offer smallest completion time...
    # this means that the mapping algorithm has to take into account the mapping
    # of the edges of the task graph on the links.
    # Note:: this is a heuristic for independent tasks... so we are not going to
    # schedule any link
    print "STARTING MIN-MIN MAPPING"
    ShortestTasks = Mapping_Functions.FindUnMappedTaskWithSmallestWCET(TG,False)
    while len(ShortestTasks)>0 :
        TaskToBeMapped = ShortestTasks.pop()
        # map the task on the Node that yields smallest Completion time
        CandidateNodes=Mapping_Functions.FindNodeWithSmallestCompletionTime(AG,TG,TaskToBeMapped,True)
        print "\tCANDIDATE NODES FOR MAPPING:",CandidateNodes
        if len(CandidateNodes)>0:
            ChosenNode=random.choice(CandidateNodes)
            print "\t\tMAPPING TASK",TaskToBeMapped, "ON NODE:",ChosenNode
            TG.node[TaskToBeMapped]['Node'] = ChosenNode
            AG.node[ChosenNode]['MappedTasks'].append(TaskToBeMapped)
            Scheduling_Functions.Add_TG_TaskToNode(TG,AG,TaskToBeMapped,ChosenNode,False)
        if len(ShortestTasks) == 0:
            ShortestTasks = Mapping_Functions.FindUnMappedTaskWithSmallestWCET(TG,False)
    print "MIN-MIN MAPPING FINISHED..."
    Scheduling_Functions.ReportMappedTasks(AG)
    return None


def Max_Min_Mapping (TG,AG,NoCRG,Report):
    # this function finds the task with the biggest WCET and
    # maps it on the machine that can offer smallest completion time...
    # this means that the mapping algorithm has to take into account the mapping
    # of the edges of the task graph on the links.
    # Note:: this is a heuristic for independent tasks... so we are not going to
    # schedule any link
    print "STARTING MIN-MAX MAPPING"
    LongestTasks = Mapping_Functions.FindUnMappedTaskWithBiggestWCET(TG,False)
    while len(LongestTasks)>0 :
        TaskToBeMapped = LongestTasks.pop()
        # map the task on the Node that yields smallest Completion time
        CandidateNodes=Mapping_Functions.FindNodeWithSmallestCompletionTime(AG,TG,TaskToBeMapped,True)
        print "CANDIDATE NODES FOR MAPPING:",CandidateNodes
        if len(CandidateNodes)>0:
            ChosenNode=random.choice(CandidateNodes)
            print "\tMAPPING TASK",TaskToBeMapped, "ON NODE:",ChosenNode
            TG.node[TaskToBeMapped]['Node'] = ChosenNode
            AG.node[ChosenNode]['MappedTasks'].append(TaskToBeMapped)
            Scheduling_Functions.Add_TG_TaskToNode(TG,AG,TaskToBeMapped,ChosenNode,False)
        if len(LongestTasks) == 0:
            LongestTasks = Mapping_Functions.FindUnMappedTaskWithBiggestWCET(TG,False)
    print "MIN-MAX MAPPING FINISHED..."
    Scheduling_Functions.ReportMappedTasks(AG)
    return None