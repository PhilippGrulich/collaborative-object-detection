import os
import subprocess as sp
import time

import cv2
from demjson import decode


import diffImage

edgePath = "/../nn_splitting/edge/"
cloudPath = "/../nn_splitting/cloud/"


def detect(config):

    print("start")

    if config.processOnEdgeBtn.isChecked():
        """Edge"""
        if config.splittingCheckbox.checkState():
            """Splitting"""
            splittingLayer = str(config.splittingLayerComboBox.currentText())
            if config.compressionCheckbox.checkState():
                splittingDetection(int(splittingLayer), config, True,
                                   str(config.vectorCompressionCombobox.currentText()))
            else:
                splittingDetection(int(splittingLayer), config)
        else:
            cloudDetection(config)

    else:
        """Cloud"""
        if config.compressionCheckbox.checkState():
            """Compression"""
            jpegCompressionFactor = str(config.jpgCompressionCombobox.currentText())[:-1]
            print(jpegCompressionFactor)
            jpegDetection(config, int(jpegCompressionFactor))

        elif config.diffCheckbox.checkState():
            """diff compression"""
            diffCloudDetection(config)
        else:
            cloudDetection(config)


def diffCloudDetection(config):
    diffImage.addInputImage()

    imagePath = "./input.png"

    if os.path.isfile("./data/edgePartition"):
        os.remove("./data/edgePartition")

    edgeComand = "." + edgePath + "bin/darknet detector test ." + edgePath + "bin/voc.names ." + edgePath + "bin/tiny-yolo-voc.cfg ." + edgePath + "bin/tiny-yolo-voc.weights " \
                                                                                                                                                   "-thresh 0.24 " + str(
        imagePath) + " 50  -1"
    print(edgeComand)
    config.edgeFileSize = 1

    filelist = [f for f in os.listdir("result/") if f.startswith("crop")]
    size = 0
    pngSize = os.path.getsize("./input.png")
    if len(filelist) == 0:
        config.setSizeField(pngSize)
        config.edgeFileSize = 1
    else:
        for f in filelist:
            size = size + os.path.getsize(os.path.join("result/", f))
        print("edgeSize " + str(size))
        config.setSizeField(size)
        config.edgeFileSize = pngSize / size

    config.edgeLatency = 0
    result = sp.Popen(edgeComand, shell=True, stdout=sp.PIPE)
    result.wait()
    for line in result.stdout:
        l = line.rstrip()
        r = decode(str(l.decode("utf-8")))
        evaluateAccuracy(r, config)
        setResultText(r, config)



def cloudDetection(config):
    imagePath = "./input.png"

    if os.path.isfile("./data/edgePartition"):
        os.remove("./data/edgePartition")

    edgeComand = "." + edgePath + "bin/darknet detector test ." + edgePath + "bin/voc.names ." + edgePath + "bin/tiny-yolo-voc.cfg ." + edgePath + "bin/tiny-yolo-voc.weights " \
                                                                                                                                                   "-thresh 0.24 " + str(

        imagePath) + " 50  -1"
    print(edgeComand)
    config.edgeFileSize = 1

    config.setSizeField(os.path.getsize("./input.png"))

    config.edgeLatency = 0

    result = sp.Popen(edgeComand, shell=True, stdout=sp.PIPE)
    result.wait()
    for line in result.stdout:
        l = line.rstrip()
        r = decode(str(l.decode("utf-8")))
        evaluateAccuracy(r, config)

        setResultText(r, config)
        if config.processOnEdgeBtn.isChecked():
            evaluateTime(r, config)
        else:
            config.edgeLatency = 0

def evaluateTime(record, config):
    config.edgeLatency = record["time"]



def setResultText(record, config):
    config.text = ""
    # config.resultText.clear()
    if "predication" in record:
        for detectedClass in record["predication"]:
            config.text = config.text + detectedClass["class"] + "\n"

    # config.resultText.insertPlainText("\n")
    # config.resultText.insertPlainText("\n")


def getGroups(classes):
    result = {}
    for referenceClasses in classes:
        if referenceClasses["class"] in result:
            result[referenceClasses["class"]] = result[referenceClasses["class"]] + 1
        else:
            result[referenceClasses["class"]] = 1
    return result


