# Copyright (C) Siavoosh Payandeh Azad
import unittest
import sys
import os
import re

# Setting up the python path to import the functions
current_path = re.sub('src/unittest/Python', '', str(os.getcwd()))
print("current path:", current_path)
sys.path.append(current_path)

if __name__ == '__main__':
    unittest.main()