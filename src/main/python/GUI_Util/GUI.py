# Copyright (C) Siavoosh Payandeh Azad


import Tkinter as tk
import ttk
import tkFileDialog
from PIL import ImageTk, Image
import tkMessageBox
from ConfigAndPackages import Config, PackageFile

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    option_menu_width = 15
    entry_width = 10

    # Task Graph Config
    tg_starting_row = 0
    tg_starting_col = 0

    # Task clustering Config
    cl_opt_start_row = 0
    cl_opt_start_col = 4

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # ---------------------------------------------
        #                   TG
        # ---------------------------------------------
        self.tg_label = tk.Label(self, text="Task Graph Type:")
        self.available_tgs = ['RandomDependent', 'RandomIndependent', 'Manual', 'FromDOTFile']
        self.tg_type = tk.StringVar(self)
        self.tg_type.set('RandomDependent')
        self.tg_type_option = tk.OptionMenu(self, self.tg_type, *self.available_tgs, command=self._tg_type_cont)
        self.tg_type_option.config(width=self.option_menu_width)

        self.num_of_tasks_label = tk.Label(self, text="Number of Tasks:")
        self.num_of_tasks = tk.Entry(self, width=self.entry_width)

        self.num_of_crit_tasks_label = tk.Label(self, text="Number of Critical Tasks:")
        self.num_of_crit_tasks = tk.Entry(self, width=self.entry_width)

        self.num_of_edge_label = tk.Label(self, text="Number TG Edges:")
        self.num_of_edge = tk.Entry(self, width=self.entry_width)

        self.wcet_range_label = tk.Label(self, text="WCET Range:")
        self.wcet_range = tk.Entry(self, width=self.entry_width)

        self.edge_weight_range_label = tk.Label(self, text="Edge Weight Range:")
        self.edge_weight_range = tk.Entry(self, width=self.entry_width)

        self.release_range_label = tk.Label(self, text="Task Release Range:")
        self.release_range = tk.Entry(self, width=self.entry_width)

        self.tg_browse = tk.Entry(self, bg='gray')
        self.tg_browse.insert(0, "TG File Path...")

        self.tg_browse_button = tk.Button(self, text="Browse", command=self._get_tg_file)
        tk.Label(self, text="Task Graph Settings", font="-weight bold").grid(column=self.tg_starting_col,
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

        ttk.Separator(self, orient='vertical').grid(column=self.tg_starting_col+3,
                                                    row=self.tg_starting_row, rowspan=12, sticky="ns")
        # ---------------------------------------------
        #                   Clustering
        # ---------------------------------------------
        self.clustering_opt_var = tk.BooleanVar(self)
        self.clustering_opt_enable = tk.Checkbutton(self, text="Clustering Optimization",
                                                    variable=self.clustering_opt_var,
                                                    command=self._clustering_cont)
        self.clustering_iter_label = tk.Label(self, text="Clustering Iterations:")
        self.clustering_iterations = tk.Entry(self, width=self.entry_width)

        self.clustering_cost_label = tk.Label(self, text="Cost Function Type:")
        available_costs = ['SD', 'SD+MAX', 'MAX', 'SUMCOM', 'AVGUTIL', 'MAXCOM']
        self.clustering_cost = tk.StringVar(self)
        self.clustering_cost.set('SD+MAX')
        self.clustering_costOpt = tk.OptionMenu(self, self.clustering_cost, *available_costs)
        self.clustering_costOpt.config(width=self.option_menu_width)

        tk.Label(self, text="Clustering Settings", font="-weight bold").grid(column=self.cl_opt_start_col,
                                                                             row=self.cl_opt_start_row,
                                                                             columnspan=2)
        self.clustering_opt_var.set('False')
        self.clustering_iterations.insert(0, '1000')
        self.clustering_opt_enable.grid(column=self.cl_opt_start_col, row=self.cl_opt_start_row+1)

    def _get_tg_file(self):
        path = tkFileDialog.askopenfilename()
        if path:
            self.tg_browse.delete(0, 'end')
            self.tg_browse.insert(1, path)

    def _tg_type_cont(self, tg_type):
        if tg_type == 'RandomDependent':

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


class Page2(Page):  # architecture graph

    vlp_alg_list = ['LocalSearch', 'IterativeLocalSearch']

    routing_dict = {'2D': ['XY', 'West First', 'North Last', 'Negative First', 'From File'],
                    '3D': ['XYZ', 'Negative First', 'From File']}

    flow_control_list = ['Wormhole', 'StoreAndForward']
    # Architecture Graph Config
    topology_starting_row = 0
    topology_starting_col = 0

    # vertical Link placement optimization
    vl_placement_starting_row = 0
    vl_placement_starting_col = 4

    # Routing Config
    routing_starting_row = 8
    routing_starting_col = 0

    option_menu_width = 15
    entry_width = 10

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # ---------------------------------------------
        #                   topology
        # ---------------------------------------------
        self.topology_label = tk.Label(self, text="Topology:")
        available_topologies = ['2DTorus', '2DMesh', '2DLine', '2DRing', '3DMesh']
        self.topology = tk.StringVar()
        self.topology_option = tk.OptionMenu(self, self.topology, *available_topologies,
                                             command=self.network_size_cont)
        self.topology_option.config(width=self.option_menu_width)

        self.network_size_x = tk.Spinbox(self, from_=1, to=10, width=self.entry_width)
        self.network_size_y = tk.Spinbox(self, from_=1, to=10, width=self.entry_width)
        self.network_size_z = tk.Spinbox(self, from_=1, to=10, width=self.entry_width)

        tk.Label(self, text="Topology Config", font="-weight bold").grid(column=0, row=0, columnspan=2)
        self.topology.set('2DMesh')
        self.topology_label.grid(column=self.topology_starting_col, row=self.topology_starting_row+1)
        self.topology_option.grid(column=self.topology_starting_col+1, row=self.topology_starting_row+1, sticky='w')

        x_size_label = tk.Label(self, text="X Size:")
        y_size_label = tk.Label(self, text="Y Size:")
        z_size_label = tk.Label(self, text="Z Size:")

        self.network_size_x.delete(0, 'end')
        self.network_size_x.insert(0, 3)
        self.network_size_y.delete(0, 'end')
        self.network_size_y.insert(0, 3)
        self.network_size_z.delete(0, 'end')
        self.network_size_z.insert(0, 1)

        x_size_label.grid(column=self.topology_starting_col, row=self.topology_starting_row+2)
        self.network_size_x.grid(column=self.topology_starting_col+1, row=self.topology_starting_row+2, sticky='w')
        y_size_label.grid(column=self.topology_starting_col, row=3)
        self.network_size_y.grid(column=self.topology_starting_col+1, row=self.topology_starting_row+3, sticky='w')
        z_size_label.grid(column=self.topology_starting_col, row=4)
        self.network_size_z.grid(column=self.topology_starting_col+1, row=self.topology_starting_row+4, sticky='w')
        self.network_size_z.config(state='disabled')
        ttk.Separator(self, orient='horizontal').grid(column=self.topology_starting_col,
                                                      row=self.topology_starting_row+6, columnspan=2, sticky="ew")

        ttk.Separator(self, orient='vertical').grid(column=self.topology_starting_col+2,
                                                    row=self.topology_starting_row+1, rowspan=12, sticky="ns")
        # ----------------------------------------
        #           Vertical Link Placement
        # ----------------------------------------
        self.vl_placement_enable = tk.BooleanVar(self)
        self.vl_placement_enable.set('False')
        self.vl_placement_enable_box = tk.Checkbutton(self, text="Enable VL Placement Optimization",
                                                      variable=self.vl_placement_enable,
                                                      command=self._vl_placement_func)

        self.vlp_alg_label = tk.Label(self, text="Opt algorithm:")
        self.vlp_alg = tk.StringVar()
        self.vlp_alg.set('LocalSearch')
        self.vlp_alg_option = tk.OptionMenu(self, self.vlp_alg, *self.vlp_alg_list, command=self._vlp_alg_func)
        self.vlp_alg_option.config(width=15)

        self.num_of_vls_label = tk.Label(self, text="Number of VLs:")
        self.num_of_vls = tk.Entry(self, width=10)

        self.vlp_iter_ls_label = tk.Label(self, text="LS Iterations:")
        self.vlp_iter_ls = tk.Entry(self, width=10)

        self.vlp_iter_ils_label = tk.Label(self, text="ILS Iterations:")
        self.vlp_iter_ils = tk.Entry(self, width=10)

        tk.Label(self, text="Vertical Link Placement Optimization",
                 font="-weight bold").grid(column=self.vl_placement_starting_col,
                                           row=self.vl_placement_starting_row, columnspan=2)

        self.vl_placement_enable_box.grid(column=self.vl_placement_starting_col,
                                          row=self.vl_placement_starting_row+1, columnspan=2,  sticky="ew")
        self.vl_placement_enable_box.config(state='disable')

        # ---------------------------------------------
        #                   Routing
        # ---------------------------------------------
        self.routing_label = tk.Label(self, text="Routing Algorithm:")
        available_routings = self.routing_dict['2D']
        self.routing_alg = tk.StringVar()
        self.routing_alg.set(self.routing_dict['2D'][0])
        self.routing_alg_option = tk.OptionMenu(self, self.routing_alg, *available_routings,
                                                command=self._routing_func)
        self.routing_alg_option.config(width=10)

        self.routing_type_label = tk.Label(self, text="Routing type:")
        available_routings_types = ['MinimalPath', 'NonMinimalPath']
        self.routing_type = tk.StringVar()
        self.routing_type.set('MinimalPath')
        self.routing_type_option = tk.OptionMenu(self, self.routing_type, *available_routings_types)
        self.routing_type_option.config(width=15)

        self.routing_browse = tk.Entry(self, bg='gray')
        self.routing_browse.insert(0, "Routing File Path...")

        self.routing_browse_button = tk.Button(self, text="Browse", command=self._get_routing_file)

        self.flow_control_label = tk.Label(self, text="Flow Control:")
        available_flow_controls = self.flow_control_list
        self.flow_control = tk.StringVar()
        self.flow_control.set(self.flow_control_list[0])
        self.flow_control_option = tk.OptionMenu(self, self.flow_control, *available_flow_controls,
                                                 command=self._routing_func)

        tk.Label(self, text="Routing Settings", font="-weight bold").grid(column=self.routing_starting_col,
                                                                          row=self.routing_starting_row, columnspan=2)
        self.routing_label.grid(column=self.routing_starting_col, row=self.routing_starting_row+1)
        self.routing_alg_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+1)

        self.routing_type_label.grid(column=self.routing_starting_col, row=self.routing_starting_row+2)
        self.routing_type_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+2)
        self.routing_type_option.config(state='disable')

        self.flow_control_label.grid(column=self.routing_starting_col, row=self.routing_starting_row+4)
        self.flow_control_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+4)
        self.flow_control_option.config(state='normal')

    def network_size_cont(self, topology):
        if '3D' in topology:
            self.network_size_z.config(state='normal')
            self.vl_placement_enable_box.config(state='normal')

            self.routing_alg_option.grid_forget()

            del self.routing_alg_option
            self.routing_alg.set('Please Select...')
            self.routing_alg_option = tk.OptionMenu(self, self.routing_alg, *self.routing_dict['3D'],
                                                    command=self._routing_func)
            self.routing_alg_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+1)
            self.routing_alg_option.config(width=10)

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
            self.routing_alg_option = tk.OptionMenu(self, self.routing_alg, *self.routing_dict['2D'],
                                                    command=self._routing_func)
            self.routing_alg_option.grid(column=self.routing_starting_col+1, row=self.routing_starting_row+1)
            self.routing_alg_option.config(width=10)

            self.routing_type.set("Please Select...")
            self.routing_type_option.config(state='disable')
            self.routing_browse.grid_forget()
            self.routing_browse_button.grid_forget()

            self.network_size_z.delete(0, 'end')
            self.network_size_z.insert(0, 1)
            self.network_size_z.config(state='disabled')

    def _vlp_alg_func(self, event):
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

    def _get_routing_file(self):
        path = tkFileDialog.askopenfilename()
        if path:
            self.routing_browse.delete(0, 'end')
            self.routing_browse.insert(1, path)


