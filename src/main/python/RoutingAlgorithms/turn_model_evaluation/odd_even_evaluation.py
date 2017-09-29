from ConfigAndPackages.all_odd_even_turn_model import all_odd_even_list
from networkx import all_shortest_paths, all_simple_paths
import difflib
import statistics
from ConfigAndPackages import Config
import copy
import sys
from ArchGraphUtilities import AG_Functions
from RoutingAlgorithms import Routing
from RoutingAlgorithms.RoutingGraph_Reports import draw_rg
from RoutingAlgorithms.turn_model_evaluation.list_all_turn_models import check_tm_domination
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from RoutingAlgorithms.Routing_Functions import extended_degree_of_adaptiveness, degree_of_adaptiveness, \
    check_deadlock_freeness
from RoutingAlgorithms.Calculate_Reachability import reachability_metric, is_destination_reachable_from_source
from ArchGraphUtilities.AG_Functions import manhattan_distance
import itertools
from random import shuffle, sample
import re

def evaluate_actual_odd_even_turn_model():
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    Config.RotingType = 'MinimalPath'
    ag = copy.deepcopy(AG_Functions.generate_ag())
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

    turn_model_odd =  ['E2N', 'E2S', 'W2N', 'W2S', 'S2E', 'N2E']
    turn_model_even = ['E2N', 'E2S', 'S2W', 'S2E', 'N2W', 'N2E']

    if not check_tm_domination(turn_model_odd, turn_model_even):   # taking out the domination!
        turns_health = copy.deepcopy(turns_health_2d_network)
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))

        for node in ag.nodes():
            node_x, node_y, node_z = AG_Functions.return_node_location(node)
            if node_x % 2 == 1:
                for turn in turn_model_odd:
                    shmu.restore_broken_turn(node, turn, False)
                    from_port = str(node)+str(turn[0])+"I"
                    to_port = str(node)+str(turn[2])+"O"
                    Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
            else:
                for turn in turn_model_even:
                    shmu.restore_broken_turn(node, turn, False)
                    from_port = str(node)+str(turn[0])+"I"
                    to_port = str(node)+str(turn[2])+"O"
                    Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
        draw_rg(noc_rg)
        connectivity_metric = reachability_metric(ag, noc_rg, False)
        print "connectivity_metric:", connectivity_metric
        if check_deadlock_freeness(noc_rg):
            print "Deadlock free!"

        doa = degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
        doa_ex = extended_degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
        print "doa:", doa
        print "doa_ex", doa_ex

        sys.stdout.flush()

def enumerate_all_odd_even_turn_models():
    all_odd_evens_file = open('Generated_Files/Turn_Model_Lists/odd_even_tm_list_dl_free.txt', 'w')
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 6
    Config.ag.y_size = 6
    Config.ag.z_size = 1
    Config.RotingType = 'MinimalPath'
    ag = copy.deepcopy(AG_Functions.generate_ag())
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

    turn_model_list = []
    for length in range(0, len(turns_health_2d_network.keys())+1):
        for item in list(itertools.combinations(turns_health_2d_network.keys(), length)):
            if len(item) > 0:
                turn_model_list.append(list(item))

    connected_counter = 0
    deadlock_free_counter = 0
    tm_counter = 0
    for turn_model_odd in turn_model_list:
        for turn_model_even in turn_model_list:
            if not check_tm_domination(turn_model_odd, turn_model_even):   # taking out the domination!
                turns_health = copy.deepcopy(turns_health_2d_network)
                shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
                shmu.setup_noc_shm(ag, turns_health, False)
                noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))

                for node in ag.nodes():
                    node_x, node_y, node_z = AG_Functions.return_node_location(node)
                    if node_x % 2 == 1:
                        for turn in turn_model_odd:
                            shmu.restore_broken_turn(node, turn, False)
                            from_port = str(node)+str(turn[0])+"I"
                            to_port = str(node)+str(turn[2])+"O"
                            Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                    else:
                        for turn in turn_model_even:
                            shmu.restore_broken_turn(node, turn, False)
                            from_port = str(node)+str(turn[0])+"I"
                            to_port = str(node)+str(turn[2])+"O"
                            Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                connectivity_metric = reachability_metric(ag, noc_rg, False)
                if connectivity_metric == number_of_pairs:
                    connected_counter += 1
                    if check_deadlock_freeness(noc_rg):
                        deadlock_free_counter += 1
                        all_odd_evens_file.write("["+str(turn_model_odd)+","+str(turn_model_even)+"],\n")

                tm_counter += 1
                sys.stdout.write("\rchecked TM: %i " % tm_counter +
                                 " number of fully connected TM: %i" % connected_counter +
                                 " number of deadlock free connected TM: %i" % deadlock_free_counter)
                sys.stdout.flush()
    all_odd_evens_file.close()
    return None


