# Copyright (C) Siavoosh Payandeh Azad


import Tkinter

class ConfigAppp(Tkinter.Tk):

    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()


    def initialize(self):
        self.grid()

        AvailableTopologies = ['2DTorus', '2DMesh', '2DLine', '2DRing', '3DMesh']
        Topology = Tkinter.StringVar()
        Topology.set('2DMesh')
        TopologyOption = Tkinter.OptionMenu(self, Topology, *AvailableTopologies
                                            ,command=self.NetworkSizeCont)
        TopologyOption.grid(column=0,row=0)

        NetworkSize_X = Tkinter.Spinbox(self, from_=0, to=10)
        NetworkSize_Y = Tkinter.Spinbox(self, from_=0, to=10)
        NetworkSize_Z = Tkinter.Spinbox(self, from_=0, to=10)

        NetworkSize_X.grid(column=1,row=0)
        NetworkSize_Y.grid(column=1,row=1)
        NetworkSize_Z.grid(column=1,row=2)


        quitButton = Tkinter.Button(self, text="Apply", command=self.ApplyButton)
        quitButton.grid(column=1,row=5)

        quitButton = Tkinter.Button(self, text="cancel", command=self.CancelButton)
        quitButton.grid(column=2,row=5)

    def NetworkSizeCont(self, Topology):
        if '3D' in Topology:
            self.NetworkSize_Z.config(state='normal')
        else:
            self.NetworkSize_Z.config(state='disabled')


    def ApplyButton(self):
        # apply changes...
        self.destroy()

    def CancelButton(self):
        self.destroy()