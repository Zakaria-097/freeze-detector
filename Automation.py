# Importing all necessary libraries 
import cv2 
import os 
from PIL import Image
import imagehash
import numpy as np
import collections 
import os, shutil
import webbrowser
from tkinter import filedialog # needed to allow users to select video 
import itertools

try:

    # creating a folder named data 
    if not os.path.exists('Zaks_frames_scan'): 
        os.makedirs('Zaks_frames_scan')
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
    folder = 'Zaks_frames_scan'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))



    #remove stuff in our text file if stuff already there
    f = open('testing.txt', 'r+')
    f.truncate(0)
    f.close()

    f2 = open('testing2.txt', 'r+')
    f2.truncate(0)
    f2.close()

    f3 = open('timestamped_frames.txt', 'r+')
    f3.truncate(0)
    f3.close()



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
            frame_name = './Zaks_frames_scan/frame' + str(count) + '.jpg'

            # writing the extracted images
            cv2.imwrite(frame_name, frame)

            #hashing each frame
            zaks_Hash = imagehash.phash(Image.open(frame_name))

            print("   Scanning ->" + str(frame_name) + " = " + str(zaks_Hash))

            #open text file
            file1 = open("testing.txt","a")
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
        print ("\n" + "   Scanning 100% Complete " + "\n")  

    def openResults():
        #after result is written to testing2.txt -> open them so the user can see the reult 
        webbrowser.open("timestamped_frames.txt")
        webbrowser.open("testing2.txt")

    def noDupsFound():
        #write to results txt file that no dups found
        file20 = open("testing2.txt","a")
        file20.write( "\n" + "   Scanning Complete:"  + "\n" + "\n" + "   No Freeze Found! ")
        file20.close()
        #spit out the result to inform the user
        webbrowser.open("testing2.txt")


    testing_file = open('testing.txt')
    #this skips the first 81 lines in the txt file - 81 lines = 4 minutes
    lines = testing_file.readlines()[72:]
    testing_file.close()

    #duplicate testing in testing.txt
    with open('testing.txt') as infile:
 
        counts = collections.Counter(l.strip() for l in lines)
        variable_test = 0

    for line, counts in counts.most_common():

        file2 = open("testing2.txt","a")

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

    



text = "Freeze Detector"
from PIL import Image, ImageDraw, ImageFont
import numpy as np
myfont = ImageFont.truetype("verdanab.ttf", 12)
size = myfont.getsize(text)
img = Image.new("1",size,"black")
draw = ImageDraw.Draw(img)
draw.text((0, 0), text, "white", font=myfont)
pixels = np.array(img, dtype=np.uint8)
chars = np.array([' ','#'], dtype="U1")[pixels]
strings = chars.view('U' + str(chars.shape[1])).flatten()
print( "\n".join(strings))


print ("\n" + "\n" + "\n" + "      Welcome to 'Freeze Detector' Developed by SmartOdds Ltd")
print ("\n" + "      This program was developed by Zakaria for the SAT's Team")

def aboutSection():
    print ("\n" + "\n" + "         Welcome to Freeze Detector ")
    print ( "         This program was developed to check for freezes & pauses within a given video file")



def askUser():

    userInput = input("\n"  +  "      Enter 'start' To Continue: " )

    if (userInput == "about"):
        aboutSection()


    if (userInput == "start" or userInput=="start " or userInput=="START" or userInput=="START " or userInput=="Start" or userInput=="Start "):
        automationFunction()

    if (userInput =="exit" or userInput =="exit " or userInput=="EXIT" or userInput =="quit"):
        import sys
        sys.exit()

    if(userInput != "start" and userInput!="start " and userInput!="START" and userInput!="START " and userInput!="Start" and userInput!="Start " and userInput !="exit"):
        askUser()

askUser()