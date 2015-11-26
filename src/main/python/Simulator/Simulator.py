# Copyright (C) 2015 Siavoosh Payandeh Azad

# starting to write the simulator with SimPy...
import simpy
import numpy

from ConfigAndPackages import Config
from FaultInjector import FaultEvent

def Processor(env, Node, Schedule):
    """
    Runs tasks on each node
    :param env: simulation environment
    :param Node: Node ID number
    :param Schedule: schedule of the tasks on the Node
    :return: none
    """
    Found = False
    TaskNum = None
    length = 0
    while True:
        for key in Schedule.keys():
            if env.now == Schedule[key][0]:
                print float("{0:.1f}".format(env.now)), "\tNODE:: Found Task", key, " to run on Node:", Node
                length = Schedule[key][1]-Schedule[key][0]
                Found = True
                TaskNum = key
                break
        if Found:
            print float("{0:.1f}".format(env.now)), "\tNODE:: Starting Task", TaskNum, "on Node:", Node
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tNODE:: Task", TaskNum, "execution finished on Node", Node
            Found = False
        else:
            yield env.timeout(1)


def Link(env, Link, Schedule):
    """
    Runs tasks on each link
    :param env: simulation environment
    :param Link: Link number
    :param Schedule: schedule of the tasks on the link
    :return: none
    """
    Found = False
    TaskNum = None
    length = 0
    while True:
        for key in Schedule.keys():
            if env.now == Schedule[key][0][0]:
                print float("{0:.1f}".format(env.now)), "\tLINK:: Found Task", key, " to run on Link:", Link
                length = Schedule[key][0][1]-Schedule[key][0][0]
                Found = True
                TaskNum = key
        if Found:
            print float("{0:.1f}".format(env.now)), "\tLINK:: Starting Task", TaskNum, "on Link:", Link
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tLINK:: Task", TaskNum, "execution finished on Link", Link
            Found = False
        else:
            yield env.timeout(1)



def RunSimualtor(Runtime, AG, SHM, NoCRG):
    print "==========================================="
    print "STARTING SIMULATION..."
    env = simpy.Environment()
    for node in AG.nodes():
        # print node, AG.node[node]["Scheduling"]
        env.process(Processor(env, node, AG.node[node]['PE'].Scheduling))
    for link in AG.edges():
        # print link, AG.edge[link[0]][link[1]]["Scheduling"]
        env.process(Link(env, link, AG.edge[link[0]][link[1]]["Scheduling"]))

    FaultTimeList = []
    FaultTime = 0
    if Config.EventDrivenFaultInjection:
        TimeUntilNextFault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
        FaultTime += TimeUntilNextFault
        while FaultTime < Runtime:
            FaultTimeList.append(float("{0:.1f}".format(FaultTime)))
            TimeUntilNextFault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
            FaultTime += TimeUntilNextFault
        print FaultTimeList
        env.process(FaultEvent(env, AG, SHM, NoCRG, FaultTimeList))

    env.run(until=Runtime)
    print "SIMULATION FINISHED..."
