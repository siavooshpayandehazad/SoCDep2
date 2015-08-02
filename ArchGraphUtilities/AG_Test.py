# Copyright (C) Siavoosh Payandeh Azad

import AG_Functions
from ConfigAndPackages import Config


def AG_Test():
    print "==========================================="
    print "STARTING AG TESTS..."
    if AG_Functions.ReturnNodeLocation(0) != (0, 0, 0):
        raise ValueError('Error in ReturnNodeLocation function... CASE 1')

    if AG_Functions.ReturnNodeLocation(Config.Network_X_Size * Config.Network_Y_Size * Config.Network_Z_Size - 1) != \
       (Config.Network_X_Size -1, Config.Network_Y_Size - 1, Config.Network_Z_Size - 1):
        raise ValueError('Error in ReturnNodeLocation function... CASE 2')

    if AG_Functions.ReturnNodeNumber(0, 0, 0) != 0:
        raise ValueError('Error in ReturnNodeNumber function... CASE 1')

    if AG_Functions.ReturnNodeNumber(Config.Network_X_Size -1, Config.Network_Y_Size -1, Config.Network_Z_Size -1) !=\
            Config.Network_X_Size * Config.Network_Y_Size * Config.Network_Z_Size - 1:
        raise ValueError('Error in ReturnNodeNumber function... CASE 2')

    print "AG TESTS PASSED SUCCESSFULLY..."
    return None