# Copyright (C) Siavoosh Payandeh Azad


import Tkinter
import ttk
import tkFileDialog
import tkMessageBox
from ConfigAndPackages import Config
from ConfigAndPackages import PackageFile

from PIL import ImageTk, Image


class ConfigApp(Tkinter.Tk):

    apply_button = False

    # Task clustering Config
    cl_opt_start_row = 2
    cl_opt_start_col = 3

    # Mapping Algorithm Config
    mapping_opt_start_row = 6
    mapping_opt_start_col = 3

    # Architecture Graph Config
    topology_starting_row = 2
    topology_starting_col = 0

    # Task Graph Config
    tg_starting_row = 7
    tg_starting_col = 0

    # Routing Config
    routing_starting_row = 15
    routing_starting_col = 0

    # Fault Handling
    fault_starting_row = 2
    fault_starting_col = 6

    # visualization
    viz_starting_row = 7
    viz_starting_col = 6

    # Animation Frame generation
    anim_starting_row = 12
    anim_starting_col = 6

    # vertical Link placement optimization
    vl_placement_starting_row = 2
    vl_placement_starting_col = 9

    # Dependability Config
    dependability_starting_row = 8
    dependability_starting_col = 9

    # PMC Config
    pmc_starting_row = 12
    pmc_starting_col = 9

    option_menu_width = 15
    entry_width = 10

    routing_dict = {'2D': ['XY', 'West First', 'North Last', 'Negative First', 'From File'],
                    '3D': ['XYZ', 'Negative First', 'From File']}

    mapping_dict = {'Manual': ['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing', 'NMap', 'MinMin',
                               'MaxMin', 'MinExecutionTime', 'MinimumCompletionTime'],
                    'RandomDependent': ['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing', 'NMap'],
                    'RandomIndependent': ['MinMin', 'MaxMin', 'MinExecutionTime', 'MinimumCompletionTime']}

    vlp_alg_list = ['LocalSearch', 'IterativeLocalSearch']

    flow_control_list = ['Wormhole', 'StoreAndForward']

    def __init__(self, parent):

        Tkinter.Tk.__init__(self, parent)
        self.parent = parent

        img = ImageTk.PhotoImage(Image.open("GUI_Util/Jelly.png"))

        # This work, "Jelly.png", is a derivative of "Sea Ghost" by Joey Gannon,
        # used under CC BY-SA.  The original version can be found here:
        # https://www.flickr.com/photos/brunkfordbraun/679827214
        # This work is under same license as the original
        
        self.label1 = Tkinter.Label(self, text="", image=img)
        self.label1.image = img
        # ---------------------------------------------
        #                   topology
        # ---------------------------------------------
        self.topology_label = Tkinter.Label(self, text="Topology:")
        available_topologies = ['2DTorus', '2DMesh', '2DLine', '2DRing', '3DMesh']
        self.topology = Tkinter.StringVar()
        self.topology_option = Tkinter.OptionMenu(self, self.topology, *available_topologies,
                                                  command=self.network_size_cont)
        self.topology_option.config(width=self.option_menu_width)

        self.network_size_x = Tkinter.Spinbox(self, from_=1, to=10, width=self.entry_width)
        self.network_size_y = Tkinter.Spinbox(self, from_=1, to=10, width=self.entry_width)
        self.network_size_z = Tkinter.Spinbox(self, from_=1, to=10, width=self.entry_width)

        # ---------------------------------------------
        #                   TG
        # ---------------------------------------------
        self.tg_label = Tkinter.Label(self, text="Task Graph Type:")
        self.available_tgs = ['RandomDependent', 'RandomIndependent', 'Manual', 'FromDOTFile']
        self.tg_type = Tkinter.StringVar(self)
        self.tg_type.set('RandomDependent')
        self.tg_type_option = Tkinter.OptionMenu(self, self.tg_type, *self.available_tgs, command=self._tg_type_cont)
        self.tg_type_option.config(width=self.option_menu_width)

        self.num_of_tasks_label = Tkinter.Label(self, text="Number of Tasks:")
        self.num_of_tasks = Tkinter.Entry(self, width=self.entry_width)

        self.num_of_crit_tasks_label = Tkinter.Label(self, text="Number of Critical Tasks:")
        self.num_of_crit_tasks = Tkinter.Entry(self, width=self.entry_width)

        self.num_of_edge_label = Tkinter.Label(self, text="Number TG Edges:")
        self.num_of_edge = Tkinter.Entry(self, width=self.entry_width)

        self.wcet_range_label = Tkinter.Label(self, text="WCET Range:")
        self.wcet_range = Tkinter.Entry(self, width=self.entry_width)

        self.edge_weight_range_label = Tkinter.Label(self, text="Edge Weight Range:")
        self.edge_weight_range = Tkinter.Entry(self, width=self.entry_width)

        self.release_range_label = Tkinter.Label(self, text="Task Release Range:")
        self.release_range = Tkinter.Entry(self, width=self.entry_width)

        self.tg_browse = Tkinter.Entry(self, bg='gray')
        self.tg_browse.insert(0, "TG File Path...")

        self.tg_browse_button = Tkinter.Button(self, text="Browse", command=self._get_tg_file)

        # ---------------------------------------------
        #                   Routing
        # ---------------------------------------------
        self.routing_label = Tkinter.Label(self, text="Routing Algorithm:")
        available_routings = self.routing_dict['2D']
        self.routing_alg = Tkinter.StringVar()
        self.routing_alg.set(self.routing_dict['2D'][0])
        self.routing_alg_option = Tkinter.OptionMenu(self, self.routing_alg, *available_routings,
                                                     command=self._routing_func)
        self.routing_alg_option.config(width=self.option_menu_width)

        self.routing_type_label = Tkinter.Label(self, text="Routing type:")
        available_routings_types = ['MinimalPath', 'NonMinimalPath']
        self.routing_type = Tkinter.StringVar()
        self.routing_type.set('MinimalPath')
        self.routing_type_option = Tkinter.OptionMenu(self, self.routing_type, *available_routings_types)
        self.routing_type_option.config(width=self.option_menu_width)

        self.routing_browse = Tkinter.Entry(self, bg='gray')
        self.routing_browse.insert(0, "Routing File Path...")

        self.routing_browse_button = Tkinter.Button(self, text="Browse", command=self._get_routing_file)

        self.flow_control_label = Tkinter.Label(self, text="Flow Control:")
        available_flow_controls = self.flow_control_list
        self.flow_control = Tkinter.StringVar()
        self.flow_control.set(self.flow_control_list[0])
        self.flow_control_option = Tkinter.OptionMenu(self, self.flow_control, *available_flow_controls,
                                                      command=self._routing_func)
        # ---------------------------------------------
        #                   Clustering
        # ---------------------------------------------
        self.clustering_opt_var = Tkinter.BooleanVar(self)
        self.clustering_opt_enable = Tkinter.Checkbutton(self, text="Clustering Optimization",
                                                         variable=self.clustering_opt_var,
                                                         command=self._clustering_cont)
        self.clustering_iter_label = Tkinter.Label(self, text="Clustering Iterations:")
        self.clustering_iterations = Tkinter.Entry(self, width=self.entry_width)

        self.clustering_cost_label = Tkinter.Label(self, text="Cost Function Type:")
        available_costs = ['SD', 'SD+MAX', 'MAX', 'SUMCOM', 'AVGUTIL', 'MAXCOM']
        self.clustering_cost = Tkinter.StringVar(self)
        self.clustering_cost.set('SD+MAX')
        self.clustering_costOpt = Tkinter.OptionMenu(self, self.clustering_cost, *available_costs)
        self.clustering_costOpt.config(width=self.option_menu_width)
        # ---------------------------------------------
        #                   Mapping
        # ---------------------------------------------
        self.mapping_label = Tkinter.Label(self, text="Mapping Algorithm:")
        self.mapping = Tkinter.StringVar(self)
        self.mapping.set('LocalSearch')
        self.mapping_option = Tkinter.OptionMenu(self, self.mapping, *self.mapping_dict['RandomDependent'],
                                                 command=self._mapping_alg_cont)
        self.mapping_option.config(width=self.option_menu_width)

        self.mapping_cost_label = Tkinter.Label(self, text="Cost Function Type:")
        available_mapping_costs = ['SD', 'SD+MAX', 'MAX', 'CONSTANT']
        self.mapping_cost = Tkinter.StringVar(self)
        self.mapping_cost.set('SD+MAX')
        self.mapping_cost_opt = Tkinter.OptionMenu(self, self.mapping_cost, *available_mapping_costs)
        self.mapping_cost_opt.config(width=self.option_menu_width)
        # ---------------------------------------------
        #           Local Search
        # ---------------------------------------------
        self.ls_iter_label = Tkinter.Label(self, text="LS Iterations:")
        self.ls_iter = Tkinter.Entry(self, width=self.entry_width)
        self.ls_iter.insert(0, '100')

        self.ils_iter_label = Tkinter.Label(self, text="ILS Iterations:")
        self.ils_iter = Tkinter.Entry(self, width=self.entry_width)
        self.ils_iter.insert(0, '10')

        # ---------------------------------------------
        #           Simulated Annealing
        # ---------------------------------------------

        self.sa_label = Tkinter.Label(self, text="Annealing Schedule:")
        available_annealing = ['Linear', 'Exponential', 'Adaptive', 'Markov', 'Logarithmic', 'Aart', 'Huang']
        self.annealing = Tkinter.StringVar()
        self.annealing.set('Linear')
        self.annealing_option = Tkinter.OptionMenu(self, self.annealing,
                                                   *available_annealing, command=self._annealing_termination)
        self.annealing_option.config(width=self.option_menu_width)

        self.sa_term_label = Tkinter.Label(self, text="Termination Criteria:")
        available_termination = ['StopTemp', 'IterationNum']
        self.termination = Tkinter.StringVar()
        self.termination.set('StopTemp')
        self.terminationOption = Tkinter.OptionMenu(self, self.termination,
                                                    *available_termination, command=self._annealing_termination)
        self.terminationOption.config(width=self.option_menu_width)

        self.sa_iter_label = Tkinter.Label(self, text="Number of Iterations:")
        self.sa_iterations = Tkinter.Entry(self, width=self.entry_width)
        self.sa_iterations.insert(0, '100000')

        self.sa_init_temp_Label = Tkinter.Label(self, text="Initial Temperature:")
        self.sa_init_temp = Tkinter.Entry(self, width=self.entry_width)
        self.sa_init_temp.insert(0, '100')

        self.sa_stop_temp_Label = Tkinter.Label(self, text="Stop Temperature:")
        self.sa_stop_temp = Tkinter.Entry(self, width=self.entry_width)
        self.sa_stop_temp.insert(0, '5')

        self.sa_alpha_Label = Tkinter.Label(self, text="Cooling ratio:")
        self.sa_alpha = Tkinter.Entry(self, width=self.entry_width)
        self.sa_alpha.insert(0, '0.999')

        self.sa_log_const_Label = Tkinter.Label(self, text="Log cooling constant:")
        self.sa_log_const = Tkinter.Entry(self, width=self.entry_width)
        self.sa_log_const.insert(0, '1000')

        self.cost_monitor_Label = Tkinter.Label(self, text="Cost Monitor Queue Size:")
        self.cost_monitor = Tkinter.Entry(self, width=self.entry_width)
        self.cost_monitor.insert(0, '2000')

        self.cost_monitor_slope_Label = Tkinter.Label(self, text="Slope Range For Cooling:")
        self.cost_monitor_slope = Tkinter.Entry(self, width=self.entry_width)
        self.cost_monitor_slope.insert(0, '0.02')

        self.max_steady_state_Label = Tkinter.Label(self, text="Max steps/no improvement:")
        self.max_steady_state = Tkinter.Entry(self, width=self.entry_width)
        self.max_steady_state.insert(0, '30000')

        self.markov_num_Label = Tkinter.Label(self, text="Length of Markov Chain:")
        self.markov_num = Tkinter.Entry(self, width=self.entry_width)
        self.markov_num.insert(0, '2000')

        self.markov_temp_step_Label = Tkinter.Label(self, text="Temperature step:")
        self.markov_temp_step = Tkinter.Entry(self, width=self.entry_width)
        self.markov_temp_step.insert(0, '1')

        self.sa_delta_Label = Tkinter.Label(self, text="Delta:")
        self.sa_delta = Tkinter.Entry(self, width=self.entry_width)
        self.sa_delta.insert(0, '0.05')

        # ---------------------------------------------
        #               Fault Injection
        # ---------------------------------------------
        self.fault_injection = Tkinter.BooleanVar(self)
        self.fault_injection_enable = Tkinter.Checkbutton(self, text="Event Driven Fault Injection",
                                                          variable=self.fault_injection,
                                                          command=self._fault_injection)

        self.mtbf_label = Tkinter.Label(self, text="MTBF (sec):")
        self.mtbf = Tkinter.Entry(self, width=self.entry_width)
        self.mtbf.insert(0, '2')

        self.sd_mtbf_label = Tkinter.Label(self, text="TBF's Standard Deviation:")
        self.sd_mtbf = Tkinter.Entry(self, width=self.entry_width)
        self.sd_mtbf.insert(0, '0.1')

        self.run_time_label = Tkinter.Label(self, text="Program RunTime:")
        self.run_time = Tkinter.Entry(self, width=self.entry_width)
        self.run_time.insert(0, '10')

        # ---------------------------------------------
        #               Viz
        # ---------------------------------------------
        self.all_viz = Tkinter.BooleanVar(self)
        self.all_viz.set('False')
        self.all_viz_enable = Tkinter.Checkbutton(self, text="Check/Un-check all reports",
                                                  variable=self.all_viz, command=self._all_viz_func,
                                                  wraplength=100)

        self.rg_draw = Tkinter.BooleanVar(self)
        self.rg_draw.set('False')
        self.rg_draw_enable = Tkinter.Checkbutton(self, text="Routing Graph", variable=self.rg_draw)

        self.shm_draw = Tkinter.BooleanVar(self)
        self.shm_draw.set('False')
        self.shm_draw_enable = Tkinter.Checkbutton(self, text="System Health Map", variable=self.shm_draw)

        self.mapping_Draw = Tkinter.BooleanVar(self)
        self.mapping_Draw.set('False')
        self.mapping_draw_enable = Tkinter.Checkbutton(self, text="Mapping Report", variable=self.mapping_Draw)

        self.pmcg_draw = Tkinter.BooleanVar(self)
        self.pmcg_draw.set('False')
        self.pmcg_draw_enable = Tkinter.Checkbutton(self, text="PMCG Report", variable=self.pmcg_draw)

        self.ttg_draw = Tkinter.BooleanVar(self)
        self.ttg_draw.set('False')
        self.ttg_draw_enable = Tkinter.Checkbutton(self, text="TTG Report", variable=self.ttg_draw)

        # ---------------------------------------------
        #               Anim
        # ---------------------------------------------
        self.anim_enable = Tkinter.BooleanVar(self)
        self.anim_enable.set('False')
        self.anim_enableBox = Tkinter.Checkbutton(self, text="Generate Animation Frames",
                                                  variable=self.anim_enable, command=self._animation_config)

        self.frame_rez_label = Tkinter.Label(self, text="Frame Resolution(dpi):")
        self.frame_rez = Tkinter.Entry(self, width=self.entry_width)
        self.frame_rez.insert(0, '20')

        # ----------------------------------------
        #           Vertical Link Placement
        # ----------------------------------------
        self.vl_placement_enable = Tkinter.BooleanVar(self)
        self.vl_placement_enable.set('False')
        self.vl_placement_enable_box = Tkinter.Checkbutton(self, text="Enable VL Placement Optimization",
                                                           variable=self.vl_placement_enable,
                                                           command=self._vl_placement_func,
                                                           wraplength=200)

        self.vlp_alg_label = Tkinter.Label(self, text="Opt algorithm:")
        self.vlp_alg = Tkinter.StringVar()
        self.vlp_alg.set('LocalSearch')
        self.vlp_alg_option = Tkinter.OptionMenu(self, self.vlp_alg, *self.vlp_alg_list, command=self._vlp_alg_func)
        self.vlp_alg_option.config(width=self.option_menu_width)

        self.num_of_vls_label = Tkinter.Label(self, text="Number of VLs:")
        self.num_of_vls = Tkinter.Entry(self, width=self.entry_width)

        self.vlp_iter_ls_label = Tkinter.Label(self, text="LS Iterations:")
        self.vlp_iter_ls = Tkinter.Entry(self, width=self.entry_width)

        self.vlp_iter_ils_label = Tkinter.Label(self, text="ILS Iterations:")
        self.vlp_iter_ils = Tkinter.Entry(self, width=self.entry_width)
        # ----------------------------------------
        #           Dependability section
        # ----------------------------------------
        self.slack_number_label = Tkinter.Label(self, text="Task Slack Count:")
        self.slack_number = Tkinter.Spinbox(self, from_=0, to=10, width=self.entry_width)

        self.com_slack_number_label = Tkinter.Label(self, text="Com. Slack Count:")
        self.com_slack_number = Tkinter.Spinbox(self, from_=0, to=10, width=self.entry_width)

        self.num_of_rects_label = Tkinter.Label(self, text="NoCDepend Rectangle #:")
        self.num_of_rects = Tkinter.Spinbox(self, from_=1, to=10, width=self.entry_width)
        self.num_of_rects.delete(0, 'end')
        self.num_of_rects.insert(0, 3)

        self.error_message = Tkinter.Label(self, text="", font="-weight bold", fg="red")

        # ----------------------------------------
        #           PMC config
        # ----------------------------------------
        self.pmc_enable = Tkinter.BooleanVar(self)
        self.pmc_enable.set('False')
        self.pmc_enable_check_box = Tkinter.Checkbutton(self, text="Enable PMC config",
                                                        variable=self.pmc_enable, command=self._pmc_func)

        self.pmc_type_label = Tkinter.Label(self, text="PMC Model:")
        self.available_pmc_types = ['Sequentially diagnosable', 'One Step Diagnosable']
        self.pmc_type = Tkinter.StringVar(self)
        self.pmc_type.set('Sequentially diagnosable')
        self.pmc_type_opt = Tkinter.OptionMenu(self, self.pmc_type, *self.available_pmc_types,
                                               command=self._t_fault_control)
        self.pmc_type_opt.config(width=self.option_menu_width)

        self.t_fault_diagnosable_label = Tkinter.Label(self, text="T-Fault Diagnosable:")
        self.t_fault_diagnosable = Tkinter.Entry(self, width=self.entry_width)

        self.error_message = Tkinter.Label(self, text="", font="-weight bold", fg="red")

        self._initialize()

    def _initialize(self):

        self.grid()

        self.label1.grid(row=0, column=1, sticky='eW')
        self.label1.bind("<Enter>", self._on_enter)

        logo = Tkinter.Label(self, text="SCHEDULE AND DEPEND CONFIG GUI", font="-weight bold")
        logo.grid(column=1, row=0, columnspan=7)
        ttk.Separator(self, orient='horizontal').grid(column=0, row=1, columnspan=11, sticky="ew")

        # ----------------------------------------
        Tkinter.Label(self, text="Topology Config", font="-weight bold").grid(column=self.topology_starting_col,
                                                                              row=self.topology_starting_row,
                                                                              columnspan=2)
        self.topology.set('2DMesh')
        self.topology_label.grid(column=self.topology_starting_col, row=self.topology_starting_row+1)
        self.topology_option.grid(column=self.topology_starting_col+1, row=self.topology_starting_row+1, sticky='w')

        x_size_label = Tkinter.Label(self, text="X Size:")
        y_size_label = Tkinter.Label(self, text="Y Size:")
        z_size_label = Tkinter.Label(self, text="Z Size:")

        self.network_size_x.delete(0, 'end')
        self.network_size_x.insert(0, 3)
        self.network_size_y.delete(0, 'end')
        self.network_size_y.insert(0, 3)
        self.network_size_z.delete(0, 'end')
        self.network_size_z.insert(0, 1)

        x_size_label.grid(column=self.topology_starting_col, row=self.topology_starting_row+2)
        self.network_size_x.grid(column=self.topology_starting_col+1, row=self.topology_starting_row+2, sticky='w')
        y_size_label.grid(column=self.topology_starting_col, row=self.topology_starting_row+3)
        self.network_size_y.grid(column=self.topology_starting_col+1, row=self.topology_starting_row+3, sticky='w')
        z_size_label.grid(column=self.topology_starting_col, row=self.topology_starting_row+4)
        self.network_size_z.grid(column=self.topology_starting_col+1, row=self.topology_starting_row+4, sticky='w')
        self.network_size_z.config(state='disabled')

        ttk.Separator(self, orient='vertical').grid(column=self.topology_starting_col+2,
                                                    row=self.topology_starting_row+1, rowspan=16, sticky="ns")
        ttk.Separator(self, orient='horizontal').grid(column=self.topology_starting_col,
                                                      row=self.topology_starting_row+5, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   TG
        # ----------------------------------------
        Tkinter.Label(self, text="Task Graph Settings", font="-weight bold").grid(column=self.tg_starting_col,
                                                                                  row=self.tg_starting_row,
                                                                                  columnspan=2)
        self.tg_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+1, sticky='w')
        self.tg_type_option.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+1, sticky='w')

        self.num_of_tasks_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+2, sticky='w')
        self.num_of_tasks.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+2, sticky='w')
        self.num_of_tasks.insert(0, '35')

        self.num_of_crit_tasks_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+3, sticky='w')
        self.num_of_crit_tasks.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+3, sticky='w')
        self.num_of_crit_tasks.insert(0, '0')

        self.num_of_edge_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+4, sticky='w')
        self.num_of_edge.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+4, sticky='w')
        self.num_of_edge.insert(0, '20')

        self.wcet_range_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+5, sticky='w')
        self.wcet_range.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+5, sticky='w')
        self.wcet_range.insert(0, '15')

        self.edge_weight_range_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+6, sticky='w')
        self.edge_weight_range.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+6, sticky='w')
        self.edge_weight_range.insert(0, '7')

        self.release_range_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+7, sticky='w')
        self.release_range.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+7, sticky='w')
        self.release_range.insert(0, '5')

        ttk.Separator(self, orient='horizontal').grid(column=self.tg_starting_col,
                                                      row=self.tg_starting_row+8, columnspan=2, sticky="ew")

        # ---------------------------------------------
        #                   Routing
        # ---------------------------------------------
        Tkinter.Label(self, text="Routing Settings", font="-weight bold").grid(column=self.routing_starting_col,
                                                                               row=self.routing_starting_row,
                                                                               columnspan=2)
        self.routing_label.grid(column=self.routing_starting_col, row=self.routing_starting_row+1)
        self.routing_alg_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+1)

        self.routing_type_label.grid(column=self.routing_starting_col, row=self.routing_starting_row+2)
        self.routing_type_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+2)
        self.routing_type_option.config(state='disable')

        self.flow_control_label.grid(column=self.routing_starting_col, row=self.routing_starting_row+4)
        self.flow_control_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+4)
        self.flow_control_option.config(state='normal')
        ttk.Separator(self, orient='horizontal').grid(column=self.routing_starting_col,
                                                      row=self.routing_starting_row+5, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   CTG
        # ----------------------------------------
        Tkinter.Label(self, text="Clustering Settings", font="-weight bold").grid(column=self.cl_opt_start_col,
                                                                                  row=self.cl_opt_start_row,
                                                                                  columnspan=2)
        self.clustering_opt_var.set('False')
        self.clustering_iterations.insert(0, '1000')
        self.clustering_opt_enable.grid(column=self.cl_opt_start_col, row=self.cl_opt_start_row+1)

        ttk.Separator(self, orient='horizontal').grid(column=self.cl_opt_start_col, row=self.cl_opt_start_row+4,
                                                      columnspan=2, sticky="ew")

        # ----------------------------------------
        #                   Mapping
        # ----------------------------------------
        Tkinter.Label(self, text="Mapping Settings", font="-weight bold").grid(column=self.mapping_opt_start_col,
                                                                               row=self.mapping_opt_start_row,
                                                                               columnspan=2)
        self.mapping_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+1)
        self.mapping_option.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+1)

        self.mapping_cost_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+2)
        self.mapping_cost_opt.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+2)

        self.ls_iter_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+3)
        self.ls_iter.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+3)

        ttk.Separator(self, orient='vertical').grid(column=self.cl_opt_start_col+2,
                                                    row=self.cl_opt_start_row+1, rowspan=14, sticky="ns")
        ttk.Separator(self, orient='horizontal').grid(column=self.mapping_opt_start_col,
                                                      row=self.mapping_opt_start_row+11, columnspan=2, sticky="ew")
        # ----------------------------------------
        #               Fault
        # ----------------------------------------
        Tkinter.Label(self, text="Fault Settings", font="-weight bold").grid(column=self.fault_starting_col,
                                                                             row=self.fault_starting_row,
                                                                             columnspan=2)
        self.fault_injection.set('False')
        self.fault_injection_enable.grid(column=self.fault_starting_col, row=self.fault_starting_row+1)

        ttk.Separator(self, orient='horizontal').grid(column=self.fault_starting_col,
                                                      row=self.fault_starting_row+5, columnspan=2, sticky="ew")

        ttk.Separator(self, orient='vertical').grid(column=self.fault_starting_col+2,
                                                    row=self.fault_starting_row+1, rowspan=12, sticky="ns")
        # ----------------------------------------
        #                   Viz
        # ----------------------------------------
        Tkinter.Label(self, text="Visualization Config", font="-weight bold").grid(column=self.viz_starting_col,
                                                                                   row=self.viz_starting_row,
                                                                                   columnspan=2)

        self.all_viz_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+1, columnspan=1, sticky='w')

        self.shm_draw_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+2, sticky='W')
        self.rg_draw_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+3, sticky='W')
        self.mapping_draw_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+4, sticky='W')
        self.pmcg_draw_enable.grid(column=self.viz_starting_col+1, row=self.viz_starting_row+3, sticky='W')
        self.ttg_draw_enable.grid(column=self.viz_starting_col+1, row=self.viz_starting_row+4, sticky='W')

        ttk.Separator(self, orient='horizontal').grid(column=self.viz_starting_col,
                                                      row=self.viz_starting_row+5, columnspan=2, sticky="ew")
        # ----------------------------------------
        #               Animation
        # ----------------------------------------
        Tkinter.Label(self, text="Animation Frames Config", font="-weight bold").grid(column=self.anim_starting_col,
                                                                                      row=self.anim_starting_row,
                                                                                      columnspan=2)

        self.anim_enableBox.grid(column=self.anim_starting_col, row=self.anim_starting_row+1,
                                 sticky='W')
        ttk.Separator(self, orient='horizontal').grid(column=self.anim_starting_col, row=self.anim_starting_row+3,
                                                      columnspan=2, sticky="ew")
        # ----------------------------------------
        #           Vertical Link Placement
        # ----------------------------------------
        Tkinter.Label(self, text="Vertical Link Placement Optimization",
                      font="-weight bold").grid(column=self.vl_placement_starting_col,
                                                row=self.vl_placement_starting_row, columnspan=2)

        self.vl_placement_enable_box.grid(column=self.vl_placement_starting_col, row=self.vl_placement_starting_row+1)
        self.vl_placement_enable_box.config(state='disable')

        ttk.Separator(self,
                      orient='horizontal').grid(column=self.vl_placement_starting_col,
                                                row=self.vl_placement_starting_row+6, columnspan=2, sticky="ew")
        # ----------------------------------------
        #           Dependability section
        # ----------------------------------------
        Tkinter.Label(self, text="Dependability Config", 
                      font="-weight bold").grid(column=self.dependability_starting_col,
                                                row=self.dependability_starting_row, columnspan=2)
        self.slack_number_label.grid(column=self.dependability_starting_col, row=self.dependability_starting_row+1)
        self.slack_number.grid(column=self.dependability_starting_col+1, row=self.dependability_starting_row+1)

        self.com_slack_number_label.grid(column=self.dependability_starting_col, row=self.dependability_starting_row+2)
        self.com_slack_number.grid(column=self.dependability_starting_col+1, row=self.dependability_starting_row+2)

        self.num_of_rects_label.grid(column=self.dependability_starting_col, row=self.dependability_starting_row+3)
        self.num_of_rects.grid(column=self.dependability_starting_col+1, row=self.dependability_starting_row+3)

        ttk.Separator(self, orient='horizontal').grid(column=self.dependability_starting_col,
                                                      row=self.dependability_starting_row+4, columnspan=2, sticky="ew")
        # ----------------------------------------
        #           PMC Graph
        # ----------------------------------------
        Tkinter.Label(self, text="PMC Config", font="-weight bold").grid(column=self.pmc_starting_col,
                                                                         row=self.pmc_starting_row, columnspan=2)

        self.pmc_enable_check_box.grid(column=self.pmc_starting_col, row=self.pmc_starting_row+1, sticky='w')

        ttk.Separator(self, orient='horizontal').grid(column=self.pmc_starting_col,
                                                      row=self.pmc_starting_row+4, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   Buttons
        # ----------------------------------------
        self.error_message.grid(column=4, row=19, columnspan=5)

        quit_button = Tkinter.Button(self, text="Apply", command=self._apply_button, width=15)
        quit_button.grid(column=4, row=20, columnspan=2, rowspan=2)

        quit_button = Tkinter.Button(self, text="cancel", command=self._cancel_button)
        quit_button.grid(column=6, row=20, columnspan=2, rowspan=2)

    def network_size_cont(self, topology):
        if '3D' in topology:
            self.network_size_z.config(state='normal')
            self.vl_placement_enable_box.config(state='normal')
            self.routing_alg_option.grid_forget()
            del self.routing_alg_option
            self.routing_alg.set('Please Select...')
            self.routing_alg_option = Tkinter.OptionMenu(self, self.routing_alg, *self.routing_dict['3D'],
                                                         command=self._routing_func)
            self.routing_alg_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+1)
            self.routing_alg_option.config(width=self.option_menu_width)

            self.routing_type.set("Please Select...")
            self.routing_type_option.config(state='disable')
            self.routing_browse.grid_forget()
            self.routing_browse_button.grid_forget()

            self.network_size_z.delete(0, 'end')
            self.network_size_z.insert(0, 2)
        else:
            self.vl_placement_enable_box.deselect()
            self.vl_placement_enable_box.config(state='disable')
            self.vlp_alg_label.grid_forget()
            self.vlp_alg_option.grid_forget()
            self.num_of_vls_label.grid_forget()
            self.num_of_vls.grid_forget()
            self.vlp_iter_ls_label.grid_forget()
            self.vlp_iter_ls.grid_forget()
            self.vlp_iter_ils_label.grid_forget()
            self.vlp_iter_ils.grid_forget()

            self.routing_alg_option.grid_forget()
            del self.routing_alg_option
            self.routing_alg.set('Please Select...')
            self.routing_alg_option = Tkinter.OptionMenu(self, self.routing_alg, *self.routing_dict['2D'],
                                                         command=self._routing_func)
            self.routing_alg_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+1)
            self.routing_alg_option.config(width=self.option_menu_width)

            self.routing_type.set("Please Select...")
            self.routing_type_option.config(state='disable')
            self.routing_browse.grid_forget()
            self.routing_browse_button.grid_forget()

            self.network_size_z.delete(0, 'end')
            self.network_size_z.insert(0, 1)
            self.network_size_z.config(state='disabled')

    def _tg_type_cont(self, tg_type):
        if tg_type == 'RandomDependent':
            self.mapping_option.grid_forget()
            del self.mapping_option
            self.mapping.set('Please Select...')
            self.mapping_option = Tkinter.OptionMenu(self, self.mapping, *self.mapping_dict['RandomDependent'],
                                                     command=self._mapping_alg_cont)
            self.mapping_option.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+1)
            self.mapping_option.config(width=self.option_menu_width)
            self._clear_mapping()

            self.num_of_tasks_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+2)
            self.num_of_tasks.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+2)
            self.num_of_tasks.delete(0, 'end')
            self.num_of_tasks.insert(0, '35')

            self.num_of_crit_tasks_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+3)
            self.num_of_crit_tasks.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+3)
            self.num_of_crit_tasks.delete(0, 'end')
            self.num_of_crit_tasks.insert(0, '0')

            self.num_of_edge_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+4)
            self.num_of_edge.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+4)
            self.num_of_edge.delete(0, 'end')
            self.num_of_edge.insert(0, '20')

            self.wcet_range_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+5)
            self.wcet_range.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+5)
            self.wcet_range.delete(0, 'end')
            self.wcet_range.insert(0, '15')

            self.edge_weight_range_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+6)
            self.edge_weight_range.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+6)
            self.edge_weight_range.delete(0, 'end')
            self.edge_weight_range.insert(0, '7')

            self.release_range_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+7)
            self.release_range.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+7)
            self.release_range.delete(0, 'end')
            self.release_range.insert(0, '5')

            self.tg_browse.grid_forget()
            self.tg_browse_button.grid_forget()

        elif tg_type == 'RandomIndependent':
            self.mapping_option.grid_forget()
            del self.mapping_option
            self.mapping.set('Please Select...')
            self.mapping_option = Tkinter.OptionMenu(self, self.mapping, *self.mapping_dict['RandomIndependent'],
                                                     command=self._mapping_alg_cont)
            self.mapping_option.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+1)
            self.mapping_option.config(width=self.option_menu_width)
            self._clear_mapping()

            self.num_of_tasks_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+2)
            self.num_of_tasks.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+2)
            self.num_of_tasks.delete(0, 'end')
            self.num_of_tasks.insert(0, '35')

            self.num_of_crit_tasks_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+3)
            self.num_of_crit_tasks.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+3)
            self.num_of_crit_tasks.delete(0, 'end')
            self.num_of_crit_tasks.insert(0, '0')

            self.wcet_range_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+4)
            self.wcet_range.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+4)
            self.wcet_range.delete(0, 'end')
            self.wcet_range.insert(0, '15')

            self.release_range_label.grid(column=self.tg_starting_col, row=self.tg_starting_row+5)
            self.release_range.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+5)
            self.release_range.delete(0, 'end')
            self.release_range.insert(0, '5')

            self.num_of_edge_label.grid_forget()
            self.num_of_edge.grid_forget()

            self.edge_weight_range.grid_forget()
            self.edge_weight_range_label.grid_forget()

            self.tg_browse.grid_forget()
            self.tg_browse_button.grid_forget()

        elif tg_type == 'Manual':
            self.mapping_option.grid_forget()
            del self.mapping_option
            self.mapping.set('Please Select...')
            self.mapping_option = Tkinter.OptionMenu(self, self.mapping, *self.mapping_dict['Manual'],
                                                     command=self._mapping_alg_cont)
            self.mapping_option.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+1)
            self.mapping_option.config(width=self.option_menu_width)
            self._clear_mapping()

            self.tg_browse.grid_forget()
            self.tg_browse_button.grid_forget()

            self.num_of_tasks_label.grid_forget()
            self.num_of_tasks.grid_forget()

            self.num_of_crit_tasks_label.grid_forget()
            self.num_of_crit_tasks.grid_forget()

            self.num_of_edge_label.grid_forget()
            self.num_of_edge.grid_forget()

            self.wcet_range_label.grid_forget()
            self.wcet_range.grid_forget()

            self.release_range_label.grid_forget()
            self.release_range.grid_forget()

            self.edge_weight_range.grid_forget()
            self.edge_weight_range_label.grid_forget()

        elif tg_type == 'FromDOTFile':
            self.mapping_option.grid_forget()
            del self.mapping_option
            self.mapping.set('Please Select...')
            self.mapping_option = Tkinter.OptionMenu(self, self.mapping, *self.mapping_dict['Manual'],
                                                     command=self._mapping_alg_cont)
            self.mapping_option.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+1)
            self.mapping_option.config(width=self.option_menu_width)
            self._clear_mapping()

            self.tg_browse.grid(column=self.tg_starting_col, row=self.tg_starting_row+2, sticky='e')
            self.tg_browse_button.grid(column=self.tg_starting_col+1, row=self.tg_starting_row+2)

            self.num_of_tasks_label.grid_forget()
            self.num_of_tasks.grid_forget()

            self.num_of_crit_tasks_label.grid_forget()
            self.num_of_crit_tasks.grid_forget()

            self.num_of_edge_label.grid_forget()
            self.num_of_edge.grid_forget()

            self.wcet_range_label.grid_forget()
            self.wcet_range.grid_forget()

            self.release_range_label.grid_forget()
            self.release_range.grid_forget()

            self.edge_weight_range.grid_forget()
            self.edge_weight_range_label.grid_forget()

    def _all_viz_func(self):
        if self.all_viz.get():
            self.pmcg_draw.set(True)
            self.mapping_Draw.set(True)
            self.rg_draw.set(True)
            self.shm_draw.set(True)
            self.ttg_draw.set(True)
        else:
            self.pmcg_draw.set(False)
            self.mapping_Draw.set(False)
            self.rg_draw.set(False)
            self.shm_draw.set(False)
            self.ttg_draw.set(False)

    def _get_tg_file(self):
        path = tkFileDialog.askopenfilename()
        if path:
            self.tg_browse.delete(0, 'end')
            self.tg_browse.insert(1, path)

    def _get_routing_file(self):
        path = tkFileDialog.askopenfilename()
        if path:
            self.routing_browse.delete(0, 'end')
            self.routing_browse.insert(1, path)

    def _vl_placement_func(self):
        if self.vl_placement_enable.get():
            self.vlp_alg_label.grid(column=self.vl_placement_starting_col,
                                    row=self.vl_placement_starting_row+2, sticky='w')
            self.vlp_alg_option.grid(column=self.vl_placement_starting_col+1,
                                     row=self.vl_placement_starting_row+2, sticky='w')
            self.num_of_vls_label.grid(column=self.vl_placement_starting_col,
                                       row=self.vl_placement_starting_row+3, sticky='w')
            self.num_of_vls.grid(column=self.vl_placement_starting_col+1,
                                 row=self.vl_placement_starting_row+3, sticky='w')
            self.num_of_vls.delete(0, 'end')
            self.num_of_vls.insert(0, '5')

            self.vlp_iter_ls_label.grid(column=self.vl_placement_starting_col,
                                        row=self.vl_placement_starting_row+4, sticky='w')
            self.vlp_iter_ls.grid(column=self.vl_placement_starting_col+1,
                                  row=self.vl_placement_starting_row+4, sticky='w')
            self.vlp_iter_ls.delete(0, 'end')
            self.vlp_iter_ls.insert(0, '10')

        else:
            self.vlp_alg_label.grid_forget()
            self.vlp_alg_option.grid_forget()
            self.num_of_vls_label.grid_forget()
            self.num_of_vls.grid_forget()
            self.vlp_iter_ls_label.grid_forget()
            self.vlp_iter_ls.grid_forget()
            self.vlp_iter_ils_label.grid_forget()
            self.vlp_iter_ils.grid_forget()

    def _pmc_func(self):
        if self.pmc_enable.get():
            self.pmc_type_label.grid(column=self.pmc_starting_col, row=self.pmc_starting_row+2, sticky='w')
            self.pmc_type_opt.grid(column=self.pmc_starting_col+1, row=self.pmc_starting_row+2, sticky='w')
        else:
            self.pmc_type_label.grid_forget()
            self.pmc_type_opt.grid_forget()

    def _t_fault_control(self):
        if self.pmc_type.get() == 'One Step Diagnosable':
            self.t_fault_diagnosable_label.grid(column=self.pmc_starting_col, row=self.pmc_starting_row+3, sticky='w')
            self.t_fault_diagnosable.grid(column=self.pmc_starting_col+1, row=self.pmc_starting_row+3, sticky='w')
        else:
            self.t_fault_diagnosable_label.grid_forget()
            self.t_fault_diagnosable.grid_forget()

    def _vlp_alg_func(self):
        if self.vlp_alg.get() == 'LocalSearch':
            self.vlp_iter_ls_label.grid(column=self.vl_placement_starting_col,
                                        row=self.vl_placement_starting_row+4, sticky='w')
            self.vlp_iter_ls.grid(column=self.vl_placement_starting_col+1,
                                  row=self.vl_placement_starting_row+4, sticky='w')
            self.vlp_iter_ls.delete(0, 'end')
            self.vlp_iter_ls.insert(0, '10')

            self.vlp_iter_ils_label.grid_forget()
            self.vlp_iter_ils.grid_forget()

        elif self.vlp_alg.get() == 'IterativeLocalSearch':
            self.vlp_iter_ls_label.grid(column=self.vl_placement_starting_col,
                                        row=self.vl_placement_starting_row+4, sticky='w')
            self.vlp_iter_ls.grid(column=self.vl_placement_starting_col+1,
                                  row=self.vl_placement_starting_row+4, sticky='w')
            self.vlp_iter_ls.delete(0, 'end')
            self.vlp_iter_ls.insert(0, '10')

            self.vlp_iter_ils_label.grid(column=self.vl_placement_starting_col,
                                         row=self.vl_placement_starting_row+5, sticky='w')
            self.vlp_iter_ils.grid(column=self.vl_placement_starting_col+1,
                                   row=self.vl_placement_starting_row+5, sticky='w')
            self.vlp_iter_ils.delete(0, 'end')
            self.vlp_iter_ils.insert(0, '10')

    def _routing_func(self, event):
        if self.routing_alg.get() in ['XY', 'XYZ']:
            self.routing_type_option.config(state='disable')
        else:
            self.routing_type_option.config(state='normal')

        if self.routing_alg.get() == 'From File':
            self.routing_browse.grid(column=self.routing_starting_col, row=self.routing_starting_row+3, sticky='e')
            self.routing_browse_button.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+3)
        else:
            self.routing_browse.grid_forget()
            self.routing_browse_button.grid_forget()

    def _clustering_cont(self):
        if self.clustering_opt_var.get():
            self.clustering_iter_label.grid(column=self.cl_opt_start_col, row=self.cl_opt_start_row+2)
            self.clustering_iterations.grid(column=self.cl_opt_start_col+1, row=self.cl_opt_start_row+2)
            self.clustering_iterations.delete(0, 'end')
            self.clustering_iterations.insert(0, '1000')

            self.clustering_cost_label.grid(column=self.cl_opt_start_col, row=self.cl_opt_start_row+3)
            self.clustering_costOpt.grid(column=self.cl_opt_start_col+1, row=self.cl_opt_start_row+3)
        else:
            self.clustering_iter_label.grid_forget()
            self.clustering_iterations.grid_forget()
            self.clustering_cost_label.grid_forget()
            self.clustering_costOpt.grid_forget()

    def _clear_mapping(self):
        self._clear_sa_mapping()
        self.ls_iter_label.grid_forget()
        self.ls_iter.grid_forget()
        self.ils_iter_label.grid_forget()
        self.ils_iter.grid_forget()
        self.mapping_cost_label.grid_forget()
        self.mapping_cost_opt.grid_forget()

    def _mapping_alg_cont(self):
        if self.mapping.get() in ['SimulatedAnnealing', 'LocalSearch', 'IterativeLocalSearch']:
            self.mapping_cost_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+2)
            self.mapping_cost_opt.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+2)
        else:
            self.mapping_cost_label.grid_forget()
            self.mapping_cost_opt.grid_forget()

        if self.mapping.get() == 'SimulatedAnnealing':
            self._clear_sa_mapping()
            self.annealing.set('Linear')
            self.sa_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+3)
            self.annealing_option.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+3)

            self.sa_init_temp.delete(0, 'end')
            self.sa_init_temp.insert(0, '100')
            self.sa_init_temp_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+4)
            self.sa_init_temp.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+4)

            self.termination.set('StopTemp')
            self.sa_term_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+5)
            self.terminationOption.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+5)

            self.sa_iterations.delete(0, 'end')
            self.sa_iterations.insert(0, '100000')
            self.sa_iter_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+6)
            self.sa_iterations.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+6)
        else:
            self._clear_sa_mapping()

        if self.mapping.get() in ['LocalSearch', 'IterativeLocalSearch']:
            self.ls_iter.delete(0, 'end')
            self.ls_iter.insert(0, '100')
            self.ls_iter_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+3)
            self.ls_iter.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+3)
        else:
            self.ls_iter_label.grid_forget()
            self.ls_iter.grid_forget()

        if self.mapping.get() == 'IterativeLocalSearch':
            self.ils_iter.delete(0, 'end')
            self.ils_iter.insert(0, '10')
            self.ils_iter_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+4)
            self.ils_iter.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+4)
        else:
            self.ils_iter_label.grid_forget()
            self.ils_iter.grid_forget()

    def _annealing_termination(self):
        if self.mapping.get() == 'SimulatedAnnealing':
            if self.annealing.get() == 'Linear' or self.termination.get() == 'IterationNum':
                self.sa_stop_temp.grid_forget()
                self.sa_stop_temp_Label.grid_forget()

                self.sa_iter_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+6)
                self.sa_iterations.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+6)

            elif self.termination.get() == 'StopTemp' and self.annealing.get() != 'Linear':
                self.sa_iterations.grid_forget()
                self.sa_iter_label.grid_forget()

                self.sa_stop_temp.delete(0, 'end')
                self.sa_stop_temp.insert(0, '5')
                self.sa_stop_temp_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+6)
                self.sa_stop_temp.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+6)
            else:
                self.sa_stop_temp.grid_forget()
                self.sa_stop_temp_Label.grid_forget()

                self.sa_iterations.grid_forget()
                self.sa_iter_label.grid_forget()

            if self.annealing.get() in ['Exponential', 'Adaptive', 'Aart', 'Huang']:
                self.sa_alpha.delete(0, 'end')
                self.sa_alpha.insert(0, '0.999')
                self.sa_alpha_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+7)
                self.sa_alpha.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+7)
            else:
                self.sa_alpha_Label.grid_forget()
                self.sa_alpha.grid_forget()

            if self.annealing.get() == 'Logarithmic':
                self.sa_log_const.delete(0, 'end')
                self.sa_log_const.insert(0, '1000')
                self.sa_log_const_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+7)
                self.sa_log_const.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+7)
            else:
                self.sa_log_const_Label.grid_forget()
                self.sa_log_const.grid_forget()

            if self.annealing.get() == 'Adaptive':

                self.cost_monitor_slope.delete(0, 'end')
                self.cost_monitor_slope.insert(0, '0.02')
                self.cost_monitor_slope_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+9)
                self.cost_monitor_slope.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+9)

                self.max_steady_state.delete(0, 'end')
                self.max_steady_state.insert(0, '30000')
                self.max_steady_state_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+10)
                self.max_steady_state.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+10)
            else:
                self.max_steady_state_Label.grid_forget()
                self.max_steady_state.grid_forget()

                self.cost_monitor_slope_Label.grid_forget()
                self.cost_monitor_slope.grid_forget()

            if self.annealing.get() == 'Markov':
                self.markov_num.delete(0, 'end')
                self.markov_num.insert(0, '2000')
                self.markov_num_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+7)
                self.markov_num.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+7)

                self.markov_temp_step.delete(0, 'end')
                self.markov_temp_step.insert(0, '1')
                self.markov_temp_step_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+8)
                self.markov_temp_step.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+8)
            else:
                self.markov_num_Label.grid_forget()
                self.markov_num.grid_forget()

                self.markov_temp_step_Label.grid_forget()
                self.markov_temp_step.grid_forget()

            if self.annealing.get() in ['Aart', 'Adaptive', 'Huang']:
                self.cost_monitor.delete(0, 'end')
                self.cost_monitor.insert(0, '2000')
                self.cost_monitor_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+8)
                self.cost_monitor.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+8)
            else:
                self.cost_monitor_Label.grid_forget()
                self.cost_monitor.grid_forget()

            if self.annealing.get() in ['Aart', 'Huang']:
                self.sa_delta.delete(0, 'end')
                self.sa_delta.insert(0, '0.05')
                self.sa_delta_Label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+9)
                self.sa_delta.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+9)
            else:
                self.sa_delta_Label.grid_forget()
                self.sa_delta.grid_forget()

    def _clear_sa_mapping(self):
        self.sa_init_temp.grid_forget()
        self.sa_init_temp_Label.grid_forget()

        self.sa_stop_temp.grid_forget()
        self.sa_stop_temp_Label.grid_forget()

        self.sa_iterations.grid_forget()
        self.sa_iter_label.grid_forget()

        self.terminationOption.grid_forget()
        self.sa_term_label.grid_forget()

        self.sa_label.grid_forget()
        self.annealing_option.grid_forget()

        self.sa_alpha_Label.grid_forget()
        self.sa_alpha.grid_forget()

        self.sa_log_const_Label.grid_forget()
        self.sa_log_const.grid_forget()

        self.sa_delta_Label.grid_forget()
        self.sa_delta.grid_forget()

        self.max_steady_state_Label.grid_forget()
        self.max_steady_state.grid_forget()

        self.cost_monitor_slope_Label.grid_forget()
        self.cost_monitor_slope.grid_forget()

        self.cost_monitor_Label.grid_forget()
        self.cost_monitor.grid_forget()

        self.markov_num_Label.grid_forget()
        self.markov_num.grid_forget()

        self.markov_temp_step_Label.grid_forget()
        self.markov_temp_step.grid_forget()

    def _fault_injection(self):
        if self.fault_injection.get():
            self.mtbf_label.grid(column=self.fault_starting_col, row=self.fault_starting_row+2)
            self.mtbf.grid(column=self.fault_starting_col+1, row=self.fault_starting_row+2)

            self.sd_mtbf_label.grid(column=self.fault_starting_col, row=self.fault_starting_row+3)
            self.sd_mtbf.grid(column=self.fault_starting_col+1, row=self.fault_starting_row+3)

            self.run_time_label.grid(column=self.fault_starting_col, row=self.fault_starting_row+4)
            self.run_time.grid(column=self.fault_starting_col+1, row=self.fault_starting_row+4)
        else:
            self.mtbf_label.grid_forget()
            self.mtbf.grid_forget()
            self.sd_mtbf_label.grid_forget()
            self.sd_mtbf.grid_forget()
            self.run_time_label.grid_forget()
            self.run_time.grid_forget()

    def _check_for_errors(self):
        if self.mapping.get() == 'Please Select...':
            self.error_message.config(text="Please Select Mapping Algorithm!")
            return False

        elif self.routing_alg.get() == 'Please Select...':
            self.error_message.config(text="Please Select Routing Algorithm!")
            return False

        elif self.routing_type.get() == 'Please Select...':
            if self.routing_alg.get() not in ['XY', 'XYZ']:
                self.error_message.config(text="Please Select Routing Type!")
                return False
            else:
                self.error_message.config(text="")
                return True
        elif self.routing_alg.get() == 'From File':
            if self.routing_browse.get() == 'Routing File Path...':
                self.error_message.config(text="Please Select Routing File!")
                return False
        elif int(self.network_size_z.get()) < 2 and '3D' in self.topology.get():
            if self.vl_placement_enable.get():
                self.error_message.config(text="Can not optimize VL placement for 1 layer NoC")
                return False
        else:
            self.error_message.config(text="")
            return True

    def _on_enter(self, event):
        tkMessageBox.showinfo("License Message", "The logo picture is a derivative of \"Sea Ghost\" by Joey Gannon, " +
                              "used under CC BY-SA. The original version can be found here: " +
                              "https://www.flickr.com/photos/brunkfordbraun/679827214 " +
                              "This work is under same license as the original."
                              "(https://creativecommons.org/licenses/by-sa/2.0/)")

    def _animation_config(self):
        if self.anim_enable.get() is True:
            self.frame_rez_label.grid(column=self.anim_starting_col, row=self.anim_starting_row+2)
            self.frame_rez.grid(column=self.anim_starting_col+1, row=self.anim_starting_row+2)
        else:
            self.frame_rez.grid_forget()
            self.frame_rez_label.grid_forget()

    def _apply_button(self):
        # apply changes...
        if self._check_for_errors():
            # tg Config
            Config.tg.type = self.tg_type.get()
            Config.tg.num_of_tasks = int(self.num_of_tasks.get())
            Config.tg.num_of_critical_tasks = int(self.num_of_crit_tasks.get())
            Config.tg.num_of_edges = int(self.num_of_edge.get())
            Config.tg.wcet_range = int(self.wcet_range.get())
            Config.tg.edge_weight_range = int(self.edge_weight_range.get())
            Config.tg.release_range = int(self.release_range.get())
            if self.tg_type.get() == 'FromDOTFile':
                Config.tg.dot_file_path = self.tg_browse.get()
            # topology config
            Config.ag.topology = self.topology.get()
            Config.ag.x_size = int(self.network_size_x.get())
            Config.ag.y_size = int(self.network_size_y.get())
            Config.ag.z_size = int(self.network_size_z.get())

            # clustering config
            Config.clustering.iterations = int(self.clustering_iterations.get())
            Config.Clustering_Optimization = self.clustering_opt_var.get()
            Config.clustering.cost_function = self.clustering_cost.get()

            # mapping config
            Config.Mapping_CostFunctionType = self.mapping_cost.get()

            Config.LocalSearchIteration = int(self.ls_iter.get())
            Config.IterativeLocalSearchIterations = int(self.ils_iter.get())

            Config.Mapping_Function = self.mapping.get()
            Config.SA_AnnealingSchedule = self.annealing.get()
            Config.TerminationCriteria = self.termination.get()
            Config.SimulatedAnnealingIteration = int(self.sa_iterations.get())
            Config.SA_InitialTemp = int(self.sa_init_temp.get())
            Config.SA_StopTemp = int(self.sa_stop_temp.get())
            Config.SA_Alpha = float(self.sa_alpha.get())
            Config.LogCoolingConstant = int(self.sa_log_const.get())
            Config.CostMonitorQueSize = int(self.cost_monitor.get())
            Config.SlopeRangeForCooling = float(self.cost_monitor_slope.get())
            Config.MaxSteadyState = int(self.max_steady_state.get())
            Config.MarkovTempStep = float(self.markov_temp_step.get())
            Config.MarkovNum = int(self.markov_num.get())
            Config.Delta = float(self.sa_delta.get())

            # Fault Config
            Config.EventDrivenFaultInjection = self.fault_injection.get()
            Config.MTBF = float(self.mtbf.get())
            Config.SD4MTBF = float(self.sd_mtbf.get())
            Config.ProgramRunTime = float(self.run_time.get())

            # Viz Config
            Config.viz.mapping = self.mapping_Draw.get()
            Config.viz.rg = self.rg_draw.get()
            Config.viz.shm = self.shm_draw.get()
            Config.viz.pmcg = self.pmcg_draw.get()
            Config.viz.ttg = self.ttg_draw.get()

            Config.viz.mapping_frames = self.anim_enable.get()
            Config.viz.frame_resolution = int(self.frame_rez.get())

            # Routing
            Config.FlowControl = self.flow_control.get()

            if self.topology.get() == 'From File':
                Config.SetRoutingFromFile = True
                Config.RoutingFilePath = self.routing_browse.get()
            else:
                if '3D' in self.topology.get():
                    if self.routing_alg.get() == 'Negative First':
                        Config.UsedTurnModel = PackageFile.NegativeFirst3D_TurnModel
                    elif self.routing_alg.get() == 'XYZ':
                        Config.UsedTurnModel = PackageFile.XYZ_TurnModel
                elif '2D' in self.topology.get():
                    if self.routing_alg.get() == 'XY':
                        Config.UsedTurnModel = PackageFile.XY_TurnModel
                    elif self.routing_alg.get() == 'West First':
                        Config.UsedTurnModel = PackageFile.WestFirst_TurnModel
                    elif self.routing_alg.get() == 'North Last':
                        Config.UsedTurnModel = PackageFile.NorthLast_TurnModel
                    elif self.routing_alg.get() == 'Negative First':
                        Config.UsedTurnModel = PackageFile.NegativeFirst2D_TurnModel

                if self.routing_alg.get() in ['XY', 'XYZ']:
                    if self.routing_type.get() == 'Please Select...':
                        Config.RotingType = 'MinimalPath'
                else:
                    Config.RotingType = self.routing_type.get()

            # VL Placement

            Config.FindOptimumAG = self.vl_placement_enable.get()
            if self.vl_placement_enable.get():
                Config.vl_opt.vl_opt_alg = self.vlp_alg.get()
                Config.vl_opt.vl_num = int(self.num_of_vls.get())

            # dependability Config
            Config.Communication_SlackCount = int(self.com_slack_number.get())
            Config.Task_SlackCount = int(self.slack_number.get())
            Config.NumberOfRects = int(self.num_of_rects.get())

            # PMC Config
            if self.pmc_enable.get():
                Config.GeneratePMCG = self.pmc_enable.get()
                if self.pmc_type.get() == 'One Step Diagnosable':
                    Config.OneStepDiagnosable = True
                    Config.OneStepDiagnosable = int(self.t_fault_diagnosable.get())
                else:
                    Config.OneStepDiagnosable = False

            self.apply_button = True
            self.destroy()

    def _cancel_button(self):
        self.destroy()