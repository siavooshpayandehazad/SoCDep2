# Copyright (C) Siavoosh Payandeh Azad
import unittest
import sys
import os
import re

# Setting up the python path to import the functions
current_path = re.sub('unittest', '', str(os.getcwd()))
sys.path.append(current_path)
# Add Imports here:
from RoutingAlgorithms.Calculate_Reachability import is_node_inside_rectangle
from ConfigAndPackages import Config


class UnitTesting(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()