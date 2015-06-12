============================================================================
	  _________      .__               .___    .__          
	 /   _____/ ____ |  |__   ____   __| _/_ __|  |   ____  
	 \_____  \_/ ___\|  |  \_/ __ \ / __ |  |  \  | _/ __ \ 
	 /        \  \___|   Y  \  ___// /_/ |  |  /  |_\  ___/ 
	/_______  /\___  >___|  /\___  >____ |____/|____/\___  >
	        \/     \/     \/     \/     \/               \/ 

	                   .___
	_____    ____    __| _/
	\__  \  /    \  / __ | 
	 / __ \|   |  \/ /_/ | 
	(____  /___|  /\____ | 
	     \/     \/      \/

	________                                   .___
	\______ \   ____ ______   ____   ____    __| _/
	 |    |  \_/ __ \\____ \_/ __ \ /    \  / __ | 
	 |    `   \  ___/|  |_> >  ___/|   |  \/ /_/ | 
	/_______  /\___  >   __/ \___  >___|  /\____ | 
	        \/     \/|__|        \/     \/      \/  
==============================================================================
AUTHOR:  SIAVOOSH PAYANDEH AZAD
DATE:    MAY 2015
LICENSE: GNU GENERAL PUBLIC LICENSE Version 2
PYTHON VER: 2.6.9
THE GOAL OF THIS PROGRAM IS TO MAKE A PLATFORM FOR TESTING SOME DEPENDABILITY 
STUFF ON DIFFERENT ARCHITECTURES....
Copyright (C) 2015 Siavoosh Payandeh Azad
===============================================================================
How To generate RoutingFile.txt:
    This file is made to enable user to manually control routing algorithm
    via turn model in every single router.
    This file starts with the following 2 lines:
        Ports:
	        N W L E S
	This will show what are the allowed ports in the network.
	Important note: Make sure that the Local is in the middle, and opposite
	directions should have same distance from local. This would be used to
	construct the direct paths in the router.
	And then the user can push the turns for each router by the following
	structure:
        Node 0:
	        N2E E2N
	These would be the allowed turns on router 0.
	The path to file should be specified in Config file by setting
	RoutingFilePath properly.
===============================================================================

ToDo:

    - I want to run a Reliability Analysis of the system... so we can have
      a sense about the state of the system state...

    - can we generate some file based on scheduling to feed in Noxim?

    - can we get TG specifications automatically from some benchmark alg??