def evaluate_doa_for_all_odd_even_turn_model_list():
    all_odd_evens_file = open('Generated_Files/Turn_Model_Lists/all_odd_evens_doa.txt', 'w')
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    Config.RotingType = 'MinimalPath'
    ag = copy.deepcopy(AG_Functions.generate_ag())
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

    turn_model_list = []
    for length in range(0, len(turns_health_2d_network.keys())+1):
        for item in list(itertools.combinations(turns_health_2d_network.keys(), length)):
            if len(item) > 0:
                turn_model_list.append(list(item))

    classes_of_doa = {}
    classes_of_doax = {}
    tm_counter = 0

    all_odd_evens_file.write("    #  |                  "+'%51s' % " "+" \t|")
    all_odd_evens_file.write(" DoA    |   DoAx | \tC-metric\n")
    all_odd_evens_file.write("-------|--------------------------------------------" +
                             "----------------------------|--------|--------|-------------"+"\n")
    for turn_model in all_odd_even_list:
        turn_model_odd = turn_model[0]
        turn_model_even = turn_model[1]

        turns_health = copy.deepcopy(turns_health_2d_network)
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)
        noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))

        for node in ag.nodes():
            node_x, node_y, node_z = AG_Functions.return_node_location(node)
            if node_x % 2 == 1:
                for turn in turn_model_odd:
                    shmu.restore_broken_turn(node, turn, False)
                    from_port = str(node)+str(turn[0])+"I"
                    to_port = str(node)+str(turn[2])+"O"
                    Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
            else:
                for turn in turn_model_even:
                    shmu.restore_broken_turn(node, turn, False)
                    from_port = str(node)+str(turn[0])+"I"
                    to_port = str(node)+str(turn[2])+"O"
                    Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
        doa = degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
        doa_ex = extended_degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)

        if round(doa, 2) not in classes_of_doa.keys():
            classes_of_doa[round(doa, 2)] = [tm_counter]
        else:
            classes_of_doa[round(doa, 2)].append(tm_counter)

        if round(doa_ex, 2) not in classes_of_doax.keys():
            classes_of_doax[round(doa_ex, 2)] = [tm_counter]
        else:
            classes_of_doax[round(doa_ex, 2)].append(tm_counter)

        all_odd_evens_file.write('%5s' % str(tm_counter)+"  | even turn model:"+'%53s' % str(turn_model_even)+"\t|")
        all_odd_evens_file.write("        |        |\n")
        all_odd_evens_file.write("       | odd turn model: "+'%53s' % str(turn_model_odd)+" \t|")

        all_odd_evens_file.write('%8s' % str(round(doa, 2)) + "|" + '%8s' % str(round(doa_ex, 2)) +
                                 "|\n")     # +'%8s' % str(round(connectivity_metric,2))+"\n")
        all_odd_evens_file.write("-------|--------------------------------------------" +
                                 "----------------------------|--------|--------|-------------"+"\n")
        tm_counter += 1
        sys.stdout.write("\rchecked TM: %i " % tm_counter)
        sys.stdout.flush()
    print
    print "----------------------------------------"
    print "classes of DOA:", sorted(classes_of_doa.keys())
    for item in sorted(classes_of_doa.keys()):
        print item,  sorted(classes_of_doa[item])
        # print
    print "------------------------------"
    print "classes of DOA_ex:", sorted(classes_of_doax.keys())
    for item in sorted(classes_of_doax.keys()):
        print item,  sorted(classes_of_doax[item])

    all_odd_evens_file.close()
    return None