class Page3(Page):
    # Mapping Algorithm Config
    mapping_opt_start_row = 0
    mapping_opt_start_col = 0
    mapping_dict = {'Manual': ['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing', 'NMap', 'MinMin',
                               'MaxMin', 'MinExecutionTime', 'MinimumCompletionTime'],
                    'RandomDependent': ['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing', 'NMap'],
                    'RandomIndependent': ['MinMin', 'MaxMin', 'MinExecutionTime', 'MinimumCompletionTime']}
    option_menu_width = 15
    entry_width = 10

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        # ---------------------------------------------
        #                   Mapping
        # ---------------------------------------------
        self.mapping_label = tk.Label(self, text="Mapping Algorithm:")
        self.mapping = tk.StringVar(self)
        self.mapping.set('LocalSearch')
        self.mapping_option = tk.OptionMenu(self, self.mapping, *self.mapping_dict['Manual'],
                                            command=self._mapping_alg_cont)
        self.mapping_option.config(width=self.option_menu_width)

        self.mapping_cost_label = tk.Label(self, text="Cost Function Type:")
        available_mapping_costs = ['SD', 'SD+MAX', 'MAX', 'CONSTANT']
        self.mapping_cost = tk.StringVar(self)
        self.mapping_cost.set('SD+MAX')
        self.mapping_cost_opt = tk.OptionMenu(self, self.mapping_cost, *available_mapping_costs)
        self.mapping_cost_opt.config(width=self.option_menu_width)

        # ---------------------------------------------
        #           Local Search
        # ---------------------------------------------
        self.ls_iter_label = tk.Label(self, text="LS Iterations:")
        self.ls_iter = tk.Entry(self, width=self.entry_width)
        self.ls_iter.insert(0, '100')

        self.ils_iter_label = tk.Label(self, text="ILS Iterations:")
        self.ils_iter = tk.Entry(self, width=self.entry_width)
        self.ils_iter.insert(0, '10')

        # ---------------------------------------------
        #           Simulated Annealing
        # ---------------------------------------------
        self.sa_label = tk.Label(self, text="Annealing Schedule:")
        available_annealing = ['Linear', 'Exponential', 'Adaptive', 'Markov', 'Logarithmic', 'Aart', 'Huang']
        self.annealing = tk.StringVar()
        self.annealing.set('Linear')
        self.annealing_option = tk.OptionMenu(self, self.annealing,
                                              *available_annealing, command=self._annealing_termination)
        self.annealing_option.config(width=self.option_menu_width)

        self.sa_term_label = tk.Label(self, text="Termination Criteria:")
        available_termination = ['StopTemp', 'IterationNum']
        self.termination = tk.StringVar()
        self.termination.set('StopTemp')
        self.terminationOption = tk.OptionMenu(self, self.termination,
                                               *available_termination, command=self._annealing_termination)
        self.terminationOption.config(width=self.option_menu_width)

        self.sa_iter_label = tk.Label(self, text="Number of Iterations:")
        self.sa_iterations = tk.Entry(self, width=self.entry_width)
        self.sa_iterations.insert(0, '100000')

        self.sa_init_temp_Label = tk.Label(self, text="Initial Temperature:")
        self.sa_init_temp = tk.Entry(self, width=self.entry_width)
        self.sa_init_temp.insert(0, '100')

        self.sa_stop_temp_Label = tk.Label(self, text="Stop Temperature:")
        self.sa_stop_temp = tk.Entry(self, width=self.entry_width)
        self.sa_stop_temp.insert(0, '5')

        self.sa_alpha_Label = tk.Label(self, text="Cooling ratio:")
        self.sa_alpha = tk.Entry(self, width=self.entry_width)
        self.sa_alpha.insert(0, '0.999')

        self.sa_log_const_Label = tk.Label(self, text="Log cooling constant:")
        self.sa_log_const = tk.Entry(self, width=self.entry_width)
        self.sa_log_const.insert(0, '1000')

        self.cost_monitor_Label = tk.Label(self, text="Cost Monitor Queue Size:")
        self.cost_monitor = tk.Entry(self, width=self.entry_width)
        self.cost_monitor.insert(0, '2000')

        self.cost_monitor_slope_Label = tk.Label(self, text="Slope Range For Cooling:")
        self.cost_monitor_slope = tk.Entry(self, width=self.entry_width)
        self.cost_monitor_slope.insert(0, '0.02')

        self.max_steady_state_Label = tk.Label(self, text="Max steps/no improvement:")
        self.max_steady_state = tk.Entry(self, width=self.entry_width)
        self.max_steady_state.insert(0, '30000')

        self.markov_num_Label = tk.Label(self, text="Length of Markov Chain:")
        self.markov_num = tk.Entry(self, width=self.entry_width)
        self.markov_num.insert(0, '2000')

        self.markov_temp_step_Label = tk.Label(self, text="Temperature step:")
        self.markov_temp_step = tk.Entry(self, width=self.entry_width)
        self.markov_temp_step.insert(0, '1')

        self.sa_delta_Label = tk.Label(self, text="Delta:")
        self.sa_delta = tk.Entry(self, width=self.entry_width)
        self.sa_delta.insert(0, '0.05')

        tk.Label(self, text="Mapping Settings", font="-weight bold").grid(column=self.mapping_opt_start_col,
                                                                          row=self.mapping_opt_start_row,
                                                                          columnspan=2)
        self.mapping_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+1)
        self.mapping_option.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+1)

        self.mapping_cost_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+2)
        self.mapping_cost_opt.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+2)

        self.ls_iter_label.grid(column=self.mapping_opt_start_col, row=self.mapping_opt_start_row+3)
        self.ls_iter.grid(column=self.mapping_opt_start_col+1, row=self.mapping_opt_start_row+3)

    def _mapping_alg_cont(self, event):
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

    def _annealing_termination(self, event):
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

    def _clear_mapping(self):
        self._clear_sa_mapping()
        self.ls_iter_label.grid_forget()
        self.ls_iter.grid_forget()
        self.ils_iter_label.grid_forget()
        self.ils_iter.grid_forget()
        self.mapping_cost_label.grid_forget()
        self.mapping_cost_opt.grid_forget()


