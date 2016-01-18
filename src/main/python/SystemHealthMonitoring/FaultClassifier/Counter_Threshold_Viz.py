# Copyright (C) 2015 Siavoosh Payandeh Azad
import matplotlib.pyplot as plt
from ConfigAndPackages import Config


def counter_threshold_viz(ag, counter_threshold):

    fig = plt.figure(figsize=(15, 100))
    plt.subplots_adjust(hspace=0.1)
    max_threshold_value = max(Config.fault_counter_threshold, Config.health_counter_threshold,
                              Config.intermittent_counter_threshold)
    count = 0
    for node in ag.nodes():

        location = str(node)
        length = len(counter_threshold.counters_f_report[location])
        count += 1
        ax1 = fig.add_subplot(length, 1, count)
        ax1.fill_between(range(0, length+1)+[length],
                         counter_threshold.counters_h_report[location]+[0, max_threshold_value], 0, facecolor='g')
        ax1.fill_between(range(0, length+1)+[length],
                         counter_threshold.counters_f_report[location]+[0, max_threshold_value], 0, facecolor='r')
        ax1.fill_between(range(0, length+1)+[length],
                         counter_threshold.counters_i_report[location]+[0, max_threshold_value], 0, edgecolor='k')
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax1.get_yticklabels(), visible=False)
        ax1.set_ylabel(r'PE'+str(node), size=14, rotation=0)
        # print counter_threshold.counters_f_report[location]
        # print counter_threshold.counters_i_report[location]
        # print counter_threshold.counters_h_report[location]

    for node in ag.nodes():
        location = "R"+str(node)
        length = len(counter_threshold.counters_f_report[location])
        count += 1
        ax1 = fig.add_subplot(length, 1, count)
        ax1.fill_between(range(0, length+1)+[length],
                         counter_threshold.counters_h_report[location]+[0, max_threshold_value], 0, facecolor='g')
        ax1.fill_between(range(0, length+1)+[length],
                         counter_threshold.counters_f_report[location]+[0, max_threshold_value], 0, facecolor='r')
        ax1.fill_between(range(0, length+1)+[length],
                         counter_threshold.counters_i_report[location]+[0, max_threshold_value], 0, edgecolor='k')
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax1.get_yticklabels(), visible=False)
        ax1.set_ylabel(r'R'+str(node), size=14, rotation=0)
        # print location
        # print counter_threshold.counters_f_report[location]
        # print counter_threshold.counters_i_report[location]
        # print counter_threshold.counters_h_report[location]

    for link in ag.edges():
        location = "L"+str(link[0])+str(link[1])
        length = len(counter_threshold.counters_f_report[location])
        count += 1
        ax1 = fig.add_subplot(length, 1, count)
        ax1.fill_between(range(0, length+1)+[length],
                         counter_threshold.counters_h_report[location]+[0, max_threshold_value], 0, facecolor='g')
        ax1.fill_between(range(0, length+1)+[length],
                         counter_threshold.counters_f_report[location]+[0, max_threshold_value], 0, facecolor='r')
        ax1.fill_between(range(0, length+1)+[length],
                         counter_threshold.counters_i_report[location]+[0, max_threshold_value], 0, edgecolor='k')
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax1.get_yticklabels(), visible=False)
        ax1.set_ylabel(r'L'+location, size=14, rotation=0)
        # print location
        # print counter_threshold.counters_f_report[location]
        # print counter_threshold.counters_i_report[location]
        # print counter_threshold.counters_h_report[location]

    plt.savefig("GraphDrawings/Counter_Threshold_Viz.png", dpi=200)
    plt.clf()
    plt.close(fig)