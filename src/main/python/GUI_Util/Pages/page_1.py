# Copyright (C) Siavoosh Payandeh Azad
from page_class import Page
import Tkinter as tk
import ttk
import tkFileDialog


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