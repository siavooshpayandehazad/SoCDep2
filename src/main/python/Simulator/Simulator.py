# Copyright (C) 2015 Siavoosh Payandeh Azad

# starting to write the simulator with SimPy...
import simpy
import numpy

from ConfigAndPackages import Config
from FaultInjector import FaultEvent
from SystemHealthMonitoring.FaultClassifier import CounterThreshold


def Processor(env, Node, Schedule, counter_threshold, logging):
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
            counter_threshold.decrease_counter(Node, logging)
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tNODE:: Task", TaskNum, "execution finished on Node", Node
            Found = False
        else:
            yield env.timeout(1)

def Router(env, Node, Schedule, counter_threshold, logging):
    Found = False
    TaskNum = None
    length = 0
    #print "HERE:",Schedule
    while True:

        for key in Schedule.keys():
            if env.now == Schedule[key][0][0]:
                print float("{0:.1f}".format(env.now)), "\tRouter:: Found Task", key, " to run on Router:", Node
                length = Schedule[key][0][1]-Schedule[key][0][0]
                Found = True
                TaskNum = key
                break
        if Found:
            print float("{0:.1f}".format(env.now)), "\tRouter:: Starting Task", TaskNum, "on Router:", Node
            dict = {Node: "R"}
            counter_threshold.decrease_counter(dict, logging)
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tRouter:: Task", TaskNum, "execution finished on Router", Node
            Found = False
        else:
            yield env.timeout(1)


def Link(env, Link, Schedule, counter_threshold, logging):
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
            counter_threshold.decrease_counter(Link, logging)
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tLINK:: Task", TaskNum, "execution finished on Link", Link
            Found = False
        else:
            yield env.timeout(1)


def RunSimulator(Runtime, AG, SHM, NoCRG, logging):
    print "==========================================="
    print "STARTING SIMULATION..."
    env = simpy.Environment()
    counter_threshold = CounterThreshold.CounterThreshold(3)
    for node in AG.nodes():
        # print node, AG.node[node]["Scheduling"]
        env.process(Processor(env, node, AG.node[node]['PE'].Scheduling, counter_threshold, logging))
        env.process(Router(env, node, AG.node[node]['Router'].Scheduling, counter_threshold, logging))
    for link in AG.edges():
        # print link, AG.edge[link[0]][link[1]]["Scheduling"]
        env.process(Link(env, link, AG.edge[link[0]][link[1]]["Scheduling"], counter_threshold, logging))

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
        env.process(FaultEvent(env, AG, SHM, NoCRG, FaultTimeList, counter_threshold, logging))

    env.run(until=Runtime)
    print "DEAD Components:", counter_threshold.dead_components
    print "SIMULATION FINISHED..."