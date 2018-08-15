#!/usr/bin/python3

import subprocess as sp
import os

for filename in os.listdir("diff_comp/"):
	#print(frame + " " + layer + " "+ size + " "+ p)
	comand = "./3rdparty/zfp/bin/zfp -h -z diff_comp/"+filename+" -o diff_comp/"+filename+"_decomp"
	print(comand)
	sp.Popen(comand, shell=True).wait()
		

	