def evaluateAccuracy(record, config):
    print("eval" + str(record) )
    f = open(config.detectionFile)
    lines = f.readlines()
    ln = int(config.count / 10)
    print(ln)
    print(lines[ln])
    r2 = decode(lines[ln])
    f.close()
    TP = 0
    FP = 0
    FN = 0

    detectedGroups = getGroups(record["predication"])
    referenceGroups = getGroups(r2["predication"])
    print(detectedGroups)
    for detectedClass, count in detectedGroups.items():
        if detectedClass in referenceGroups:
            if referenceGroups[detectedClass] >= count:
                TP = TP + count
                FP = FP + referenceGroups[detectedClass] - count
            else:
                TP = TP + referenceGroups[detectedClass]
                FN = FN + count - referenceGroups[detectedClass]
        else:
            FP = FP + count

    for detectedClass, count in referenceGroups.items():
        if detectedClass not in detectedGroups:
            FN = FN + count

    print("TP:", TP, " FP:", FP, " FN:", FN)

    if TP == 0 and (FP == 0 or FN == 0):
        config.f1 = 1
        return

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    if recall + precision == 0:
        config.f1 = 0
    else:
        config.f1 = 2 * (recall * precision) / (recall + precision)

    print("TP:", TP, " FP:", FP, " FN:", FN, " precission:", precision, " recall", recall, " f1:", config.f1)


def jpegDetection(config, jpegCompressionFactor):
    imagePath = "./input.png"

    if os.path.isfile("./data/edgePartition"):
        os.remove("./data/edgePartition")

    start = time.time()

    img = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
    cv2.imwrite('./compress_img1.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, jpegCompressionFactor])

    config.edgeLatency = time.time() - start

    imagePath = './compress_img1.jpg'

    edgeComand = "." + edgePath + "bin/darknet detector test ." + edgePath + "bin/voc.names ." + edgePath + "bin/tiny-yolo-voc.cfg ." + edgePath + "bin/tiny-yolo-voc.weights " \
                                                                                                                                                   "-thresh 0.24 " + str(
        imagePath) + " 50  -1"
    print(edgeComand)
    pngSize = os.path.getsize("./input.png")
    jpegSize = os.path.getsize(imagePath)
    config.setSizeField(jpegSize)
    config.edgeFileSize = pngSize / jpegSize
    result = sp.Popen(edgeComand, shell=True, stdout=sp.PIPE)
    result.wait()
    print("Bla " )
    for line in result.stdout:
        l = line.rstrip()
        r = decode(str(l.decode("utf-8")))
        evaluateAccuracy(r, config)
        setResultText(r, config)


def splittingDetection(splittingLayer, config, compress=False, compressionBit="0"):
    imagePath = "./input.png"
    """
       Edge detection
       """

    if os.path.isfile("./data/edgePartition"):
        os.remove("./data/edgePartition")

    edgeComand = "." + edgePath + "bin/darknet detector part ." + edgePath + "bin/voc.names ." + edgePath + "bin/tiny-yolo-voc.cfg ." + edgePath + "bin/tiny-yolo-voc.weights " \
                                                                                                                                                   "-thresh 0.24 " + str(
        imagePath) + " 50 " + str(splittingLayer) + " "
    print(edgeComand)

    start = time.time()
    result = sp.Popen(edgeComand, shell=True, stdout=sp.PIPE)
    result.wait()
    for line in result.stdout:
        l = line.rstrip()
        print(l)
        r = decode(str(l.decode("utf-8")))
        evaluateTime(r, config)


    if os.path.isfile("./data/edgePartition"):
        edgeFileSize = os.path.getsize('./data/edgePartition')
        inputFileSize = os.path.getsize(imagePath)
        config.edgeFileSize = inputFileSize / edgeFileSize
        config.setSizeField(edgeFileSize)

    if compress == True:
        edgeFileSize = os.path.getsize('./data/edgePartition')
        compressComand = "." + edgePath + "3rdparty/zfp/bin/zfp -f -1 " + str(
            edgeFileSize / 4) + " -i " + './data/edgePartition' + " -z compressed -p " + compressionBit + " -h"
        print(compressComand)
        start = time.time()
        sp.Popen(compressComand, shell=True).wait()
        config.edgeLatency = config.edgeLatency + time.time() - start
        decompressComand = "." + edgePath + "3rdparty/zfp/bin/zfp -h -z " + 'compressed' + " -o ./data/edgePartition"
        print(decompressComand)
        sp.Popen(decompressComand, shell=True).wait()
        edgeFileSize = os.path.getsize("compressed")
        config.setSizeField(edgeFileSize)

        inputFileSize = os.path.getsize(imagePath)
        config.edgeFileSize = inputFileSize / edgeFileSize

    cloudComand = "." + cloudPath + "bin/darknet detector test ." + cloudPath + "bin/voc.names ." + cloudPath + "bin/tiny-yolo-voc.cfg ." + cloudPath + "bin/tiny-yolo-voc.weights " \
                                                                                                                                                        "-thresh 0.24 " + str(
        imagePath) + " ./data/edgePartition " + str(splittingLayer - 1) + " "

    print(cloudComand)
    result = sp.Popen(cloudComand, shell=True, stdout=sp.PIPE)
    result.wait()
    for line in result.stdout:
        l = line.rstrip()
        r = decode(str(l.decode("utf-8")))
        print("Line: " + str(r))
        evaluateAccuracy(r, config)
        setResultText(r, config)

