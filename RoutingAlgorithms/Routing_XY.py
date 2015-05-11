__author__ = 'siavoosh'



def ReturnPath (AG,SourceNode,DestinationNode):
    ListOfLinks= []
    if SourceNode == 0:
        if DestinationNode == 1:
            ListOfLinks=[(0,1)]
        elif DestinationNode == 2:
            ListOfLinks=[(0,2)]
        elif DestinationNode == 3:
            ListOfLinks=[(0,1),(1,3)]

    if SourceNode == 1:
        if DestinationNode == 0:
            ListOfLinks=[(1,0)]
        elif DestinationNode == 2:
            ListOfLinks=[(1,0),(0,2)]
        elif DestinationNode == 3:
            ListOfLinks=[(1,3)]

    if SourceNode == 2:
        if DestinationNode == 0:
            ListOfLinks=[(2,0)]
        elif DestinationNode == 1:
            ListOfLinks=[(2,3),(3,1)]
        elif DestinationNode == 3:
            ListOfLinks=[(2,3)]

    if SourceNode == 3:
        if DestinationNode == 0:
            ListOfLinks=[(3,2),(2,0)]
        elif DestinationNode == 1:
            ListOfLinks=[(3,1)]
        elif DestinationNode == 2:
            ListOfLinks=[(3,2)]
    return ListOfLinks