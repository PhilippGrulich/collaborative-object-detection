import cv2
import subprocess as sp
import os
import cv2
import time

bg1 = cv2.bgsegm.createBackgroundSubtractorMOG()


def clearFolder():
    filelist = [ f for f in os.listdir("result/")  ]
    for f in filelist:
        os.remove(os.path.join("result/", f))

def addInputImage():
    clearFolder()
    image = cv2.imread("input.png")
    res = bg1.apply(image)
    cv2.imwrite("diff.png", res)
    #cv2.imwrite("../differential_image/diff.png", res)
    cv2.imwrite("raw.png", image)
    #cv2.imwrite("../differential_image/raw.png", image)
    comand = "../differential_image/diff_image"
    print(comand)
    sp.Popen(comand, shell=True).wait()



#edgePath = "/../nn_splitting/edge/"
#cloudPath = "/../nn_splitting/cloud/"



#vidcap = cv2.VideoCapture('../frame_extractor/highway.mp4')
#success,image = vidcap.read()
#count = 0
#success = True
#while success:
#    success,image = vidcap.read()
#    cv2.imwrite("input.png", image)     # save frame as JPEG file
#    print(count)
#    if count % 10 == 0:
#        addInputImage()
#        time.sleep(2)
#    print("input")
#    if cv2.waitKey(10) == 27:                     # exit if Escape is hit
#        break

#    count += 1