class Page4(Page):      # testing
    # PMC Config
    pmc_starting_row = 0
    pmc_starting_col = 4

    # Dependability Config
    dependability_starting_row = 0
    dependability_starting_col = 0

    # Fault Handling
    fault_starting_row = 5
    fault_starting_col = 0

    option_menu_width = 15
    entry_width = 10

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # ----------------------------------------
        #           Dependability section
        # ----------------------------------------
        self.slack_number_label = tk.Label(self, text="Task Slack Count:")
        self.slack_number = tk.Spinbox(self, from_=0, to=10, width=self.entry_width)

        self.com_slack_number_label = tk.Label(self, text="Com. Slack Count:")
        self.com_slack_number = tk.Spinbox(self, from_=0, to=10, width=self.entry_width)

        self.num_of_rects_label = tk.Label(self, text="NoCDepend Rectangle #:")
        self.num_of_rects = tk.Spinbox(self, from_=1, to=10, width=self.entry_width)
        self.num_of_rects.delete(0, 'end')
        self.num_of_rects.insert(0, 3)

        self.error_message = tk.Label(self, text="", font="-weight bold", fg="red")

        # ----------------------------------------
        #           PMC config
        # ----------------------------------------
        self.pmc_enable = tk.BooleanVar(self)
        self.pmc_enable.set('False')
        self.pmc_enable_check_box = tk.Checkbutton(self, text="Enable PMC config",
                                                   variable=self.pmc_enable, command=self._pmc_func)

        self.pmc_type_label = tk.Label(self, text="PMC Model:")
        self.available_pmc_types = ['Sequentially diagnosable', 'One Step Diagnosable']
        self.pmc_type = tk.StringVar(self)
        self.pmc_type.set('Sequentially diagnosable')
        self.pmc_type_opt = tk.OptionMenu(self, self.pmc_type, *self.available_pmc_types,
                                          command=self._t_fault_control)
        self.pmc_type_opt.config(width=self.option_menu_width)

        self.t_fault_diagnosable_label = tk.Label(self, text="T-Fault Diagnosable:")
        self.t_fault_diagnosable = tk.Entry(self, width=self.entry_width)

        self.error_message = tk.Label(self, text="", font="-weight bold", fg="red")
        # ----------------------------------------
        #           Dependability section
        # ----------------------------------------
        tk.Label(self, text="Dependability Config",
                 font="-weight bold").grid(column=self.dependability_starting_col,
                                           row=self.dependability_starting_row, columnspan=2)
        self.slack_number_label.grid(column=self.dependability_starting_col, row=self.dependability_starting_row+1)
        self.slack_number.grid(column=self.dependability_starting_col+1, row=self.dependability_starting_row+1)

        self.com_slack_number_label.grid(column=self.dependability_starting_col, row=self.dependability_starting_row+2)
        self.com_slack_number.grid(column=self.dependability_starting_col+1, row=self.dependability_starting_row+2)

        self.num_of_rects_label.grid(column=self.dependability_starting_col, row=self.dependability_starting_row+3)
        self.num_of_rects.grid(column=self.dependability_starting_col+1, row=self.dependability_starting_row+3)

        ttk.Separator(self, orient='vertical').grid(column=self.dependability_starting_col+3,
                                                    row=self.dependability_starting_row+1, rowspan=6, sticky="ns")
        ttk.Separator(self, orient='horizontal').grid(column=self.dependability_starting_col,
                                                      row=self.dependability_starting_row+4, columnspan=2, sticky="ew")
        # ---------------------------------------------
        #               Fault Injection
        # ---------------------------------------------
        self.fault_injection = tk.BooleanVar(self)
        self.fault_injection_enable = tk.Checkbutton(self, text="Event Driven Fault Injection",
                                                     variable=self.fault_injection,
                                                     command=self._fault_injection)

        self.mtbf_label = tk.Label(self, text="MTBF (sec):")
        self.mtbf = tk.Entry(self, width=self.entry_width)
        self.mtbf.insert(0, '2')

        self.sd_mtbf_label = tk.Label(self, text="TBF's Standard Deviation:")
        self.sd_mtbf = tk.Entry(self, width=self.entry_width)
        self.sd_mtbf.insert(0, '0.1')

        self.run_time_label = tk.Label(self, text="Program RunTime:")
        self.run_time = tk.Entry(self, width=self.entry_width)
        self.run_time.insert(0, '10')
        # ----------------------------------------
        #           PMC Graph
        # ----------------------------------------
        tk.Label(self, text="PMC Config", font="-weight bold").grid(column=self.pmc_starting_col,
                                                                    row=self.pmc_starting_row, columnspan=2)

        self.pmc_enable_check_box.grid(column=self.pmc_starting_col, row=self.pmc_starting_row+1, sticky='w')

        # ----------------------------------------
        #               Fault
        # ----------------------------------------
        tk.Label(self, text="Fault Settings", font="-weight bold").grid(column=self.fault_starting_col,
                                                                        row=self.fault_starting_row,
                                                                        columnspan=2)
        self.fault_injection.set('False')
        self.fault_injection_enable.grid(column=self.fault_starting_col, row=self.fault_starting_row+1)

    def _pmc_func(self):
        if self.pmc_enable.get():
            self.pmc_type_label.grid(column=self.pmc_starting_col, row=self.pmc_starting_row+2, sticky='w')
            self.pmc_type_opt.grid(column=self.pmc_starting_col+1, row=self.pmc_starting_row+2, sticky='w')
        else:
            self.pmc_type_label.grid_forget()
            self.pmc_type_opt.grid_forget()

    def _t_fault_control(self, event):
        if self.pmc_type.get() == 'One Step Diagnosable':
            self.t_fault_diagnosable_label.grid(column=self.pmc_starting_col, row=self.pmc_starting_row+3, sticky='w')
            self.t_fault_diagnosable.grid(column=self.pmc_starting_col+1, row=self.pmc_starting_row+3, sticky='w')
        else:
            self.t_fault_diagnosable_label.grid_forget()
            self.t_fault_diagnosable.grid_forget()

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


