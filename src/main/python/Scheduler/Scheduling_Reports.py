# Copyright (C) 2015 Siavoosh Payandeh Azad

import matplotlib.pyplot as plt
from Scheduling_Functions_Routers import find_last_allocated_time_on_router
from Scheduling_Functions_Nodes import find_last_allocated_time_on_node
from Scheduling_Functions_Links import find_last_allocated_time_on_link
from ConfigAndPackages import Config
import random


##########################################################################
#
#                           SCHEDULING REPORT
#
#
##########################################################################
def report_mapped_tasks(ag, logging):
    logging.info("===========================================")
    logging.info("          REPORTING SCHEDULING ")
    logging.info("===========================================")
    for node in ag.nodes():
        logging.info("NODE"+str(node)+"CONTAINS THE FOLLOWING TASKS:"+str(ag.node[node]['PE'].mapped_tasks) +
                     "\tWITH SCHEDULING:"+str(ag.node[node]['PE'].scheduling))
    for link in ag.edges():
        logging.info("LINK" + str(link)+"CONTAINS THE FOLLOWING TG's Edges:" +
                     str(ag.edge[link[0]][link[1]]['MappedTasks']) + "\tWITH SCHEDULING:" +
                     str(ag.edge[link[0]][link[1]]['Scheduling']))
    return None


def report_scheduling_memory_usage(ag):
    print "==========================================="
    print "        SCHEDULING MEMORY REPORT"
    print "==========================================="
    counter = 0
    for node in ag.nodes():
        counter += len(ag.node[node]['PE'].scheduling)
        counter += len(ag.node[node]['Router'].scheduling)
    for link in ag.edges():
        counter += len(ag.edge[link[0]][link[1]]['Scheduling'])
    print "SCHEDULE MEMORY USE:", counter


##########################################################################
#
#
#                   Generating Gantt Charts
#
##########################################################################
def generate_gantt_charts(tg, ag, file_name):
    print ("===========================================")
    print ("GENERATING SCHEDULING GANTT CHARTS...")
    node_makespan_list = []
    router_makespan_list = []
    link_makespan_list = []
    for node in ag.nodes():
        node_makespan_list.append(find_last_allocated_time_on_node(ag, node, logging=None))
        router_makespan_list.append(find_last_allocated_time_on_router(ag, node, logging=None))
    for link in ag.edges():
        link_makespan_list.append(find_last_allocated_time_on_link(ag, link, logging=None))
    if len(link_makespan_list) > 0:
        max_time_link = max(link_makespan_list)
    else:
        max_time_link = 0
    if len(node_makespan_list) > 0:
        max_time_node = max(node_makespan_list)
    else:
        max_time_node = 0
    if len(router_makespan_list) > 0:
        max_time_router = max(router_makespan_list)
    else:
        max_time_router = 0
    max_time = max(max_time_link, max_time_node, max_time_router)

    node_counter = 0
    router_counter = 0
    link_counter = 0
    for node in ag.nodes():
        if len(ag.node[node]['PE'].mapped_tasks) > 0:
            node_counter += 1
        if len(ag.node[node]['Router'].mapped_tasks) > 0:
            router_counter += 1
    for Link in ag.edges():
        if len(ag.edge[Link[0]][Link[1]]['MappedTasks']) > 0:
            link_counter += 1
    num_of_plots = node_counter + link_counter + router_counter
    if num_of_plots < 10:
        num_of_plots = 10
    count = 1
    fig = plt.figure(figsize=(max_time/10+1, num_of_plots/2))
    plt.subplots_adjust(hspace=0.1)
    count, ax1 = add_pe_to_drawing(tg, ag, num_of_plots, fig, node_counter,
                                   link_counter, router_counter, max_time, count)
    count, ax1 = add_routers_to_drawing(tg, ag, num_of_plots, fig, node_counter,
                                        link_counter, router_counter, max_time, count)
    count, ax1 = add_links_to_drawing(tg, ag, num_of_plots, fig, node_counter, link_counter,
                                      router_counter, max_time, count)

    if link_counter+node_counter+router_counter > 0:
        if ax1 is not None:
            ax1.xaxis.set_ticks_position('bottom')
    plt.savefig("GraphDrawings/"+file_name+".png", dpi=200, bbox_inches='tight')
    plt.clf()
    plt.close(fig)
    print ("\033[35m* VIZ::\033[0mSCHEDULING GANTT CHARTS CREATED AT: GraphDrawings/Scheduling.png")
    return None


