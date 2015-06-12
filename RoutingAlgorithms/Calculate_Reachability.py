# Copyright (C) Siavoosh Payandeh Azad

from Routing import FindRouteInRouteGraph

def CalculateReachability (AG,NoCRG):
    for SourceNode in AG.nodes():
        for DestinationNode in AG.nodes():
            if SourceNode != DestinationNode:
                if FindRouteInRouteGraph(NoCRG,SourceNode,DestinationNode,False,False) is None:
                    print "No Path From", SourceNode,"To",DestinationNode
                    AG.node[SourceNode]['Unreachable'].append(DestinationNode)
