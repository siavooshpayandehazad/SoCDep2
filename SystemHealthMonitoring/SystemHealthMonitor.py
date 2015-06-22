# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import hashlib
import copy,random
from ConfigAndPackages import Config
from Mapper import Mapping_Functions

class SystemHealthMonitor:
    def __init__(self):
        self.SHM = networkx.DiGraph()   # System Health Map
        self.SnapShot = None
        self.MPM={}                     # Most Probable Mapping Lib

    def SetUp_NoC_SystemHealthMap(self,ArchGraph,TurnsHealth):
        print "==========================================="
        print "PREPARING SYSTEM HEALTH MAP..."
        for nodes in ArchGraph.nodes():
            self.SHM.add_node(nodes, TurnsHealth=copy.deepcopy(TurnsHealth), NodeHealth=True, NodeSpeed=100)
        for link in ArchGraph.edges():
            self.SHM.add_edge(link[0], link[1], LinkHealth=True)
        print "SYSTEM HEALTH MAP CREATED..."

    def Report_NoC_SystemHealthMap(self):
        print "==========================================="
        print "      REPORTING SYSTEM HEALTH MAP"
        print "==========================================="
        for Node in self.SHM.nodes():
            print "\tNODE:" ,Node
            print "\t\tNODE HEALTH:", self.SHM.node[Node]['NodeHealth']
            print "\t\tNODE SPEED:", self.SHM.node[Node]['NodeSpeed']
            print "\t\tTURNS:", self.SHM.node[Node]['TurnsHealth']
            print "\t=============="
        for Edge in self.SHM.edges():
            print "\tLINK:", Edge, "\t", self.SHM.edge[Edge[0]][Edge[1]]['LinkHealth']

    ##################################################
    def BreakLink(self,link,Report):
        if Report:print "==========================================="
        if Report:print "\033[33mSYSTEM HEALTH MAP::\033[0m BREAKING LINK:", link
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = False

    def RestoreBrokenLink(self, link, Report):
        if Report:print "==========================================="
        if Report:print "\033[33mSYSTEM HEALTH MAP::\033[0m LINK:", link, "RESTORED..."
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = True

    ##################################################
    def BreakTurn(self, Node, Turn, Report):
        if Report:print "==========================================="
        if Report:print "\033[33mSYSTEM HEALTH MAP::\033[0m BREAKING TURN:",Turn, "IN NODE", Node
        self.SHM.node[Node]['TurnsHealth'][Turn]=False

    def RestoreBrokenTurn(self, Node, Turn, Report):
        if Report:print "==========================================="
        if Report:print "\033[33mSYSTEM HEALTH MAP::\033[0m TURN:", Turn, "IN NODE", Node, "RESTORED"
        self.SHM.node[Node]['TurnsHealth'][Turn] = True

    ##################################################
    def IntroduceAging(self, Node, SpeedDown, Report):
        if Report: print "==========================================="
        self.SHM.node[Node]['NodeSpeed'] = self.SHM.node[Node]['NodeSpeed']*(1-SpeedDown)
        if Report: print "\033[33mSYSTEM HEALTH MAP::\033[0m AGEING NODE:", Node, "... SPEED DROPPED TO:", self.SHM.node[Node]['NodeSpeed'], "%"
        if self.SHM.node[Node]['NodeSpeed'] == 0:
            self.BreakNode(Node, True)

    ##################################################
    def BreakNode(self, Node, Report):
        if Report: print "==========================================="
        self.SHM.node[Node]['NodeHealth']=False
        if Report: print "\033[33mSYSTEM HEALTH MAP::\033[0m NODE",Node,"IS BROKEN..."

    def RestoreBrokenNode(self, Node, Report):
        if Report: print "==========================================="
        self.SHM.node[Node]['NodeHealth']=False
        if Report: print "\033[33mSYSTEM HEALTH MAP::\033[0m NODE",Node,"IS RESTORED..."

    ##################################################
    def TakeSnapShotOfSystemHealth(self):
        self.SnapShot = copy.deepcopy(self.SHM)
        print "A SNAPSHOT OF SYSTEM HEALTH HAS BEEN STORED..."
        return None

    def RestoreToPreviousSnapShot (self):
        self.SHM = copy.deepcopy(self.SnapShot)
        print "SYSTEM HEALTH MAP HAS BEEN RESTORED TO PREVIOUS SNAPSHOT..."
        self.SnapShot = None
        return None

    ##################################################
    def GenerateFaultConfig (self):
        """
        Generates a string (FaultConfig) from the configuration of the faults in the SHM
        :return: FaultConfig string
        """
        FaultConfig = ""
        for node in self.SHM.nodes():
            FaultConfig += str(node)
            FaultConfig += "T" if self.SHM.node[node]['NodeHealth'] else "F"
            FaultConfig += str(int(self.SHM.node[node]['NodeSpeed']))
            for Turn in self.SHM.node[node]['TurnsHealth']:
                FaultConfig += "T" if self.SHM.node[node]['TurnsHealth'][Turn] else "F"
        return FaultConfig

    ##################################################
    def AddCurrentMappingToMPM (self, TG):
        """
        Adds a mapping (Extracted from TG) under a fault configuration to MPM.
        The dictionary key would be the hash of fault config
        :param TG: Task Graph
        :return: None
        """
        MappingString = Mapping_Functions.MappingIntoString(TG)
        self.MPM[hashlib.md5(self.GenerateFaultConfig()).hexdigest()] = MappingString
        return None

    ##################################################
    def ReportMPM(self):
        print "==========================================="
        print "      REPORTING MOST PROBABLE MAPPING "
        print "==========================================="
        for item in self.MPM:
            print "KEY:",item,"\t\tMAPPING:",self.MPM[item]
        return None

    ##################################################
    def CleanMPM(self):
        self.MPM={}
        return None

    ##################################################
    def ApplyInitialFaults(self):
        for BrokenLink in Config.ListOfBrokenLinks:
            self.BreakLink(BrokenLink,True)

        for NodeWithBrokenTurn in Config.ListOfBrokenTurns:
            self.BreakTurn(NodeWithBrokenTurn,Config.ListOfBrokenTurns[NodeWithBrokenTurn],True)

        for AgedPE in Config.ListOfAgedPEs:
            self.IntroduceAging(AgedPE, Config.ListOfAgedPEs[AgedPE],True)

        for BrokenNode in Config.ListOfBrokenPEs:
            self.BreakNode(BrokenNode,True)

    ##################################################
    def RandomFaultInjection(self):
        ChosenFault = random.choice(['Link','Turn','PE','Age'])
        if ChosenFault == 'Link':
            ChosenLink = random.choice(self.SHM.edges())
            self.BreakLink(ChosenLink,True)
        elif ChosenFault == 'Turn':
            ChosenNode = random.choice(self.SHM.nodes())
            ChosenTurn = random.choice(self.SHM.node[ChosenNode]['TurnsHealth'].keys())
            self.BreakTurn(ChosenNode,ChosenTurn,True)
        elif ChosenFault == 'PE':
            ChosenNode = random.choice(self.SHM.nodes())
            self.BreakNode(ChosenNode,True)
        elif ChosenFault == 'Age':
            ChosenNode = random.choice(self.SHM.nodes())
            RandomSpeedDown = random.choice([0.3, 0.25, 0.2, 0.15, 0.1, 0.05])
            self.IntroduceAging(ChosenNode, RandomSpeedDown ,True)

    # ToDo: To insert Transient Faults... (probably we need some event handler)
    # ToDo: To implement Intermittent Faults
    # ToDO: To implement the classification algorithm
    # ToDo: To implement the partial mapping with distance driven cost function