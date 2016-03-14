# Copyright (C) 2015 Siavoosh Payandeh Azad
import matplotlib.pyplot as plt
from ConfigAndPackages import Config


def counter_threshold_viz(ag, counter_threshold):
    """
    Generates visualization for the counter-threshold module and saves it in GraphDrawings folder.
    :param ag: architecture graph
    :param counter_threshold: counter_threshold object
    :return: None
    """
    width = len(counter_threshold.viz_counter_list["0"])
    number_of_plots = 0
    if Config.enable_link_counters:
        number_of_plots += len(ag.edges())
    if Config.enable_pe_counters:
        number_of_plots += len(ag.nodes())
    if Config.enable_router_counters:
        number_of_plots += len(ag.nodes())
    # number_of_plots = len(counter_threshold.viz_counter_list)
    fig = plt.figure(figsize=(width/10, 20))
    plt.subplots_adjust(hspace=0.01)
    max_threshold_value = max(Config.fault_counter_threshold, Config.health_counter_threshold,
                              Config.intermittent_counter_threshold)+0.05
    count = 0
    # for Processing elements
    if Config.enable_pe_counters:
        for node in ag.nodes():

            location = str(node)
            last_number = counter_threshold.viz_counter_list[location][-1]
            count += 1
            # we add the graphs one by one, the Health graph is at the back, then Fault graph and then intermittent
            # graph in front.
            ax1 = fig.add_subplot(number_of_plots, 1, count)
            # Generating health monitor counters visualization
            ax1.fill_between(counter_threshold.viz_counter_list[location]+[last_number, last_number],
                             counter_threshold.counters_h_report[location]+[0, max_threshold_value], 0,
                             facecolor='g')
            # Generating fault monitor counters visualization
            ax1.fill_between(counter_threshold.viz_counter_list[location]+[last_number, last_number],
                             counter_threshold.counters_f_report[location]+[0, max_threshold_value], 0,
                             facecolor='r')
            # Generating intermittent monitor counters visualization
            ax1.fill_between(counter_threshold.viz_counter_list[location]+[last_number, last_number],
                             counter_threshold.counters_i_report[location]+[0, max_threshold_value], 0,
                             edgecolor='k')
            # disable x and y axis ticks
            plt.setp(ax1.get_xticklabels(), visible=False)
            plt.setp(ax1.get_yticklabels(), visible=False)
            # move the y labels away
            ax1.yaxis.set_label_coords(-0.01, 0)
            ax1.set_ylabel(r'PE'+str(node), size=14, rotation=0)
            # removes the extra white space at the end of the graph
            ax1.set_xlim(0, last_number+1)

    # For Routers
    if Config.enable_router_counters:
        for node in ag.nodes():
            location = "R"+str(node)
            last_number = counter_threshold.viz_counter_list[location][-1]
            count += 1
            ax1 = fig.add_subplot(number_of_plots, 1, count)
            # Generating health monitor counters visualization
            ax1.fill_between(counter_threshold.viz_counter_list[location]+[last_number, last_number],
                             counter_threshold.counters_h_report[location]+[0, max_threshold_value], 0, facecolor='g')
            # Generating fault monitor counters visualization
            ax1.fill_between(counter_threshold.viz_counter_list[location]+[last_number, last_number],
                             counter_threshold.counters_f_report[location]+[0, max_threshold_value], 0, facecolor='r')
            # Generating intermittent monitor counters visualization
            ax1.fill_between(counter_threshold.viz_counter_list[location]+[last_number, last_number],
                             counter_threshold.counters_i_report[location]+[0, max_threshold_value], 0, edgecolor='k')
            # disable x and y axis ticks
            plt.setp(ax1.get_xticklabels(), visible=False)
            plt.setp(ax1.get_yticklabels(), visible=False)
            ax1.set_ylabel(r'R'+str(node), size=14, rotation=0)
            # move the y labels away
            ax1.yaxis.set_label_coords(-0.01, 0)
            # removes the extra white space at the end of the graph
            ax1.set_xlim(0, last_number+1)

    # for physical links
    if Config.enable_link_counters:
        link_counter = 0
        for link in ag.edges():
            location = "L"+str(link[0])+str(link[1])
            last_number = counter_threshold.viz_counter_list[location][-1]
            count += 1
            link_counter += 1
            ax1 = fig.add_subplot(number_of_plots, 1, count)
            # Generating health monitor counters visualization
            ax1.fill_between(counter_threshold.viz_counter_list[location]+[last_number, last_number],
                             counter_threshold.counters_h_report[location]+[0, max_threshold_value], 0, facecolor='g')
            # Generating fault monitor counters visualization
            ax1.fill_between(counter_threshold.viz_counter_list[location]+[last_number, last_number],
                             counter_threshold.counters_f_report[location]+[0, max_threshold_value], 0, facecolor='r')
            # Generating intermittent monitor counters visualization
            ax1.fill_between(counter_threshold.viz_counter_list[location]+[last_number, last_number],
                             counter_threshold.counters_i_report[location]+[0, max_threshold_value], 0, edgecolor='k')
            # disable x and y axis ticks
            if link_counter != len(ag.edges()):
                plt.setp(ax1.get_xticklabels(), visible=False)
            plt.setp(ax1.get_yticklabels(), visible=False)
            # move the y labels away
            ax1.yaxis.set_label_coords(-0.01, 0)
            ax1.set_ylabel(location, size=14, rotation=0)
            # removes the extra white space at the end of the graph
            ax1.set_xlim(0, last_number+1)

    plt.savefig("GraphDrawings/Counter_Threshold_Viz.png", dpi=120, bbox_inches='tight')
    plt.clf()
    plt.close(fig)
