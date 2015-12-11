# Copyright (C) 2015 Siavoosh Payandeh Azad

# starting to write the simulator with SimPy...
import simpy
import numpy

from ConfigAndPackages import Config
from FaultInjector import fault_event
from Scheduler import Scheduling_Reports
from SystemHealthMonitoring.FaultClassifier import CounterThreshold


def processor_sim(env, node, schedule, fault_time_list, counter_threshold, logging):
    """
    Runs tasks on each node
    :param env: simulation environment
    :param node: Node ID number
    :param schedule: schedule of the tasks on the Node
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    found = False
    task_num = None
    length = 0
    while True:
        for key in schedule.keys():
            if env.now == schedule[key][0]:
                print float("{0:.1f}".format(env.now)), "\tNODE:: Found Task", key, " to run on Node:", node
                length = schedule[key][1]-schedule[key][0]
                found = True
                task_num = key
                break
        if found:
            print float("{0:.1f}".format(env.now)), "\tNODE:: Starting Task", task_num, "on Node:", node
            for fault_time in fault_time_list:
                if env.now <= fault_time <= env.now+length:
                    pass
                else:
                    counter_threshold.increase_health_counter(node, logging)
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tNODE:: Task", task_num, "execution finished on Node", node
            found = False
        else:
            yield env.timeout(1)


def router_sim(env, node, schedule, fault_time_list, counter_threshold, logging):
    """
    runs tasks on the routers
    :param env: simulation environment
    :param node: ID of the node to be simulated
    :param schedule: schedule of the tasks on the Router
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    found = False
    task_num = None
    length = 0
    # print "HERE:",Schedule
    while True:

        for key in schedule.keys():
            if env.now == schedule[key][0][0]:
                print float("{0:.1f}".format(env.now)), "\tRouter:: Found Task", key, " to run on Router:", node
                length = schedule[key][0][1]-schedule[key][0][0]
                found = True
                task_num = key
                break
        if found:
            print float("{0:.1f}".format(env.now)), "\tRouter:: Starting Task", task_num, "on Router:", node
            location_dict = {node: "R"}
            for fault_time in fault_time_list:
                if env.now <= fault_time <= env.now+length:
                    pass
                else:
                    counter_threshold.increase_health_counter(location_dict, logging)
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tRouter:: Task", task_num, "execution finished on Router", node
            found = False
        else:
            yield env.timeout(1)


def link_sim(env, link, schedule, fault_time_list, counter_threshold, logging):
    """
    Runs tasks on each link
    :param env: simulation environment
    :param link: link number
    :param schedule: schedule of the tasks on the link
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    found = False
    task_num = None
    length = 0
    while True:
        for key in schedule.keys():
            if env.now == schedule[key][0][0]:
                print float("{0:.1f}".format(env.now)), "\tLINK:: Found Task", key, " to run on Link:", link
                length = schedule[key][0][1]-schedule[key][0][0]
                found = True
                task_num = key
        if found:
            print float("{0:.1f}".format(env.now)), "\tLINK:: Starting Task", task_num, "on Link:", link
            for fault_time in fault_time_list:
                if env.now <= fault_time <= env.now+length:
                    pass
                else:
                    counter_threshold.increase_health_counter(link, logging)
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tLINK:: Task", task_num, "execution finished on Link", link
            found = False
        else:
            yield env.timeout(1)


def run_simulator(runtime, AG, SHM, NoCRG, logging):
    print "==========================================="
    print "STARTING SIMULATION..."
    env = simpy.Environment()
    counter_threshold = CounterThreshold.CounterThreshold(Config.fault_counter_threshold,
                                                          Config.health_counter_threshold, 0)

    fault_time_list = []
    fault_time = 0
    if Config.EventDrivenFaultInjection:
        time_until_next_fault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
        fault_time += time_until_next_fault
        while fault_time < runtime:
            fault_time_list.append(float("{0:.1f}".format(fault_time)))
            time_until_next_fault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
            fault_time += time_until_next_fault
        print fault_time_list
        env.process(fault_event(env, AG, SHM, NoCRG, fault_time_list, counter_threshold, logging))

    for node in AG.nodes():
        # print node, AG.node[node]["Scheduling"]
        env.process(processor_sim(env, node, AG.node[node]['PE'].Scheduling,
                                  fault_time_list, counter_threshold, logging))
        env.process(router_sim(env, node, AG.node[node]['Router'].Scheduling,
                               fault_time_list, counter_threshold, logging))
    for link in AG.edges():
        # print link, AG.edge[link[0]][link[1]]["Scheduling"]
        env.process(link_sim(env, link, AG.edge[link[0]][link[1]]["Scheduling"],
                             fault_time_list, counter_threshold, logging))

    env.run(until=runtime)
    print "SIMULATION FINISHED..."
    counter_threshold.report(len(AG.nodes()))
    Scheduling_Reports.report_scheduling_memory_usage(AG)
    return None