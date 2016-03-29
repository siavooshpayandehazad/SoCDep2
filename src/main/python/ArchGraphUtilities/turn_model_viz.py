# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import all_2d_turn_model_package
import matplotlib.pyplot as plt
from RoutingAlgorithms import Routing


def viz_2d_turn_model():
    print ("===========================================")
    print ("GENERATING TURN MODEL VISUALIZATIONS...")
    fig = plt.figure(figsize=(19, 12))
    count = 1
    for turn_model in all_2d_turn_model_package.all_2d_turn_models:
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

        ax1.text(0, 0.8, str(Routing.return_turn_model_name(turn_model))+": "+str(turn_model), fontsize=5)
        count += 1
        ax1.axis('off')
    plt.axis('off')
    plt.savefig("GraphDrawings/Turn_Model.png", dpi=300, bbox_inches='tight')
    plt.clf()
    plt.close(fig)
    # print ("\033[35m* VIZ::\033[0m Turn Model viz " +
    #       "TURN MODEL VIZ CREATED AT: GraphDrawings/Turn_Model_"+turn_model_name+".png")
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