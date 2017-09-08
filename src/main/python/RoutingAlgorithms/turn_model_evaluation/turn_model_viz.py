# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import all_2d_turn_model_package
import matplotlib.pyplot as plt
from RoutingAlgorithms.Routing_Functions import return_turn_model_name
from  ConfigAndPackages.all_odd_even_turn_model import *
import random
import os
import ast
import operator


def draw_turn_model(turn_model, ax1, x_position):
    if "E2S" in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax1.annotate("",
                 xy=(x_position, 0.2), xycoords='data',
                 xytext=(x_position+0.2, 0.4), textcoords='data',
                 size=20,
                 arrowprops=dict(arrowstyle="->", color=color,
                                 connectionstyle="angle, angleA=0, angleB=90, rad=0")
                 )
    if "S2W" in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax1.annotate("",
                 xy=(x_position+0.2, 0.4), xycoords='data',
                 xytext=(x_position+0.4, 0.2), textcoords='data',
                 size=20,
                 arrowprops=dict(arrowstyle="->", color=color,
                                 connectionstyle="angle, angleA=90, angleB=0, rad=0")
                 )
    if "N2E" in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax1.annotate("",
                 xy=(x_position+0.2, 0), xycoords='data',
                 xytext=(x_position, 0.2), textcoords='data',
                 size=20,
                 arrowprops=dict(arrowstyle="->", color=color,
                                 connectionstyle="angle, angleA=90, angleB=0, rad=0")
                 )
    if "W2N" in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax1.annotate("",
                 xy=(x_position+0.4, 0.2), xycoords='data',
                 xytext=(x_position+0.2, 0.0), textcoords='data',
                 size=20,
                 arrowprops=dict(arrowstyle="->", color=color,
                                 connectionstyle="angle, angleA=0, angleB=90, rad=0")
                 )
    # #######################
    if "S2E" in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax1.annotate("",
                 xy=(x_position+0.2, 1), xycoords='data',
                 xytext=(x_position+0.0, 0.8), textcoords='data',
                 size=20,
                 arrowprops=dict(arrowstyle="->", color=color,
                                 connectionstyle="angle, angleA=90, angleB=0, rad=0")
                 )
    if "W2S" in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax1.annotate("",
                 xy=(x_position+0.4, 0.8), xycoords='data',
                 xytext=(x_position+0.2, 1), textcoords='data',
                 size=20,
                 arrowprops=dict(arrowstyle="->", color=color,
                                 connectionstyle="angle, angleA=0, angleB=90, rad=0")
                 )
    if "E2N" in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax1.annotate("",
                 xy=(x_position, 0.8), xycoords='data',
                 xytext=(x_position+0.2, 0.6), textcoords='data',
                 size=20,
                 arrowprops=dict(arrowstyle="->", color=color,
                                 connectionstyle="angle, angleA=180, angleB=90, rad=0")
                 )
    if "N2W" in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax1.annotate("",
                 xy=(x_position+0.2, 0.6), xycoords='data',
                 xytext=(x_position+0.4, 0.8), textcoords='data',
                 size=20,
                 arrowprops=dict(arrowstyle="->", color=color,
                                 connectionstyle="angle, angleA=90, angleB=0, rad=0")
                 )
    return None


def viz_2d_odd_even_turn_model():
    """
    Reads all the 2D turn models and draw them in a file at GraphDrawings/Turn_Model.png
    :return: None
    """
    print ("===========================================")
    print ("GENERATING TURN MODEL VISUALIZATIONS...")

    odd_even_directory = "GraphDrawings/odd_even_viz"
    if not os.path.isdir(odd_even_directory):
        os.makedirs(odd_even_directory)

    for turn_model_set in all_odd_even_list:
        fig = plt.figure(figsize=(19, 12))
        ax1 = plt.subplot(7, 8, 0)
        draw_turn_model(turn_model_set[0], ax1, 0)
        draw_turn_model(turn_model_set[1], ax1, 0.6)

        ax1.text(0.1, 1.1, "odd", fontsize=10)
        ax1.text(0.7, 1.1, "even", fontsize=10)
        #ax1.text(0, 0.8, str(turn_model), fontsize=5)
        ax1.axis('off')
        plt.axis('off')
        plt.savefig(odd_even_directory+"/Turn_Model_"+str(all_odd_even_list.index(turn_model_set))+".png", dpi=300, bbox_inches='tight')
        plt.clf()
        plt.close(fig)
    # print ("\033[35m* VIZ::\033[0m Turn Model viz " +
    #       "TURN MODEL VIZ CREATED AT: GraphDrawings/Turn_Model_"+turn_model_name+".png")
    print ("TURN MODEL VISUALIZATIONS READY...")
    return None