class Page5(Page):      # visualization

    # visualization
    viz_starting_row = 0
    viz_starting_col = 0

    # Animation Frame generation
    anim_starting_row = 0
    anim_starting_col = 4

    option_menu_width = 15
    entry_width = 10

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.all_viz = tk.BooleanVar(self)
        self.all_viz.set('False')
        all_viz_enable = tk.Checkbutton(self, text="Check/Un-check all reports",
                                        variable=self.all_viz, command=self._all_viz_func,
                                        wraplength=100)

        self.rg_draw = tk.BooleanVar(self)
        self.rg_draw.set('False')
        rg_draw_enable = tk.Checkbutton(self, text="Routing Graph", variable=self.rg_draw)

        self.shm_draw = tk.BooleanVar(self)
        self.shm_draw.set('False')
        shm_draw_enable = tk.Checkbutton(self, text="System Health Map", variable=self.shm_draw)

        self.mapping_Draw = tk.BooleanVar(self)
        self.mapping_Draw.set('False')
        mapping_draw_enable = tk.Checkbutton(self, text="Mapping Report", variable=self.mapping_Draw)

        self.pmcg_draw = tk.BooleanVar(self)
        self.pmcg_draw.set('False')
        pmcg_draw_enable = tk.Checkbutton(self, text="PMCG Report", variable=self.pmcg_draw)

        self.ttg_draw = tk.BooleanVar(self)
        self.ttg_draw.set('False')
        ttg_draw_enable = tk.Checkbutton(self, text="TTG Report", variable=self.ttg_draw)

        label = tk.Label(self, text="Visualization Config", font="-weight bold")
        label.grid(column=self.viz_starting_col, row=self.viz_starting_row, columnspan=2)
        all_viz_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+1, columnspan=1, sticky='w')

        shm_draw_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+2, sticky='W')
        rg_draw_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+3, sticky='W')
        mapping_draw_enable.grid(column=self.viz_starting_col, row=self.viz_starting_row+4, sticky='W')
        pmcg_draw_enable.grid(column=self.viz_starting_col+1, row=self.viz_starting_row+3, sticky='W')
        ttg_draw_enable.grid(column=self.viz_starting_col+1, row=self.viz_starting_row+4, sticky='W')
        ttk.Separator(self, orient='vertical').grid(column=self.viz_starting_col+3,
                                                    row=self.viz_starting_row+1, rowspan=4, sticky="ns")

        # ---------------------------------------------
        #               Anim
        # ---------------------------------------------
        self.anim_enable = tk.BooleanVar(self)
        self.anim_enable.set('False')
        self.anim_enableBox = tk.Checkbutton(self, text="Generate Animation Frames",
                                             variable=self.anim_enable, command=self._animation_config)

        self.frame_rez_label = tk.Label(self, text="Frame Resolution(dpi):")
        self.frame_rez = tk.Entry(self, width=self.entry_width)
        self.frame_rez.insert(0, '20')

        tk.Label(self, text="Animation Frames Config", font="-weight bold").grid(column=self.anim_starting_col,
                                                                                 row=self.anim_starting_row,
                                                                                 columnspan=2)

        self.anim_enableBox.grid(column=self.anim_starting_col, row=self.anim_starting_row+1,
                                 sticky='W')

    def _animation_config(self):
        if self.anim_enable.get() is True:
            self.frame_rez_label.grid(column=self.anim_starting_col, row=self.anim_starting_row+2)
            self.frame_rez.grid(column=self.anim_starting_col+1, row=self.anim_starting_row+2)
        else:
            self.frame_rez.grid_forget()
            self.frame_rez_label.grid_forget()

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