def report_odd_even_turn_model_fault_tolerance(viz, routing_type, combination):
    """
    generates 2D architecture graph with all combinations C(len(ag.nodes), combination)
    of links and writes the average connectivity metric in a file.
    :param viz: if true, generates the visualization files
    :param routing_type: can be "minimal" or "nonminimal"
    :param combination: number of links to be present in the network
    :return: None
    """
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    tm_counter = 0
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1

    selected_turn_models = [677, 678, 697, 699, 717, 718, 737, 739, 757, 759, 778, 779, 797,
                            799, 818, 819, 679, 738, 777, 798]
    selected_turn_models = [578]
    if routing_type == "minimal":
        Config.RotingType = 'MinimalPath'
    else:
        Config.RotingType = 'NonMinimalPath'

    ag = copy.deepcopy(AG_Functions.generate_ag(report=False))
    sub_ag_list = list(itertools.combinations(ag.edges(), combination))
    turns_health = copy.deepcopy(turns_health_2d_network)
    shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
    shmu.setup_noc_shm(ag, turns_health, False)

    for turn_id in selected_turn_models:
        counter = 0
        metric_sum = 0
        turn_model = all_odd_even_list[turn_id]

        turn_model_odd = turn_model[0]
        turn_model_even = turn_model[1]

        file_name = str(tm_counter)+'_eval'
        turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+file_name+'.txt', 'a+')
        if viz:
            file_name_viz = str(tm_counter)+'_eval_'+str(len(ag.edges())-counter)
            turn_model_eval_viz_file = open('Generated_Files/Internal/odd_even'+file_name_viz+'.txt', 'w')
        else:
            turn_model_eval_viz_file = None

        for sub_ag in sub_ag_list:
            for link in list(sub_ag):
                shmu.break_link(link, False)

            noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))
            for node in ag.nodes():
                node_x, node_y, node_z = AG_Functions.return_node_location(node)
                if node_x % 2 == 1:
                    for turn in turn_model_odd:
                        shmu.restore_broken_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                else:
                    for turn in turn_model_even:
                        shmu.restore_broken_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')

            connectivity_metric = reachability_metric(ag, noc_rg, False)
            counter += 1
            metric_sum += connectivity_metric
            if viz:
                turn_model_eval_viz_file.write(str(float(metric_sum)/counter)+"\n")
            # print "#:"+str(counter)+"\t\tC.M.:"+str(connectivity_metric)+"\t\t avg:", \
            #     float(metric_sum)/counter, "\t\tstd:", std
            for link in list(sub_ag):
                shmu.restore_broken_link(link, False)
            for node in ag.nodes():
                node_x, node_y, node_z = AG_Functions.return_node_location(node)
                if node_x % 2 == 1:
                    for turn in turn_model_odd:
                        shmu.break_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'REMOVE')
                else:
                    for turn in turn_model_even:
                        shmu.break_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'REMOVE')

        shuffle(sub_ag_list)

        if counter > 0:
            avg_connectivity = float(metric_sum)/counter
        else:
            avg_connectivity = 0
        turn_model_eval_file.write(str(len(ag.edges())-combination)+"\t\t"+str(avg_connectivity)+"\n")
        if viz:
            turn_model_eval_viz_file.close()
        turn_model_eval_file.close()
        sys.stdout.write("\rchecked TM: %i " % tm_counter+"\t\t\tnumber of healthy links: %i " % combination)
        sys.stdout.flush()
        tm_counter += 1
    return None


def return_links_in_path(path):
    links = []
    for i in range(0, len(path)-1):
        start = int(re.findall('\d+',  path[i])[0])
        end = int(re.findall('\d+',  path[i+1])[0])
        if start != end:
            links.append(str(start)+"_"+str(end))
    return links


def find_similarity_in_paths(link_dict,paths):
    link_dictionary = {}
    for i in range(0, len(paths)):
        for link in return_links_in_path(paths[i]):
            if link in link_dictionary.keys():
                link_dictionary[link] +=1
            else:
                link_dictionary[link] = 1

    for link in sorted(link_dictionary.keys()):
        if link_dictionary[link] >1:
            if link_dictionary[link] == float(len(paths)):
                if link in link_dict.keys():
                    #link_dict[link] += link_dictionary[link]/float(len(paths))
                    link_dict[link] += 1.0
                else:
                    #link_dict[link] = link_dictionary[link]/float(len(paths))
                    link_dict[link] = 1.0
        else:
            if len(paths)==1:
                if link in link_dict.keys():
                    link_dict[link] += 1.0
                else:
                    link_dict[link] = 1.0
            else:
                pass

    return link_dict