def viz_all_turn_models(dimension, routing_type):
    """
    Draws all the turn models in 2D or 3D
    :param dimension: 2D or 3D
    :return: None
    """
    if dimension == '2D':
        if routing_type in ["M", "NM"]:
            viz_2d_turn_model(all_2d_turn_model_package.all_2d_turn_models)
        else:
            print "ARGUMENT ERROR:: Routing type should be either M or NM..."

    if dimension == '3D':
        if routing_type == "NM":
            viz_3d_turn_model("Non_Minimal/all_3D_10t_turn_models", 40, 30, 12, 13)
            viz_3d_turn_model("Non_Minimal/all_3D_11t_turn_models", 40, 30, 14, 13)
            viz_3d_turn_model("Non_Minimal/all_3D_12t_turn_models", 40, 30, 14, 13)
            viz_3d_turn_model("Non_Minimal/all_3D_13t_turn_models", 40, 30, 14, 13)
            viz_3d_turn_model("Non_Minimal/all_3D_14t_turn_models", 40, 30, 14, 13)
            viz_3d_turn_model("Non_Minimal/all_3D_15t_turn_models", 40, 30, 14, 13)
            viz_3d_turn_model("Non_Minimal/all_3D_16t_turn_models", 40, 30, 14, 13)
            viz_3d_turn_model("Non_Minimal/all_3D_17t_turn_models", 50, 45, 14, 13)
            viz_3d_turn_model("Non_Minimal/all_3D_18t_turn_models", 50, 45, 14, 13)
        elif routing_type == "M":
            viz_3d_turn_model("Minimal/all_3D_12t_turn_models", 50, 45, 14, 13)
            viz_3d_turn_model("Minimal/all_3D_13t_turn_models", 50, 45, 14, 13)
            viz_3d_turn_model("Minimal/all_3D_14t_turn_models", 50, 45, 14, 13)
            viz_3d_turn_model("Minimal/all_3D_15t_turn_models", 50, 45, 14, 13)
            viz_3d_turn_model("Minimal/all_3D_16t_turn_models", 50, 45, 14, 13)
            viz_3d_turn_model("Minimal/all_3D_17t_turn_models", 50, 45, 14, 13)
            viz_3d_turn_model("Minimal/all_3D_18t_turn_models", 50, 45, 14, 13)
    return None


def viz_turn_model_evaluation(cost_file_name):
    """
    Visualizes the cost of solutions during local search mapping optimization process
    :param cost_file_name: Name of the Cost File (Holds values of cost function for different mapping steps)
    :return: None
    """
    print ("===========================================")
    print ("GENERATING TURN MODEL EVALUATION VISUALIZATIONS...")
    print 'READING Generated_Files/Internal/'+cost_file_name+'.txt'
    fig, ax1 = plt.subplots()
    try:
        viz_file = open('Generated_Files/Internal/'+cost_file_name+'.txt', 'r')
        con_metric = []
        line = viz_file.readline()
        con_metric.append(float(line))
        while line != "":
            con_metric.append(float(line))
            line = viz_file.readline()
        solution_num = range(0, len(con_metric))
        viz_file.close()

        ax1.set_ylabel('Connectivity Metric')
        ax1.set_xlabel('time')
        ax1.plot(solution_num, con_metric, '#5095FD')

    except IOError:
        print ('CAN NOT OPEN', cost_file_name+'.txt')

    plt.savefig("GraphDrawings/"+str(cost_file_name)+".png", dpi=300)
    print ("\033[35m* VIZ::\033[0m Turn Model Evaluation " +
           "GRAPH CREATED AT: GraphDrawings/"+str(cost_file_name)+".png")
    plt.clf()
    plt.close(fig)
    return None


