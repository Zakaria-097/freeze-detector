# Importing all necessary libraries 
import cv2 
import sys
import os 
from PIL import Image
import imagehash
import numpy as np
import collections 
import os, shutil
import webbrowser
from tkinter import filedialog #allow users to select video 
import art 
from PIL import Image

try:
    # creating a folder named data 
    if not os.path.exists('frames'): 
        os.makedirs('frames')
    # if not created then raise error
except OSError: 
    print ('Error: Creating directory of data') 


def automationFunction():

    def exit_program():
        import sys
        sys.exit()

    #initial variables
    count = 0
    counter_id = 0
    goneThroughScan = 0


    #remove stuff in data directory if stuff already in there
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


    #clear previous entries
    with open('hashes.txt', 'r+') as tes, \
        open('results.txt', 'r+') as tes2, \
        open('timestamped_frames.txt', 'r+') as tes3: tes.truncate(0), tes2.truncate(0), tes3.truncate(0)
        

    selected_fileName = filedialog.askopenfilename( filetypes = ( ("Video Files", "*.mp4"), ("All Files", "*.*") ))

    # Read the video from specified path 
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

            print("   Scanning ->" + str(frame_name) + " = " + str(zaks_Hash))

            #open text file
            file1 = open("hashes.txt","a")
            sss = str(zaks_Hash)
            file1.write("\n" + sss)
            file1.close()

            file3 = open("timestamped_frames.txt","a")
            sofn = frame_name.split('/')[2:]
            string_of_frame_name = str(sofn)
            # counter_id_str = str(counter_id)

            file3.write("\n" + current_time_of_video + " " +  string_of_frame_name + " = " + sss)
            file3.close()

            #iterate over each 3 seconds in the video / used for hashes_with_frames.txt
            counter_id = counter_id + 3

            goneThroughScan = 1

            cap.set(1, count)

            #break while scanning if user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else: 
            cap.release()
            break

    def scanningCompleted():
        print ("\n" + "   Scanning 100% Complete ")  

    def openResults():
        #after result is written to results.txt -> open them so the user can see the result 
        webbrowser.open("timestamped_frames.txt")
        webbrowser.open("results.txt")

    def noDupsFound():
        #write to results txt file that no dups found
        file20 = open("results.txt","a")
        file20.write( "\n" + "   Scanning Complete:"  + "\n" + "\n" + "   No Freeze Found! ")
        file20.close()
        
        #spit out the result to inform the user
        print("\n   No Freeze Found!")
        exitMessage()


    testing_file = open('hashes.txt')
    #this skips the first 81 lines in the txt file - 81 lines = 4 minutes
    lines = testing_file.readlines()[72:]
    testing_file.close()

    #duplicate testing in hashes.txt
    with open('hashes.txt') as infile:
 
        counts = collections.Counter(l.strip() for l in lines)
        variable_test = 0

    for line, counts in counts.most_common():

        file2 = open("results.txt","a")

        if (counts > 3):

            variable_test = 1
            string_count = str(counts)
            print ( "\n"+"   Hash:  " + line + "           duplicates: " + string_count)
            file2.write("\n""   Hash:  " + line + "           duplicates: " + string_count)
            file2.close()


    if (variable_test == 1 and goneThroughScan == 1): 
        scanningCompleted()
        openResults()
                        
    if (variable_test == 0 and goneThroughScan == 1): 
        scanningCompleted()
        noDupsFound()
        
    # Release all space and windows once done 
    cv2.destroyAllWindows()

    exit_program()


art.tprint("\nFreeze Detector")

print ("      Welcome to 'Freeze Detector' Developed by SmartOdds Ltd")
print ("\n" + "      This program was developed by Zakaria for the SAT's Team")

def aboutSection():
    print ("\n" + "\n" + "         Welcome to Freeze Detector ")
    print ( "         This program was developed to check for freezes & pauses within a given video file")


def exitMessage():
    userInput = input("\n\n"  +  "  Thank you for using this service :) Press any key to quit." )

def askUser():

    userInput = input("\n"  +  "      Enter 'start' To Scan Your File: " )

    if (userInput == "about"):
        aboutSection()

    if (userInput == "start" or userInput=="start " or userInput=="START" or userInput=="START " or userInput=="Start" or userInput=="Start "):
        automationFunction()

    if (userInput =="e" or userInput =="exit " or userInput=="EXIT" or userInput =="quit"): 
        sys.exit()

    if(userInput != "start" and userInput!="start " and userInput!="START" and userInput!="START " and userInput!="Start" and userInput!="Start " and userInput !="exit"):
        askUser()

askUser()