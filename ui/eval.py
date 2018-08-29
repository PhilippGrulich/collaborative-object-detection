# /bin/darknet detector part ./bin/voc.names ./bin/tiny-yolo-voc.cfg ./bin/tiny-yolo-voc.weights -thresh 0.24 ./frame_50.jpg 50 -1

import subprocess as sp
import os
import cv2

import time
from shutil import copyfile
edgePath = "/../nn_splitting/edge/"
cloudPath = "/../nn_splitting/cloud/"


def cloudDetection():
    imagePath = "./input.png"

    if os.path.isfile("./data/edgePartition"):
        os.remove("./data/edgePartition")

    edgeComand = "." + edgePath + "bin/darknet detector test ." + edgePath + "bin/voc.names ." + edgePath + "bin/tiny-yolo-voc.cfg ." + "/../nn_splitting/tiny-yolo-voc.weights " \
                                                                                                                                                   "-thresh 0.24 " + str(
        imagePath) + " 50  -1 >> framedata/berlin/"+str(count)+".json"
    print(edgeComand)
    sp.Popen(edgeComand, shell=True).wait()


vidcap = cv2.VideoCapture('../video/highway.mp4')
vidcap = cv2.VideoCapture('../video/Berlin Street.mp4')


count = 0
success = True
while success:
    success,image = vidcap.read()
        # save frame as JPEG file
    print(count)
    if count % 10 == 0:
        cv2.imwrite("input.png", image)
        cloudDetection()
        copyfile("predictions.png","framedata/berlin/input_"+str(count)+".png")

    print("input")
    if cv2.waitKey(10) == 27:                     # exit if Escape is hit
        break

    count += 1