def viz_all_turn_models_against_each_other():
    """
    Generates visualization of average connectivity metric vs number of links present
    in the network
    :return: None
    """
    print ("===========================================")
    print ("GENERATING TURN MODEL EVALUATION VISUALIZATIONS...")
    fig = plt.figure()

    ax1 = plt.subplot(111)
    turn_model_eval_directory = "Generated_Files/Turn_Model_Eval"
    file_list = [txt_file for txt_file in os.listdir(turn_model_eval_directory) if txt_file.endswith(".txt")]
    sorted(file_list)
    counter = 0
    for txt_file in file_list:
        viz_file = open(turn_model_eval_directory+"/"+txt_file, 'r')
        line = viz_file.readline()
        value_list = []
        while line != "":
            value = line.split()
            value_list.append(float(value[1]))
            line = viz_file.readline()
        index_list = range(0, len(value_list))
        viz_file.close()
        value_list = sorted(value_list)
        random.seed(counter)
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        color = '#%02X%02X%02X' % (r, g, b)
        file_name = txt_file.split("_")
        ax1.plot(index_list, value_list, color, label=str("{0:0=2d}".format(int(file_name[0]))))
        counter += 1

    handles, labels = ax1.get_legend_handles_labels()
    hl = sorted(zip(handles, labels), key=operator.itemgetter(1))
    handles2, labels2 = zip(*hl)

    lgd = ax1.legend(handles2, labels2, loc='center left',  bbox_to_anchor=(1, 0.5), ncol=3)
    ax1.grid('on')
    plt.axvline(24, color='b', linestyle='--')
    plt.xlabel('Number of working links in the network', fontsize=16)
    plt.ylabel('Average connectivity metric', fontsize=16)
    plt.savefig("GraphDrawings/Turn_Models_Fault_Tolerance_Eval.png", bbox_extra_artists=(lgd,),
                bbox_inches='tight', dpi=300)
    plt.clf()
    plt.close(fig)
    print ("\033[35m* VIZ::\033[0m Turn Model Evaluation " +
           "GRAPH CREATED AT: GraphDrawings/Turn_Models_Fault_Tolerance_Eval.png")
    return None


def viz_2d_turn_model(turn_model_list):
    """
    Reads all the 2D turn models and draw them in a file at GraphDrawings/Turn_Model.png
    :return: None
    """
    print ("===========================================")
    print ("GENERATING TURN MODEL VISUALIZATIONS...")
    fig = plt.figure(figsize=(19, 12))
    count = 1
    for turn_model in turn_model_list:
        ax1 = plt.subplot(7, 8, count)
        if "E2S" in turn_model:
            color = 'black'
        else:
            color = 'red'
        ax1.annotate("",
                     xy=(0, 0.5), xycoords='data',
                     xytext=(0.2, 0.7), textcoords='data',
                     size=20,
                     arrowprops=dict(arrowstyle="->", color=color,
                                     connectionstyle="angle, angleA=0, angleB=90, rad=0")
                     )
        if "S2W" in turn_model:
            color = 'black'
        else:
            color = 'red'
        ax1.annotate("",
                     xy=(0.2, 0.7), xycoords='data',
                     xytext=(0.4, 0.5), textcoords='data',
                     size=20,
                     arrowprops=dict(arrowstyle="->", color=color,
                                     connectionstyle="angle, angleA=90, angleB=0, rad=0")
                     )
        if "N2E" in turn_model:
            color = 'black'
        else:
            color = 'red'
        ax1.annotate("",
                     xy=(0.2, 0.3), xycoords='data',
                     xytext=(0.0, 0.5), textcoords='data',
                     size=20,
                     arrowprops=dict(arrowstyle="->", color=color,
                                     connectionstyle="angle, angleA=90, angleB=0, rad=0")
                     )
        if "W2N" in turn_model:
            color = 'black'
        else:
            color = 'red'
        ax1.annotate("",
                     xy=(0.4, 0.5), xycoords='data',
                     xytext=(0.2, 0.3), textcoords='data',
                     size=20,
                     arrowprops=dict(arrowstyle="->", color=color,
                                     connectionstyle="angle, angleA=0, angleB=90, rad=0")
                     )
        # #######################
        if "S2E" in turn_model:
            color = 'black'
        else:
            color = 'red'
        ax1.annotate("",
                     xy=(0.75, 0.7), xycoords='data',
                     xytext=(0.55, 0.5), textcoords='data',
                     size=20,
                     arrowprops=dict(arrowstyle="->", color=color,
                                     connectionstyle="angle, angleA=90, angleB=0, rad=0")
                     )
        if "W2S" in turn_model:
            color = 'black'
        else:
            color = 'red'
        ax1.annotate("",
                     xy=(0.95, 0.5), xycoords='data',
                     xytext=(0.75, 0.7), textcoords='data',
                     size=20,
                     arrowprops=dict(arrowstyle="->", color=color,
                                     connectionstyle="angle, angleA=0, angleB=90, rad=0")
                     )
        if "E2N" in turn_model:
            color = 'black'
        else:
            color = 'red'
        ax1.annotate("",
                     xy=(0.55, 0.5), xycoords='data',
                     xytext=(0.75, 0.3), textcoords='data',
                     size=20,
                     arrowprops=dict(arrowstyle="->", color=color,
                                     connectionstyle="angle, angleA=180, angleB=90, rad=0")
                     )
        if "N2W" in turn_model:
            color = 'black'
        else:
            color = 'red'
        ax1.annotate("",
                     xy=(0.75, 0.3), xycoords='data',
                     xytext=(0.95, 0.5), textcoords='data',
                     size=20,
                     arrowprops=dict(arrowstyle="->", color=color,
                                     connectionstyle="angle, angleA=90, angleB=0, rad=0")
                     )

        ax1.text(0, 0.9, str(return_turn_model_name(turn_model)), fontsize=10)
        ax1.text(0, 0.8, str(turn_model), fontsize=5)
        count += 1
        ax1.axis('off')
    plt.axis('off')
    plt.savefig("GraphDrawings/Turn_Model.png", dpi=300, bbox_inches='tight')
    plt.clf()
    plt.close(fig)
    # print ("\033[35m* VIZ::\033[0m Turn Model viz " +
    #       "TURN MODEL VIZ CREATED AT: GraphDrawings/Turn_Model_"+turn_model_name+".png")
    print ("TURN MODEL VISUALIZATIONS READY...")
    return None


