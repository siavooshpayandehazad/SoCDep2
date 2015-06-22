# Copyright (C) 2015 Siavoosh Payandeh Azad

import os

def GenerateFileDirectories():
    GraphDirectory = "GraphDrawings"
    if not os.path.isdir(GraphDirectory):
        os.makedirs(GraphDirectory)

    GeneratedFilesDirectory = "Generated_Files"
    if not os.path.isdir(GeneratedFilesDirectory):
        os.makedirs(GeneratedFilesDirectory)

    return None
