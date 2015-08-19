# Copyright (C) Siavoosh Payandeh Azad


import Tkinter
import ttk
import tkFileDialog
import tkMessageBox
from ConfigAndPackages import Config
from ConfigAndPackages import PackageFile

from PIL import ImageTk, Image

class ConfigAppp(Tkinter.Tk):

    Apply_Button = False

    # Task clustering Config
    Cl_OptStartRow = 2
    Cl_OptStartCol = 3

    # Mapping Algorithm Config
    Mapping_OptStartRow = 6
    Mapping_OptStartCol = 3

    # Architecture Graph Config
    Topology_StartingRow = 2
    Topology_StartingCol = 0

    # Task Graph Config
    TG_StartingRow = 7
    TG_StartingCol = 0

    # Routing Config
    Routing_StartingRow = 15
    Routing_StartingCol = 0

    # Fault Handling
    Fault_StartingRow = 2
    Fault_StartingCol = 6

    # visualization
    Viz_StartingRow = 7
    Viz_StartingCol = 6

    # Animation Frame generation
    Anim_StartingRow = 12
    Anim_StartingCol = 6

    # vertical Link placement optimization
    VLPlacement_StartingRow = 2
    VLPlacement_StartingCol = 9

    # Dependability Config
    Dependability_StartingRow = 8
    Dependability_StartingCol = 9

    # PMC Config
    PMC_StartingRow = 11
    PMC_StartingCol = 9

    OptionMenuWidth = 15
    EntryWidth = 10

    RoutingDict = {'2D': ['XY', 'West First', 'North Last', 'Negative First', 'From File'],
                   '3D': ['XYZ', 'Negative First', 'From File']}

    MappingDict = {'Manual': ['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing',
                   'NMap', 'MinMin', 'MaxMin', 'MinExecutionTime', 'MinimumCompletionTime'],
                   'RandomDependent':['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing', 'NMap'],
                   'RandomIndependent':['MinMin', 'MaxMin', 'MinExecutionTime', 'MinimumCompletionTime']}

    VLP_Alg_List = ['LocalSearch', 'IterativeLocalSearch']

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        # ---------------------------------------------
        #                   Topology
        # ---------------------------------------------
        self.TopologyLabel = Tkinter.Label(self, text="Topology:")
        AvailableTopologies = ['2DTorus', '2DMesh', '2DLine', '2DRing', '3DMesh']
        self.Topology = Tkinter.StringVar()
        self.TopologyOption = Tkinter.OptionMenu(self, self.Topology, *AvailableTopologies,
                                                 command=self.NetworkSizeCont)
        self.TopologyOption.config(width=self.OptionMenuWidth)

        self.NetworkSize_X = Tkinter.Spinbox(self, from_=1, to=10, width=self.EntryWidth)
        self.NetworkSize_Y = Tkinter.Spinbox(self, from_=1, to=10, width=self.EntryWidth)
        self.NetworkSize_Z = Tkinter.Spinbox(self, from_=1, to=10, width=self.EntryWidth)

        # ---------------------------------------------
        #                   TG
        # ---------------------------------------------
        self.TG_Label = Tkinter.Label(self, text="Task Graph Type:")
        self.AvailableTGs = ['RandomDependent','RandomIndependent','Manual']
        self.TGType = Tkinter.StringVar(self)
        self.TGType.set('RandomDependent')
        self.TGTypeOption = Tkinter.OptionMenu(self, self.TGType, *self.AvailableTGs, command=self.TGTypeCont)
        self.TGTypeOption.config(width=self.OptionMenuWidth)

        self.NumOfTasks_Label = Tkinter.Label(self, text="Number of Tasks:")
        self.NumOfTasks = Tkinter.Entry(self, width=self.EntryWidth)

        self.NumOfCritTasks_Label = Tkinter.Label(self, text="Number of Critical Tasks:")
        self.NumOfCritTasks = Tkinter.Entry(self, width=self.EntryWidth)

        self.NumOfEdge_Label = Tkinter.Label(self, text="Number TG Edges:")
        self.NumOfEdge = Tkinter.Entry(self, width=self.EntryWidth)

        self.WCET_Range_Label = Tkinter.Label(self, text="WCET Range:")
        self.WCET_Range = Tkinter.Entry(self, width=self.EntryWidth)

        self.EdgeWeight_Range_Label = Tkinter.Label(self, text="Edge Weight Range:")
        self.EdgeWeight_Range = Tkinter.Entry(self, width=self.EntryWidth)

        self.Release_Range_Label = Tkinter.Label(self, text="Task Release Range:")
        self.Release_Range = Tkinter.Entry(self, width=self.EntryWidth)

        self.TGBrowse = Tkinter.Entry(self, bg='gray')
        self.TGBrowse.insert(0, "TG File Path...")

        self.TGBrowseButton = Tkinter.Button(self, text="Browse", command=self.GetTGFile)

        # ---------------------------------------------
        #                   Routing
        # ---------------------------------------------
        self.RoutingLabel = Tkinter.Label(self, text="Routing Algorithm:")
        AvailableRoutings = self.RoutingDict['2D']
        self.RoutingAlg = Tkinter.StringVar()
        self.RoutingAlg.set(self.RoutingDict['2D'][0])
        self.RoutingAlgOption = Tkinter.OptionMenu(self, self.RoutingAlg, *AvailableRoutings, command=self.RoutingFunc)
        self.RoutingAlgOption.config(width=self.OptionMenuWidth)

        self.RoutingTypeLabel = Tkinter.Label(self, text="Routing type:")
        AvailableRoutingsTypes = ['MinimalPath', 'NonMinimalPath']
        self.RoutingType = Tkinter.StringVar()
        self.RoutingType.set('MinimalPath')
        self.RoutingTypeOption = Tkinter.OptionMenu(self, self.RoutingType, *AvailableRoutingsTypes)
        self.RoutingTypeOption.config(width=self.OptionMenuWidth)

        self.RoutingBrowse = Tkinter.Entry(self, bg='gray')
        self.RoutingBrowse.insert(0, "Routing File Path...")

        self.RoutingBrowseButton = Tkinter.Button(self, text="Browse", command=self.GetRoutingFile)

        # ---------------------------------------------
        #                   Clustering
        # ---------------------------------------------
        self.ClusteringOptVar = Tkinter.BooleanVar(self)
        self.ClusteringOptEnable = Tkinter.Checkbutton(self, text="Clustering Optimization",
                                                       variable=self.ClusteringOptVar, command=self.ClusteringCont)
        self.ClusteringIterLabel = Tkinter.Label(self, text="Clustering Iterations:")
        self.ClusteringIterations = Tkinter.Entry(self, width=self.EntryWidth)

        self.ClusteringCostLabel = Tkinter.Label(self, text="Cost Function Type:")
        AvailableCosts = ['SD', 'SD+MAX']
        self.ClusterCost = Tkinter.StringVar(self)
        self.ClusterCost.set('SD+MAX')
        self.ClusterCostOpt = Tkinter.OptionMenu(self, self.ClusterCost, *AvailableCosts)
        self.ClusterCostOpt.config(width=self.OptionMenuWidth)
        # ---------------------------------------------
        #                   Mapping
        # ---------------------------------------------
        self.Mapping_Label = Tkinter.Label(self, text="Mapping Algorithm:")
        self.Mapping = Tkinter.StringVar(self)
        self.Mapping.set('LocalSearch')
        self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *self.MappingDict['RandomDependent'],
                                                command=self.MappingAlgCont)
        self.MappingOption.config(width=self.OptionMenuWidth)

        self.MappingCostLabel = Tkinter.Label(self, text="Cost Function Type:")
        AvailableMappingCosts = ['SD', 'SD+MAX', 'CONSTANT']
        self.MappingCost = Tkinter.StringVar(self)
        self.MappingCost.set('SD+MAX')
        self.MappingCostOpt = Tkinter.OptionMenu(self, self.MappingCost, *AvailableMappingCosts)
        self.MappingCostOpt.config(width=self.OptionMenuWidth)
        # ---------------------------------------------
        #           Local Search
        # ---------------------------------------------
        self.LS_Iter_Label = Tkinter.Label(self, text="LS Iterations:")
        self.LS_Iter = Tkinter.Entry(self, width=self.EntryWidth)
        self.LS_Iter.insert(0, '100')

        self.ILS_Iter_Label = Tkinter.Label(self, text="ILS Iterations:")
        self.ILS_Iter = Tkinter.Entry(self, width=self.EntryWidth)
        self.ILS_Iter.insert(0, '10')

        # ---------------------------------------------
        #           Simulated Annealing
        # ---------------------------------------------

        self.SA_Label = Tkinter.Label(self, text="Annealing Schedule:")
        AvailableAnnealing = ['Linear', 'Exponential', 'Adaptive', 'Markov', 'Logarithmic', 'Aart', 'Huang']
        self.Annealing = Tkinter.StringVar()
        self.Annealing.set('Linear')
        self.AnnealingOption = Tkinter.OptionMenu(self, self.Annealing,
                                                  *AvailableAnnealing, command=self.Annealing_Termination)
        self.AnnealingOption.config(width=self.OptionMenuWidth)

        self.SA_Term_Label = Tkinter.Label(self, text="Termination Criteria:")
        AvailableTermination = ['StopTemp', 'IterationNum']
        self.Termination = Tkinter.StringVar()
        self.Termination.set('StopTemp')
        self.TerminationOption = Tkinter.OptionMenu(self, self.Termination,
                                                    *AvailableTermination, command=self.Annealing_Termination)
        self.TerminationOption.config(width=self.OptionMenuWidth)

        self.SA_IterLabel = Tkinter.Label(self, text="Number of Iterations:")
        self.SA_Iterations = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_Iterations.insert(0, '100000')

        self.SA_InitTemp_Label = Tkinter.Label(self, text="Initial Temperature:")
        self.SA_InitTemp = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_InitTemp.insert(0, '100')

        self.SA_StopTemp_Label = Tkinter.Label(self, text="Stop Temperature:")
        self.SA_StopTemp = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_StopTemp.insert(0, '5')

        self.SA_Alpha_Label = Tkinter.Label(self, text="Cooling ratio:")
        self.SA_Alpha = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_Alpha.insert(0, '0.999')


        self.SA_LoG_Const_Label = Tkinter.Label(self, text="Log cooling constant:")
        self.SA_LoG_Const = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_LoG_Const.insert(0, '1000')

        self.CostMonitor_Label = Tkinter.Label(self, text="Cost Monitor Queue Size:")
        self.CostMonitor = Tkinter.Entry(self, width=self.EntryWidth)
        self.CostMonitor.insert(0, '2000')


        self.CostMonitorSlope_Label = Tkinter.Label(self, text="Slope Range For Cooling:")
        self.CostMonitorSlope = Tkinter.Entry(self, width=self.EntryWidth)
        self.CostMonitorSlope.insert(0, '0.02')

        self.MaxSteadyState_Label = Tkinter.Label(self, text="Max steps/no improvement:")
        self.MaxSteadyState = Tkinter.Entry(self, width=self.EntryWidth)
        self.MaxSteadyState.insert(0, '30000')


        self.MarkovNum_Label = Tkinter.Label(self, text="Length of Markov Chain:")
        self.MarkovNum = Tkinter.Entry(self, width=self.EntryWidth)
        self.MarkovNum.insert(0, '2000')

        self.MarkovTempStep_Label = Tkinter.Label(self, text="Temperature step:")
        self.MarkovTempStep = Tkinter.Entry(self, width=self.EntryWidth)
        self.MarkovTempStep.insert(0, '1')

        self.SA_Delta_Label = Tkinter.Label(self, text="Delta:")
        self.SA_Delta = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_Delta.insert(0, '0.05')

        # ---------------------------------------------
        #               Fault Injection
        # ---------------------------------------------
        self.FaultInjection = Tkinter.BooleanVar(self)
        self.FaultInjectionEnable = Tkinter.Checkbutton(self, text="Event Driven Fault Injection",
                                                        variable=self.FaultInjection,
                                                        command=self.Fault_Injection)

        self.MTBF_Label = Tkinter.Label(self, text="MTBF (sec):")
        self.MTBF = Tkinter.Entry(self, width=self.EntryWidth)
        self.MTBF.insert(0, '2')

        self.SDMTBF_Label = Tkinter.Label(self, text="TBF's Standard Deviation:")
        self.SDMTBF = Tkinter.Entry(self, width=self.EntryWidth)
        self.SDMTBF.insert(0, '0.1')

        self.RunTime_Label = Tkinter.Label(self, text="Program RunTime:")
        self.RunTime = Tkinter.Entry(self, width=self.EntryWidth)
        self.RunTime.insert(0, '10')

        # ---------------------------------------------
        #               Viz
        # ---------------------------------------------
        self.AllViz = Tkinter.BooleanVar(self)
        self.AllViz.set('False')
        self.AllVizEnable = Tkinter.Checkbutton(self, text="Check/Un-check all reports",
                                                variable=self.AllViz, command=self.AllVizFunc,
                                                wraplength=100)

        self.RG_Draw = Tkinter.BooleanVar(self)
        self.RG_Draw.set('False')
        self.RG_DrawEnable = Tkinter.Checkbutton(self, text="Routing Graph", variable=self.RG_Draw)

        self.SHM_Draw = Tkinter.BooleanVar(self)
        self.SHM_Draw.set('False')
        self.SHM_DrawEnable = Tkinter.Checkbutton(self, text="System Health Map", variable=self.SHM_Draw)

        self.Mapping_Draw = Tkinter.BooleanVar(self)
        self.Mapping_Draw.set('False')
        self.Mapping_DrawEnable = Tkinter.Checkbutton(self, text="Mapping Report", variable=self.Mapping_Draw)

        self.PMCG_Draw = Tkinter.BooleanVar(self)
        self.PMCG_Draw.set('False')
        self.PMCG_DrawEnable = Tkinter.Checkbutton(self, text="PMCG Report", variable=self.PMCG_Draw)

        self.TTG_Draw = Tkinter.BooleanVar(self)
        self.TTG_Draw.set('False')
        self.TTG_DrawEnable = Tkinter.Checkbutton(self, text="TTG Report", variable=self.TTG_Draw)

        # ---------------------------------------------
        #               Anim
        # ---------------------------------------------
        self.AnimEnable = Tkinter.BooleanVar(self)
        self.AnimEnable.set('False')
        self.AnimEnableBox = Tkinter.Checkbutton(self, text="Generate Animation Frames",
                                                 variable=self.AnimEnable, command=self.AnimationConfig)

        self.FrameRezLabel = Tkinter.Label(self, text="Frame Resolution(dpi):")
        self.FrameRez = Tkinter.Entry(self, width=self.EntryWidth)
        self.FrameRez.insert(0, '20')

        # ----------------------------------------
        #           Vertical Link Placement
        # ----------------------------------------
        self.VLPlacementEnable = Tkinter.BooleanVar(self)
        self.VLPlacementEnable.set('False')
        self.VLPlacementEnableBox = Tkinter.Checkbutton(self, text="Enable VL Placement Optimization",
                                                        variable=self.VLPlacementEnable, command=self.VLPlacementFunc,
                                                        wraplength=200)

        self.VLP_Alg_Label = Tkinter.Label(self, text="Opt algorithm:")
        self.VLP_Alg = Tkinter.StringVar()
        self.VLP_Alg.set('LocalSearch')
        self.VLP_AlgOption = Tkinter.OptionMenu(self, self.VLP_Alg,
                                                  *self.VLP_Alg_List, command=self.VLPAlgFunc)
        self.VLP_AlgOption.config(width=self.OptionMenuWidth)

        self.NumOfVLs_Label = Tkinter.Label(self, text="Number of VLs:")
        self.NumOfVLs = Tkinter.Entry(self, width=self.EntryWidth)

        self.VLP_IterationsLS_Label = Tkinter.Label(self, text="LS Iterations:")
        self.VLP_IterationsLS = Tkinter.Entry(self, width=self.EntryWidth)

        self.VLP_IterationsILS_Label = Tkinter.Label(self, text="ILS Iterations:")
        self.VLP_IterationsILS = Tkinter.Entry(self, width=self.EntryWidth)
        # ----------------------------------------
        #           Dependability section
        # ----------------------------------------
        self.SlackNumber_Label = Tkinter.Label(self, text="Slack Numbers:")
        self.SlackNumber = Tkinter.Spinbox(self, from_=0, to=10, width=self.EntryWidth)

        self.NumberOfRects_Label = Tkinter.Label(self, text="NoCDepend Rectangle #:")
        self.NumberOfRects = Tkinter.Spinbox(self, from_=1, to=10, width=self.EntryWidth)
        self.NumberOfRects.delete(0, 'end')
        self.NumberOfRects.insert(0, 3)

        self.ErrorMessage = Tkinter.Label(self, text="", font="-weight bold", fg="red")

        # ----------------------------------------
        #           PMC config
        # ----------------------------------------
        self.PMCEnable = Tkinter.BooleanVar(self)
        self.PMCEnable.set('False')
        self.PMCEnableEnableBox = Tkinter.Checkbutton(self, text="Enable PMC config",
                                                      variable=self.PMCEnable, command=self.PMCFunc)

        self.PMCType_Label = Tkinter.Label(self, text="PMC Model:")
        self.AvailablePMCTypes = ['Sequentially diagnosable', 'One Step Diagnosable']
        self.PMCType = Tkinter.StringVar(self)
        self.PMCType.set('Sequentially diagnosable')
        self.PMCTypeOption = Tkinter.OptionMenu(self, self.PMCType, *self.AvailablePMCTypes, command=self.TfaultControl)
        self.PMCTypeOption.config(width=self.OptionMenuWidth)

        self.TfaultDiagnosable_Label = Tkinter.Label(self, text="T-Fault Diagnosable:")
        self.TfaultDiagnosable = Tkinter.Entry(self , width=self.EntryWidth)


        self.ErrorMessage = Tkinter.Label(self, text="",font="-weight bold", fg="red")

        self.initialize()

    def initialize(self):

        self.grid()

        img = ImageTk.PhotoImage(Image.open("GUI_Util/Jelly.png"))

        # This work, "Jelly.png", is a derivative of "Sea Ghost" by Joey Gannon,
        # used under CC BY-SA.  The original version can be found here:
        # https://www.flickr.com/photos/brunkfordbraun/679827214
        # This work is under same license as the original

        self.label1 = Tkinter.Label(self, text="", image=img)
        self.label1.image = img
        self.label1.grid(row=0, column=1, sticky='eW')
        self.label1.bind("<Enter>", self.on_enter)


        LOGO = Tkinter.Label(self, text="SCHEDULE AND DEPEND CONFIG GUI", font="-weight bold")
        LOGO.grid(column=1, row=0, columnspan=7)
        ttk.Separator(self, orient='horizontal').grid(column=0, row=1, columnspan=11, sticky="ew")

        # ----------------------------------------
        Tkinter.Label(self, text="Topology Config", font="-weight bold").grid(column=self.Topology_StartingCol,
                                                                              row=self.Topology_StartingRow,
                                                                              columnspan=2)
        self.Topology.set('2DMesh')
        self.TopologyLabel.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+1)
        self.TopologyOption.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+1, sticky='w')

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
        self.NetworkSize_X.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+2, sticky ='w')
        YSizeLabel.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+3)
        self.NetworkSize_Y.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+3, sticky ='w')
        ZSizeLabel.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+4)
        self.NetworkSize_Z.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+4, sticky ='w')
        self.NetworkSize_Z.config(state='disabled')

        ttk.Separator(self, orient='vertical').grid(column=self.Topology_StartingCol+2,
                                                    row=self.Topology_StartingRow+1, rowspan=16, sticky="ns")
        ttk.Separator(self, orient='horizontal').grid(column=self.Topology_StartingCol,
                                                      row=self.Topology_StartingRow+5, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   TG
        # ----------------------------------------
        Tkinter.Label(self, text="Task Graph Settings",font="-weight bold").grid(column=self.TG_StartingCol,
                                                                                 row=self.TG_StartingRow,
                                                                                 columnspan=2)
        self.TG_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+1, sticky='w')
        self.TGTypeOption.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+1, sticky='w')

        self.NumOfTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+2, sticky='w')
        self.NumOfTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+2, sticky='w')
        self.NumOfTasks.insert(0, '35')

        self.NumOfCritTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+3, sticky='w')
        self.NumOfCritTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+3, sticky='w')
        self.NumOfCritTasks.insert(0, '0')

        self.NumOfEdge_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+4, sticky='w')
        self.NumOfEdge.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+4, sticky='w')
        self.NumOfEdge.insert(0, '20')

        self.WCET_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+5, sticky='w')
        self.WCET_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+5, sticky='w')
        self.WCET_Range.insert(0, '15')

        self.EdgeWeight_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+6, sticky='w')
        self.EdgeWeight_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+6, sticky='w')
        self.EdgeWeight_Range.insert(0, '7')

        self.Release_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+7, sticky='w')
        self.Release_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+7, sticky='w')
        self.Release_Range.insert(0, '5')

        ttk.Separator(self, orient='horizontal').grid(column=self.TG_StartingCol,
                                                      row=self.TG_StartingRow+8, columnspan=2, sticky="ew")

        # ---------------------------------------------
        #                   Routing
        # ---------------------------------------------
        Tkinter.Label(self, text="Routing Settings",font="-weight bold").grid(column=self.Routing_StartingCol,
                                                                              row=self.Routing_StartingRow,
                                                                              columnspan=2)
        self.RoutingLabel.grid(column=self.Routing_StartingCol, row=self.Routing_StartingRow+1)
        self.RoutingAlgOption.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+1)

        self.RoutingTypeLabel.grid(column=self.Routing_StartingCol, row=self.Routing_StartingRow+2)
        self.RoutingTypeOption.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+2)
        self.RoutingTypeOption.config(state='disable')

        ttk.Separator(self, orient='horizontal').grid(column=self.Routing_StartingCol,
                                                      row=self.Routing_StartingRow+4, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   CTG
        # ----------------------------------------
        Tkinter.Label(self, text="Clustering Settings",font="-weight bold").grid(column=self.Cl_OptStartCol,
                                                                                 row=self.Cl_OptStartRow,
                                                                                 columnspan=2)
        self.ClusteringOptVar.set('False')
        self.ClusteringIterations.insert(0, '1000')
        self.ClusteringOptEnable.grid(column=self.Cl_OptStartCol, row=self.Cl_OptStartRow+1)

        ttk.Separator(self, orient='horizontal').grid(column=self.Cl_OptStartCol, row=self.Cl_OptStartRow+4,
                                                      columnspan=2, sticky="ew")

        # ----------------------------------------
        #                   Mapping
        # ----------------------------------------
        Tkinter.Label(self, text="Mapping Settings", font="-weight bold").grid(column=self.Mapping_OptStartCol,
                                                                              row=self.Mapping_OptStartRow,
                                                                              columnspan=2)
        self.Mapping_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+1)
        self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)

        self.MappingCostLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+2)
        self.MappingCostOpt.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+2)

        self.LS_Iter_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+3)
        self.LS_Iter.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+3)

        ttk.Separator(self, orient='vertical').grid(column=self.Cl_OptStartCol+2,
                                                    row=self.Cl_OptStartRow+1, rowspan=14, sticky="ns")
        ttk.Separator(self, orient='horizontal').grid(column=self.Mapping_OptStartCol,
                                                      row=self.Mapping_OptStartRow+11, columnspan=2, sticky="ew")
        # ----------------------------------------
        #               Fault
        # ----------------------------------------
        Tkinter.Label(self, text="Fault Settings",font="-weight bold").grid(column=self.Fault_StartingCol,
                                                                            row=self.Fault_StartingRow,
                                                                            columnspan=2)
        self.FaultInjection.set('False')
        self.FaultInjectionEnable.grid(column=self.Fault_StartingCol, row=self.Fault_StartingRow+1)

        ttk.Separator(self, orient='horizontal').grid(column=self.Fault_StartingCol,
                                                      row=self.Fault_StartingRow+5, columnspan=2, sticky="ew")

        ttk.Separator(self, orient='vertical').grid(column=self.Fault_StartingCol+2,
                                                    row=self.Fault_StartingRow+1, rowspan=12, sticky="ns")
        # ----------------------------------------
        #                   Viz
        # ----------------------------------------
        Tkinter.Label(self, text="Visualization Config",font="-weight bold").grid(column=self.Viz_StartingCol,
                      row=self.Viz_StartingRow, columnspan=2)

        self.AllVizEnable.grid(column=self.Viz_StartingCol, row=self.Viz_StartingRow+1, columnspan=1, sticky='w' )

        self.SHM_DrawEnable.grid(column=self.Viz_StartingCol, row=self.Viz_StartingRow+2, sticky='W')
        self.RG_DrawEnable.grid(column=self.Viz_StartingCol, row=self.Viz_StartingRow+3, sticky='W')
        self.Mapping_DrawEnable.grid(column=self.Viz_StartingCol, row=self.Viz_StartingRow+4, sticky='W')
        self.PMCG_DrawEnable.grid(column=self.Viz_StartingCol+1, row=self.Viz_StartingRow+3, sticky='W')
        self.TTG_DrawEnable.grid(column=self.Viz_StartingCol+1, row=self.Viz_StartingRow+4, sticky='W')

        ttk.Separator(self, orient='horizontal').grid(column=self.Viz_StartingCol,
                                                      row=self.Viz_StartingRow+5, columnspan=2, sticky="ew")

        # ----------------------------------------
        #               Animation
        # ----------------------------------------
        Tkinter.Label(self, text="Animation Frames Config",font="-weight bold").grid(column=self.Anim_StartingCol,
                                                                                     row=self.Anim_StartingRow,
                                                                                     columnspan=2)

        self.AnimEnableBox.grid(column=self.Anim_StartingCol, row=self.Anim_StartingRow+1,
                                sticky='W')
        ttk.Separator(self, orient='horizontal').grid(column=self.Anim_StartingCol, row=self.Anim_StartingRow+3,
                                                      columnspan=2, sticky="ew")

        # ----------------------------------------
        #           Vertical Link Placement
        # ----------------------------------------
        Tkinter.Label(self, text="Vertical Link Placement Optimization", font="-weight bold").grid(column=self.VLPlacement_StartingCol,
                      row=self.VLPlacement_StartingRow, columnspan=2)

        self.VLPlacementEnableBox.grid(column=self.VLPlacement_StartingCol, row=self.VLPlacement_StartingRow+1)
        self.VLPlacementEnableBox.config(state='disable')

        ttk.Separator(self, orient='horizontal').grid(column=self.VLPlacement_StartingCol,
                                                      row=self.VLPlacement_StartingRow+6, columnspan=2, sticky="ew")
        # ----------------------------------------
        #           Dependability section
        # ----------------------------------------
        Tkinter.Label(self, text="Dependability Config", font="-weight bold").grid(column=self.Dependability_StartingCol,
                      row=self.Dependability_StartingRow, columnspan=2)

        self.SlackNumber_Label.grid(column=self.Dependability_StartingCol, row=self.Dependability_StartingRow+1)
        self.SlackNumber.grid(column=self.Dependability_StartingCol+1, row=self.Dependability_StartingRow+1)


        self.NumberOfRects_Label.grid(column=self.Dependability_StartingCol, row=self.Dependability_StartingRow+2)
        self.NumberOfRects.grid(column=self.Dependability_StartingCol+1, row=self.Dependability_StartingRow+2)

        ttk.Separator(self, orient='horizontal').grid(column=self.Dependability_StartingCol,
                                                      row=self.Dependability_StartingRow+3, columnspan=2, sticky="ew")

        # ----------------------------------------
        #           PMC Graph
        # ----------------------------------------
        Tkinter.Label(self, text="PMC Config",font="-weight bold").grid(column=self.PMC_StartingCol,
                      row=self.PMC_StartingRow, columnspan=2)

        self.PMCEnableEnableBox.grid(column=self.PMC_StartingCol, row=self.PMC_StartingRow+1, sticky='w')

        ttk.Separator(self, orient='horizontal').grid(column=self.PMC_StartingCol,
                                                      row=self.PMC_StartingRow+4, columnspan=2, sticky="ew")

        # ----------------------------------------
        #                   Buttons
        # ----------------------------------------

        self.ErrorMessage.grid(column=4, row=19, columnspan=5)

        quitButton = Tkinter.Button(self, text="Apply", command=self.ApplyButton, width=15)
        quitButton.grid(column=4,row=20, columnspan=2, rowspan=2)

        quitButton = Tkinter.Button(self, text="cancel", command=self.CancelButton)
        quitButton.grid(column=6,row=20, columnspan=2, rowspan=2)


    def NetworkSizeCont(self, Topology):
        if '3D' in Topology:
            self.NetworkSize_Z.config(state='normal')
            self.VLPlacementEnableBox.config(state='normal')
            self.RoutingAlgOption.grid_forget()
            del self.RoutingAlgOption
            self.RoutingAlg.set('Please Select...')
            self.RoutingAlgOption = Tkinter.OptionMenu(self, self.RoutingAlg, *self.RoutingDict['3D'],
                                                       command=self.RoutingFunc)
            self.RoutingAlgOption.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+1)
            self.RoutingAlgOption.config(width=self.OptionMenuWidth)

            self.RoutingType.set("Please Select...")
            self.RoutingTypeOption.config(state='disable')
            self.RoutingBrowse.grid_forget()
            self.RoutingBrowseButton.grid_forget()

            self.NetworkSize_Z.delete(0, 'end')
            self.NetworkSize_Z.insert(0, 2)
        else:
            self.VLPlacementEnableBox.config(state='disable')
            self.RoutingAlgOption.grid_forget()
            del self.RoutingAlgOption
            self.RoutingAlg.set('Please Select...')
            self.RoutingAlgOption = Tkinter.OptionMenu(self, self.RoutingAlg, *self.RoutingDict['2D'],
                                                       command=self.RoutingFunc)
            self.RoutingAlgOption.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+1)
            self.RoutingAlgOption.config(width=self.OptionMenuWidth)

            self.RoutingType.set("Please Select...")
            self.RoutingTypeOption.config(state='disable')
            self.RoutingBrowse.grid_forget()
            self.RoutingBrowseButton.grid_forget()

            self.NetworkSize_Z.delete(0, 'end')
            self.NetworkSize_Z.insert(0, 1)
            self.NetworkSize_Z.config(state='disabled')


    def TGTypeCont(self, TGType):
        if TGType == 'RandomDependent':
            self.MappingOption.grid_forget()
            del self.MappingOption
            self.Mapping.set('Please Select...')
            self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *self.MappingDict['RandomDependent'],
                                                    command=self.MappingAlgCont)
            self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)
            self.MappingOption.config(width=self.OptionMenuWidth)
            self.ClearMapping()

            self.NumOfTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+2)
            self.NumOfTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+2)
            self.NumOfTasks.delete(0, 'end')
            self.NumOfTasks.insert(0, '35')

            self.NumOfCritTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+3)
            self.NumOfCritTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+3)
            self.NumOfCritTasks.delete(0, 'end')
            self.NumOfCritTasks.insert(0, '0')

            self.NumOfEdge_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+4)
            self.NumOfEdge.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+4)
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

            self.TGBrowse.grid_forget()
            self.TGBrowseButton.grid_forget()

        elif TGType == 'RandomIndependent':
            self.MappingOption.grid_forget()
            del self.MappingOption
            self.Mapping.set('Please Select...')
            self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *self.MappingDict['RandomIndependent'],
                                                    command=self.MappingAlgCont)
            self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)
            self.MappingOption.config(width=self.OptionMenuWidth)
            self.ClearMapping()

            self.NumOfTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+2)
            self.NumOfTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+2)
            self.NumOfTasks.delete(0, 'end')
            self.NumOfTasks.insert(0, '35')

            self.NumOfCritTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+3)
            self.NumOfCritTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+3)
            self.NumOfCritTasks.delete(0, 'end')
            self.NumOfCritTasks.insert(0, '0')

            self.WCET_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+4)
            self.WCET_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+4)
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

            self.TGBrowse.grid_forget()
            self.TGBrowseButton.grid_forget()

        elif TGType == 'Manual':
            self.MappingOption.grid_forget()
            del self.MappingOption
            self.Mapping.set('Please Select...')
            self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *self.MappingDict['Manual'],
                                                    command=self.MappingAlgCont)
            self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)
            self.MappingOption.config(width=self.OptionMenuWidth)
            self.ClearMapping()

            self.TGBrowse.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+2, sticky='e')
            self.TGBrowseButton.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+2)

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

    def AllVizFunc(self):
        if self.AllViz.get():
            self.PMCG_Draw.set(True)
            self.Mapping_Draw.set(True)
            self.RG_Draw.set(True)
            self.SHM_Draw.set(True)
            self.TTG_Draw.set(True)
        else:
            self.PMCG_Draw.set(False)
            self.Mapping_Draw.set(False)
            self.RG_Draw.set(False)
            self.SHM_Draw.set(False)
            self.TTG_Draw.set(False)

    def GetTGFile(self):
        Path = tkFileDialog.askopenfilename()
        if Path:
            self.TGBrowse.delete(0,'end')
            self.TGBrowse.insert(1, Path)

    def GetRoutingFile(self):
        Path = tkFileDialog.askopenfilename()
        if Path:
            self.RoutingBrowse.delete(0,'end')
            self.RoutingBrowse.insert(1, Path)

    def VLPlacementFunc(self):
        if self.VLPlacementEnable.get():
            self.VLP_Alg_Label.grid(column=self.VLPlacement_StartingCol,
                                    row=self.VLPlacement_StartingRow+2, sticky='w')
            self.VLP_AlgOption.grid(column=self.VLPlacement_StartingCol+1,
                                    row=self.VLPlacement_StartingRow+2, sticky='w')
            self.NumOfVLs_Label.grid(column=self.VLPlacement_StartingCol,
                                     row=self.VLPlacement_StartingRow+3, sticky='w')
            self.NumOfVLs.grid(column=self.VLPlacement_StartingCol+1,
                               row=self.VLPlacement_StartingRow+3, sticky='w')
            self.NumOfVLs.delete(0,'end')
            self.NumOfVLs.insert(0, '5')

            self.VLP_IterationsLS_Label.grid(column=self.VLPlacement_StartingCol,
                                             row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.grid(column=self.VLPlacement_StartingCol+1,
                                       row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.delete(0,'end')
            self.VLP_IterationsLS.insert(0, '10')

        else:
            self.VLP_Alg_Label.grid_forget()
            self.VLP_AlgOption.grid_forget()
            self.NumOfVLs_Label.grid_forget()
            self.NumOfVLs.grid_forget()
            self.VLP_IterationsLS_Label.grid_forget()
            self.VLP_IterationsLS.grid_forget()
            self.VLP_IterationsILS_Label.grid_forget()
            self.VLP_IterationsILS.grid_forget()
    def PMCFunc(self):
        if self.PMCEnable.get():
            self.PMCType_Label.grid(column=self.PMC_StartingCol, row=self.PMC_StartingRow+2, sticky='w')
            self.PMCTypeOption.grid(column=self.PMC_StartingCol+1, row=self.PMC_StartingRow+2, sticky='w')
        else:
            self.PMCType_Label.grid_forget()
            self.PMCTypeOption.grid_forget()

    def TfaultControl(self, PMCType):
        if self.PMCType.get()=='One Step Diagnosable':
            self.TfaultDiagnosable_Label.grid(column=self.PMC_StartingCol, row=self.PMC_StartingRow+3, sticky='w')
            self.TfaultDiagnosable.grid(column=self.PMC_StartingCol+1, row=self.PMC_StartingRow+3, sticky='w')
        else:
            self.TfaultDiagnosable_Label.grid_forget()
            self.TfaultDiagnosable.grid_forget()

    def VLPAlgFunc(self, VLP_Alg):
        if self.VLP_Alg.get()=='LocalSearch':
            self.VLP_IterationsLS_Label.grid(column=self.VLPlacement_StartingCol,
                                             row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.grid(column=self.VLPlacement_StartingCol+1,
                                       row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.delete(0, 'end')
            self.VLP_IterationsLS.insert(0, '10')

            self.VLP_IterationsILS_Label.grid_forget()
            self.VLP_IterationsILS.grid_forget()

        elif self.VLP_Alg.get()=='IterativeLocalSearch':
            self.VLP_IterationsLS_Label.grid(column=self.VLPlacement_StartingCol,
                                             row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.grid(column=self.VLPlacement_StartingCol+1,
                                       row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.delete(0, 'end')
            self.VLP_IterationsLS.insert(0, '10')

            self.VLP_IterationsILS_Label.grid(column=self.VLPlacement_StartingCol,
                                              row=self.VLPlacement_StartingRow+5, sticky='w')
            self.VLP_IterationsILS.grid(column=self.VLPlacement_StartingCol+1,
                                        row=self.VLPlacement_StartingRow+5, sticky='w')
            self.VLP_IterationsILS.delete(0, 'end')
            self.VLP_IterationsILS.insert(0, '10')

    def RoutingFunc(self, Routing):
        if self.RoutingAlg.get() in ['XY', 'XYZ']:
            self.RoutingTypeOption.config(state='disable')
        else:
            self.RoutingTypeOption.config(state='normal')

        if self.RoutingAlg.get() == 'From File':
            self.RoutingBrowse.grid(column = self.Routing_StartingCol, row=self.Routing_StartingRow+3, sticky='e')
            self.RoutingBrowseButton.grid(column = self.Routing_StartingCol+1, row=self.Routing_StartingRow+3)
        else:
            self.RoutingBrowse.grid_forget()
            self.RoutingBrowseButton.grid_forget()

    def ClusteringCont(self):
        if self.ClusteringOptVar.get():
            self.ClusteringIterLabel.grid(column=self.Cl_OptStartCol, row=self.Cl_OptStartRow+2)
            self.ClusteringIterations.grid(column=self.Cl_OptStartCol+1, row=self.Cl_OptStartRow+2)
            self.ClusteringIterations.delete(0, 'end')
            self.ClusteringIterations.insert(0, '1000')

            self.ClusteringCostLabel.grid(column=self.Cl_OptStartCol, row=self.Cl_OptStartRow+3)
            self.ClusterCostOpt.grid(column=self.Cl_OptStartCol+1, row=self.Cl_OptStartRow+3)
        else:
            self.ClusteringIterLabel.grid_forget()
            self.ClusteringIterations.grid_forget()
            self.ClusteringCostLabel.grid_forget()
            self.ClusterCostOpt.grid_forget()

    def ClearMapping(self):
        self.Clear_SA_Mapping()
        self.LS_Iter_Label.grid_forget()
        self.LS_Iter.grid_forget()
        self.ILS_Iter_Label.grid_forget()
        self.ILS_Iter.grid_forget()
        self.MappingCostLabel.grid_forget()
        self.MappingCostOpt.grid_forget()


    def MappingAlgCont(self, Mapping):
        if self.Mapping.get() in ['SimulatedAnnealing','LocalSearch','IterativeLocalSearch']:
            self.MappingCostLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+2)
            self.MappingCostOpt.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+2)
        else:
            self.MappingCostLabel.grid_forget()
            self.MappingCostOpt.grid_forget()

        if self.Mapping.get() == 'SimulatedAnnealing':
            self.Clear_SA_Mapping()
            self.Annealing.set('Linear')
            self.SA_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+3)
            self.AnnealingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+3)

            self.SA_InitTemp.delete(0, 'end')
            self.SA_InitTemp.insert(0, '100')
            self.SA_InitTemp_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+4)
            self.SA_InitTemp.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+4)

            self.Termination.set('StopTemp')
            self.SA_Term_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+5)
            self.TerminationOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+5)

            self.SA_Iterations.delete(0, 'end')
            self.SA_Iterations.insert(0, '100000')
            self.SA_IterLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+6)
            self.SA_Iterations.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+6)

        else:
            self.Clear_SA_Mapping()

        if self.Mapping.get() in ['LocalSearch','IterativeLocalSearch']:
            self.LS_Iter.delete(0, 'end')
            self.LS_Iter.insert(0, '100')
            self.LS_Iter_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+3)
            self.LS_Iter.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+3)
        else:
            self.LS_Iter_Label.grid_forget()
            self.LS_Iter.grid_forget()

        if self.Mapping.get()=='IterativeLocalSearch':
            self.ILS_Iter.delete(0, 'end')
            self.ILS_Iter.insert(0, '10')
            self.ILS_Iter_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+4)
            self.ILS_Iter.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+4)

        else:
            self.ILS_Iter_Label.grid_forget()
            self.ILS_Iter.grid_forget()

    def Annealing_Termination(self, Annealing):
        if self.Mapping.get() == 'SimulatedAnnealing':
            if self.Annealing.get()=='Linear' or self.Termination.get()=='IterationNum':
                self.SA_StopTemp.grid_forget()
                self.SA_StopTemp_Label.grid_forget()

                self.SA_IterLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+6)
                self.SA_Iterations.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+6)

            elif self.Termination.get()=='StopTemp' and self.Annealing.get() != 'Linear':
                self.SA_Iterations.grid_forget()
                self.SA_IterLabel.grid_forget()

                self.SA_StopTemp.delete(0, 'end')
                self.SA_StopTemp.insert(0, '5')
                self.SA_StopTemp_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+6)
                self.SA_StopTemp.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+6)
            else:
                self.SA_StopTemp.grid_forget()
                self.SA_StopTemp_Label.grid_forget()

                self.SA_Iterations.grid_forget()
                self.SA_IterLabel.grid_forget()

            if self.Annealing.get() in ['Exponential','Adaptive','Aart', 'Huang']:
                self.SA_Alpha.delete(0, 'end')
                self.SA_Alpha.insert(0, '0.999')
                self.SA_Alpha_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+7)
                self.SA_Alpha.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+7)
            else:
                self.SA_Alpha_Label.grid_forget()
                self.SA_Alpha.grid_forget()

            if self.Annealing.get() == 'Logarithmic':
                self.SA_LoG_Const.delete(0, 'end')
                self.SA_LoG_Const.insert(0, '1000')
                self.SA_LoG_Const_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+7)
                self.SA_LoG_Const.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+7)
            else:
                self.SA_LoG_Const_Label.grid_forget()
                self.SA_LoG_Const.grid_forget()

            if self.Annealing.get() == 'Adaptive':

                self.CostMonitorSlope.delete(0, 'end')
                self.CostMonitorSlope.insert(0, '0.02')
                self.CostMonitorSlope_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+9)
                self.CostMonitorSlope.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+9)

                self.MaxSteadyState.delete(0, 'end')
                self.MaxSteadyState.insert(0, '30000')
                self.MaxSteadyState_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+10)
                self.MaxSteadyState.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+10)
            else:
                self.MaxSteadyState_Label.grid_forget()
                self.MaxSteadyState.grid_forget()

                self.CostMonitorSlope_Label.grid_forget()
                self.CostMonitorSlope.grid_forget()

            if self.Annealing.get() == 'Markov':
                self.MarkovNum.delete(0, 'end')
                self.MarkovNum.insert(0, '2000')
                self.MarkovNum_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+7)
                self.MarkovNum.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+7)

                self.MarkovTempStep.delete(0, 'end')
                self.MarkovTempStep.insert(0, '1')
                self.MarkovTempStep_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+8)
                self.MarkovTempStep.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+8)
            else:
                self.MarkovNum_Label.grid_forget()
                self.MarkovNum.grid_forget()

                self.MarkovTempStep_Label.grid_forget()
                self.MarkovTempStep.grid_forget()

            if self.Annealing.get() in ['Aart', 'Adaptive', 'Huang']:
                self.CostMonitor.delete(0, 'end')
                self.CostMonitor.insert(0, '2000')
                self.CostMonitor_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+8)
                self.CostMonitor.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+8)
            else:
                self.CostMonitor_Label.grid_forget()
                self.CostMonitor.grid_forget()

            if self.Annealing.get() in ['Aart', 'Huang']:
                self.SA_Delta.delete(0, 'end')
                self.SA_Delta.insert(0, '0.05')
                self.SA_Delta_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+9)
                self.SA_Delta.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+9)
            else:
                self.SA_Delta_Label.grid_forget()
                self.SA_Delta.grid_forget()

    def Clear_SA_Mapping(self):
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

        self.SA_Alpha_Label.grid_forget()
        self.SA_Alpha.grid_forget()

        self.SA_LoG_Const_Label.grid_forget()
        self.SA_LoG_Const.grid_forget()

        self.SA_Delta_Label.grid_forget()
        self.SA_Delta.grid_forget()

        self.MaxSteadyState_Label.grid_forget()
        self.MaxSteadyState.grid_forget()

        self.CostMonitorSlope_Label.grid_forget()
        self.CostMonitorSlope.grid_forget()

        self.CostMonitor_Label.grid_forget()
        self.CostMonitor.grid_forget()

        self.MarkovNum_Label.grid_forget()
        self.MarkovNum.grid_forget()

        self.MarkovTempStep_Label.grid_forget()
        self.MarkovTempStep.grid_forget()

    def Fault_Injection(self):
        if self.FaultInjection.get():
            self.MTBF_Label.grid(column=self.Fault_StartingCol, row=self.Fault_StartingRow+2)
            self.MTBF.grid(column=self.Fault_StartingCol+1, row=self.Fault_StartingRow+2)

            self.SDMTBF_Label.grid(column=self.Fault_StartingCol, row=self.Fault_StartingRow+3)
            self.SDMTBF.grid(column=self.Fault_StartingCol+1, row=self.Fault_StartingRow+3)

            self.RunTime_Label.grid(column=self.Fault_StartingCol, row=self.Fault_StartingRow+4)
            self.RunTime.grid(column=self.Fault_StartingCol+1, row=self.Fault_StartingRow+4)
        else:
            self.MTBF_Label.grid_forget()
            self.MTBF.grid_forget()
            self.SDMTBF_Label.grid_forget()
            self.SDMTBF.grid_forget()
            self.RunTime_Label.grid_forget()
            self.RunTime.grid_forget()


    def CheckForErrors(self):
        if self.Mapping.get() == 'Please Select...':
            self.ErrorMessage.config(text="Please Select Mapping Algorithm!")
            return False

        elif self.RoutingAlg.get() == 'Please Select...':
            self.ErrorMessage.config(text="Please Select Routing Algorithm!")
            return False

        elif self.RoutingType.get() == 'Please Select...':
            if self.RoutingAlg.get() not in ['XY', 'XYZ']:
                self.ErrorMessage.config(text="Please Select Routing Type!")
                return False
            else:
                self.ErrorMessage.config(text ="")
                return True
        elif self.RoutingAlg.get() == 'From File':
            if self.RoutingBrowse.get() == 'Routing File Path...':
                self.ErrorMessage.config(text="Please Select Routing File!")
                return False
        elif int(self.NetworkSize_Z.get()) <2 and '3D' in self.Topology.get():
            if self.VLPlacementEnable.get():
                self.ErrorMessage.config(text="Can not optimize VL placement for 1 layer NoC")
                return False
        else:
            self.ErrorMessage.config(text="")
            return True

    def on_enter(self, event):
        tkMessageBox.showinfo("License Message", "The logo picture is a derivative of \"Sea Ghost\" by Joey Gannon, " +
                              "used under CC BY-SA. The original version can be found here: " +
                              "https://www.flickr.com/photos/brunkfordbraun/679827214 " +
                              "This work is under same license as the original."
                              "(https://creativecommons.org/licenses/by-sa/2.0/)")

    def AnimationConfig(self):
        if self.AnimEnable.get() == True:
            self.FrameRezLabel.grid(column=self.Anim_StartingCol, row=self.Anim_StartingRow+2)
            self.FrameRez.grid(column=self.Anim_StartingCol+1, row=self.Anim_StartingRow+2)
        else:
            self.FrameRez.grid_forget()
            self.FrameRezLabel.grid_forget()

    def ApplyButton(self):
        # apply changes...
        if self.CheckForErrors():
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
            Config.ClusteringIteration = int(self.ClusteringIterations.get())
            Config.Clustering_Optimization = self.ClusteringOptVar.get()
            Config.Clustering_CostFunctionType = self.ClusterCost.get()

            # Mapping Config

            Config.Mapping_CostFunctionType = self.MappingCost.get()

            Config.LocalSearchIteration = int(self.LS_Iter.get())
            Config.IterativeLocalSearchIterations = int(self.ILS_Iter.get())

            Config.Mapping_Function = self.Mapping.get()
            Config.SA_AnnealingSchedule = self.Annealing.get()
            Config.TerminationCriteria = self.Termination.get()
            Config.SimulatedAnnealingIteration = int(self.SA_Iterations.get())
            Config.SA_InitialTemp = int(self.SA_InitTemp.get())
            Config.SA_StopTemp = int(self.SA_StopTemp.get())
            Config.SA_Alpha = float(self.SA_Alpha.get())
            Config.LogCoolingConstant = int(self.SA_LoG_Const.get())
            Config.CostMonitorQueSize = int(self.CostMonitor.get())
            Config.SlopeRangeForCooling = float(self.CostMonitorSlope.get())
            Config.MaxSteadyState = int(self.MaxSteadyState.get())
            Config.MarkovTempStep = float(self.MarkovTempStep.get())
            Config.MarkovNum = int(self.MarkovNum.get())
            Config.Delta = float(self.SA_Delta.get())

            # Fault Config
            Config.EventDrivenFaultInjection = self.FaultInjection.get()
            Config.MTBF = float(self.MTBF.get())
            Config.SD4MTBF = float(self.SDMTBF.get())
            Config.ProgramRunTime = float(self.RunTime.get())

            # Viz Config
            Config.Mapping_Drawing = self.Mapping_Draw.get()
            Config.RG_Draw = self.RG_Draw.get()
            Config.SHM_Drawing = self.SHM_Draw.get()
            Config.PMCG_Drawing = self.PMCG_Draw.get()
            Config.TTG_Drawing = self.TTG_Draw.get()

            Config.GenMappingFrames = self.AnimEnable.get()
            Config.FrameResolution = int(self.FrameRez.get())

            # Routing
            if self.Topology.get() == 'From File':
                Config.SetRoutingFromFile = True
                Config.RoutingFilePath = self.RoutingBrowse.get()
            else:
                if '3D' in self.Topology.get():
                    if self.RoutingAlg.get() == 'Negative First':
                        Config.UsedTurnModel = PackageFile.NegativeFirst3D_TurnModel
                    elif self.RoutingAlg.get() == 'XYZ':
                        Config.UsedTurnModel = PackageFile.XYZ_TurnModel
                elif '2D' in self.Topology.get():
                    if self.RoutingAlg.get() == 'XY':
                        Config.UsedTurnModel = PackageFile.XY_TurnModel
                    elif self.RoutingAlg.get() == 'West First':
                        Config.UsedTurnModel = PackageFile.WestFirst_TurnModel
                    elif self.RoutingAlg.get() == 'North Last':
                        Config.UsedTurnModel = PackageFile.NorthLast_TurnModel
                    elif self.RoutingAlg.get() == 'Negative First':
                        Config.UsedTurnModel = PackageFile.NegativeFirst2D_TurnModel

                if self.RoutingAlg.get() in ['XY', 'XYZ']:
                    if self.RoutingType.get() == 'Please Select...':
                        Config.RotingType = 'MinimalPath'
                else:
                    Config.RotingType = self.RoutingType.get()

            # VL Placement
            Config.FindOptimumAG = self.VLPlacementEnable.get()
            if self.VLPlacementEnable.get():
                Config.VL_OptAlg = self.VLP_Alg.get()
                Config.VerticalLinksNum = int(self.NumOfVLs.get())

            # dependability Config
            Config.SlackCount = int(self.SlackNumber.get())
            Config.NumberOfRects = int(self.NumberOfRects.get())

            # PMC Config
            if self.PMCEnable.get():
                Config.GeneratePMCG = self.PMCEnable.get()
                if self.PMCType.get() == 'One Step Diagnosable':
                    Config.OneStepDiagnosable = True
                    Config.OneStepDiagnosable = int(self.TfaultDiagnosable.get())
                else:
                    Config.OneStepDiagnosable = False

            self.Apply_Button = True
            self.destroy()

    def CancelButton(self):
        self.destroy()