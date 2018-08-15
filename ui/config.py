from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.QtWidgets import QMainWindow
import numpy as np

import imagedetector

class Config:
    play = False
    networkSelectionComboBox = None
    videoSelectionComboBox = None
    compressionCheckbox = None
    diffCheckbox = None
    splittingLayerComboBox = None
    vectorCompressionCombobox = None
    jpgCompressionCombobox = None
    splittingCheckbox = None
    compressionArray = []
    edgeFileSize = 0
    edgeLatency = 0
    edgeLatencyArray = [0]
    accuracyArray = []
    playing=False
    f1 = 0
    videoFile= None
    cloudLayer =None
    edgeLayer = None

    resultText = None

    def updateRun(self, e):
        print("updateRun")
        self.playing = not self.playing
        print(e)

    def setSizeField(self,size):
        size = int(size / 1024)
        size = "{:,}".format(size)
        self.transferedLabel.setText(str(size) + "kb transferred")

    def updateSettings(self):
        print("update settings")

        videoText = str(self.videoSelectionComboBox.currentText())
        if videoText == "Highway":
            self.videoFile = '../frame_extractor/highway.mp4'
            self.detectionFile = "highway.csv"
        elif videoText == "Berlin Street":
            self.videoFile = 'Berlin Street.mp4'
            self.detectionFile = "berlin.csv"

        if(self.edgeLayer is not None and self.cloudLayer is not  None):
            splittingLayer = int(str(self.splittingLayerComboBox.currentText()))
            self.edgeLayer.setText(str(splittingLayer)+ " layer on edge")
            self.cloudLayer.setText(str(15-splittingLayer)+ " layer in cloud")

        self.jpgCompressionCombobox.setEnabled(False)
        self.splittingLayerComboBox.setEnabled(False)
        self.vectorCompressionCombobox.setEnabled(False)
        self.compressionCheckbox.setEnabled(True)
        self.compressionCheckbox.setCheckable(True)


        #self.splittingCheckbox.setCheckable(False)

        if self.processOnEdgeBtn != None:
            self.splittingCheckbox.setEnabled(True)
            if self.processOnEdgeBtn.isChecked():
                self.splittingCheckbox.setCheckable(True)
                if self.splittingCheckbox.checkState():
                    self.splittingLayerComboBox.setEnabled(True)
                    if self.compressionCheckbox.checkState():
                        self.vectorCompressionCombobox.setEnabled(True)
            else:
                if self.diffCheckbox.checkState():
                    self.jpgCompressionCombobox.setEnabled(False)
                    self.compressionCheckbox.setEnabled(False)
                    self.compressionCheckbox.setCheckable(False)
                elif self.compressionCheckbox.checkState():
                    self.jpgCompressionCombobox.setEnabled(True)
                self.splittingCheckbox.setCheckable(False)
                self.splittingCheckbox.setEnabled(False)
                #self.splittingCheckbox.setCheckable(False)

    def updateImage(self):
        print(self.text)
        if self.resultText != None:
            self.resultText.clear()
            self.resultText.insertPlainText(self.text)
            if self.compressionCheckbox.checkState():
                self.jpgCompressionCombobox.setEnabled(True)
            self.splittingCheckbox.setCheckable(False)
            #self.splittingCheckbox.setCheckable(False)


        pixmap = QPixmap('input.png')
        pixmap = pixmap.scaled(700, 700, Qt.KeepAspectRatio)
        self.rawImage.setPixmap(pixmap)
        #  self.predImage.load("./predictions.png")
        pixmap = QPixmap('predictions.png')
        pixmap = pixmap.scaled(700, 700, Qt.KeepAspectRatio)
        self.predImage.setPixmap(pixmap)
        #index = len(self.compressionArray)
        self.compressionArray.append(self.edgeFileSize)
        self.edgeLatencyArray.append(self.edgeLatency*1000)
        self.accuracyArray.append(self.f1)
        #print(self.compressionArray)
        # self.add_data(self.compressionArray, self.compressionChart, color=Qt.red)
        self.compressionChart.plot(self.compressionArray)
        self.latencyChart.plot(self.edgeLatencyArray)
        self.accuracyChart.plot(self.accuracyArray)


        print("update image")

    def add_data(self, data, chart, color=None):
        curve = QLineSeries(chart)
        curve.setName("latency")
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        for x in data:
            curve.append(x[0], x[1])
        # curve.append(series_to_polyline(xdata, ydata))
        chart.addSeries(curve)
        chart.createDefaultAxes()
        return curve;
