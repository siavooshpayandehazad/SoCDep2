# Copyright (C) Siavoosh Payandeh Azad

import Calculate_Reachability
import Config

def ReachabilityTest ():
    Node = 0
    Rectangle = (0,Config.Network_X_Size * Config.Network_Y_Size * Config.Network_Z_Size -1 )
    if not Calculate_Reachability.IsNodeInsideRectangle(Rectangle,Node):
        raise ValueError('Error in IsNodeInsideRectangle function... ')
    return None