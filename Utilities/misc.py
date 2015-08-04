# Copyright (C) 2015 Siavoosh Payandeh Azad
from ConfigAndPackages import Config
import os

def DrawLogo ():
    print ("===================================================================================================================")
    print ("  _________      .__               .___    .__             ____    ________                                   .___")
    print (" /   _____/ ____ |  |__   ____   __| _/_ __|  |   ____    /  _ \   \______ \   ____ ______   ____   ____    __| _/")
    print (" \_____  \_/ ___\|  |  \_/ __ \ / __ |  |  \  | _/ __ \   >  _ </\  |    |  \_/ __ \\\\____ \_/ __ \ /    \  / __ | ")
    print (" _____/   \  \___|   Y  \  ___// /_/ |  |  /  |_\  ___/  /  <_\ \/  |    `   \  ___/|  |_> >  ___/|   |  \/ /_/ | ")
    print ("/_______  /\___  >___|  /\___  >____ |____/|____/\___  > \_____\ \ /_______  /\___  >   __/ \___  >___|  /\____ | ")
    print ("        \/     \/     \/     \/     \/               \/         \/         \/     \/|__|        \/     \/      \/ ")
    print ("===================================================================================================================")
    print ("AUTHOR:  SIAVOOSH PAYANDEH AZAD")
    print ("DATE:    MAY 2015")
    print ("THE GOAL OF THIS PROGRAM IS TO MAKE A PLATFORM FOR TESTING SOME ")
    print ("DEPENDABILITY STUFF ON DIFFERENT ARCHITECTURES....")
    print ("================================================================================")
    print ("DEBUG DETAILS:", Config.DebugDetails)
    print ("DEBUG INFO:", Config.DebugInfo)
    print ("===========================================")
    return None

def GenerateFileDirectories():
    GraphDirectory = "GraphDrawings"
    if not os.path.isdir(GraphDirectory):
        os.makedirs(GraphDirectory)

    filelist = [file for file in os.listdir(GraphDirectory) if file.endswith(".png")]
    for file in filelist:
        os.remove(GraphDirectory +'/'+file)

    AnimationDirectory = "GraphDrawings/Mapping_Animation_Material"
    if not os.path.isdir(AnimationDirectory):
        os.makedirs(AnimationDirectory)

    filelist = [file for file in os.listdir(AnimationDirectory) if file.endswith(".png")]
    for file in filelist:
        os.remove(AnimationDirectory +'/'+file)

    GeneratedFilesDirectory = "Generated_Files"
    if not os.path.isdir(GeneratedFilesDirectory):
        os.makedirs(GeneratedFilesDirectory)

    filelist = [file for file in os.listdir(GeneratedFilesDirectory) if file.endswith(".txt")]
    for file in filelist:
        os.remove(GeneratedFilesDirectory +'/'+file)

    InternalFilesDirectory = "Generated_Files/Internal"
    if not os.path.isdir(InternalFilesDirectory):
        os.makedirs(InternalFilesDirectory)
    filelist = [file for file in os.listdir(InternalFilesDirectory) if file.endswith(".txt")]
    for file in filelist:
        os.remove(InternalFilesDirectory +'/'+file)
    return None
