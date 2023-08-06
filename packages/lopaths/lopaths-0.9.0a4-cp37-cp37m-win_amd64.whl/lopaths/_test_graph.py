'''
'''
import sys
import os


import numpy as np

import matplotlib as mpl
if os.name == 'posix':
    # if executed on a Windows server. Comment out this line, if you are working
    # on a desktop computer that is not Windows.
    mpl.use('Agg')
try:
    from .test_graph import *
except ImportError:
    from test_graph import *

if __name__ == '__main__':
    from vemomoto_core.tools.tee import Tee
    if len(sys.argv) > 1:
        teeObject = Tee(sys.argv[1])


        

if __name__ == '__main__':
    
    restart = True
    restart = False
    print("Start")
    fileNameSave = "testRoadNetwork_small"
    fileNameSave = "testRoadNetwork2"
    fileNameSave = "testRoadNetwork"
    fileNameSave = "GraphTest"
    
    fileNameEdges = "RoadNet_North.csv" 
    fileNameEdges = "ExportEdges_BC.csv" 
    fileNameEdges = "LakeNetworkExample_full.csv"
    
    show = True
    show = False 
    tester = GraphTester.new(fileNameSave, fileNameEdges, restart)
    
    #"""
    optimizations = [
        {"None"},
        {"find_plateaus"},
        {"tree_bound"},
        {"pruning_bound"},
        {"pruning_bound_extended"},
        {"reject_identical"},
        {"joint_reject"},
        {"reuse_queries"}
        ]
    #tester.test_optimizations(sourceNo=50, sinkNo=1000, optimizations="find_plateaus")
    tester.test_optimizations(sourceNo=50, sinkNo=100)
    tester.test_optimizations()
    tester.test_optimizations(sourceNo=100, sinkNo=200)
    tester.test_optimizations(sourceNo=200, sinkNo=500)
    tester.test_optimizations(sourceNo=50, sinkNo=1000, optimizations=optimizations)
    """
    
    tester.test_REVC_LOC(show)
    tester.test_REVC_stretch(show)
    tester.test_REVC_source_sink(False, show=show)
    tester.test_REVC_approximations(repetitions=20, show=show)
    tester.save()
    acceptionFactors = np.array([0.6, 0.8, 1.])
    rejectionFactors = np.array([1., 1.05, 1.1, 1.15, 1.2, 1.3])
    tester.test_REVC_approximations(acceptionFactors, rejectionFactors, 100, 20, show)
    
    #"""
    #tester.test_REVC_all(show)
