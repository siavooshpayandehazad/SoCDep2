# Copyright (C) 2015 Siavoosh Payandeh Azad
from Mapper.Mapping_Functions import clear_mapping_for_reconfiguration, read_mapping_from_file, write_mapping_to_file, mapping_into_string
from Mapper.Mapping_Reports import draw_mapping_distribution, draw_mapping
from Mapper.Mapping import mapping
from Scheduler.Scheduling_Functions import clear_scheduling
from Scheduler.Scheduler import schedule_all
from Scheduler.Scheduling_Reports import generate_gantt_charts
from SystemHealthMonitoring import SHMU_Reports
from ConfigAndPackages import Config
import copy


def system_reconfiguration(tg, ag, shmu, noc_rg, critical_rg, noncritical_rg, iteration, logging):
    init_mapping_string = mapping_into_string(tg)
    clear_mapping_for_reconfiguration(tg, ag)
    clear_scheduling(ag)

    SHMU_Reports.draw_shm(shmu.SHM, iteration=iteration)
    if Config.read_mapping_from_file:
        read_mapping_from_file(tg, ag, shmu.SHM, noc_rg, critical_rg, noncritical_rg,
                               Config.mapping_file_path, logging)
        schedule_all(tg, ag, shmu.SHM, False, logging)
    else:
        best_tg, best_ag = mapping(tg, ag, noc_rg, critical_rg, noncritical_rg, shmu.SHM, logging, iteration, initial_mapping_string=init_mapping_string)
        if best_ag is not None and best_tg is not None:
            tg = copy.deepcopy(best_tg)
            ag = copy.deepcopy(best_ag)
            del best_tg, best_ag
            # SHM.add_current_mapping_to_mpm(tg)
            write_mapping_to_file(ag, "mapping_report_"+str(iteration))
    if Config.viz.mapping_distribution:
        draw_mapping_distribution(ag, shmu)
    if Config.viz.mapping:
        draw_mapping(tg, ag, shmu.SHM, "Mapping_post_opt_"+str(iteration))
    if Config.viz.scheduling:
        generate_gantt_charts(tg, ag, "SchedulingTG_"+str(iteration))
    return tg, ag,