def viz_3d_turn_model(file_name, size_x, size_y, rows, columns):
    """
    Draws all the turn models in the file "file_name" in a canvas of size_x*size_y and
    in "rows" rows and "columns" columns.
    :param file_name: source file of the turn models
    :param size_x: width of the picture
    :param size_y: height of the picture
    :param rows: number of rows of turn models per canvas
    :param columns: number of columns of turn models per canvas
    :return: None
    """
    print ("===========================================")
    print ("GENERATING TURN MODEL VISUALIZATIONS...")
    fig = plt.figure(figsize=(size_x, size_y))
    page_counter = 0
    count = 1
    turn_model_counter = 0
    data_file = open('ConfigAndPackages/turn_models_3D/'+file_name+'.txt', 'r')
    line = data_file.readline()
    while line != "":
        start = line.index("[")
        end = line.index("]")+1
        turn_model = ast.literal_eval(line[start:end])
        ax1 = plt.subplot(rows, columns, count)

        turn_set = ["E2S", "S2W", "N2E", "W2N"]
        draw_turn_model_counter_clockwise(ax1, turn_model, turn_set, 0.1, 0.1, "60", "0")
        turn_set = ["E2D", "D2W", "U2E", "W2U"]
        draw_turn_model_counter_clockwise(ax1, turn_model, turn_set, 0.15, 0.35, "90", "0")
        draw_turn_model_counter_clockwise_yz(ax1, turn_model, 0, 0.22)

        turn_set = ["S2E", "W2S", "E2N", "N2W"]
        draw_turn_model_clockwise(ax1, turn_model, turn_set, 0.55, 0.1, "60", "0")
        turn_set = ["D2E", "W2D", "E2U", "U2W"]
        draw_turn_model_clockwise(ax1, turn_model, turn_set,  0.6, 0.35, "90", "0")
        draw_turn_model_clockwise_yz(ax1, turn_model, 0.45, 0.22)

        ax1.text(0, 0.62, str(turn_model_counter), fontsize=10)
        count += 1
        turn_model_counter += 1
        ax1.axis('off')
        if count == rows*columns+1:
            plt.axis('off')
            plt.savefig("GraphDrawings/"+file_name[file_name.find("/"):]+str(page_counter)+".png",
                        dpi=100, bbox_inches='tight')
            plt.clf()
            plt.close(fig)
            page_counter += 1
            count = 1
            del fig
            del ax1
            print ("GENERATING TURN MODEL VISUALIZATIONS... Page:"+str(page_counter))
            fig = plt.figure(figsize=(size_x, size_y))
        line = data_file.readline()
    if page_counter == 0:
        plt.axis('off')
        plt.savefig("GraphDrawings/"+file_name[file_name.find("/"):]+".png", dpi=100, bbox_inches='tight')
        plt.clf()
        plt.close(fig)
    else:
        plt.axis('off')
        plt.savefig("GraphDrawings/"+file_name[file_name.find("/"):]+str(page_counter)+".png",
                    dpi=100, bbox_inches='tight')
        plt.clf()
        plt.close(fig)
    # print ("\033[35m* VIZ::\033[0m Turn Model viz " +
    #       "TURN MODEL VIZ CREATED AT: GraphDrawings/Turn_Model_"+turn_model_name+".png")
    print ("TURN MODEL VISUALIZATIONS READY...")
    return None


