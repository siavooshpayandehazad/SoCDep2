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

    def test_is_node_inside_rectangle(self):
        # test that every node in network is inside a cube with size of network
        rectangle = (0, Config.ag.x_size*Config.ag.y_size*Config.ag.z_size-1)
        for node in range(0, Config.ag.x_size*Config.ag.y_size*Config.ag.z_size-1):
            self.assertEqual(is_node_inside_rectangle(rectangle, node), True)

        node = Config.ag.x_size * Config.ag.y_size * Config.ag.z_size
        self.assertEqual(is_node_inside_rectangle(rectangle, node), False)


if __name__ == '__main__':
    unittest.main()
