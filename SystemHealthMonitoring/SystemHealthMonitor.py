# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import hashlib
import copy, re
from Mapper import Mapping_Functions
import SHM_Reports,SHM_Functions
from ConfigAndPackages import Config

class SystemHealthMonitor:
    def __init__(self):
        self.SHM = networkx.DiGraph()   # System Health Map
        self.SnapShot = None
        self.MPM={}                     # Most Probable Mapping Lib

    def SetUp_NoC_SystemHealthMap(self, ArchGraph, TurnsHealth):
        print ("===========================================")
        print ("PREPARING SYSTEM HEALTH MAP...")
        if not Config.SetRoutingFromFile:
            for node in ArchGraph.nodes():
                self.SHM.add_node(node, TurnsHealth=copy.deepcopy(TurnsHealth), NodeHealth=True, NodeSpeed=100)
        else:
            try:
                RoutingFile = open(Config.RoutingFilePath, 'r')
            except IOError:
                print ('CAN NOT OPEN', Config.RoutingFilePath)

            while True:
                line = RoutingFile.readline()
                if "Ports" in line:
                    Ports = RoutingFile.readline()
                    PortList = Ports.split( )
                    print ("PortList", PortList)
                if "Node" in line:
                    NodeID = int(re.search(r'\d+', line).group())
                    NodeTurnsHealth = copy.deepcopy(TurnsHealth)
                    line = RoutingFile.readline()
                    TurnsList = line.split()
                    for turn in NodeTurnsHealth.keys():
                        if turn not in TurnsList:
                            NodeTurnsHealth[turn] = False
                    self.SHM.add_node(NodeID, TurnsHealth=copy.deepcopy(NodeTurnsHealth), NodeHealth=True, NodeSpeed=100)
                if line == '':
                    break
            for node in ArchGraph.nodes():
                if node not in self.SHM.nodes():
                    self.SHM.add_node(node, TurnsHealth=copy.deepcopy(TurnsHealth), NodeHealth=True, NodeSpeed=100)
        for link in ArchGraph.edges():
            self.SHM.add_edge(link[0], link[1], LinkHealth=True)
        print ("SYSTEM HEALTH MAP CREATED...")

    ##################################################
    def BreakLink(self,link,Report):
        if Report:print ("===========================================")
        if Report:print ("\033[33mSHM::\033[0m BREAKING LINK:", link)
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = False

    def RestoreBrokenLink(self, link, Report):
        if Report:print ("===========================================")
        if Report:print ("\033[33mSHM::\033[0m LINK:", link, "RESTORED...")
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = True

    ##################################################
    def BreakTurn(self, Node, Turn, Report):
        if Report:print ("===========================================")
        if Report:print ("\033[33mSHM::\033[0m BREAKING TURN:", Turn, "IN NODE", Node)
        self.SHM.node[Node]['TurnsHealth'][Turn] = False

    def RestoreBrokenTurn(self, Node, Turn, Report):
        if Report:print ("===========================================")
        if Report:print ("\033[33mSHM::\033[0m TURN:", Turn, "IN NODE", Node, "RESTORED")
        self.SHM.node[Node]['TurnsHealth'][Turn] = True

    ##################################################
    def IntroduceAging(self, Node, SpeedDown, Report):
        if Report: print ("===========================================")
        self.SHM.node[Node]['NodeSpeed'] = self.SHM.node[Node]['NodeSpeed']*(1-SpeedDown)
        if Report: print ("\033[33mSHM::\033[0m AGEING NODE:", Node, "... SPEED DROPPED TO:",
                          self.SHM.node[Node]['NodeSpeed'], "%")
        if self.SHM.node[Node]['NodeSpeed'] == 0:
            self.BreakNode(Node, True)

    ##################################################
    def BreakNode(self, Node, Report):
        if Report: print ("===========================================")
        self.SHM.node[Node]['NodeHealth'] = False
        if Report: print ("\033[33mSHM::\033[0m NODE", Node, "IS BROKEN...")

    def RestoreBrokenNode(self, Node, Report):
        if Report: print ("===========================================")
        self.SHM.node[Node]['NodeHealth'] = True
        if Report: print ("\033[33mSHM::\033[0m NODE", Node, "IS RESTORED...")

    ##################################################
    def TakeSnapShotOfSystemHealth(self):
        self.SnapShot = copy.deepcopy(self.SHM)
        print ("A SNAPSHOT OF SYSTEM HEALTH HAS BEEN STORED...")
        return None

    ##################################################
    def RestoreToPreviousSnapShot (self):
        self.SHM = copy.deepcopy(self.SnapShot)
        print ("SYSTEM HEALTH MAP HAS BEEN RESTORED TO PREVIOUS SNAPSHOT...")
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

    # ToDO: To implement the classification algorithm