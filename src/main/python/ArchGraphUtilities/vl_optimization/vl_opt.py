# Copyright (C) Siavoosh Payandeh Azad

from ArchGraphUtilities.Arch_Graph_Reports import draw_vl_opt
from vl_opt_local_search import opt_ag_vertical_link_iterative_local_search, opt_ag_vertical_link_local_search
from vl_opt_simulated_annealing import opt_ag_vertical_link_sa
from ConfigAndPackages import Config


def optimize_ag_vertical_links(ag, shmu, logging):
    """
    Optimizes the vertical link placement by calling the appropriate optimization function
    :param ag: architecture graph
    :param shmu: System Health Monitoring Unit
    :param logging: logging file
    :return: True if gets a valid optimization algorithm name from Config file else, raise value error
    """
    ag_cost_file = open('Generated_Files/Internal/vl_opt_cost.txt', 'w')
    ag_cost_file.close()

    if Config.ag.z_size < 2:
        raise ValueError("Can not optimize VL placement with 1 layer... (NOC is still 2D)")
    if Config.vl_opt.vl_opt_alg == "LocalSearch":
        opt_ag_vertical_link_local_search(ag, shmu, "vl_opt_cost", logging)
        draw_vl_opt()
        return True
    elif Config.vl_opt.vl_opt_alg == "IterativeLocalSearch":
        opt_ag_vertical_link_iterative_local_search(ag, shmu, "vl_opt_cost", logging)
        draw_vl_opt()
        return True
    elif Config.vl_opt.vl_opt_alg == "SimulatedAnnealing":
        opt_ag_vertical_link_sa(ag, shmu, "vl_opt_cost", logging)
        draw_vl_opt()
        return True
    else:
        raise ValueError("vl_opt_alg parameter is not valid")
