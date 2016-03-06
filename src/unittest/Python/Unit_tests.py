# Copyright (C) Siavoosh Payandeh Azad
import unittest
import sys
import os
import re

# Setting up the python path to import the functions
CurrentPath = re.sub('UnitTest', '', str(os.getcwd()))
sys.path.append(CurrentPath)
# Add Imports here:
from ArchGraphUtilities.AG_Functions import return_node_location, return_node_number, manhattan_distance
from RoutingAlgorithms.Calculate_Reachability import is_node_inside_rectangle
from ConfigAndPackages import Config


class UnitTesting(unittest.TestCase):

    def test_return_node_number(self):
        self.assertEqual(return_node_number(0, 0, 0), 0)
        for k in range(0, Config.ag.z_size):
            for j in range(0, Config.ag.y_size):
                for i in range(0, Config.ag.x_size):
                    self.assertEqual(return_node_number(i, j, k),
                                     i + j*Config.ag.x_size+k*Config.ag.y_size*Config.ag.x_size)
        self.assertEqual(return_node_number(Config.ag.x_size-1, Config.ag.y_size-1, Config.ag.z_size-1),
                         Config.ag.x_size * Config.ag.y_size * Config.ag.z_size - 1)

    def test_return_node_location(self):
        for k in range(0, Config.ag.z_size):
            for j in range(0, Config.ag.y_size):
                for i in range(0, Config.ag.x_size):
                    # we have the assumption that return_node_number is fully tested...
                    self.assertEqual(return_node_location(return_node_number(i, j, k)), (i, j, k))

    def test_manhattan_distance(self):
        self.assertEqual(manhattan_distance(0, 0), 0)
        last_node_number = return_node_number(Config.ag.x_size-1, Config.ag.y_size-1, Config.ag.z_size-1)
        self.assertEqual(manhattan_distance(0, last_node_number),
                         Config.ag.x_size+Config.ag.y_size+Config.ag.z_size-3)

    def test_is_node_inside_rectangle(self):
        # test that every node in network is inside a cube with size of network
        rectangle = (0, Config.ag.x_size*Config.ag.y_size*Config.ag.z_size-1)
        for node in range(0, Config.ag.x_size*Config.ag.y_size*Config.ag.z_size-1):
            self.assertEqual(is_node_inside_rectangle(rectangle, node), True)

        node = Config.ag.x_size * Config.ag.y_size * Config.ag.z_size
        self.assertEqual(is_node_inside_rectangle(rectangle, node), False)

    # todo: test merge_rectangle_with_node


if __name__ == '__main__':
    unittest.main()
