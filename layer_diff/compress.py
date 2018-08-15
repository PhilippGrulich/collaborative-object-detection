#!/usr/bin/python3

import subprocess as sp

precisions = [0.1,0.05, 0.01, 0.001, 0.0001]
images = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
layers = ["layer_0_2768896", "layer_1_692224", "  layer_2_1384448", "layer_3_346112", "layer_4_692224",
          "layer_5_173056", "layer_6_346112", "layer_7_86528", "layer_8_173056", "layer_9_43264", "layer_10_86528",
          "layer_11_86528",
          "layer_12_173056",
          "layer_13_173056",
          "layer_14_21125",
          "layer_15_21125"]
offset = 1

for i in range(offset, len(images)):
    for l in layers:
        for p in precisions:
            print(str(p) + " - " + str(images[i - offset]) + " - " + str(images[i]))
            comand = "./layer_compress c "+l.split("_")[2] +" "+  str(p) + " frame_" + str(images[i - offset]) + " frame_" + str(images[i]) + " " + l
            print(comand)
            sp.Popen(comand, shell=True).wait()
