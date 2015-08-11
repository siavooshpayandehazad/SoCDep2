# Copyright (C) Siavoosh Payandeh Azad


import Tkinter
import ttk
from ConfigAndPackages import Config

class ConfigAppp(Tkinter.Tk):

    Cancel_Button = False

    Cl_OptStartRow = 1
    Cl_OptStartCol = 4

    Mapping_OptStartRow = 5
    Mapping_OptStartCol = 4

    Topology_StartingRow = 1
    Topology_StartingCol = 0

    TG_StartingRow = 7
    TG_StartingCol = 0

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent

        self.LOGO = Tkinter.Label(self, text="SCHEDULE AND DEPEND CONFIG GUI")

        # ---------------------------------------------
        #                   Topology
        # ---------------------------------------------
        self.TopologyLabel = Tkinter.Label(self, text="Topology:")
        AvailableTopologies = ['2DTorus', '2DMesh', '2DLine', '2DRing', '3DMesh']
        self.Topology = Tkinter.StringVar()
        self.TopologyOption = Tkinter.OptionMenu(self, self.Topology, *AvailableTopologies,
                                                 command=self.NetworkSizeCont)
        self.NetworkSize_X = Tkinter.Spinbox(self, from_=0, to=10)
        self.NetworkSize_Y = Tkinter.Spinbox(self, from_=0, to=10)
        self.NetworkSize_Z = Tkinter.Spinbox(self, from_=0, to=10)
        # ---------------------------------------------
        #                   TG
        # ---------------------------------------------
        self.TG_Label = Tkinter.Label(self, text="Task Graph Type:")
        AvailableTGs = ['RandomDependent','RandomIndependent','Manual']
        self.TGType = Tkinter.StringVar(self)
        self.TGType.set('RandomDependent')
        self.TGTypeOption = Tkinter.OptionMenu(self, self.TGType, *AvailableTGs, command=self.TGTypeCont)

        self.NumOfTasks_Label = Tkinter.Label(self, text="Number of Tasks:")
        self.NumOfTasks = Tkinter.Entry(self)

        self.NumOfCritTasks_Label = Tkinter.Label(self, text="Number of Critical Tasks:")
        self.NumOfCritTasks = Tkinter.Entry(self)

        self.NumOfEdge_Label = Tkinter.Label(self, text="Number TG Edges:")
        self.NumOfEdge = Tkinter.Entry(self)

        self.WCET_Range_Label = Tkinter.Label(self, text="WCET Range:")
        self.WCET_Range = Tkinter.Entry(self)

        self.EdgeWeight_Range_Label = Tkinter.Label(self, text="Edge Weight Range:")
        self.EdgeWeight_Range = Tkinter.Entry(self)

        self.Release_Range_Label = Tkinter.Label(self, text="Task Release Range:")
        self.Release_Range = Tkinter.Entry(self)

        # ---------------------------------------------
        #                   Clustering
        # ---------------------------------------------
        self.ClusteringOptVar = Tkinter.BooleanVar(self)
        self.ClusteringOptEnable = Tkinter.Checkbutton(self, text="Clustering Optimization",
                                                       variable=self.ClusteringOptVar, command=self.ClusteringCont)
        self.ClusteringIterLabel = Tkinter.Label(self, text="Clustering Iterations:")
        self.ClusteringIterations = Tkinter.Entry(self)
        self.ClusteringCostLabel = Tkinter.Label(self, text="Cost Function Type:")
        AvailableCosts = ['SD', 'SD+MAX']
        self.ClusterCost = Tkinter.StringVar(self)
        self.ClusterCost.set('SD+MAX')
        self.ClusterCostOpt = Tkinter.OptionMenu(self, self.ClusterCost, *AvailableCosts)
        # ---------------------------------------------
        #                   Mapping
        # ---------------------------------------------
        self.Mapping_Label = Tkinter.Label(self, text="Mapping Algorithm:")
        AvailableMappings = ['MinMin', 'MaxMin', 'MinExecutionTime', 'MinimumCompletionTime',
                             'LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing', 'NMap']
        self.Mapping = Tkinter.StringVar(self)
        self.Mapping.set('LocalSearch')
        self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *AvailableMappings, command=self.MappingAlgCont)
        # ---------------------------------------------
        #           Simulated Annealing
        # ---------------------------------------------

        self.SA_Label = Tkinter.Label(self, text="Annealing Schedule:")
        AvailableAnnealing = ['Linear', 'Exponential', 'Adaptive', 'Markov', 'Logarithmic', 'Aart', 'Huang']
        self.Annealing = Tkinter.StringVar()
        self.Annealing.set('Linear')
        self.AnnealingOption = Tkinter.OptionMenu(self, self.Annealing,
                                                  *AvailableAnnealing, command=self.Annealing_Termination)

        self.SA_Term_Label = Tkinter.Label(self, text="Termination Criteria:")
        AvailableTermination = ['StopTemp', 'IterationNum']
        self.Termination = Tkinter.StringVar()
        self.Termination.set('StopTemp')
        self.TerminationOption = Tkinter.OptionMenu(self, self.Termination,
                                                    *AvailableTermination, command=self.Annealing_Termination)

        self.SA_IterLabel = Tkinter.Label(self, text="Number of Iterations:")
        self.SA_Iterations = Tkinter.Entry(self)
        self.SA_Iterations.insert(0, '100000')

        self.SA_InitTemp_Label = Tkinter.Label(self, text="Initial Temperature:")
        self.SA_InitTemp = Tkinter.Entry(self)
        self.SA_InitTemp.insert(0, '100')

        self.SA_StopTemp_Label = Tkinter.Label(self, text="Stop Temperature:")
        self.SA_StopTemp = Tkinter.Entry(self)
        self.SA_StopTemp.insert(0, '5')

        self.SA_Alpha_Label = Tkinter.Label(self, text="Cooling ratio:")
        self.SA_Alpha = Tkinter.Entry(self)
        self.SA_Alpha.insert(0, '0.999')


        self.SA_LoG_Const_Label = Tkinter.Label(self, text="Log cooling constant:")
        self.SA_LoG_Const = Tkinter.Entry(self)
        self.SA_LoG_Const.insert(0, '1000')

        self.CostMonitor_Label = Tkinter.Label(self, text="Cost Monitor Queue Size:")
        self.CostMonitor = Tkinter.Entry(self)
        self.CostMonitor.insert(0, '2000')


        self.CostMonitorSlope_Label = Tkinter.Label(self, text="Slope Range For Cooling:")
        self.CostMonitorSlope = Tkinter.Entry(self)
        self.CostMonitorSlope.insert(0, '0.02')

        self.MaxSteadyState_Label = Tkinter.Label(self, text="Maximum steps without improvement:")
        self.MaxSteadyState = Tkinter.Entry(self)
        self.MaxSteadyState.insert(0, '30000')


        self.MarkovNum_Label = Tkinter.Label(self, text="Length of Markov Chain:")
        self.MarkovNum = Tkinter.Entry(self)
        self.MarkovNum.insert(0, '2000')

        self.MarkovTempStep_Label = Tkinter.Label(self, text="Temperature step:")
        self.MarkovTempStep = Tkinter.Entry(self)
        self.MarkovTempStep.insert(0, '1')

        self.SA_Delta_Label = Tkinter.Label(self, text="Delta:")
        self.SA_Delta = Tkinter.Entry(self)
        self.SA_Delta.insert(0, '0.05')

        # ---------------------------------------------
        self.initialize()


    def initialize(self):

        self.grid()
        self.LOGO.grid(column=1, row=0, columnspan=3)
        # ----------------------------------------
        Tkinter.Label(self, text="Topology Settings").grid(column=self.Topology_StartingCol,
                                                                     row=self.Topology_StartingRow)
        self.Topology.set('2DMesh')
        self.TopologyLabel.grid(column=self.Topology_StartingCol,row=self.Topology_StartingRow+1)
        self.TopologyOption.grid(column=self.Topology_StartingCol+1,row=self.Topology_StartingRow+1)

        XSizeLabel = Tkinter.Label(self, text="X Size:")
        YSizeLabel = Tkinter.Label(self, text="Y Size:")
        ZSizeLabel = Tkinter.Label(self, text="Z Size:")

        self.NetworkSize_X.delete(0, 'end')
        self.NetworkSize_X.insert(0, 3)
        self.NetworkSize_Y.delete(0, 'end')
        self.NetworkSize_Y.insert(0, 3)
        self.NetworkSize_Z.delete(0, 'end')
        self.NetworkSize_Z.insert(0, 1)

        XSizeLabel.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+2)
        self.NetworkSize_X.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+2)
        YSizeLabel.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+3)
        self.NetworkSize_Y.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+3)
        ZSizeLabel.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+4)
        self.NetworkSize_Z.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+4)
        self.NetworkSize_Z.config(state='disabled')

        ttk.Separator(self, orient='vertical').grid(column=self.Topology_StartingCol+2,
                                                    row=self.Topology_StartingRow+1, rowspan=10, sticky="ns")
        ttk.Separator(self, orient='horizontal').grid(column=self.Topology_StartingCol,
                                                      row=self.Topology_StartingRow+5, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   TG
        # ----------------------------------------
        Tkinter.Label(self, text="Task Graph Settings").grid(column=self.TG_StartingCol,
                                                             row=self.TG_StartingRow)
        self.TG_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+1)
        self.TGTypeOption.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+1)

        self.NumOfTasks_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+2)
        self.NumOfTasks.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+2)
        self.NumOfTasks.insert(0, '35')

        self.NumOfCritTasks_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+3)
        self.NumOfCritTasks.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+3)
        self.NumOfCritTasks.insert(0, '0')

        self.NumOfEdge_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+4)
        self.NumOfEdge.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+4)
        self.NumOfEdge.insert(0, '20')

        self.WCET_Range_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+5)
        self.WCET_Range.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+5)
        self.WCET_Range.insert(0, '15')

        self.EdgeWeight_Range_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+6)
        self.EdgeWeight_Range.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+6)
        self.EdgeWeight_Range.insert(0, '7')

        self.Release_Range_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+7)
        self.Release_Range.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+7)
        self.Release_Range.insert(0, '5')

        ttk.Separator(self, orient='horizontal').grid(column=self.TG_StartingCol,
                                                      row=self.TG_StartingRow+8, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   CTG
        # ----------------------------------------
        self.ClusteringOptVar.set('False')
        self.ClusteringIterations.insert(0, '1000')
        self.ClusteringOptEnable.grid(column=self.Cl_OptStartCol, row=self.Cl_OptStartRow)
        ttk.Separator(self, orient='horizontal').grid(column=self.Cl_OptStartCol, row=self.Cl_OptStartRow+3,
                                                      columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   Mapping
        # ----------------------------------------
        self.Mapping_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow)
        self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow)


        ttk.Separator(self, orient='vertical').grid(column=self.Cl_OptStartCol+2,
                                                    row=self.Cl_OptStartRow, rowspan=10, sticky="ns")
        ttk.Separator(self, orient='horizontal').grid(column=self.Mapping_OptStartCol,
                                                      row=self.Mapping_OptStartRow+9, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   Buttons
        # ----------------------------------------
        quitButton = Tkinter.Button(self, text="Apply", command=self.ApplyButton)
        quitButton.grid(column=1,row=20)

        quitButton = Tkinter.Button(self, text="cancel", command=self.CancelButton)
        quitButton.grid(column=2,row=20)

    def NetworkSizeCont(self, Topology):
        if '3D' in Topology:
            self.NetworkSize_Z.config(state='normal')
        else:
            self.NetworkSize_Z.delete(0, 'end')
            self.NetworkSize_Z.insert(0, 1)
            self.NetworkSize_Z.config(state='disabled')

    def TGTypeCont(self, TGType):
        if TGType == 'RandomDependent':
            self.NumOfTasks_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+2)
            self.NumOfTasks.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+2)
            self.NumOfTasks.delete(0, 'end')
            self.NumOfTasks.insert(0, '35')

            self.NumOfCritTasks_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+3)
            self.NumOfCritTasks.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+3)
            self.NumOfCritTasks.delete(0, 'end')
            self.NumOfCritTasks.insert(0, '0')

            self.NumOfEdge_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+4)
            self.NumOfEdge.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+4)
            self.NumOfEdge.delete(0, 'end')
            self.NumOfEdge.insert(0, '20')

            self.WCET_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+5)
            self.WCET_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+5)
            self.WCET_Range.delete(0, 'end')
            self.WCET_Range.insert(0, '15')

            self.EdgeWeight_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+6)
            self.EdgeWeight_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+6)
            self.EdgeWeight_Range.delete(0, 'end')
            self.EdgeWeight_Range.insert(0, '7')

            self.Release_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+7)
            self.Release_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+7)
            self.Release_Range.delete(0, 'end')
            self.Release_Range.insert(0, '5')

        elif TGType == 'RandomIndependent':
            self.NumOfTasks_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+2)
            self.NumOfTasks.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+2)
            self.NumOfTasks.delete(0, 'end')
            self.NumOfTasks.insert(0, '35')

            self.NumOfCritTasks_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+3)
            self.NumOfCritTasks.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+3)
            self.NumOfCritTasks.delete(0, 'end')
            self.NumOfCritTasks.insert(0, '0')

            self.WCET_Range_Label.grid(column=self.TG_StartingCol,row=self.TG_StartingRow+4)
            self.WCET_Range.grid(column=self.TG_StartingCol+1,row=self.TG_StartingRow+4)
            self.WCET_Range.delete(0, 'end')
            self.WCET_Range.insert(0, '15')

            self.Release_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+5)
            self.Release_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+5)
            self.Release_Range.delete(0, 'end')
            self.Release_Range.insert(0, '5')


            self.NumOfEdge_Label.grid_forget()
            self.NumOfEdge.grid_forget()

            self.EdgeWeight_Range.grid_forget()
            self.EdgeWeight_Range_Label.grid_forget()

        elif TGType == 'Manual':
            self.NumOfTasks_Label.grid_forget()
            self.NumOfTasks.grid_forget()

            self.NumOfCritTasks_Label.grid_forget()
            self.NumOfCritTasks.grid_forget()

            self.NumOfEdge_Label.grid_forget()
            self.NumOfEdge.grid_forget()

            self.WCET_Range_Label.grid_forget()
            self.WCET_Range.grid_forget()

            self.Release_Range_Label.grid_forget()
            self.Release_Range.grid_forget()

            self.EdgeWeight_Range.grid_forget()
            self.EdgeWeight_Range_Label.grid_forget()

    def ClusteringCont(self):
        if self.ClusteringOptVar.get():
            self.ClusteringIterLabel.grid(column=self.Cl_OptStartCol, row=self.Cl_OptStartRow + 1)
            self.ClusteringIterations.grid(column=self.Cl_OptStartCol+1, row=self.Cl_OptStartRow + 1)
            self.ClusteringIterations.delete(0, 'end')
            self.ClusteringIterations.insert(0, '1000')

            self.ClusteringCostLabel.grid(column=self.Cl_OptStartCol, row=self.Cl_OptStartRow + 2)
            self.ClusterCostOpt.grid(column=self.Cl_OptStartCol+1, row=self.Cl_OptStartRow + 2)
        else:
            self.ClusteringIterLabel.grid_forget()
            self.ClusteringIterations.grid_forget()
            self.ClusteringCostLabel.grid_forget()
            self.ClusterCostOpt.grid_forget()


    def MappingAlgCont(self, Mapping):
        if self.Mapping.get() == 'SimulatedAnnealing':
            self.Annealing.set('Linear')
            self.SA_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+1)
            self.AnnealingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)

            self.SA_InitTemp.delete(0, 'end')
            self.SA_InitTemp.insert(0, '100')
            self.SA_InitTemp_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+2)
            self.SA_InitTemp.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+2)

            self.Termination.set('StopTemp')
            self.SA_Term_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+3)
            self.TerminationOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+3)

            self.SA_Iterations.delete(0, 'end')
            self.SA_Iterations.insert(0, '100000')
            self.SA_IterLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+4)
            self.SA_Iterations.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+4)



        else:

            self.SA_InitTemp.grid_forget()
            self.SA_InitTemp_Label.grid_forget()

            self.SA_StopTemp.grid_forget()
            self.SA_StopTemp_Label.grid_forget()

            self.SA_Iterations.grid_forget()
            self.SA_IterLabel.grid_forget()

            self.TerminationOption.grid_forget()
            self.SA_Term_Label.grid_forget()

            self.SA_Label.grid_forget()
            self.AnnealingOption.grid_forget()

    def Annealing_Termination(self, Annealing):
        if self.Mapping.get() == 'SimulatedAnnealing':
            if self.Annealing.get()=='Linear' or self.Termination.get()=='IterationNum':
                self.SA_StopTemp.grid_forget()
                self.SA_StopTemp_Label.grid_forget()

                self.SA_IterLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+4)
                self.SA_Iterations.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+4)
            elif self.Termination.get()=='StopTemp' and self.Annealing.get() != 'Linear':
                self.SA_Iterations.grid_forget()
                self.SA_IterLabel.grid_forget()

                self.SA_StopTemp.delete(0, 'end')
                self.SA_StopTemp.insert(0, '5')
                self.SA_StopTemp_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+4)
                self.SA_StopTemp.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+4)
            else:
                self.SA_StopTemp.grid_forget()
                self.SA_StopTemp_Label.grid_forget()

                self.SA_Iterations.grid_forget()
                self.SA_IterLabel.grid_forget()

            if self.Annealing.get() in ['Exponential','Adaptive','Aart', 'Huang']:
                self.SA_Alpha.delete(0, 'end')
                self.SA_Alpha.insert(0, '0.999')
                self.SA_Alpha_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+5)
                self.SA_Alpha.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+5)
            else:
                self.SA_Alpha_Label.grid_forget()
                self.SA_Alpha.grid_forget()

            if self.Annealing.get() == 'Logarithmic':
                self.SA_LoG_Const.delete(0, 'end')
                self.SA_LoG_Const.insert(0, '1000')
                self.SA_LoG_Const_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+5)
                self.SA_LoG_Const.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+5)
            else:
                self.SA_LoG_Const_Label.grid_forget()
                self.SA_LoG_Const.grid_forget()

            if self.Annealing.get() == 'Adaptive':

                self.CostMonitorSlope.delete(0, 'end')
                self.CostMonitorSlope.insert(0, '0.02')
                self.CostMonitorSlope_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+7)
                self.CostMonitorSlope.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+7)

                self.MaxSteadyState.delete(0, 'end')
                self.MaxSteadyState.insert(0, '30000')
                self.MaxSteadyState_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+8)
                self.MaxSteadyState.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+8)


            else:
                self.MaxSteadyState_Label.grid_forget()
                self.MaxSteadyState.grid_forget()

                self.CostMonitorSlope_Label.grid_forget()
                self.CostMonitorSlope.grid_forget()


            if self.Annealing.get() == 'Markov':
                self.MarkovNum.delete(0, 'end')
                self.MarkovNum.insert(0, '2000')
                self.MarkovNum_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+5)
                self.MarkovNum.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+5)

                self.MarkovTempStep.delete(0, 'end')
                self.MarkovTempStep.insert(0, '1')
                self.MarkovTempStep_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+6)
                self.MarkovTempStep.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+6)
            else:
                self.MarkovNum_Label.grid_forget()
                self.MarkovNum.grid_forget()

                self.MarkovTempStep_Label.grid_forget()
                self.MarkovTempStep.grid_forget()

            if self.Annealing.get() in ['Aart', 'Adaptive', 'Huang']:
                self.CostMonitor.delete(0, 'end')
                self.CostMonitor.insert(0, '2000')
                self.CostMonitor_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+6)
                self.CostMonitor.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+6)

            else:
                self.CostMonitor_Label.grid_forget()
                self.CostMonitor.grid_forget()

            if self.Annealing.get() in ['Aart', 'Huang']:
                self.SA_Delta.delete(0, 'end')
                self.SA_Delta.insert(0, '0.05')
                self.SA_Delta_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+7)
                self.SA_Delta.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+7)
            else:
                self.SA_Delta_Label.grid_forget()
                self.SA_Delta.grid_forget()


    def ApplyButton(self):
        # apply changes...

        # TG Config
        Config.TG_Type = self.TGType.get()
        Config.NumberOfTasks = int(self.NumOfTasks.get())
        Config.NumberOfCriticalTasks = int(self.NumOfCritTasks.get())
        Config.NumberOfEdges = int(self.NumOfEdge.get())
        Config.WCET_Range = int(self.WCET_Range.get())
        Config.EdgeWeightRange = int(self.EdgeWeight_Range.get())
        Config.Release_Range = int(self.Release_Range.get())

        # Topology Config
        Config.NetworkTopology = self.Topology.get()
        Config.Network_X_Size = int(self.NetworkSize_X.get())
        Config.Network_Y_Size = int(self.NetworkSize_Y.get())
        Config.Network_Z_Size = int(self.NetworkSize_Z.get())

        # Clustering Config
        Config.ClusteringIteration =  int(self.ClusteringIterations.get())
        Config.Clustering_Optimization = self.ClusteringOptVar.get()
        Config.Clustering_CostFunctionType = self.ClusterCost.get()

        # Mapping Config
        Config.Mapping_Function = self.Mapping.get()
        Config.SA_AnnealingSchedule = self.Annealing.get()
        Config.TerminationCriteria = self.Termination.get()
        Config.SimulatedAnnealingIteration = int(self.SA_Iterations.get())
        Config.SA_InitialTemp =  int(self.SA_InitTemp.get())
        Config.SA_StopTemp = int(self.SA_StopTemp.get())
        Config.SA_Alpha = float(self.SA_Alpha.get())
        Config.LogCoolingConstant = int(self.SA_LoG_Const.get())
        Config.CostMonitorQueSize = int(self.CostMonitor.get())
        Config.SlopeRangeForCooling = float(self.CostMonitorSlope.get())
        Config.MaxSteadyState = int(self.MaxSteadyState.get())
        Config.MarkovTempStep = float(self.MarkovTempStep.get())
        Config.MarkovNum = int(self.MarkovNum.get())
        Config.Delta = float(self.SA_Delta.get())

        self.destroy()

    def CancelButton(self):
        self.Cancel_Button = True
        self.destroy()