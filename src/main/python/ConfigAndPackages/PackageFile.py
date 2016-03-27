# Copyright (C) 2015 Siavoosh Payandeh Azad
################################################
#          Internal Variables
################################################
LoGDirectory = "LOGS"
################################################
#          Turn Model Sets
################################################
FULL_TurnModel_2D = ['E2N', 'E2S', 'W2N', 'W2S', 'S2W', 'S2E', 'N2W', 'N2E']
FULL_TurnModel_3D = ['E2N', 'E2S', 'W2N', 'W2S', 'S2W', 'S2E', 'N2W', 'N2E',
                     'N2U', 'N2D', 'S2U', 'S2D', 'W2U', 'W2D', 'E2U', 'E2D',
                     'U2N', 'U2S', 'U2E', 'U2W', 'D2N', 'D2S', 'D2E', 'D2W']

# 2D Turn Models:
XY_TurnModel = ['E2N', 'E2S', 'W2N', 'W2S']
YX_TurnModel = ['S2W', 'S2E', 'N2W', 'N2E']
WestFirst_TurnModel = ['E2N', 'E2S', 'W2N', 'W2S', 'S2E', 'N2E']
NorthLast_TurnModel = ['E2N', 'E2S', 'W2N', 'W2S', 'N2W', 'N2E']
NegativeFirst2D_TurnModel = ['E2N', 'E2S', 'W2N', 'S2E', 'N2W', 'N2E']

# list of all 2D Deadlock free turn models with maximum connectivity metric
# ===========================================================================
# 4 turn (14 turn models)
# #     			Turn Model					Connectivity metric
# ---------------------------------------------------------------------------
# 1	    |	['E2N', 'E2S', 'W2N', 'W2S']	|	72.0	---------------> XY
# 5 	|	['E2N', 'E2S', 'W2N', 'N2E']	|	72.0
# 7	    |	['E2N', 'E2S', 'W2S', 'S2E']	|	72.0
# 14	|	['E2N', 'E2S', 'S2E', 'N2E']	|	72.0
# 18	|	['E2N', 'W2N', 'W2S', 'N2W']	|	72.0
# 25	|	['E2N', 'W2N', 'N2W', 'N2E']	|	72.0
# 35	|	['E2N', 'S2E', 'N2W', 'N2E']	|	72.0
# 36	|	['E2S', 'W2N', 'W2S', 'S2W']	|	72.0
# 46	|	['E2S', 'W2S', 'S2W', 'S2E']	|	72.0
# 53	|	['E2S', 'S2W', 'S2E', 'N2E']	|	72.0
# 57	|	['W2N', 'W2S', 'S2W', 'N2W']	|	72.0
# 64	|	['W2N', 'S2W', 'N2W', 'N2E']	|	72.0
# 66	|	['W2S', 'S2W', 'S2E', 'N2W']	|	72.0
# 70	|	['S2W', 'S2E', 'N2W', 'N2E']	|	72.0	----------------> YX
# ===========================================================================
# 5 turns (24 turn models)
# #     			Turn Model							Connectivity metric
# ---------------------------------------------------------------------------
# 1	    |	['E2N', 'E2S', 'W2N', 'W2S', 'S2W']		|		72.0
# 2	    |	['E2N', 'E2S', 'W2N', 'W2S', 'S2E']		|		72.0
# 3	    |	['E2N', 'E2S', 'W2N', 'W2S', 'N2W']		|		72.0
# 4	    |	['E2N', 'E2S', 'W2N', 'W2S', 'N2E']		|		72.0
# 9	    |	['E2N', 'E2S', 'W2N', 'S2E', 'N2E']		|		72.0
# 10	|	['E2N', 'E2S', 'W2N', 'N2W', 'N2E']		|		72.0
# 11	|	['E2N', 'E2S', 'W2S', 'S2W', 'S2E']		|		72.0
# 15	|	['E2N', 'E2S', 'W2S', 'S2E', 'N2E']		|		72.0
# 18	|	['E2N', 'E2S', 'S2W', 'S2E', 'N2E']		|		72.0
# 20	|	['E2N', 'E2S', 'S2E', 'N2W', 'N2E']		|		72.0
# 22	|	['E2N', 'W2N', 'W2S', 'S2W', 'N2W']		|		72.0
# 26	|	['E2N', 'W2N', 'W2S', 'N2W', 'N2E']		|		72.0
# 29	|	['E2N', 'W2N', 'S2W', 'N2W', 'N2E']		|		72.0
# 30	|	['E2N', 'W2N', 'S2E', 'N2W', 'N2E']		|		72.0
# 35	|	['E2N', 'S2W', 'S2E', 'N2W', 'N2E']		|		72.0
# 36	|	['E2S', 'W2N', 'W2S', 'S2W', 'S2E']		|		72.0
# 37	|	['E2S', 'W2N', 'W2S', 'S2W', 'N2W']		|		72.0
# 46	|	['E2S', 'W2S', 'S2W', 'S2E', 'N2W']		|		72.0
# 47	|	['E2S', 'W2S', 'S2W', 'S2E', 'N2E']		|		72.0
# 50	|	['E2S', 'S2W', 'S2E', 'N2W', 'N2E']		|		72.0
# 51	|	['W2N', 'W2S', 'S2W', 'S2E', 'N2W']		|		72.0
# 53	|	['W2N', 'W2S', 'S2W', 'N2W', 'N2E']		|		72.0
# 55	|	['W2N', 'S2W', 'S2E', 'N2W', 'N2E']		|		72.0
# 56	|	['W2S', 'S2W', 'S2E', 'N2W', 'N2E']		|		72.0
# ====================================================================================
# 6 turns: (12 turn models)
# #     			Turn Model										Connectivity metric
# ------------------------------------------------------------------------------------
# 1	    |	DF	['E2N', 'E2S', 'W2N', 'W2S', 'S2W', 'S2E']		|		72.0
# 2	    |	DF	['E2N', 'E2S', 'W2N', 'W2S', 'S2W', 'N2W']		|		72.0
# 5	    |	DF	['E2N', 'E2S', 'W2N', 'W2S', 'S2E', 'N2E']		|		72.0		------------> West First
# 6	    |	DF	['E2N', 'E2S', 'W2N', 'W2S', 'N2W', 'N2E']		|		72.0		------------> North Last
# 10	|	DF	['E2N', 'E2S', 'W2N', 'S2E', 'N2W', 'N2E']		|		72.0		------------> Negative First
# 12	|	DF	['E2N', 'E2S', 'W2S', 'S2W', 'S2E', 'N2E']		|		72.0
# 15	|	DF	['E2N', 'E2S', 'S2W', 'S2E', 'N2W', 'N2E']		|		72.0
# 18	|	DF	['E2N', 'W2N', 'W2S', 'S2W', 'N2W', 'N2E']		|		72.0
# 20	|	DF	['E2N', 'W2N', 'S2W', 'S2E', 'N2W', 'N2E']		|		72.0
# 22	|	DF	['E2S', 'W2N', 'W2S', 'S2W', 'S2E', 'N2W']		|		72.0
# 27	|	DF	['E2S', 'W2S', 'S2W', 'S2E', 'N2W', 'N2E']		|		72.0
# 28	|	DF	['W2N', 'W2S', 'S2W', 'S2E', 'N2W', 'N2E']		|		72.0

