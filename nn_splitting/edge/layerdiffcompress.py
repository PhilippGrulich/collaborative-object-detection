#!/usr/bin/python3

import subprocess as sp
import os

precisions=["8", "12"]


for filename in os.listdir("diff_trash/"):
	frame = filename.split("_")[1]
	layer = filename.split("_")[3]
	size = filename.split("_")[4]
	p = filename.split("_")[5]
	#print(frame + " " + layer + " "+ size + " "+ p)
	for b in precisions:
		comand = "./3rdparty/zfp/bin/zfp -f -1 "+ size +" -i diff_trash/"+filename+" -z ./diff_comp/frame_"+frame+"_layer_"+layer+"_"+size+"_"+p+"_"+b +" -p "+b+" -h"
		print(comand)
		sp.Popen(comand, shell=True).wait()

	