def add_pe_to_drawing(tg, ag, num_of_plots, fig, node_counter, link_counter, router_counter, max_time, count):
    ax1 = None
    for node in ag.nodes():
        if len(ag.node[node]['PE'].mapped_tasks) > 0:
            ax1 = fig.add_subplot(num_of_plots, 1, count)
            for task in ag.node[node]['PE'].mapped_tasks:
                    pe_t = []
                    pe_p = []
                    pe_p.append(0)
                    pe_t.append(0)
                    slack_t = []
                    slack_p = []
                    slack_t.append(0)
                    slack_p.append(0)
                    task_color = 'w'
                    if task in ag.node[node]['PE'].scheduling:
                        if tg.node[task]['task'].criticality == 'H':
                            start_time = ag.node[node]['PE'].scheduling[task][0]
                            task_length = ag.node[node]['PE'].scheduling[task][1] - ag.node[node]['PE'].scheduling[task][0]
                            end_time = start_time + (task_length/(Config.Task_SlackCount+1))
                            pe_t.append(start_time)
                            pe_p.append(0)
                            pe_t.append(start_time)
                            pe_p.append(0.1)
                            pe_t.append(end_time)
                            pe_p.append(0.1)
                            pe_t.append(end_time)
                            pe_p.append(0)
                            task_color = '#FF878B'
                            if Config.Task_SlackCount > 0:
                                start_time = end_time
                                end_time = start_time + (task_length / (Config.Task_SlackCount+1)) * Config.Task_SlackCount
                                slack_t.append(start_time)
                                slack_p.append(0)
                                slack_t.append(start_time)
                                slack_p.append(0.1)
                                slack_t.append(end_time)
                                slack_p.append(0.1)
                                slack_t.append(end_time)
                                slack_p.append(0)
                        else:
                            start_time = ag.node[node]['PE'].scheduling[task][0]
                            end_time = ag.node[node]['PE'].scheduling[task][1]
                            pe_t.append(start_time)
                            pe_p.append(0)
                            pe_t.append(start_time)
                            pe_p.append(0.1)
                            pe_t.append(end_time)
                            pe_p.append(0.1)
                            pe_t.append(end_time)
                            pe_p.append(0)
                            if tg.node[task]['task'].criticality == 'GH':
                                task_color = '#FFC29C'
                            elif tg.node[task]['task'].criticality == 'GNH':
                                task_color = '#928AFF'
                            else:
                                if tg.node[task]['task'].type == 'Test':
                                    if 'S' in task:
                                        task_color = '#FFDA3D'
                                    else:
                                        task_color = '#FFEAA7'
                                else:
                                    task_color = '#CFECFF'
                    pe_t.append(max_time)
                    pe_p.append(0)
                    ax1.fill_between(pe_t, pe_p, 0, facecolor=task_color, edgecolor='k')
                    if Config.Task_SlackCount > 0:
                        ax1.fill_between(slack_t, slack_p, 0, facecolor='#808080', edgecolor='k')
            plt.setp(ax1.get_yticklabels(), visible=False)
            if count < link_counter + node_counter + router_counter:
                plt.setp(ax1.get_xticklabels(), visible=False)

            for task in ag.node[node]['PE'].mapped_tasks:
                if task in ag.node[node]['PE'].scheduling:
                    start_time = ag.node[node]['PE'].scheduling[task][0]
                    if tg.node[task]['task'].criticality == 'H':
                        task_length = (ag.node[node]['PE'].scheduling[task][1] -
                                       ag.node[node]['PE'].scheduling[task][0])/(Config.Task_SlackCount+1)
                        ax1.text(start_time+task_length/2 - len(str(task))/2, 0.01, str(task), fontsize=10)
                        end_time = ag.node[node]['PE'].scheduling[task][1]
                        if Config.Task_SlackCount > 0:
                            ax1.text((start_time+task_length+end_time)/2 - len(str(task)+'S')/2,
                                     0.01, str(task)+'S', fontsize=5)
                    else:
                        end_time = ag.node[node]['PE'].scheduling[task][1]
                        ax1.text((start_time+end_time)/2 - len(str(task))/2, 0.01, str(task), fontsize=5)
            ax1.yaxis.set_label_coords(-0.08, 0)
            ax1.set_ylabel(r'PE'+str(node), size=14, rotation=0)
            # removes the extra white space at the end of the graph
            ax1.set_xlim(0, max_time+1)
            count += 1
    return count, ax1


