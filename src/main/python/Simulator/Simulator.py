# Copyright (C) 2015 Siavoosh Payandeh Azad

# starting to write the simulator with SimPy...
import simpy
import numpy
from SystemHealthMonitoring import SHMU_Functions
from ConfigAndPackages import Config
from FaultInjector import fault_event
from SystemHealthMonitoring.FaultClassifier import CounterThreshold, Counter_Threshold_Viz     # Rene's addition
from SystemHealthMonitoring.FaultClassifier import MachineLearning      # Rene's addition
from Scheduler import Scheduling_Reports, Scheduling_Functions


def sim_report(env, ag, counter_threshold):
    while True:
        counter_threshold.update_report_dict(ag)
        yield env.timeout(1)
        # if env.now >= Config.ProgramRunTime:
        #     env.exit()


def processor_sim(env, ag, node, schedule_length, fault_time_dict, counter_threshold, logging):
    """
    Runs tasks on each node
    :param env: simulation environment
    :param ag: architecture graph
    :param node: Node ID number
    :param schedule_length: schedule makespan
    :param fault_time_dict: Dictionary with Fault time as key and (Location, Type) tuple as value
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    found = False
    task_num = None
    length = 0
    schedule = ag.node[node]['PE'].scheduling
    while True:
        for key in schedule.keys():
            # checks if there is a task that starts at this time!
            if env.now % schedule_length == schedule[key][0]:
                length = schedule[key][1]-schedule[key][0]
                print float("{0:.1f}".format(env.now)), "\tNODE:: Found Task", key, " to run on Node:", node, "For:", \
                    length, "Cycles"
                found = True
                task_num = key
                break
        # found a task that starts at this time!
        if found:
            print float("{0:.1f}".format(env.now)), "\tNODE:: Starting Task", task_num, "on Node:", node
            for i in range(0, int(length)):
                if float("{0:.1f}".format(env.now)) in fault_time_dict.keys():
                    if fault_time_dict[float("{0:.1f}".format(env.now))][0] == node:
                        pass
                    else:
                        counter_threshold.increase_health_counter(ag, node, logging)
                else:
                    counter_threshold.increase_health_counter(ag, node, logging)
                yield env.timeout(1)
            print float("{0:.1f}".format(env.now)), "\tNODE:: Task", task_num, "execution finished on Node", node
            found = False
        else:
            yield env.timeout(1)
        # if env.now >= Config.ProgramRunTime:
        #     env.exit()


def router_sim(env, ag, node, schedule_length, fault_time_dict, counter_threshold, logging):
    """
    runs tasks on the routers
    :param env: simulation environment
    :param ag: architecture graph
    :param node: ID of the node to be simulated
    :param schedule_length: schedule makespan
    :param fault_time_dict: Dictionary with Fault time as key and (Location, Type) tuple as value
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    found = False
    task_num = None
    length = 0
    schedule = ag.node[node]['Router'].scheduling
    # print "HERE:",Schedule
    while True:

        for key in schedule.keys():
            # checks if there is a task that starts at this time!
            if env.now % schedule_length == schedule[key][0][0]:
                length = schedule[key][0][1]-schedule[key][0][0]
                print float("{0:.1f}".format(env.now)), "\tRouter:: Found Task", key, " to run on Router:", node,\
                    "For:", length, "Cycles"
                found = True
                task_num = key
                break
        # found a task that starts at this time!
        if found:
            print float("{0:.1f}".format(env.now)), "\tRouter:: Starting Task", task_num, "on Router:", node
            location_dict = {node: "R"}
            for i in range(0, int(length)):
                if float("{0:.1f}".format(env.now)) in fault_time_dict.keys():
                    if fault_time_dict[float("{0:.1f}".format(env.now))][0] == location_dict:
                        pass
                    else:
                        counter_threshold.increase_health_counter(ag, location_dict, logging)
                else:
                    counter_threshold.increase_health_counter(ag, location_dict, logging)
                yield env.timeout(1)

            print float("{0:.1f}".format(env.now)), "\tRouter:: Task", task_num, "execution finished on Router", node
            found = False
        else:
            yield env.timeout(1)
        # if env.now >= Config.ProgramRunTime:
        #    env.exit()


