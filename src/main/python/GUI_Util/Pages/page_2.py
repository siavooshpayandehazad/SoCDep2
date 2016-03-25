# Copyright (C) Siavoosh Payandeh Azad
from page_class import Page
import Tkinter as tk
import tkFileDialog
import ttk


class Page2(Page):  # architecture graph

    vlp_alg_list = ['LocalSearch', 'IterativeLocalSearch']

    routing_dict = {'2D': ['XY', 'YX', 'West First', 'North Last', 'Negative First', 'From File'],
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
        self.routing_alg_option.config(width=self.option_menu_width)

        self.routing_type_label = tk.Label(self, text="Routing type:")
        available_routings_types = ['MinimalPath', 'NonMinimalPath']
        self.routing_type = tk.StringVar()
        self.routing_type.set('MinimalPath')
        self.routing_type_option = tk.OptionMenu(self, self.routing_type, *available_routings_types)
        self.routing_type_option.config(width=self.option_menu_width)

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
            self.routing_alg_option = tk.OptionMenu(self, self.routing_alg, *self.routing_dict['2D'],
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