def add_routers_to_drawing(tg, ag, num_of_plots, fig, node_counter, link_counter, router_counter, max_time, count):
    """
    :param tg: task Graph
    :param ag: Architecture Graph
    :param num_of_plots: Total Number of plots (All PEs that have mapping+All routers that pass a packet+all links)
    :param fig: a mathplotlib figure
    :param node_counter: counter that shows number of active nodes
    :param link_counter: counter that shows the number of active links
    :param router_counter:
    :param max_time: maximum execution time on the network
    :param count: counter of the number of plots added to this point
    :return: count ,ax1
    """
    ax1 = None
    for node in ag.nodes():
        if len(ag.node[node]['Router'].mapped_tasks) > 0:
            ax1 = fig.add_subplot(num_of_plots, 1, count)
            schedule_list = []
            zorder = len(ag.node[node]['Router'].mapped_tasks)
            for task in ag.node[node]['Router'].mapped_tasks:
                pe_t = [0, 0]
                pe_p = [0.1, 0]
                edge_color = 'w'
                slack_t = [0]
                slack_p = [0]

                if task in ag.node[node]['Router'].scheduling:
                    if tg.edge[task[0]][task[1]]['Criticality'] == 'H':
                        start_time = 0
                        end_time = 0
                        for batch_and_schedule in ag.node[node]['Router'].scheduling[task]:
                            start_time = batch_and_schedule[0]
                            # batch_num = batch_and_schedule[2]
                            task_length = batch_and_schedule[1] - start_time
                            end_time = batch_and_schedule[1]
                            pe_t.append(start_time)
                            pe_p.append(0)
                            pe_t.append(start_time)
                            pe_p.append(0.1)
                            pe_t.append(end_time)
                            pe_p.append(0.1)
                            pe_t.append(end_time)
                            pe_p.append(0)
                            edge_color = '#FF878B'
                            if Config.Communication_SlackCount > 0:
                                start_time = end_time
                                end_time = start_time + (task_length / (Config.Communication_SlackCount+1)) * Config.Communication_SlackCount
                                slack_t.append(start_time)
                                slack_p.append(0)
                                slack_t.append(start_time)
                                slack_p.append(0.1)
                                slack_t.append(end_time)
                                slack_p.append(0.1)
                                slack_t.append(end_time)
                                slack_p.append(0)
                        schedule_list.append((start_time, end_time, 1))
                        zorder -= 1
                    else:
                        for batch_and_schedule in ag.node[node]['Router'].scheduling[task]:

                            start_time = batch_and_schedule[0]
                            end_time = batch_and_schedule[1]
                            prob = batch_and_schedule[3]

                            pe_t.append(start_time)
                            pe_p.append(0)
                            pe_t.append(start_time)
                            pe_p.append(0.1 * prob)

                            past_prob = 0
                            for added_rect in schedule_list:
                                if added_rect[0] <= start_time < added_rect[1]:
                                    past_prob += added_rect[2]

                            if past_prob > 0:
                                pe_t.append(start_time)
                                prob = batch_and_schedule[3]+past_prob
                                pe_p.append(0.1 * prob)

                            up_dict = {}
                            for added_rect in schedule_list:
                                if start_time < added_rect[0] < end_time:
                                    if added_rect[0] in up_dict:
                                        up_dict[added_rect[0]] += added_rect[2]
                                    else:
                                        up_dict[added_rect[0]] = added_rect[2]

                            down_dict = {}
                            for added_rect in schedule_list:
                                if start_time < added_rect[1] < end_time:
                                    if added_rect[1] in down_dict:
                                        down_dict[added_rect[1]] += added_rect[2]
                                    else:
                                        down_dict[added_rect[1]] = added_rect[2]

                            for time_instant in sorted(up_dict.keys()+down_dict.keys()):
                                if time_instant in up_dict.keys():
                                    pe_t.append(time_instant)
                                    pe_p.append(0.1 * prob)
                                    prob = up_dict[time_instant] + prob
                                    pe_t.append(time_instant)
                                    pe_p.append(0.1 * prob)

                                if time_instant in down_dict.keys():
                                    pe_t.append(time_instant)
                                    pe_p.append(0.1 * prob)
                                    prob = prob - down_dict[time_instant]
                                    pe_t.append(time_instant)
                                    pe_p.append(0.1 * prob)

                            past_prob = 0
                            for added_rect in schedule_list:
                                if added_rect[0] < end_time <= added_rect[1]:
                                        past_prob += added_rect[2]

                            if past_prob > 0:
                                pe_t.append(end_time)
                                prob = batch_and_schedule[3]+past_prob
                                pe_p.append(0.1 * prob)
                            else:
                                pe_t.append(end_time)
                                pe_p.append(0.1 * batch_and_schedule[3])
                            pe_t.append(end_time)
                            pe_p.append(0)
                            random.seed(task)
                            r = random.randrange(0, 255)
                            g = random.randrange(0, 255)
                            b = random.randrange(0, 255)
                            edge_color = '#%02X%02X%02X' % (r, g, b)
                            # edge_color = '#CFECFF'
                            # print TryOutList
                            schedule_list.append((start_time, end_time, batch_and_schedule[3]))
                            zorder -= 1

                pe_t.append(max_time)
                pe_p.append(0)
                pe_t.append(max_time)
                pe_p.append(0.1)
                pe_t.append(max_time)
                pe_p.append(0)
                if tg.node[task[0]]['task'].type == 'Test' or tg.node[task[1]]['task'].type == 'Test':
                    ax1.fill_between(pe_t, pe_p, 0, color=edge_color, edgecolor='k', zorder=zorder, hatch='\\')
                else:
                    ax1.fill_between(pe_t, pe_p, 0, color=edge_color, edgecolor=edge_color, zorder=zorder)
                if Config.Communication_SlackCount > 0:
                    ax1.fill_between(slack_t, slack_p, 0, color='#808080', edgecolor='#808080')

            plt.setp(ax1.get_yticklabels(), visible=False)
            if count < link_counter+node_counter+router_counter:
                plt.setp(ax1.get_xticklabels(), visible=False)

            ax1.yaxis.set_label_coords(-0.08, 0)
            ax1.set_ylabel(r'R'+str(node), size=14, rotation=0)
            # removes the extra white space at the end of the graph
            ax1.set_xlim(0, max_time+1)
            count += 1
    return count, ax1