def link_sim(env, ag, link, schedule_length, fault_time_dict, counter_threshold, logging):
    """
    Runs tasks on each link
    :param env: simulation environment
    :param ag: architecture graph
    :param link: link number
    :param schedule_length: schedule makespan
    :param fault_time_dict: Dictionary with Fault time as key and (Location, Type) tuple as value
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    found = False
    task_num = None
    length = 0
    schedule = ag.edge[link[0]][link[1]]["Scheduling"]
    while True:
        for key in schedule.keys():
            # checks if there is a task that starts at this time!
            if env.now % schedule_length == schedule[key][0][0]:
                length = schedule[key][0][1]-schedule[key][0][0]
                print float("{0:.1f}".format(env.now)), "\tLINK:: Found Task", key, " to run on Link:", link, \
                    "For:", length, "Cycles"
                found = True
                task_num = key
        # found a task that starts at this time!
        if found:
            print float("{0:.1f}".format(env.now)), "\tLINK:: Starting Task", task_num, "on Link:", link
            for i in range(0, int(length)):
                if float("{0:.1f}".format(env.now)) in fault_time_dict.keys():
                    if fault_time_dict[float("{0:.1f}".format(env.now))][0] == link:
                        pass
                    else:
                        counter_threshold.increase_health_counter(ag, link, logging)
                else:
                    counter_threshold.increase_health_counter(ag, link, logging)
                yield env.timeout(1)
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tLINK:: Task", task_num, "execution finished on Link", link
            found = False
        else:
            yield env.timeout(1)
        # if env.now >= Config.ProgramRunTime:
        #     env.exit()


def run_simulator(runtime, ag, shmu, noc_rg, logging):
    """
    prepares and runs the simulator
    :param runtime: duration of which the user wants to run the program in cycles
    :param ag: architecture graph
    :param shmu: system health monitoring unit
    :param noc_rg: noc routing graph
    :param logging: logging file
    :return: None
    """
    print "==========================================="
    print "SETTING UP THE SIMULATOR..."
    env = simpy.Environment()
    print "SETTING UP counter-threshold MODULE..."
    if Config.classification_method == "counter_threshold":

        counter_threshold = CounterThreshold.CounterThreshold(Config.fault_counter_threshold,
                                                              Config.health_counter_threshold,
                                                              Config.intermittent_counter_threshold)
    elif Config.classification_method == "machine_learning":
        counter_threshold = MachineLearning.MachineLearning(Config.fault_counter_threshold,     # Rene's addition
                                                            Config.health_counter_threshold*3,
                                                            Config.intermittent_counter_threshold)
    else:
        raise ValueError("Unknown Classification Method!! Check config file")

    fault_time_dict = {}
    fault_time = 0
    schedule_length = Scheduling_Functions.find_schedule_make_span(ag)
    if Config.EventDrivenFaultInjection:
        time_until_next_fault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
        fault_time += time_until_next_fault
        while fault_time < runtime:
            fault_location, fault_type = SHMU_Functions.random_fault_generation(shmu.SHM)
            fault_time_dict[float("{0:.1f}".format(fault_time))] = (fault_location, fault_type)
            time_until_next_fault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
            fault_time += time_until_next_fault

        env.process(fault_event(env, ag, shmu, noc_rg, schedule_length, fault_time_dict, counter_threshold, logging))

    print "SETTING UP ROUTERS AND PES..."
    for node in ag.nodes():
        # print node, AG.node[node]["Scheduling"]
        env.process(processor_sim(env, ag, node, schedule_length,
                                  fault_time_dict, counter_threshold, logging))
        env.process(router_sim(env, ag, node, schedule_length,
                               fault_time_dict, counter_threshold, logging))

    print "SETTING UP LINKS..."
    for link in ag.edges():
        # print link, AG.edge[link[0]][link[1]]["Scheduling"]
        env.process(link_sim(env, ag, link, schedule_length,
                             fault_time_dict, counter_threshold, logging))

    env.process(sim_report(env, ag, counter_threshold))
    print "STARTING SIMULATION..."
    env.run(until=runtime)
    print "SIMULATION FINISHED..."
    counter_threshold.report(len(ag.nodes()), len(ag.edges()))
    Counter_Threshold_Viz.counter_threshold_viz(ag, counter_threshold)
    Scheduling_Reports.report_scheduling_memory_usage(ag)
    return None
