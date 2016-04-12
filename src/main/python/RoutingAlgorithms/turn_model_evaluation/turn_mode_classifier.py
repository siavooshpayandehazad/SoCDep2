# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import PackageFile
import ast


def classify_3d_turn_models():
    data_file = open('ConfigAndPackages/turn_models_3D/Minimal/all_3D_18t_turn_models.txt', 'r')
    result_file = open('Generated_Files/Turn_Model_Eval/3D_18_turns_classification.txt', 'w')
    line = data_file.readline()

    print "----------------------------------------------------------------------------------------------"
    print "Description of classes:"
    print "1: both restricted turns, start from the same direction"
    print "2: both restricted turns, end to the same direction"
    print "3: beginning direction of one restricted turn is ending direction of the other restricted turn"
    print "0: none of above"
    print "----------------------------------------------------------------------------------------------"

    result_file.write("---------------------------------------------------------" +
                      "-------------------------------------\n")
    result_file.write("Description of classes:\n")
    result_file.write("1: both restricted turns, start from the same direction\n")
    result_file.write("2: both restricted turns, end to the same direction\n")
    result_file.write("3: beginning direction of one restricted turn is ending direction " +
                      "of the other restricted turn\n")
    result_file.write("0: none of above\n")
    result_file.write("--------------------------------------------------------------------------" +
                      "--------------------\n")
    print "\t\t Restricted Turns\t\t|\t  Classes \t\t\t\tBad Turn"
    print "\tXY\t\tXZ\t\tYZ\t|\txy  xz  yz \t\t\t\tModel"

    result_file.write("\t\t Restricted Turns\t\t|\t Classes \t\t\t\t\tBad Turn\n")
    result_file.write("\tXY\t\tXZ\t\tYZ\t|\txy xz yz \t\t\t\t\tModel\n")
    print "----------------------------------------------------------------------------------------------"
    result_file.write("-------------------------------------------------------------------" +
                      "---------------------------\n")
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

        all_out_ports = str(xy[0][2])+str(xy[1][2])+str(xz[0][2])+str(xz[1][2])+str(yz[0][2])+str(yz[1][2])
        number_of_different_ports = 0
        found_ports = []
        for port in all_out_ports:
            if port not in found_ports:
                number_of_different_ports += 1
                found_ports.append(port)

        all_in_ports = str(xy[0][0])+str(xy[1][0])+str(xz[0][0])+str(xz[1][0])+str(yz[0][0])+str(yz[1][0])
        number_of_different_in_ports = 0
        found_in_ports = []
        for port in all_in_ports:
            if port not in found_in_ports:
                number_of_different_in_ports += 1
                found_in_ports.append(port)

        general_class = str(xy_class)+str(xz_class)+str(yz_class)

        case_2_2_3_2 = 0
        if number_of_different_ports == 2:
            if general_class in ["223", "232", "322"]:
                case_2_2_3_2 = 1

        # in this case, we have number_of_different_in_ports = 2 and we have a combination of classes
        # that mostly depend on input ports (including one class 3)
        case_1_1_3_2 = 0
        if number_of_different_in_ports == 2:
            if general_class in ["113", "131", "311"]:
                case_1_1_3_2 = 1

        case_3_3_3 = 0
        if general_class == "333":
            case_3_3_3 = 1

        bad_turn_model = 0
        if case_2_2_3_2 == 1 or case_1_1_3_2 == 1 or case_3_3_3 == 1:
            bad_turn_model = 1

        if bad_turn_model == 1:
            print "\033[33m"+str(xy), "\t", xz, "\t", yz, "\t|\t", xy_class, " ", xz_class, " ", yz_class, \
                "\t\t", case_2_2_3_2, case_1_1_3_2, case_3_3_3, "\t\t"+str(bad_turn_model)+"\033[0m"
        else:
            print xy, "\t", xz, "\t", yz, "\t|\t", xy_class, " ", xz_class, " ", yz_class, \
                "\t\t", case_2_2_3_2, case_1_1_3_2, case_3_3_3, "\t\t",bad_turn_model

        result_file.write(str(xy)+"\t"+str(xz)+"\t"+str(yz)+"\t|\t"+str(xy_class)+"  "+str(xz_class)+"  "+
                          str(yz_class) + "\t\t\t"+str(case_2_2_3_2)+"  "+str(case_1_1_3_2)+"  "+str(case_3_3_3) +
                          "\t\t\t"+str(bad_turn_model)+"\n")
        # print "-------------------------------------------------------------------"
        line = data_file.readline()
    data_file.close()
    result_file.close()
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
