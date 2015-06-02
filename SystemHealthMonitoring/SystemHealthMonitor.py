__author__ = 'siavoosh'
import networkx
import copy
class SystemHealthMap:

    def __init__(self):
        self.SHM = networkx.DiGraph()

    def SetUp_NoC_SystemHealthMap(self,ArchGraph):

        print "PREPARING SYSTEM HEALTH MAP..."
        TurnsHealth={"N2W":True,"N2E":True,
                    "S2W":True,"S2E":True,
                    "W2N":True,"W2S":True,
                    "E2N":True,"E2S":True}
        NodeHealth=True
        for nodes in ArchGraph.nodes():
            self.SHM.add_node(nodes,TurnsHealth=copy.deepcopy(TurnsHealth),NodeHealth=NodeHealth)
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