def test():
    all_odd_evens_file = open('Generated_Files/Turn_Model_Lists/all_odd_evens_doa.txt', 'w')
    turns_health_2d_network = {"N2W": False, "N2E": False, "S2W": False, "S2E": False,
                               "W2N": False, "W2S": False, "E2N": False, "E2S": False}
    Config.ag.topology = '2DMesh'
    Config.ag.x_size = 3
    Config.ag.y_size = 3
    Config.ag.z_size = 1
    Config.RotingType = 'NonMinimalPath'
    ag = copy.deepcopy(AG_Functions.generate_ag())
    shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
    turns_health = copy.deepcopy(turns_health_2d_network)
    shmu.setup_noc_shm(ag, turns_health, False)
    noc_rg = copy.deepcopy(Routing.generate_noc_route_graph(ag, shmu, [], False,  False))



    classes_of_doa_ratio = []
    turn_model_class_dict = {}
    selected_turn_models =[578, 603, 677, 819, 154, 579,777]
    for turn_model in all_odd_even_list:
    #for item in selected_turn_models:
        #print item
        #turn_model = all_odd_even_list[item]

        link_dict = {}
        turn_model_index = all_odd_even_list.index(turn_model)
        turn_model_odd = turn_model[0]
        turn_model_even = turn_model[1]

        for node in ag.nodes():
                node_x, node_y, node_z = AG_Functions.return_node_location(node)
                if node_x % 2 == 1:
                    for turn in turn_model_odd:
                        shmu.restore_broken_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')
                else:
                    for turn in turn_model_even:
                        shmu.restore_broken_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'ADD')

        number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

        all_paths_in_graph = []
        for source_node in ag.nodes():
                for destination_node in ag.nodes():
                    if source_node != destination_node:
                        if is_destination_reachable_from_source(noc_rg, source_node, destination_node):
                                #print source_node, "--->", destination_node
                                if Config.RotingType == 'MinimalPath':
                                    shortest_paths = list(all_shortest_paths(noc_rg, str(source_node)+str('L')+str('I'), str(destination_node)+str('L')+str('O')))
                                    paths = []
                                    for path in shortest_paths:
                                        minimal_hop_count = manhattan_distance(source_node, destination_node)
                                        if (len(path)/2)-1 <= minimal_hop_count:
                                            paths.append(path)
                                            all_paths_in_graph.append(path)
                                else:
                                    paths = list(all_simple_paths(noc_rg, str(source_node)+str('L')+str('I'), str(destination_node)+str('L')+str('O')))
                                    all_paths_in_graph+=paths
                                link_dict = find_similarity_in_paths(link_dict, paths)

        #for item in link_dict.keys():
        #    print '%7s' %"{:3.3f}".format(link_dict[item]),
        #print
        metric = 0
        for item in link_dict.keys():
            metric += link_dict[item]

        if Config.RotingType == 'MinimalPath':
            doa = degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
            metric = doa/(float(metric)/len(ag.edges()))
            metric = float("{:3.3f}".format(metric))
            print "Turn Model ", '%5s' %turn_model_index, "\tdoa:", "{:3.3f}".format(doa), "\tmetric:", "{:3.3f}".format(metric)
        else:
            doa_ex = extended_degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
            metric = doa_ex/(float(metric)/len(ag.edges()))
            metric = float("{:3.3f}".format(metric))
            print "Turn Model ", '%5s' %turn_model_index, "\tdoa:", "{:3.3f}".format(doa_ex), "\tmetric:", "{:3.3f}".format(metric)

        if metric not in classes_of_doa_ratio:
            classes_of_doa_ratio.append(metric)
        if metric in turn_model_class_dict.keys():
            turn_model_class_dict[metric].append(turn_model_index)
        else:
            turn_model_class_dict[metric]=[turn_model_index]

        for node in ag.nodes():
                node_x, node_y, node_z = AG_Functions.return_node_location(node)
                if node_x % 2 == 1:
                    for turn in turn_model_odd:
                        shmu.break_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'REMOVE')
                else:
                    for turn in turn_model_even:
                        shmu.break_turn(node, turn, False)
                        from_port = str(node)+str(turn[0])+"I"
                        to_port = str(node)+str(turn[2])+"O"
                        Routing.update_noc_route_graph(noc_rg, from_port, to_port, 'REMOVE')

    print "classes of doa_ratio", classes_of_doa_ratio
    for item in sorted(turn_model_class_dict.keys()):
        print item, turn_model_class_dict[item]

    return None
