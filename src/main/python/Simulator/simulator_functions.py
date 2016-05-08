# Copyright (C) 2016 Siavoosh Payandeh Azad

import numpy
import copy
from ast import literal_eval
from ConfigAndPackages import Config
from SystemHealthMonitoring import SHMU_Functions


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
    return fault_time_dict


def generate_fault_time_dict_from_file(runtime, shm):
    # todo! we have to fill this dictionary  from the file no need to update later. that is done using update func
    fault_time_dict = {}
    fault_file = open(Config.fault_injection_file, 'r')
    line = fault_file.readline()
    while line != '':
        line = line.rstrip()
        fault_item = line.split('\t')
        # print literal_eval(fault_item[1])
        fault_time_dict[float("{0:.1f}".format(float(fault_item[0])))] = (literal_eval(fault_item[1]), fault_item[2])
        line = fault_file.readline()

    return fault_time_dict


def update_fault_time_dict(current_time, fault_time_dictionary):
    fault_time_dict = copy.deepcopy(fault_time_dictionary)
    for fault_time in fault_time_dict.keys():
        if fault_time < current_time:
            fault_time_dict.pop(fault_time, None)
        else:
            dict_value = fault_time_dict[fault_time]
            fault_time_dict.pop(fault_time, None)
            fault_time_dict[fault_time-current_time] = dict_value
    return fault_time_dict