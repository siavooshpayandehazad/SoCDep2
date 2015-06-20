# Copyright (C) 2015 Siavoosh Payandeh Azad 


import copy
from TaskGraphUtilities import TG_Functions
from Scheduling_Functions import Add_TG_TaskToNode
from Scheduling_Functions import Add_TG_EdgeTo_link

def ScheduleAll(TG,AG,SHM,Report,DetailedReport):
    if Report:print "==========================================="
    if Report:print "STARTING SCHEDULING PROCESS..."
    # first schedule the high critical tasks and their high critical transactions
    MaxDistance = TG_Functions.CalculateMaxDistance(TG) + 1
    for Distance in range(0, MaxDistance):
        for Task in TG.nodes():
            if TG.node[Task]['Distance'] == Distance:
                if TG.node[Task]['Criticality']=='H':
                    Node = TG.node[Task]['Node']
                    if DetailedReport:print "\tSCHEDULING TASK",Task,"ON NODE:",Node
                    Add_TG_TaskToNode(TG,AG,SHM,Task,Node,DetailedReport)
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                            if TG.edge[Edge[0]][Edge[1]]['Criticality']=='H':
                                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                    for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                        if DetailedReport:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                        Add_TG_EdgeTo_link(TG,AG,Edge,Link,DetailedReport)

    for Distance in range(0 , MaxDistance):
        for Task in TG.nodes():
            if TG.node[Task]['Distance'] == Distance:
                if TG.node[Task]['Criticality']=='GNH' or TG.node[Task]['Criticality']=='GH':
                    Node = TG.node[Task]['Node']
                    if DetailedReport:print "\tSCHEDULING TASK",Task,"ON NODE:",Node
                    Add_TG_TaskToNode(TG,AG,SHM,Task,Node,DetailedReport)
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                            if TG.edge[Edge[0]][Edge[1]]['Criticality']=='H':
                                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                    for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                        if DetailedReport:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                        Add_TG_EdgeTo_link(TG,AG,Edge,Link,DetailedReport)

    for Distance in range(0 , MaxDistance):
        for Task in TG.nodes():
            if TG.node[Task]['Distance'] == Distance:
                if TG.node[Task]['Criticality']=='GH' or TG.node[Task]['Criticality']=='GNH':
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                            if TG.edge[Edge[0]][Edge[1]]['Criticality']=='L':
                                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                    for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                        if DetailedReport:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                        Add_TG_EdgeTo_link(TG,AG,Edge,Link,DetailedReport)

    for Distance in range(0 , MaxDistance):
        for Task in TG.nodes():
            if TG.node[Task]['Distance'] == Distance:
                if TG.node[Task]['Criticality']=='L':
                    Node = TG.node[Task]['Node']
                    if DetailedReport:print "\tSCHEDULING TASK",Task,"ON NODE:",Node
                    Add_TG_TaskToNode(TG,AG,SHM,Task,Node,DetailedReport)
                    for Edge in TG.edges():
                        if Edge[0]==Task:
                                if len(TG.edge[Edge[0]][Edge[1]]['Link'])>0:
                                    for Link in TG.edge[Edge[0]][Edge[1]]['Link']:
                                        if DetailedReport:print "\tSCHEDULING EDGE",Edge,"ON Link:",Link
                                        Add_TG_EdgeTo_link(TG,AG,Edge,Link,DetailedReport)

    if Report:print "DONE SCHEDULING..."
    return None