# 3D Turn Models:
XYZ_TurnModel = ['E2N', 'E2S', 'W2N', 'W2S', 'S2U', 'S2D', 'N2U', 'N2D', 'W2U', 'W2D', 'E2U', 'E2D']

# based on description in "Turn model based router design for 3D network on chip" by Chemli and Zitouni
NegativeFirst3D_TurnModel = ['E2N', 'E2S', 'W2N', 'S2E', 'N2W', 'N2E',
                             'N2U', 'N2D', 'S2U', 'W2U', 'E2U', 'E2D',
                             'U2N', 'U2S', 'U2E', 'U2W', 'D2N', 'D2E']

routing_alg_list_2d = [YX_TurnModel, XY_TurnModel, WestFirst_TurnModel, NorthLast_TurnModel, NegativeFirst2D_TurnModel]
routing_alg_list_3d = [XYZ_TurnModel, NegativeFirst3D_TurnModel]
################################################
#          SHM Sets
################################################
TurnsHealth_2DNetwork = {"N2W": True, "N2E": True, "S2W": True, "S2E": True,
                         "W2N": True, "W2S": True, "E2N": True, "E2S": True}

# TurnsHealth for conventional 3D NoC
TurnsHealth_3DNetwork = {"N2W": True, "N2E": True, "S2W": True, "S2E": True,
                         "W2N": True, "W2S": True, "E2N": True, "E2S": True,
                         "N2U": True, "N2D": True, "S2U": True, "S2D": True,
                         "W2U": True, "W2D": True, "E2U": True, "E2D": True,
                         "U2W": True, "U2E": True, "U2N": True, "U2S": True,
                         "D2W": True, "D2E": True, "D2N": True, "D2S": True}
################################################
#          System Package info
################################################
ImportModules = ['Tkinter', 'ttk', 'networkx',
                 'matplotlib', 'scipy', 'PIL',
                 'pympler', 'simpy', 'collections',
                 'sklearn', 'image']