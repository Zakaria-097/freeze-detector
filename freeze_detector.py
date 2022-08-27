# Importing all necessary libraries 
from stat import filemode
import cv2 
import sys
import os 
from PIL import Image
import imagehash
import collections 
import os, shutil
import webbrowser
from tkinter import filedialog #allow users to select video 
import art 
from PIL import Image


# generate directory 'frames' and all necessary files 
def generateFiles():
    
    try:
        if not os.path.exists('frames'): 
            os.makedirs('frames')
        if not os.path.exists('results.txt'):
            os.mknod('results.txt')
        if not os.path.exists('hashes.txt'):
            os.mknod('hashes.txt')
        if not os.path.exists('timestamped_frames.txt'):
            os.mknod('timestamped_frames.txt')

    except OSError: 
        print ('Error: Creating directory of data') 
      
def clearPreviousEntries():
    
    folder = 'frames'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
    with open('hashes.txt', 'r+') as tes, \
        open('results.txt', 'r+') as tes2, \
        open('timestamped_frames.txt', 'r+') as tes3: tes.truncate(0), tes3.write("initialise"), tes2.truncate(0), tes3.truncate(0)
     
def writeToFile(fileName, fileMode, message):
    file = open(fileName, fileMode)
    file.write(message)
    file.close()
     
        
def duplicatesFound(hash, currentTime):

    message = "\n" + "   Freeze found!" + "\n\n""   Duplicate Hash:  " + hash + "      Time: " + str(currentTime[0])
    writeToFile("results.txt", "a", message)

    webbrowser.open("results.txt")
    
def noDuplicatesFound():
    
    file20 = open("results.txt","a")
    file20.write( "\n" + "   Scanning Complete:"  + "\n" + "\n" + "   No Freeze Found! ")
    file20.close()

    webbrowser.open("results.txt")

def start():

    # generate necessary files
    generateFiles()
    
    # clear data from previous scan
    clearPreviousEntries()

    # set initial variables
    count = 0
    counter_id = 0
    hashCount = 1
    timeOfDup= [] # timeOfDup: used to list the exact times we've found duplicate hashes 
    
    # allow user to select a video file
    selected_fileName = filedialog.askopenfilename( filetypes = ( ("Video Files", "*.mp4"), ("All Files", "*.*") ))

    # read video from specified path 
    cap = cv2.VideoCapture(selected_fileName) 


    while cap.isOpened():
        ret, frame = cap.read()

        if ret: 
            minutes = counter_id // 60
            hours = minutes // 60
            current_time_of_video = str("%02d:%02d:%02d" % (hours, minutes % 60, counter_id % 60))

            fps = cap.get(cv2.CAP_PROP_FPS)

            #setting the counter equal to the fps - hardcoding fps will make it stagnant - getting the real fps of video will make 'count' more precise
            count = count + fps + fps + fps

            # if video is still left continue creating images 
            frame_name = './frames/frame' + str(count) + '.jpg'

            # writing the extracted images
            cv2.imwrite(frame_name, frame)
             
            #hashing each .openframe
            zaks_Hash = imagehash.phash(Image.open(frame_name))

            # log the current frame
            print("   Scanning ->" + str(zaks_Hash))

            #open text file
            file1 = open("hashes.txt","a")
            file1.write("\n" + str(zaks_Hash))
            file1.close()

            file3 = open("timestamped_frames.txt","a")
            sofn = frame_name.split('/')[2:]
            string_of_frame_name = str(sofn)

            file3.write("\n" + current_time_of_video + " " +  string_of_frame_name + " = " + str(zaks_Hash))
            file3.close()

            # iterate over each 3 seconds in the video / used for timestamped_frames.txt
            counter_id = counter_id + 3

            cap.set(1, count)

            timeOfDup.append(str(current_time_of_video))

            # compare current hash to previous hash
            with open('hashes.txt') as infile:

                lines = infile.read().splitlines()
                currentHash = lines[-1]
                previousHash = lines[-2]

                if currentHash == previousHash:
                    hashCount +=1
                else:
                    timeOfDup[:] = []

            if hashCount == 4:
                duplicatesFound(str(zaks_Hash), timeOfDup)
 
            #break while scanning if user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else: 
            cap.release()
            break

    # Release all space and windows once done 
    cv2.destroyAllWindows()

    if hashCount < 3:

        noDuplicatesFound()
        
    sys.exit()


art.tprint("\nFreeze Detector")

print ("      Welcome to 'Freeze Detector' Developed Zakaria-097")
print ("\n" + "      This program is a simple scanner to detect freezes in your video files.")

def askUser():

    userInput = input("\n"  +  "      Enter 's' To Scan Your File: " )

    target = ["s", "S"]

    if (userInput in target):
        start()
    else:
        askUser()

askUser()