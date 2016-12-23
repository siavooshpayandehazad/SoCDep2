# Copyright (C) 2016 Siavoosh Payandeh Azad

import numpy
import copy
from ast import literal_eval
from ConfigAndPackages import Config
from SystemHealthMonitoring import SHMU_Functions
import matplotlib.pyplot as plt


def generate_random_fault_time_dict(runtime, shm):
    """
    generates random fault time dictionary
    :param runtime: simulation runtime
    :param shm: system health map
    :return: fault time dictionary
    """
    fault_time_dict = {}
    fault_time = 0
    time_until_next_fault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
    fault_time += time_until_next_fault
    while fault_time < runtime:
        fault_location, fault_type = SHMU_Functions.random_fault_generation(shm)
        fault_time_dict[float("{0:.1f}".format(fault_time))] = (fault_location, fault_type)
        time_until_next_fault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
        fault_time += time_until_next_fault
    fault_file = open('Generated_Files/Injected_Faults.txt', 'w')
    for item in fault_time_dict:
        fault_file.write(str(item)+"\t"+str(fault_time_dict[item][0])+"\t"+str(fault_time_dict[item][1])+"\n")
    draw_faults_locations(fault_time_dict)
    return fault_time_dict


def generate_fault_time_dict_from_file():
    fault_time_dict = {}
    fault_file = open(Config.fault_injection_file, 'r')
    line = fault_file.readline()
    while line != '':
        line = line.rstrip()
        fault_item = line.split('\t')
        # print literal_eval(fault_item[1])
        fault_time_dict[float("{0:.1f}".format(float(fault_item[0])))] = (literal_eval(fault_item[1]), fault_item[2])
        line = fault_file.readline()
    draw_faults_locations(fault_time_dict)
    return fault_time_dict


def update_fault_time_dict(current_time, fault_time_dictionary):
    temp_dict = {}
    for fault_time in fault_time_dictionary.keys():
        if fault_time < current_time:
            pass
        else:
            dict_value = fault_time_dictionary[fault_time]
            temp_dict[fault_time-current_time] = dict_value
    return temp_dict


def draw_faults_locations(fault_time_dict):

    plt.figure()
    location_time_dictionary = {}
    for item in fault_time_dict:
        fault_location = fault_time_dict[item][0]
        if fault_location in location_time_dictionary.keys():
            location_time_dictionary[fault_location].append(int(item))
        else:
            location_time_dictionary[fault_location] = [int(item)]
    for location in location_time_dictionary.keys():
        time_list = location_time_dictionary[location]
        # print location, time_list
        values = []
        x_axis = []

        for i in range(0, int(Config.ProgramRunTime)):
            if i == 0:
                values.append(2)
            else:
                if i in time_list:
                    values.append(1)
                else:
                    values.append(0)
            x_axis.append(i)
        # print values
        # print x_axis
        # print "---------------------------"
        plt.xlim(xmin=0, xmax=Config.ProgramRunTime)
        plt.bar(x_axis, values, align='center')

        plt.savefig("GraphDrawings/Components_Fault_Drawings/Fault_config_for_loc_"+str(location)+".png", dpi=100)
        # plt.xticks(range(len(D)), D.keys())
        plt.clf()
        plt.close()
    return None