def draw_turn_model_counter_clockwise(ax, turn_model, turn_set, ofset_x, ofset_y, angle1, angle2):
    height = 0.1
    width = 0.1
    size = 5

    if turn_set[0] in turn_model:
        color = 'black'
    else:
        color = 'red'

    ax.annotate("",
                xy=(ofset_x, ofset_y+height), xycoords='data',
                xytext=(ofset_x+width, ofset_y+height*2), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle2+", angleB="+angle1+", rad=0")
                )

    if turn_set[1] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width, ofset_y+height*2), xycoords='data',
                xytext=(ofset_x+width*2, ofset_y+height), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle1+", angleB="+angle2+", rad=0")
                )
    if turn_set[2] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width, ofset_y), xycoords='data',
                xytext=(ofset_x, ofset_y+height), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle1+", angleB="+angle2+", rad=0")
                )
    if turn_set[3] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width*2, ofset_y+height), xycoords='data',
                xytext=(ofset_x+width, ofset_y), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle2+", angleB="+angle1+", rad=0")
                )


def draw_turn_model_counter_clockwise_yz(ax, turn_model, ofset_x, ofset_y):
    height = 0.1
    width = 0.05
    size = 5
    angle = "60"
    turn_set = ["N2D", "D2S", "U2N", "S2U"]
    if turn_set[0] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x, ofset_y), xycoords='data',
                xytext=(ofset_x+width, ofset_y+height*2), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle+", angleB=90, rad=0")
                )
    if turn_set[1] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width, ofset_y+height*2), xycoords='data',
                xytext=(ofset_x+width*2, ofset_y+height*2.5), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA=90, angleB="+angle+", rad=0")
                )
    if turn_set[2] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width, ofset_y), xycoords='data',
                xytext=(ofset_x, ofset_y), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA=90, angleB="+angle+", rad=0")
                )
    if turn_set[3] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width*2, ofset_y+height*2.5), xycoords='data',
                xytext=(ofset_x+width, ofset_y), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle+", angleB=90, rad=0")
                )


def draw_turn_model_clockwise(ax, turn_model, turn_set, ofset_x, ofset_y, angle1, angle2):
    height = 0.1
    width = 0.1
    size = 5
    if turn_set[0] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width, ofset_y+height*2), xycoords='data',
                xytext=(ofset_x, ofset_y+height), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle1+", angleB="+angle2+", rad=0")
                )
    if turn_set[1] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width*2, ofset_y+height), xycoords='data',
                xytext=(ofset_x+width, ofset_y+height*2), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle2+", angleB="+angle1+", rad=0")
                )
    if turn_set[2] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x, ofset_y+height), xycoords='data',
                xytext=(ofset_x+width, ofset_y), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA=180, angleB="+angle1+", rad=0")
                )
    if turn_set[3] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width, ofset_y), xycoords='data',
                xytext=(ofset_x+width*2, ofset_y+height), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle1+", angleB="+angle2+", rad=0")
                )
    return None


def draw_turn_model_clockwise_yz(ax, turn_model, ofset_x, ofset_y):
    height = 0.1
    width = 0.05
    size = 5
    turn_set = ["D2N", "S2D", "N2U", "U2S"]
    angle1 = "90"
    angle2 = "60"
    if turn_set[0] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width, ofset_y+height*2), xycoords='data',
                xytext=(ofset_x, ofset_y), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle1+", angleB="+angle2+", rad=0")
                )
    if turn_set[1] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width*2, ofset_y+height*2), xycoords='data',
                xytext=(ofset_x+width, ofset_y+height*2), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle2+", angleB="+angle1+", rad=0")
                )
    if turn_set[2] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x, ofset_y), xycoords='data',
                xytext=(ofset_x+width, ofset_y), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA=1500, angleB="+angle1+", rad=0")
                )
    if turn_set[3] in turn_model:
        color = 'black'
    else:
        color = 'red'
    ax.annotate("",
                xy=(ofset_x+width, ofset_y), xycoords='data',
                xytext=(ofset_x+width*2, ofset_y+height*2), textcoords='data',
                size=size,
                arrowprops=dict(arrowstyle="->", color=color,
                                connectionstyle="angle, angleA="+angle1+", angleB="+angle2+", rad=0")
                )
    return None
