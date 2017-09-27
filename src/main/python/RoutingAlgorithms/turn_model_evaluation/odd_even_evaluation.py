from ConfigAndPackages.all_odd_even_turn_model import all_odd_even_list
from networkx import all_shortest_paths, all_simple_paths
import difflib
from ConfigAndPackages import Config
import copy
import sys
from ArchGraphUtilities import AG_Functions
from RoutingAlgorithms import Routing
from SystemHealthMonitoring import SystemHealthMonitoringUnit
from RoutingAlgorithms.Routing_Functions import extended_degree_of_adaptiveness, degree_of_adaptiveness, \
    check_deadlock_freeness
from RoutingAlgorithms.Calculate_Reachability import reachability_metric, is_destination_reachable_from_source
from ArchGraphUtilities.AG_Functions import manhattan_distance
import itertools
from random import shuffle, sample

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
    #selected_turn_models = [677, 798]
    if routing_type == "minimal":
        Config.RotingType = 'MinimalPath'
    else:
        Config.RotingType = 'NonMinimalPath'

    for turn_id in selected_turn_models:
        counter = 0
        metric_sum = 0
        turn_model = all_odd_even_list[turn_id]

        ag = copy.deepcopy(AG_Functions.generate_ag(report=False))
        turn_model_odd = turn_model[0]
        turn_model_even = turn_model[1]

        file_name = str(tm_counter)+'_eval'
        turn_model_eval_file = open('Generated_Files/Turn_Model_Eval/'+file_name+'.txt', 'a+')
        if viz:
            file_name_viz = str(tm_counter)+'_eval_'+str(len(ag.edges())-counter)
            turn_model_eval_viz_file = open('Generated_Files/Internal/odd_even'+file_name_viz+'.txt', 'w')
        else:
            turn_model_eval_viz_file = None

        sub_ag_list = list(itertools.combinations(ag.edges(), combination))
        turns_health = copy.deepcopy(turns_health_2d_network)
        shmu = SystemHealthMonitoringUnit.SystemHealthMonitoringUnit()
        shmu.setup_noc_shm(ag, turns_health, False)

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
            del noc_rg

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
    number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)

    max_ratio = 0
    classes_of_doa_ratio = []
    turn_model_class_dict = {}
    for turn_model in all_odd_even_list:
    #for item in selected_turn_models:
        #print item
        #turn_model = all_odd_even_list[item]
        #print turn_model
        turn_model_index = all_odd_even_list.index(turn_model)
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
        #draw_rg(noc_rg)
        number_of_pairs = len(ag.nodes())*(len(ag.nodes())-1)
        doa_ex = extended_degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
        doa = degree_of_adaptiveness(ag, noc_rg, False)/float(number_of_pairs)
        sum_of_paths = 0
        sum_of_sim_ratio = 0

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
                                else:
                                    paths = list(all_simple_paths(noc_rg, str(source_node)+str('L')+str('I'), str(destination_node)+str('L')+str('O')))
                                #for path in paths:
                                #    print path
                                local_sim_ratio = 0
                                counter = 0
                                if len(paths) > 1:
                                    for i in range(0, len(paths)):
                                        for j in range(i, len(paths)):
                                            if paths[i] != paths[j]:
                                                sm=difflib.SequenceMatcher(None,paths[i],paths[j])
                                                counter += 1
                                                local_sim_ratio +=  sm.ratio()
                                    #print float(local_sim_ratio)/counter
                                    sum_of_sim_ratio += float(local_sim_ratio)/counter
                                else:

                                    sum_of_sim_ratio += 1
        if  Config.RotingType == 'MinimalPath':
            print "Turn Model ", '%5s' %turn_model_index, "\tdoa:", "{:3.3f}".format(doa), "\tsimilarity ratio:", "{:3.3f}".format(sum_of_sim_ratio), "\t\tfault tolerance metric:","{:3.5f}".format(float(doa)/sum_of_sim_ratio)
            doa_ratio = float("{:3.5f}".format(float(doa)/sum_of_sim_ratio, 5))
        else:
            print "Turn Model ", '%5s' %turn_model_index, "\tdoa:", "{:3.3f}".format(doa_ex), "\tsimilarity ratio:", "{:3.3f}".format(sum_of_sim_ratio), "\t\tfault tolerance metric:","{:3.5f}".format(float(doa_ex)/sum_of_sim_ratio)
            doa_ratio = float("{:3.5f}".format(float(doa_ex)/sum_of_sim_ratio, 5))

        if doa_ratio not in classes_of_doa_ratio:
            classes_of_doa_ratio.append(doa_ratio)
        if doa_ratio in turn_model_class_dict.keys():
            turn_model_class_dict[doa_ratio].append(turn_model_index)
        else:
            turn_model_class_dict[doa_ratio]=[turn_model_index]
        if max_ratio < doa_ratio:
            max_ratio = doa_ratio

        #print "--------------------------------------------"
        del noc_rg
    print "max doa_ratio", max_ratio
    print "classes of doa_ratio", classes_of_doa_ratio
    for item in sorted(turn_model_class_dict.keys()):
        print item, turn_model_class_dict[item]
    return None
