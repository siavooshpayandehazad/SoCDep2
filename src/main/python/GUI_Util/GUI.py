# Copyright (C) Siavoosh Payandeh Azad

from Pages import page_1, page_2, page_3, page_4, page_5
import Tkinter as tk
from PIL import ImageTk, Image
import tkMessageBox
from ConfigAndPackages import Config, PackageFile
import ttk


class MainView(tk.Tk):
    apply_button = False

    def __init__(self, parent):

        tk.Tk.__init__(self, parent)
        self.parent = parent

        self.p1 = page_1.Page1(self)
        self.p2 = page_2.Page2(self)
        self.p3 = page_3.Page3(self)
        self.p4 = page_4.Page4(self)
        self.p5 = page_5.Page5(self)

        logo_frame = tk.Frame(self)
        tab_frame = tk.Frame(self)
        container = tk.Frame(self, width=600, height=300)
        action_frame = tk.Frame(self)

        logo_frame.pack(fill='both', expand=True)
        tab_frame.pack(fill='both', expand=True)
        container.pack(fill='both', expand=True)
        action_frame.pack(fill='both', expand=True)

        img = ImageTk.PhotoImage(Image.open("GUI_Util/Jelly.png"))
        # This work, "Jelly.png", is a derivative of "Sea Ghost" by Joey Gannon,
        # used under CC BY-SA.  The original version can be found here:
        # https://www.flickr.com/photos/brunkfordbraun/679827214
        # This work is under same license as the original
        logo = tk.Label(logo_frame, text="", image=img)
        logo.bind("<Enter>", self._on_enter)
        logo.image = img

        label = tk.Label(logo_frame, text="Welcome to Schedule and Depend. This graphical user interface " +
                                          "is designed for configuration of the tool... enjoy!", wraplength=400)

        logo.pack(side="left")
        label.pack(side="left")

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
        self.h_line_1 = ttk.Separator(tab_frame, orient='horizontal')
        self.h_line_1.pack(side="top", fill='both', expand=True)
        self.h_line_2 = ttk.Separator(tab_frame, orient='horizontal')
        self.h_line_2.pack(side="bottom", fill='both', expand=True)

        self.b1.pack(side="left")
        self.b2.pack(side="left")
        self.b3.pack(side="left")
        self.b4.pack(side="left")
        self.b5.pack(side="left")

        self.h_line_3 = ttk.Separator(action_frame, orient='horizontal')
        self.error_message = tk.Label(action_frame, text="", font=("-weight bold", 10), fg="red")
        apply_button = tk.Button(action_frame, text="Apply", command=self._apply_button)
        cancel_button = tk.Button(action_frame, text="Cancel", command=self._cancel_button)

        self.h_line_3.pack(side="top", fill='both', expand=True)
        apply_button.pack(side='right')
        cancel_button.pack(side='right', padx=5)
        self.error_message.pack(side='right')

        self.p1.show()

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
        elif self.p3.mapping.get() not in self.p3.mapping_dict[self.p1.tg_type.get()]:
            self.error_message.config(text="Can not perform mapping algorithm with the current TG type")
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
            Config.viz.mapping = self.p5.mapping_Draw.get()
            Config.viz.rg = self.p5.rg_draw.get()
            Config.viz.shm = self.p5.shm_draw.get()
            Config.viz.pmcg = self.p5.pmcg_draw.get()
            Config.viz.ttg = self.p5.ttg_draw.get()

            Config.viz.mapping_frames = self.p5.anim_enable.get()
            Config.viz.frame_resolution = int(self.p5.frame_rez.get())

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

    @staticmethod
    def _on_enter(self):
        tkMessageBox.showinfo("License Message", "The logo picture is a derivative of \"Sea Ghost\" by Joey Gannon, " +
                              "used under CC BY-SA. The original version can be found here: " +
                              "https://www.flickr.com/photos/brunkfordbraun/679827214 " +
                              "This work is under same license as the original."
                              "(https://creativecommons.org/licenses/by-sa/2.0/)")