def add_links_to_drawing(tg, ag, num_of_plots, fig, node_counter, link_counter, router_counter, max_time, count):
    ax1 = None
    for Link in ag.edges():
        if len(ag.edge[Link[0]][Link[1]]['MappedTasks']) > 0:
            ax1 = fig.add_subplot(num_of_plots, 1, count)
            schedule_list = []
            zorder = len(ag.edge[Link[0]][Link[1]]['MappedTasks'])
            for task in ag.edge[Link[0]][Link[1]]['MappedTasks']:
                pe_t = [0, 0]
                pe_p = [0.1, 0]
                edge_color = 'w'
                slack_t = [0]
                slack_p = [0]

                if task in ag.edge[Link[0]][Link[1]]['Scheduling']:
                    if tg.edge[task[0]][task[1]]['Criticality'] == 'H':
                        start_time = 0
                        end_time = 0
                        for batch_and_schedule in ag.edge[Link[0]][Link[1]]['Scheduling'][task]:
                            start_time = batch_and_schedule[0]
                            task_length = batch_and_schedule[1] - start_time
                            end_time = start_time + (task_length / (Config.Communication_SlackCount+1))
                            pe_t.append(start_time)
                            pe_p.append(0)
                            pe_t.append(start_time)
                            pe_p.append(0.1)
                            pe_t.append(end_time)
                            pe_p.append(0.1)
                            pe_t.append(end_time)
                            pe_p.append(0)
                            edge_color = '#FF878B'
                            if Config.Communication_SlackCount > 0:
                                start_time = end_time
                                end_time = start_time + (task_length / (Config.Communication_SlackCount+1)) * Config.Communication_SlackCount
                                slack_t.append(start_time)
                                slack_p.append(0)
                                slack_t.append(start_time)
                                slack_p.append(0.1)
                                slack_t.append(end_time)
                                slack_p.append(0.1)
                                slack_t.append(end_time)
                                slack_p.append(0)
                        schedule_list.append((start_time, end_time, 1))
                        zorder -= 1
                    else:
                        for batch_and_schedule in ag.edge[Link[0]][Link[1]]['Scheduling'][task]:

                            start_time = batch_and_schedule[0]
                            end_time = batch_and_schedule[1]
                            prob = batch_and_schedule[3]

                            pe_t.append(start_time)
                            pe_p.append(0)
                            pe_t.append(start_time)
                            pe_p.append(0.1 * prob)

                            past_prob = 0
                            for added_rect in schedule_list:
                                if added_rect[0] <= start_time < added_rect[1]:
                                    past_prob += added_rect[2]

                            if past_prob > 0:
                                pe_t.append(start_time)
                                prob = batch_and_schedule[3]+past_prob
                                pe_p.append(0.1 * prob)

                            up_dict = {}
                            for added_rect in schedule_list:
                                if start_time < added_rect[0] < end_time:
                                    if added_rect[0] in up_dict:
                                        up_dict[added_rect[0]] += added_rect[2]
                                    else:
                                        up_dict[added_rect[0]] = added_rect[2]

                            down_dict = {}
                            for added_rect in schedule_list:
                                if start_time < added_rect[1] < end_time:
                                    if added_rect[1] in down_dict:
                                        down_dict[added_rect[1]] += added_rect[2]
                                    else:
                                        down_dict[added_rect[1]] = added_rect[2]

                            for time_instant in sorted(up_dict.keys()+down_dict.keys()):
                                if time_instant in up_dict.keys():
                                    pe_t.append(time_instant)
                                    pe_p.append(0.1 * prob)
                                    prob = up_dict[time_instant] + prob
                                    pe_t.append(time_instant)
                                    pe_p.append(0.1 * prob)

                                if time_instant in down_dict.keys():
                                    pe_t.append(time_instant)
                                    pe_p.append(0.1 * prob)
                                    prob = prob - down_dict[time_instant]
                                    pe_t.append(time_instant)
                                    pe_p.append(0.1 * prob)

                            past_prob = 0
                            for added_rect in schedule_list:
                                if added_rect[0] < end_time <= added_rect[1]:
                                        past_prob += added_rect[2]

                            if past_prob > 0:
                                pe_t.append(end_time)
                                prob = batch_and_schedule[3]+past_prob
                                pe_p.append(0.1 * prob)
                            else:
                                pe_t.append(end_time)
                                pe_p.append(0.1 * batch_and_schedule[3])
                            pe_t.append(end_time)
                            pe_p.append(0)
                            random.seed(task)
                            r = random.randrange(0, 255)
                            g = random.randrange(0, 255)
                            b = random.randrange(0, 255)
                            edge_color = '#%02X%02X%02X' % (r, g, b)
                            # edge_color = '#CFECFF'
                            # print TryOutList
                            schedule_list.append((start_time, end_time, batch_and_schedule[3]))
                            zorder -= 1

                pe_t.append(max_time)
                pe_p.append(0)
                pe_t.append(max_time)
                pe_p.append(0.1)
                pe_t.append(max_time)
                pe_p.append(0)
                if tg.node[task[0]]['task'].type == 'Test' or tg.node[task[1]]['task'].type == 'Test':
                    ax1.fill_between(pe_t, pe_p, 0, color=edge_color, edgecolor='k', zorder=zorder, hatch='\\')
                else:
                    ax1.fill_between(pe_t, pe_p, 0, color=edge_color, edgecolor=edge_color, zorder=zorder)
                if Config.Communication_SlackCount > 0:
                    ax1.fill_between(slack_t, slack_p, 0, color='#808080', edgecolor='#808080')

            plt.setp(ax1.get_yticklabels(), visible=False)
            if count < link_counter + node_counter + router_counter:
                plt.setp(ax1.get_xticklabels(), visible=False)

            ax1.yaxis.set_label_coords(-0.08, 0)
            ax1.set_ylabel(r'L'+str(Link), size=14, rotation=0)
            # removes the extra white space at the end of the graph
            ax1.set_xlim(0, max_time+1)
            count += 1
    return count, ax1
