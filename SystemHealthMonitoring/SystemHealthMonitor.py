__author__ = 'siavoosh'
import networkx
import copy
class SystemHealthMonitor:
    def __init__(self):
        self.SHM = networkx.DiGraph()   #System Health Map

    def SetUp_NoC_SystemHealthMap(self,ArchGraph,TurnsHealth):
        print "==========================================="
        print "PREPARING SYSTEM HEALTH MAP..."
        NodeHealth=True
        for nodes in ArchGraph.nodes():
            self.SHM.add_node(nodes,TurnsHealth=copy.deepcopy(TurnsHealth),NodeHealth=NodeHealth,NodeSpeed=100)
        for link in ArchGraph.edges():
            self.SHM.add_edge(link[0],link[1],LinkHealth=True)
        print "SYSTEM HEALTH MAP CREATED..."

    def Report_NoC_SystemHealthMap(self):
        print "==========================================="
        print "      REPORTING SYSTEM HEALTH MAP"
        print "==========================================="
        print "\tNODES:",self.SHM.nodes(data=True)
        print "\tEDGES:",self.SHM.edges(data=True)

    def BreakLink(self,link,Report):
        if Report:print "==========================================="
        if Report:print "BREAKING LINK:",link, "IN SYSTEM HEALTH MAP..."
        self.SHM.edge[link[0]][link[1]]['LinkHealth']=False

    def BreakTrun(self,Node,Turn,Report):
        if Report:print "==========================================="
        if Report:print "BREAKING TURN:",Turn, "IN SYSTEM HEALTH MAP..."
        self.SHM.node[Node]['TurnsHealth'][Turn]=False

    def IntroduceAging(self,Node,SpeedDown,Report):
        if Report: print "==========================================="
        self.SHM.node[Node]['NodeSpeed']=self.SHM.node[Node]['NodeSpeed']*(1-SpeedDown)
        if Report: print "AGEING NODE:",Node,"SPEED DROPPED TO:",self.SHM.node[Node]['NodeSpeed'],"%"
