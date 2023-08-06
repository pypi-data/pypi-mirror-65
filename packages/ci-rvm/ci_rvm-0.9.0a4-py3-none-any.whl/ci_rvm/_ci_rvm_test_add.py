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
from matplotlib import pyplot as plt


try:
    from ._ci_rvm_test import *
except ImportError:
    from _ci_rvm_test import *

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

np.random.seed()


def create_plots(methods=["RVM"], dataN=1000):
    directory = "CITest"
    if not os.access(directory, os.F_OK): os.makedirs(directory)
    
    
    """
    tester = DynamicalSystemTester(None)
    baseName = "DynSys"
    tester = H14Tester()
    baseName = "H14"
    """
    baseName = "LR"
    tester = LogRegressTester(seed=2, dataN=dataN)
    
    addNo = tester.dim-2
    baseName += "-" + str(addNo) + "-"
    #addNo=0
    #"""
    #create_plot(tester, [1, 3]) 
    #create_plot(tester, [0, 2], [1])
    baseName = os.path.join(directory, baseName)
    for i in range(tester.dim):
        for j in range(i+1, tester.dim):
            additional = []
            extra = 0
            for k in range(1, addNo+1):
                new = (j+k+extra) % tester.dim
                if new == i:
                    extra = 1
                    new += 1
                additional.append(new)
            #create_plot(tester, [i, j], additional, baseName+str([i,j]))
            create_plot(tester, [i, j], additional, methods=methods)

#print(g(x0))
#print(h(x0))
def plot3d():
    from mayavi import mlab
    import mayavi
    tester = LogRegressTester(dataN=1000)
    fun = tester.funs[0]
    
    l, u = -10, 10
    
    
    
    n = 30j
    
    xl, xu = 0, 4
    xdiff = xu-xl
    yl, yu = 0.5, 2
    ydiff = yu-yl
    zl, zu = -13, -3
    zdiff = zu-zl
    
    xfact = 1
    yfact = xdiff/ydiff
    zfact = xdiff/zdiff
    
    
    X, Y, Z = np.mgrid[xl*xfact:xu*xfact:n, yl*yfact:yu*yfact:n, zl*zfact:zu*zfact:n]
    
    #X, Y, Z = np.meshgrid(x, y, z)
    
    A = np.zeros_like(X)
    
    for i in range(X.shape[0]):
        print(i)
        for j in range(X.shape[1]):
            for k in range(X.shape[2]):
                A[i,j,k] = fun(np.array([X[i,j,k]/xfact, Y[i,j,k]/yfact, Z[i,j,k]/zfact]))
    A = np.maximum(A, -5000)
    mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))
    obj = mlab.contour3d(X, Y, Z, A, opacity=0.5, contours=[-311.40925355297])
    #obj.actor.actor.scale = (0.1, 1.0, 1.0)
    mlab.axes(nb_labels=0, xlabel="x1", ylabel="x2", zlabel="x3",
              )
    mlab.show()

if __name__ == '__main__':
    #os.chdir(os.path.join("test_CI", "Histone_H1"))
    
    plot3d()
    print(os.getcwd())
