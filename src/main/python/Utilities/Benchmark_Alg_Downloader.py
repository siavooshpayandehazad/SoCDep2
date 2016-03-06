# Copyright (C) 2015 Siavoosh Payandeh Azad

import os.path
import urllib
from ConfigAndPackages import Config


def download_benchmark_algorithms(Benchmark):
    testfile = urllib.FancyURLopener()

    if Benchmark == 'idct':     # Inverse Discrete Cosine Transform
        url = "http://express.ece.ucsb.edu/benchmark/jpeg/jpeg_idct_ifast_dfg__6.dot"
        DestinationFile = 'Benchmarks/idct.dot'

    elif Benchmark == 'fdct':   # Forward Discrete Cosine Transform
        url = "http://express.ece.ucsb.edu/benchmark/jpeg/jpeg_fdct_islow_dfg__6.dot"
        DestinationFile = 'Benchmarks/fdct.dot'
    elif Benchmark == 'mi':     # Matrix Inverse
        url = "http://express.ece.ucsb.edu/benchmark/mesa/invert_matrix_general_dfg__3.dot"
        DestinationFile = 'Benchmarks/mi.dot'
    else:
        print "THIS BENCHMARK IS NOT SUPPORTED..."
        return False

    if not os.path.isfile(DestinationFile):
        code = urllib.urlopen(url).code
        if code/100 >= 4:
            print "BENCHMARK IS NOT AVAILABLE..."
            return False
        else:
            print "DOWNLOADING BENCHMARK..."
            testfile.retrieve(url, DestinationFile)
            print "FINISHED DOWNLOADING..."
            Config.tg.dot_file_path = DestinationFile
            Config.tg.type = 'FromDOTFile'
            return True
    else:
        print "FILE ALREADY EXISTS..."
        Config.tg.dot_file_path = DestinationFile
        Config.tg.type = 'FromDOTFile'
        return True