class MainView(tk.Tk):
    apply_button = False

    def __init__(self, parent):

        tk.Tk.__init__(self, parent)
        self.parent = parent

        self.p1 = Page1(self)
        self.p2 = Page2(self)
        self.p3 = Page3(self)
        self.p4 = Page4(self)
        self.p5 = Page5(self)

        logo_frame = tk.Frame(self)
        tab_frame = tk.Frame(self)
        container = tk.Frame(self, width=700, height=300)
        action_frame = tk.Frame(self)
        logo_frame.grid(column=0, row=0,  sticky='w' )
        tab_frame.grid(column=0, row=1,  sticky='w')
        container.grid(column=0, row=3, sticky='w')
        action_frame.grid(column=0, row=4, sticky='w')

        img = ImageTk.PhotoImage(Image.open("GUI_Util/Jelly.png"))
        # This work, "Jelly.png", is a derivative of "Sea Ghost" by Joey Gannon,
        # used under CC BY-SA.  The original version can be found here:
        # https://www.flickr.com/photos/brunkfordbraun/679827214
        # This work is under same license as the original
        logo = tk.Label(logo_frame, text="", image=img)
        logo.bind("<Enter>", self._on_enter)
        logo.image = img

        label = tk.Label(logo_frame, text="Schedule and Depend Configuration GUI")
        logo.grid(column=0, row=0, columnspan=1, sticky='w')
        label.grid(column=1, row=0, columnspan=3 )

        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.b1 = tk.Button(tab_frame, text="Task Graph", command=lambda: self.button_command(1))
        self.b2 = tk.Button(tab_frame, text="Arch Graph", command=lambda: self.button_command(2))
        self.b3 = tk.Button(tab_frame, text="Mapping", command=lambda: self.button_command(3))
        self.b4 = tk.Button(tab_frame, text="Dependability & Testing", command=lambda: self.button_command(4))
        self.b5 = tk.Button(tab_frame, text="Visualizations", command=lambda: self.button_command(5))

        self.b1.grid(column=0, row=1, columnspan=1, sticky='w')
        self.b2.grid(column=1, row=1, columnspan=1, sticky='w')
        self.b3.grid(column=2, row=1, columnspan=1, sticky='w')
        self.b4.grid(column=3, row=1, columnspan=1, sticky='w')
        self.b5.grid(column=4, row=1, columnspan=1, sticky='w')
        ttk.Separator(self, orient='horizontal').grid(column=0, row=2, columnspan=4, sticky="ew")

        self.error_message = tk.Label(action_frame, text="", font="-weight bold", fg="red")
        apply_button = tk.Button(action_frame, text="Apply", command=self._apply_button)
        cancel_button = tk.Button(action_frame, text="Cancel", command=self._cancel_button)

        self.error_message.grid(column=0, row=0, columnspan=5)
        apply_button.grid(column=1, row=1, columnspan=2, sticky='w')
        cancel_button.grid(column=3, row=1, columnspan=2, sticky='w')

        self.p1.show()

    def _on_enter(self, event):
        tkMessageBox.showinfo("License Message", "The logo picture is a derivative of \"Sea Ghost\" by Joey Gannon, " +
                              "used under CC BY-SA. The original version can be found here: " +
                              "https://www.flickr.com/photos/brunkfordbraun/679827214 " +
                              "This work is under same license as the original."
                              "(https://creativecommons.org/licenses/by-sa/2.0/)")

    def _cancel_button(self):
        self.destroy()

    def button_command(self, button_number):

        self.b1.configure(relief='raised')
        self.b2.configure(relief='raised')
        self.b3.configure(relief='raised')
        self.b4.configure(relief='raised')
        self.b5.configure(relief='raised')

        if button_number == 1:
            self.p1.lift()
            self.b1.configure(relief='sunken')
        elif button_number == 2:
            self.p2.lift()
            self.b2.configure(relief='sunken')
        elif button_number == 3:
            self.p3.lift()
            self.b3.configure(relief='sunken')
        elif button_number == 4:
            self.p4.lift()
            self.b4.configure(relief='sunken')
        elif button_number == 5:
            self.p5.lift()
            self.b5.configure(relief='sunken')

    def _check_for_errors(self):
        if self.p3.mapping.get() == 'Please Select...':
            self.error_message.config(text="Please Select Mapping Algorithm!")
            return False

        elif self.p2.routing_alg.get() == 'Please Select...':
            self.error_message.config(text="Please Select Routing Algorithm!")
            return False

        elif self.p2.routing_type.get() == 'Please Select...':
            if self.p2.routing_alg.get() not in ['XY', 'XYZ']:
                self.error_message.config(text="Please Select Routing Type!")
                return False
            else:
                self.error_message.config(text="")
                return True
        elif self.p2.routing_alg.get() == 'From File':
            if self.p2.routing_browse.get() == 'Routing File Path...':
                self.error_message.config(text="Please Select Routing File!")
                return False
        elif int(self.p2.network_size_z.get()) < 2 and '3D' in self.p2.topology.get():
            if self.p2.vl_placement_enable.get():
                self.error_message.config(text="Can not optimize VL placement for 1 layer NoC")
                return False
        else:
            self.error_message.config(text="")
            return True

    def _apply_button(self):
        if self._check_for_errors():
            # tg Config
            Config.tg.type = self.p1.tg_type.get()
            Config.tg.num_of_tasks = int(self.p1.num_of_tasks.get())
            Config.tg.num_of_critical_tasks = int(self.p1.num_of_crit_tasks.get())
            Config.tg.num_of_edges = int(self.p1.num_of_edge.get())
            Config.tg.wcet_range = int(self.p1.wcet_range.get())
            Config.tg.edge_weight_range = int(self.p1.edge_weight_range.get())
            Config.tg.release_range = int(self.p1.release_range.get())
            if self.p1.tg_type.get() == 'FromDOTFile':
                Config.tg.dot_file_path = self.p1.tg_browse.get()
            # topology config
            Config.ag.topology = self.p2.topology.get()
            Config.ag.x_size = int(self.p2.network_size_x.get())
            Config.ag.y_size = int(self.p2.network_size_y.get())
            Config.ag.z_size = int(self.p2.network_size_z.get())

            # clustering config
            Config.clustering.iterations = int(self.p1.clustering_iterations.get())
            Config.Clustering_Optimization = self.p1.clustering_opt_var.get()
            Config.clustering.cost_function = self.p1.clustering_cost.get()

            # mapping config
            Config.Mapping_CostFunctionType = self.p3.mapping_cost.get()

            Config.LocalSearchIteration = int(self.p3.ls_iter.get())
            Config.IterativeLocalSearchIterations = int(self.p3.ils_iter.get())

            Config.Mapping_Function = self.p3.mapping.get()
            Config.SA_AnnealingSchedule = self.p3.annealing.get()
            Config.TerminationCriteria = self.p3.termination.get()
            Config.SimulatedAnnealingIteration = int(self.p3.sa_iterations.get())
            Config.SA_InitialTemp = int(self.p3.sa_init_temp.get())
            Config.SA_StopTemp = int(self.p3.sa_stop_temp.get())
            Config.SA_Alpha = float(self.p3.sa_alpha.get())
            Config.LogCoolingConstant = int(self.p3.sa_log_const.get())
            Config.CostMonitorQueSize = int(self.p3.cost_monitor.get())
            Config.SlopeRangeForCooling = float(self.p3.cost_monitor_slope.get())
            Config.MaxSteadyState = int(self.p3.max_steady_state.get())
            Config.MarkovTempStep = float(self.p3.markov_temp_step.get())
            Config.MarkovNum = int(self.p3.markov_num.get())
            Config.Delta = float(self.p3.sa_delta.get())

            # Fault Config
            Config.EventDrivenFaultInjection = self.p4.fault_injection.get()
            Config.MTBF = float(self.p4.mtbf.get())
            Config.SD4MTBF = float(self.p4.sd_mtbf.get())
            Config.ProgramRunTime = float(self.p4.run_time.get())

            # Viz Config
            Config.Mapping_Drawing = self.p5.mapping_Draw.get()
            Config.RG_Draw = self.p5.rg_draw.get()
            Config.SHM_Drawing = self.p5.shm_draw.get()
            Config.PMCG_Drawing = self.p5.pmcg_draw.get()
            Config.TTG_Drawing = self.p5.ttg_draw.get()

            Config.GenMappingFrames = self.p5.anim_enable.get()
            Config.FrameResolution = int(self.p5.frame_rez.get())

            # Routing
            Config.FlowControl = self.p2.flow_control.get()

            if self.p2.topology.get() == 'From File':
                Config.SetRoutingFromFile = True
                Config.RoutingFilePath = self.p2.routing_browse.get()
            else:
                if '3D' in self.p2.topology.get():
                    if self.p2.routing_alg.get() == 'Negative First':
                        Config.UsedTurnModel = PackageFile.NegativeFirst3D_TurnModel
                    elif self.p2.routing_alg.get() == 'XYZ':
                        Config.UsedTurnModel = PackageFile.XYZ_TurnModel
                elif '2D' in self.p2.topology.get():
                    if self.p2.routing_alg.get() == 'XY':
                        Config.UsedTurnModel = PackageFile.XY_TurnModel
                    elif self.p2.routing_alg.get() == 'West First':
                        Config.UsedTurnModel = PackageFile.WestFirst_TurnModel
                    elif self.p2.routing_alg.get() == 'North Last':
                        Config.UsedTurnModel = PackageFile.NorthLast_TurnModel
                    elif self.p2.routing_alg.get() == 'Negative First':
                        Config.UsedTurnModel = PackageFile.NegativeFirst2D_TurnModel

                if self.p2.routing_alg.get() in ['XY', 'XYZ']:
                    if self.p2.routing_type.get() == 'Please Select...':
                        Config.RotingType = 'MinimalPath'
                else:
                    Config.RotingType = self.p2.routing_type.get()

            # VL Placement
            # todo: There is something with update from 3D to 2D system.
            Config.FindOptimumAG = self.p2.vl_placement_enable.get()
            if self.p2.vl_placement_enable.get():
                Config.vl_opt.vl_opt_alg = self.p2.vlp_alg.get()
                Config.vl_opt.vl_num = int(self.p2.num_of_vls.get())

            # dependability Config
            Config.Communication_SlackCount = int(self.p4.com_slack_number.get())
            Config.Task_SlackCount = int(self.p4.slack_number.get())
            Config.NumberOfRects = int(self.p4.num_of_rects.get())

            # PMC Config
            if self.p4.pmc_enable.get():
                Config.GeneratePMCG = self.p4.pmc_enable.get()
                if self.p4.pmc_type.get() == 'One Step Diagnosable':
                    Config.OneStepDiagnosable = True
                    Config.OneStepDiagnosable = int(self.p4.t_fault_diagnosable.get())
                else:
                    Config.OneStepDiagnosable = False

            self.apply_button = True
            self.destroy()
