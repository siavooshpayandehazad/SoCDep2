# Copyright (C) 2015 Siavoosh Payandeh Azad

################################################
#          Turn Model Sets
################################################
FULL_TurnModel = ['E2N', 'E2S', 'W2N', 'W2S', 'S2W', 'S2E', 'N2W', 'N2E']
XY_TurnModel = ['E2N', 'E2S', 'W2N', 'W2S']
# at the moment there is no support adaptive routing algorithm
# These are just here...
WestFirst_TurnModel = ['E2N', 'E2S', 'W2N', 'W2S', 'S2E', 'N2E']
NorthLast_TurnModel = ['E2N', 'E2S', 'W2N', 'W2S', 'S2W', 'S2E']

################################################
#          SHM Sets
################################################

TurnsHealth_2DNetwork = {"N2W": True, "N2E": True, "S2W": True, "S2E": True,
                         "W2N": True, "W2S": True, "E2N": True, "E2S": True}

# TurnsHealth for conventional 3D NoC
# TurnsHealth_3DNetwork = {"N2W": True, "N2E": True, "S2W": True, "S2E": True,
#                          "W2N": True, "W2S": True, "E2N": True, "E2S": True,
#                          "N2U": True, "N2D": True, "S2U": True, "S2D": True,
#                          "W2U": True, "W2D": True, "E2U": True, "E2D": True}
