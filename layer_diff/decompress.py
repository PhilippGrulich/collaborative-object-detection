#!/usr/bin/python3

import subprocess as sp

offset = 10
import os

for filename in os.listdir("/home/philipp/usb/projects/yolo2_light_partitioned/diff_comp/"):
    frameOriginal = str(int(filename.split("_")[1]) - offset)
    framePartial = filename.split("_")[1]
    layer = filename.split("_")[3]
    size = filename.split("_")[4]
    p = filename.split("_")[5]
    if filename.endswith("decomp"):
        print(filename)
        print(frameOriginal + " " + framePartial + " " + layer + " " + size + " " + p)
        comand = "./layer_compress d "+ size + " " + str(p) + " frame_" +frameOriginal + " frame_" + framePartial + " layer_" + layer + "_" + size + " " + filename
        print(comand)
        sp.Popen(comand, shell=True).wait()
