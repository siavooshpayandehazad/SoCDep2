# Copyright (C) Siavoosh Payandeh Azad

import Calculate_Reachability
from ConfigAndPackages import Config


def ReachabilityTest():
    print ("===========================================")
    print ("STARTING REACH_ABILITY TESTS...")
    Node = 0
    Rectangle = (0, Config.Network_X_Size*Config.Network_Y_Size*Config.Network_Z_Size-1)
    if not Calculate_Reachability.IsNodeInsideRectangle(Rectangle, Node):
        raise ValueError('Error in IsNodeInsideRectangle function... CASE 1')

    Node = Config.Network_X_Size * Config.Network_Y_Size * Config.Network_Z_Size
    if Calculate_Reachability.IsNodeInsideRectangle(Rectangle, Node):
        raise ValueError('Error in IsNodeInsideRectangle function... CASE 2')
    # todo: test MergeRectangleWithNode

    print ("REACH_ABILITY TESTS PASSED SUCCESSFULLY...")
    return None