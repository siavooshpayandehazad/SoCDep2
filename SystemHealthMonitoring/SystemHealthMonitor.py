# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import hashlib
import copy
from Mapper import Mapping_Functions
import SHM_Reports,SHM_Functions

class SystemHealthMonitor:
    def __init__(self):
        self.SHM = networkx.DiGraph()   # System Health Map
        self.SnapShot = None
        self.MPM={}                     # Most Probable Mapping Lib

    def SetUp_NoC_SystemHealthMap(self, ArchGraph, TurnsHealth):
        print "==========================================="
        print "PREPARING SYSTEM HEALTH MAP..."
        for nodes in ArchGraph.nodes():
            self.SHM.add_node(nodes, TurnsHealth=copy.deepcopy(TurnsHealth), NodeHealth=True, NodeSpeed=100)
        for link in ArchGraph.edges():
            self.SHM.add_edge(link[0], link[1], LinkHealth=True)
        print "SYSTEM HEALTH MAP CREATED..."

    ##################################################
    def BreakLink(self,link,Report):
        if Report:print "==========================================="
        if Report:print "\033[33mSHM::\033[0m BREAKING LINK:", link
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = False

    def RestoreBrokenLink(self, link, Report):
        if Report:print "==========================================="
        if Report:print "\033[33mSHM::\033[0m LINK:", link, "RESTORED..."
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = True

    ##################################################
    def BreakTurn(self, Node, Turn, Report):
        if Report:print "==========================================="
        if Report:print "\033[33mSHM::\033[0m BREAKING TURN:", Turn, "IN NODE", Node
        self.SHM.node[Node]['TurnsHealth'][Turn] = False

    def RestoreBrokenTurn(self, Node, Turn, Report):
        if Report:print "==========================================="
        if Report:print "\033[33mSHM::\033[0m TURN:", Turn, "IN NODE", Node, "RESTORED"
        self.SHM.node[Node]['TurnsHealth'][Turn] = True

    ##################################################
    def IntroduceAging(self, Node, SpeedDown, Report):
        if Report: print "==========================================="
        self.SHM.node[Node]['NodeSpeed'] = self.SHM.node[Node]['NodeSpeed']*(1-SpeedDown)
        if Report: print "\033[33mSHM::\033[0m AGEING NODE:", Node, "... SPEED DROPPED TO:", self.SHM.node[Node]['NodeSpeed'], "%"
        if self.SHM.node[Node]['NodeSpeed'] == 0:
            self.BreakNode(Node, True)

    ##################################################
    def BreakNode(self, Node, Report):
        if Report: print "==========================================="
        self.SHM.node[Node]['NodeHealth'] = False
        if Report: print "\033[33mSHM::\033[0m NODE", Node, "IS BROKEN..."

    def RestoreBrokenNode(self, Node, Report):
        if Report: print "==========================================="
        self.SHM.node[Node]['NodeHealth'] = False
        if Report: print "\033[33mSHM::\033[0m NODE", Node, "IS RESTORED..."

    ##################################################
    def TakeSnapShotOfSystemHealth(self):
        self.SnapShot = copy.deepcopy(self.SHM)
        print "A SNAPSHOT OF SYSTEM HEALTH HAS BEEN STORED..."
        return None
    
    ##################################################
    def RestoreToPreviousSnapShot (self):
        self.SHM = copy.deepcopy(self.SnapShot)
        print "SYSTEM HEALTH MAP HAS BEEN RESTORED TO PREVIOUS SNAPSHOT..."
        self.SnapShot = None
        return None

    ##################################################
    def AddCurrentMappingToMPM (self, TG):
        """
        Adds a mapping (Extracted from TG) under a fault configuration to MPM.
        The dictionary key would be the hash of fault config
        :param TG: Task Graph
        :return: None
        """
        MappingString = Mapping_Functions.MappingIntoString(TG)
        self.MPM[hashlib.md5(SHM_Functions.GenerateFaultConfig(self)).hexdigest()] = MappingString
        return None

    ##################################################
    def CleanMPM(self):
        self.MPM={}
        return None

    ##################################################
    def ApplyFaultEvent(self, FaultLocation, FaultType):
        SHM_Reports.ReportTheEvent(FaultLocation, FaultType)
        if type(FaultLocation) is tuple:      # its a Link fault
            if FaultType == 'T':    # Transient Fault
                if self.SHM.edge[FaultLocation[0]][FaultLocation[1]]['LinkHealth']:
                    self.BreakLink(FaultLocation, True)
                    self.RestoreBrokenLink(FaultLocation, True)
                else:
                    print "\033[33mSHM:: NOTE:\033[0mLINK ALREADY BROKEN"
            elif FaultType == 'P':   # Permanent Fault
                self.BreakLink(FaultLocation, True)
        elif type(FaultLocation) is dict:   # its a Turn fault
            if FaultType == 'T':    # Transient Fault
                if self.SHM.node[FaultLocation.keys()[0]]['TurnsHealth'][FaultLocation[FaultLocation.keys()[0]]]:
                    self.BreakTurn(FaultLocation.keys()[0], FaultLocation[FaultLocation.keys()[0]], True)
                    self.RestoreBrokenTurn(FaultLocation.keys()[0], FaultLocation[FaultLocation.keys()[0]], True)
                else:
                    print "\033[33mSHM:: NOTE:\033[0mTURN ALREADY BROKEN"
            elif FaultType == 'P':   # Permanent Fault
                self.BreakTurn(FaultLocation.keys()[0], FaultLocation[FaultLocation.keys()[0]], True)
        else:           # its a Node fault
            if FaultType == 'T':    # Transient Fault
                if self.SHM.node[FaultLocation]['NodeHealth']:
                    self.BreakNode(FaultLocation, True)
                    self.RestoreBrokenNode(FaultLocation, True)
                else:
                    print "\033[33mSHM:: NOTE:\033[0m NODE ALREADY BROKEN"
            elif FaultType == 'P':   # Permanent Fault
                self.BreakNode(FaultLocation, True)
        return None

    # ToDO: To implement the classification algorithm
    # ToDo: To implement the partial mapping with distance driven cost function