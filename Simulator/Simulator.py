# Copyright (C) 2015 Siavoosh Payandeh Azad

# starting to write the simulator with SimPy...

import simpy

def Processor(env, Node, Schedule):
    Found = False
    TaskNum = None
    length = 0
    while True:
        for key in Schedule.keys():
            if env.now == Schedule[key][0]:
                print "NODE:: Found Task", key, " to run at time:", env.now
                length = Schedule[key][1]-Schedule[key][0]
                Found = True
                TaskNum = key
                break
        if Found:
            yield env.timeout(length)
            print "NODE:: Ran Task", TaskNum, "on Node:", Node
            Found = False
        else:
            yield env.timeout(1)

def Link(env, Link, Schedule):
    Found = False
    TaskNum = None
    length = 0
    while True:
        for key in Schedule.keys():
            if env.now == Schedule[key][0][0]:
                print "LINK:: Found Task", key, " to run at time:", env.now
                length = Schedule[key][0][1]-Schedule[key][0][0]
                Found = True
                TaskNum = key
        if Found:
            yield env.timeout(length)
            print "LINK:: Ran Task", TaskNum, "on Link:", Link, "Current time on link:", env.now
            Found = False
        else:
            yield env.timeout(1)


def RunSimualtor(Runtime, AG):
    env = simpy.Environment()
    for node in AG.nodes():
        # print node, AG.node[node]["Scheduling"]
        env.process(Processor(env, node, AG.node[node]["Scheduling"]))
    for link in AG.edges():
        # print link, AG.edge[link[0]][link[1]]["Scheduling"]
        env.process(Link(env, link, AG.edge[link[0]][link[1]]["Scheduling"]))
    env.run(until=10*Runtime)