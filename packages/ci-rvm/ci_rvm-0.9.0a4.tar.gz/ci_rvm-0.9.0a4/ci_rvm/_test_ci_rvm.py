'''
Created on 18.09.2019

@author: Samuel
'''
import sys
import os

import numpy as np
import matplotlib
if sys.platform != 'win32':
    # if executed on a Windows server. Comment out this line, if you are working
    # on a desktop computer that is not Windows.
    matplotlib.use('Agg')

try:
    from test_ci_rvm import *
except ModuleNotFoundError:
    from .test_ci_rvm import *

if __name__ == '__main__':
    try:
        # if vemomoto_core_tools is installed, you can call the module with an 
        # argument specifying a log file to which the output is written in addition
        # to the console.
        from vemomoto_core.tools.tee import Tee
        if len(sys.argv) > 1:
            teeObject = Tee(sys.argv[1])
    except ModuleNotFoundError:
        pass


if __name__ == '__main__':
    #os.chdir(os.path.join("test_CI", "Histone_H1"))
    
    methods = ["mixed_min", "constrained_max", "binsearch", "bisection", "RVM"]
    methods = ["Wald", "RVM", "RVM_psI", "bisection", "mixed_min", "constrained_max", "binsearch", "VM",  "gridsearch"]
    methods = ["RVM_psI"]
    #methods = ["bisection"]
    benchmark(methods, 200, dataN=50, mode="11cx") 
    sys.exit()
    benchmark(methods, 200, dataN=10000, mode="11") 
    test_LogRegress(methods)
    test_LogRegress_pred()
    test_dynamical_system()
    test_H14()
    print(os.getcwd())
