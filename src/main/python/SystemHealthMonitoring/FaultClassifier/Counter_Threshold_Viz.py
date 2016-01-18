# Copyright (C) 2015 Siavoosh Payandeh Azad
import matplotlib.pyplot as plt
from ConfigAndPackages import Config
import numpy

def counter_threshold_viz(ag, counter_threshold):
    """
    Generates visualization for the counter-threshold module and saves it in GraphDrawings folder.
    :param ag: architecture graph
    :param counter_threshold: counter_threshold object
    :return: None
    """
    num_of_plots = len(counter_threshold.counters_f_report) * 3
    width = min(len(counter_threshold.counters_f_report["0"])/10, 32768)
    # print width, num_of_plots
    fig = plt.figure(figsize=(width, num_of_plots))
    plt.subplots_adjust(hspace=0.5)
    max_threshold_value = max(Config.fault_counter_threshold, Config.health_counter_threshold,
                              Config.intermittent_counter_threshold)
    count = 0
    for node in ag.nodes():

        location = str(node)
        length = len(counter_threshold.counters_f_report[location])
        count += 1
        # we add the graphs one by one, the Health graph is at the back, then Fault graph and then intermittent
        # graph in front.
        ax1 = fig.add_subplot(length, 1, count)
        ax1.fill_between(counter_threshold.viz_counter_list[location]+[length, length],
                         counter_threshold.counters_h_report[location]+[0, max_threshold_value], 0, facecolor='g')
        ax1.fill_between(counter_threshold.viz_counter_list[location]+[length, length],
                         counter_threshold.counters_f_report[location]+[0, max_threshold_value], 0, facecolor='r')
        ax1.fill_between(counter_threshold.viz_counter_list[location]+[length, length],
                         counter_threshold.counters_i_report[location]+[0, max_threshold_value], 0, edgecolor='k')
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax1.get_yticklabels(), visible=False)
        # move the y labels away
        ax1.yaxis.set_label_coords(-0.01, 0)
        ax1.set_ylabel(r'PE'+str(node), size=14, rotation=0)
        # removes the extra white space at the end of the graph
        ax1.set_xlim(0, width+1)

    for node in ag.nodes():
        location = "R"+str(node)
        length = len(counter_threshold.counters_f_report[location])
        count += 1
        ax1 = fig.add_subplot(length, 1, count)
        ax1.fill_between(counter_threshold.viz_counter_list[location]+[length, length],
                         counter_threshold.counters_h_report[location]+[0, max_threshold_value], 0, facecolor='g')
        ax1.fill_between(counter_threshold.viz_counter_list[location]+[length, length],
                         counter_threshold.counters_f_report[location]+[0, max_threshold_value], 0, facecolor='r')
        ax1.fill_between(counter_threshold.viz_counter_list[location]+[length, length],
                         counter_threshold.counters_i_report[location]+[0, max_threshold_value], 0, edgecolor='k')
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax1.get_yticklabels(), visible=False)
        ax1.set_ylabel(r'R'+str(node), size=14, rotation=0)
         # move the y labels away
        ax1.yaxis.set_label_coords(-0.01, 0)
        # removes the extra white space at the end of the graph
        ax1.set_xlim(0, width+1)

    link_counter = 0
    for link in ag.edges():
        location = "L"+str(link[0])+str(link[1])
        length = len(counter_threshold.counters_f_report[location])
        count += 1
        link_counter += 1
        ax1 = fig.add_subplot(length, 1, count)
        ax1.fill_between(counter_threshold.viz_counter_list[location]+[length, length],
                         counter_threshold.counters_h_report[location]+[0, max_threshold_value], 0, facecolor='g')
        ax1.fill_between(counter_threshold.viz_counter_list[location]+[length, length],
                         counter_threshold.counters_f_report[location]+[0, max_threshold_value], 0, facecolor='r')
        ax1.fill_between(counter_threshold.viz_counter_list[location]+[length, length],
                         counter_threshold.counters_i_report[location]+[0, max_threshold_value], 0, edgecolor='k')
        plt.setp(ax1.get_yticklabels(), visible=False)
        if link_counter != len(ag.edges()):
            plt.setp(ax1.get_xticklabels(), visible=False)
        # move the y labels away
        ax1.yaxis.set_label_coords(-0.01, 0)
        ax1.set_ylabel(location, size=14, rotation=0)
        # removes the extra white space at the end of the graph
        ax1.set_xlim(0, width+1)

    plt.savefig("GraphDrawings/Counter_Threshold_Viz.png", dpi=200, bbox_inches='tight')
    plt.clf()
    plt.close(fig)
