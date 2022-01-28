import os
import sys
import unittest

my_dir   = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(my_dir)
sys.path.append(os.path.join(root_dir, 'src'))


test_runner = unittest.runner.TextTestRunner()
test_runner.run(unittest.TestLoader().discover('.'))
