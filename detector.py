# Importing all necessary libraries 
import cv2 
from PIL import Image
import imagehash
from tkinter import filedialog
from PIL import Image
from utils import introMsg, generateFrameFolder, generateFiles, clearPreviousEntries, writeToFile, showResults

          
def startProgam():
    
    # create folder to store the video frames
    generateFrameFolder()
    
    # create all the necessary files
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
             
            #hashing each .openframe. frame_hash is the hash value of current frame
            frame_hash = imagehash.phash(Image.open(frame_name))

            # log the current frame
            print("   Scanning ->" + str(frame_hash))

            # write the hashes
            writeToFile("hashes.txt","a", "\n" + str(frame_hash))
            
            sofn = frame_name.split('/')[2:]

            # write to timestamped_frames
            writeToFile("timestamped_frames.txt","a", "\n" + current_time_of_video + " " +  str(sofn) + " = " + str(frame_hash))

            # update the counter / used for timestamped_frames.txt
            counter_id = counter_id + 3

            cap.set(1, count)

            # populate timeOfDup with the current time. 
            timeOfDup.append(str(current_time_of_video))

            # compare current hash value to the previous hash value
            with open('hashes.txt') as infile:

                lines = infile.read().splitlines()
                currentHash = lines[-1]
                previousHash = lines[-2]

                if currentHash == previousHash:
                    hashCount +=1
                else:
                    timeOfDup[:] = []
                    hashCount = 1

            # freezes found! 
            if hashCount == 4:
                
                writeToFile("results.txt", "a", "\n" + "   Freeze found!" + "\n\n""   Duplicate Hash:  " + str(frame_hash) + "      Time: " + str(timeOfDup[0]))
                showResults()
 
            #break while scanning if user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else: 
            cap.release()
            break

    # release all space and windows once done 
    cv2.destroyAllWindows()

    # no freezes found!
    if hashCount <= 3:
        writeToFile("results.txt", "a", "\n" + "   Scanning Complete:"  + "\n" + "\n" + "   No Freeze Found! ")
        
    showResults()


introMsg()

def promptUser():

    userInput = input("\n"  +  "      Enter 's' To Scan Your File: " )

    target = ["s", "S"]

    if (userInput in target):
        startProgam()
    else:
        promptUser()

promptUser()