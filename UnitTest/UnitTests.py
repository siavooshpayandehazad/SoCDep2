# Copyright (C) Siavoosh Payandeh Azad
import unittest
import sys,os
import re

# Setting up the python path to import the functions
CurrentPath = re.sub('UnitTest', '', str(os.getcwd()))
sys.path.append(CurrentPath)
# Add Imports here:
from ArchGraphUtilities.AG_Functions import ReturnNodeLocation, ReturnNodeNumber
from RoutingAlgorithms.Calculate_Reachability import IsNodeInsideRectangle
from ConfigAndPackages import Config


class UnitTesting(unittest.TestCase):

    def test_ReturnNodeNumber(self):
        self.assertEqual(ReturnNodeNumber(0, 0, 0), 0)
        for k in range(0, Config.Network_Z_Size):
            for j in range(0, Config.Network_Y_Size):
                for i in range(0, Config.Network_X_Size):
                    self.assertEqual(ReturnNodeNumber(i, j, k),
                                     i + j*Config.Network_X_Size + k*Config.Network_Y_Size* Config.Network_X_Size)
        self.assertEqual(ReturnNodeNumber(Config.Network_X_Size -1, Config.Network_Y_Size -1, Config.Network_Z_Size -1),
                         Config.Network_X_Size * Config.Network_Y_Size * Config.Network_Z_Size - 1)

    def test_ReturnNodeLocation(self):
        for k in range(0, Config.Network_Z_Size):
            for j in range(0, Config.Network_Y_Size):
                for i in range(0, Config.Network_X_Size):
                    # we have the assumption that ReturnNodeNumber is fully tested...
                    self.assertEqual(ReturnNodeLocation(ReturnNodeNumber(i,j,k)), (i, j, k))

    def test_IsNodeInsideRectangle(self):
        # test that every node in network is inside a cube with size of network
        Rectangle = (0, Config.Network_X_Size*Config.Network_Y_Size*Config.Network_Z_Size-1)
        for Node in range(0, Config.Network_X_Size*Config.Network_Y_Size*Config.Network_Z_Size-1):
            self.assertEqual(IsNodeInsideRectangle(Rectangle, Node), True)

        Node = Config.Network_X_Size * Config.Network_Y_Size * Config.Network_Z_Size
        self.assertEqual(IsNodeInsideRectangle(Rectangle, Node), False)

    # todo: test MergeRectangleWithNode


if __name__ == '__main__':
    unittest.main()

