# Copyright (C) Siavoosh Payandeh Azad

from ArchGraphUtilities.Arch_Graph_Reports import draw_vl_opt
from vl_opt_local_search import opt_ag_vertical_link_iterative_local_search, opt_ag_vertical_link_local_search
from ConfigAndPackages import Config


def optimize_ag_vertical_links(ag, shmu, logging):
    ag_cost_file = open('Generated_Files/Internal/vl_opt_cost.txt', 'w')
    ag_cost_file.close()

    if Config.Network_Z_Size < 2:
        raise ValueError("Can not optimize VL placement with 1 layer... (NOC is still 2D)")
    if Config.VL_OptAlg == "LocalSearch":
        opt_ag_vertical_link_local_search(ag, shmu, "vl_opt_cost", logging)
        draw_vl_opt()
        return True
    elif Config.VL_OptAlg == "IterativeLocalSearch":
        opt_ag_vertical_link_iterative_local_search(ag, shmu, "vl_opt_cost", logging)
        draw_vl_opt()
        return True
    else:
        raise ValueError("VL_OptAlg parameter is not valid")