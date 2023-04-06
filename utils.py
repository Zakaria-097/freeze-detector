import os
import shutil
import sys
import art
import webbrowser

FOLDER = 'frames'

def introMsg():
    art.tprint("\nFreeze Detector")
    print ("      Welcome to 'Freeze Detector' Developed Zakaria-097")
    print ("\n" + "      This application is a simple scanner to detect freezes in your video files.")


def generateFrameFolder():
    try:
        if not os.path.exists(FOLDER): 
            os.makedirs(FOLDER)
        else:
            clearPreviousEntries()
    except OSError: 
        print ('Error: Creating directory of data') 

def generateFiles():
    
    files = ['results.txt', 'hashes.txt', 'timestamped_frames.txt']

    for file in files:
        try:
            if not os.path.exists(file):
                os.mknod(file)
            else:
                with open(file, "r+") as openFile: openFile.truncate(0)                    
        except OSError:
            print("Error: generating files")
    
      
def clearPreviousEntries():
    
    for filename in os.listdir(FOLDER):
        file_path = os.path.join(FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
     
def writeToFile(fileName, fileMode, message):
    file = open(fileName, fileMode)
    file.write(message)
    file.close()
        
def showResults():
    webbrowser.open("results.txt")
    sys.exit()