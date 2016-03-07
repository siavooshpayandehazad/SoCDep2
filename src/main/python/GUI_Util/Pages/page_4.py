# Copyright (C) Siavoosh Payandeh Azad
from page_class import Page
import Tkinter as tk
import ttk


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