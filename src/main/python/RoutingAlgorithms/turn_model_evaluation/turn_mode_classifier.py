# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import PackageFile
import ast


def classify_3d_turn_models():
    data_file = open('ConfigAndPackages/turn_models_3D/Minimal/all_3D_18t_turn_models.txt', 'r')
    line = data_file.readline()
    print "\t\t Restricted Turns\t\t|\t  Classes \t\tNumber of Digits"
    print "\tXY\t\tXZ\t\tYZ\t|\txy  xz  yz \t\t1s  2s  3s"
    print "----------------------------------------------------------------------------------------------"
    while line != "":
        start = line.index("[")
        end = line.index("]")+1
        turn_model = ast.literal_eval(line[start:end])

        xy, xz, yz = extract_restricted_turns_in_planes(turn_model)
        if xy[0][0] == xy[1][0]:
            xy_class = 1
        elif xy[0][2] == xy[1][2]:
            xy_class = 2
        elif xy[0][2] == xy[1][0] and xy[0][0] == xy[1][2]:
            xy_class = 3
        else:
            xy_class = 0

        if xz[0][0] == xz[1][0]:
            xz_class = 1
        elif xz[0][2] == xz[1][2]:
            xz_class = 2
        elif xz[0][2] == xz[1][0] and xz[0][0] == xz[1][2]:
            xz_class = 3
        else:
            xz_class = 0

        if yz[0][0] == yz[1][0]:
            yz_class = 1
        elif yz[0][2] == yz[1][2]:
            yz_class = 2
        elif yz[0][2] == yz[1][0] and yz[0][0] == yz[1][2]:
            yz_class = 3
        else:
            yz_class = 0

        general_class = str(xy_class)+str(xz_class)+str(yz_class)

        number_1 = general_class.count('1')
        number_2 = general_class.count('2')
        number_3 = general_class.count('3')

        print xy, "\t", xz, "\t", yz, "\t|\t", xy_class, " ", xz_class, " ", yz_class, \
            "\t\t", number_1, " ", number_2, " ", number_3
        # print "-------------------------------------------------------------------"
        line = data_file.readline()
    data_file.close()
    return None


def extract_restricted_turns_in_planes(turn_model):
    turn_model_xy = []
    turn_model_yz = []
    turn_model_xz = []
    for turn in turn_model:
        if turn in PackageFile.FULL_TurnModel_2D:
            turn_model_xy.append(turn)
        elif turn in ['E2U', 'W2U', 'E2D', 'W2D', 'U2E', 'U2W', 'D2E', 'D2W']:
            turn_model_xz.append(turn)
        elif turn in ['N2U', 'S2U', 'N2D', 'S2D', 'U2N', 'U2S', 'D2N', 'D2S']:
            turn_model_yz.append(turn)
    xy_restricted = []
    xz_restricted = []
    yz_restricted = []
    for turn in PackageFile.FULL_TurnModel_2D:
        if turn not in turn_model_xy:
            xy_restricted.append(turn)

    for turn in ['E2U', 'W2U', 'E2D', 'W2D', 'U2E', 'U2W', 'D2E', 'D2W']:
        if turn not in turn_model_xz:
            xz_restricted.append(turn)

    for turn in ['N2U', 'S2U', 'N2D', 'S2D', 'U2N', 'U2S', 'D2N', 'D2S']:
        if turn not in turn_model_yz:
            yz_restricted.append(turn)

    return xy_restricted, xz_restricted, yz_restricted
