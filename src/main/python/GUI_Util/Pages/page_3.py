# Copyright (C) Siavoosh Payandeh Azad
from page_class import Page
import Tkinter as tk


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