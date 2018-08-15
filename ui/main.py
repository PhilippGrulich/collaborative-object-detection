#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we create a simple
window in PyQt5.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

import sys
import imagedetector
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QPlainTextEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.QtWidgets import QMainWindow
import numpy as np
import config as c
import videoPlayer
import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


config = c.Config()


def series_to_polyline(xdata, ydata):
    """Convert series data to QPolygon(F) polyline

    This code is derived from PythonQwt's function named
    `qwt.plot_curve.series_to_polyline`"""
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(4 * polyline.size() * tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size - 1) * 2 + 1:2] = xdata
    memory[1:(size - 1) * 2 + 2:2] = ydata
    return polyline

class PlotCanvas(FigureCanvas):



    def __init__(self,  name, ylable, width=5, height=2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(None)
        self.ax =  self.figure.add_subplot(111)
        self.ax.set_title(name)
        self.ax.set_ylabel(ylable)
        self.ylable = ylable
        #self.ax.set_ylim(0,50)
        self.ax.set_xlabel("frames")

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.figure.tight_layout()



    def plot(self,data):
        self.ax.cla()
        self.ax.plot(data, 'r-')
        #self.ax.set_ylim(0,5)
        #self.ax.set_yscale("log")
        self.ax.set_ylabel(self.ylable)
        self.ax.set_xlabel("frames")
        self.draw()

class Window2(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.mainLayout = QVBoxLayout()
        # top
        self.mainLayout.addWidget(self.frameGroup())

        self.setLayout(self.mainLayout)
        self.setFixedSize(1500, 800)
        self.show()
        player = videoPlayer.Player()
        player.config = config
        player.play()

    def frameGroup(self):
        horizontalGroupBox = QGroupBox("(a) Frames display")

        topLayout = QVBoxLayout()

        #topLabel = QLabel("(a) Frame display", self)
        #topLabel.setStyleSheet("font-weight: bold;")
        #topLabel.setAlignment(Qt.AlignCenter)

        #topLayout.addWidget(topLabel, 0, 0, 1, 2)
        frameLayout = QHBoxLayout()
        leftImage = QLabel(self)
        config.rawImage = leftImage
        leftImage.setAlignment(Qt.AlignCenter)
        frameLayout.addWidget(leftImage)

        rightImage = QLabel(self)
        config.predImage = rightImage
        rightImage.setAlignment(Qt.AlignCenter)
        frameLayout.addWidget(rightImage)

        topLayout.addLayout(frameLayout)
        areaBox = QHBoxLayout()
        b = QPlainTextEdit(self)
        b.insertPlainText("You can write text here.\n")
        b.setFixedSize(1000, 200)
        config.resultText = b
        areaBox.addWidget(b)
        areaBox.setAlignment(Qt.AlignCenter)
        topLayout.addLayout(areaBox)

        pauseBtn = QPushButton()
        pauseBtn.setIcon(QIcon("icons/pause.png"))
        pauseBtn.setFixedSize(32, 32)
        pauseBtn.clicked.connect(lambda: config.updateRun("pause"))

        playBtn = QPushButton("")
        playBtn.setIcon(QIcon("icons/play.png"))
        playBtn.setFixedSize(32, 32)
        playBtn.clicked.connect(lambda: config.updateRun("play"))
        stop = QPushButton("")
        stop.setFixedSize(32, 32)
        stop.setIcon(QIcon("icons/stop.png"))

        stop.clicked.connect(lambda: config.updateRun("stop"))
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(playBtn)
        btnLayout.addWidget(pauseBtn)
        btnLayout.addWidget(stop)

        topLayout.addLayout(btnLayout)

        horizontalGroupBox.setLayout(topLayout)
        return horizontalGroupBox


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.mainLayout = QVBoxLayout()
        # top
        self.mainLayout.addWidget(self.configGroup())

        self.mainLayout.addWidget(self.evaluationGroup())
        self.mainLayout.addWidget(self.highlightGroup())

        self.setLayout(self.mainLayout)
        self.setFixedSize(500, 1000)
        self.show()

    def configGroup(self):
        horizontalGroupBox = QGroupBox("(b) Techniques configuration")

        topLayout = QGridLayout()

        #topLabel = QLabel("(b) Techniques configuration")
        #topLabel.setStyleSheet("font-weight: bold;")
        #topLabel.setAlignment(Qt.AlignCenter)

        #topLayout.addWidget(topLabel, 0, 0, 1, 2)

        videoLayout = QVBoxLayout()
        videoSelectionLayout = QHBoxLayout()
        videoSelectionLabel = QLabel("Video File:", self)
        videoSelectionLayout.addWidget(videoSelectionLabel)
        videoSelectionComboBox = QComboBox()
        videoSelectionComboBox.currentIndexChanged.connect(config.updateSettings)
        config.videoSelectionComboBox = videoSelectionComboBox
        videoSelectionComboBox.addItem("Highway")
        videoSelectionComboBox.addItem("Berlin Street")
        videoSelectionLayout.addWidget(videoSelectionComboBox)
        videoLayout.addLayout(videoSelectionLayout)

        networkelectionLayout = QHBoxLayout()
        networkSelectionLabel = QLabel("Network Selection:", self)

        networkSelectionComboBox = QComboBox()
        networkSelectionComboBox.currentIndexChanged.connect(config.updateSettings)
        config.networkSelectionComboBox = networkSelectionComboBox
        networkSelectionComboBox.addItem("Tiny Yolo")
        networkSelectionComboBox.addItem("Yolo")
        networkelectionLayout.addWidget(networkSelectionLabel)
        networkelectionLayout.addWidget(networkSelectionComboBox)
        # videoLayout.setLayout(networkelectionLayout)
        videoLayout.addLayout(networkelectionLayout)

        topLayout.addLayout(videoLayout, 1, 0)

        configWidget = QWidget()
        configLayout = QVBoxLayout()
        configWidget.setLayout(configLayout)

        transferTechniquesLabel = QLabel("Transfer Technique:")
        configLayout.addWidget(transferTechniquesLabel)
        processOnEdgeBtn = QPushButton("Process on Edge")
        processOnEdgeBtn.setCheckable(True)
        config.processOnEdgeBtn = processOnEdgeBtn
        processOnEdgeBtn.clicked.connect(config.updateSettings)
        configLayout.addWidget(processOnEdgeBtn)

        compressionCheckbox = QCheckBox("Compression")
        compressionCheckbox.stateChanged.connect(config.updateSettings)
        config.compressionCheckbox = compressionCheckbox
        configLayout.addWidget(compressionCheckbox)

        diffCheckbox = QCheckBox("Differential Communication")
        diffCheckbox.stateChanged.connect(config.updateSettings)
        config.diffCheckbox = diffCheckbox
        configLayout.addWidget(diffCheckbox)

        splittingCheckbox = QCheckBox("Splitting")
        configLayout.addWidget(splittingCheckbox)
        splittingCheckbox.stateChanged.connect(config.updateSettings)
        config.splittingCheckbox = splittingCheckbox;

        topLayout.addWidget(configWidget, 1, 1)

        parammeterLayout = QVBoxLayout()

        parammeterLayout.addWidget(QLabel("Parameters", self))

        splittLayout = QHBoxLayout()
        splittLayout.addWidget(QLabel("Splittlayer:", self))
        splittingLayerComboBox = QComboBox()
        splittingLayerComboBox.currentIndexChanged.connect(config.updateSettings)
        for x in range(1,15):
            splittingLayerComboBox.addItem(str(x))
        splittLayout.addWidget(splittingLayerComboBox)
        config.splittingLayerComboBox = splittingLayerComboBox

        parammeterLayout.addLayout(splittLayout)

        vectorCompressionLayout = QHBoxLayout()
        vectorCompressionLayout.addWidget(QLabel("Nr of compression bits:", self))
        vectorCompressionCombobox = QComboBox()
        vectorCompressionCombobox.activated.connect(config.updateSettings)
        for x in range(1, 30, 5):
            vectorCompressionCombobox.addItem(str(x))

        config.vectorCompressionCombobox = vectorCompressionCombobox
        vectorCompressionLayout.addWidget(vectorCompressionCombobox)
        parammeterLayout.addLayout(vectorCompressionLayout)

        jpgCompressionLayout = QHBoxLayout()
        jpgCompressionLayout.addWidget(QLabel("JPG Compression:", self))
        jpgCompressionCombobox = QComboBox()
        jpgCompressionCombobox.currentIndexChanged.connect(config.updateSettings)
        for x in range(0, 110, 10):
            jpgCompressionCombobox.addItem(str(x) + "%")
        config.jpgCompressionCombobox = jpgCompressionCombobox
        jpgCompressionLayout.addWidget(jpgCompressionCombobox)
        parammeterLayout.addLayout(jpgCompressionLayout)

        topLayout.addLayout(parammeterLayout, 2, 0, 1, 2)
        # topLayout.addWidget(weightLayout, 3, 0)

        horizontalGroupBox.setLayout(topLayout)
        horizontalGroupBox.setFixedSize(480, 300)

        return horizontalGroupBox

    def evaluationGroup(self):
        horizontalGroupBox = QGroupBox("(c) Evaluation")
        horizontalGroupBox.setMinimumWidth(100)
        qvbox = QVBoxLayout()
        horizontalGroupBox.setLayout(qvbox)

        tabs = QTabWidget()

        latencyTab = QWidget()
        latencyLayout = QVBoxLayout()
        config.latencyChart  = PlotCanvas("Latency", "ms", width=5, height=4)
        latencyLayout.addWidget(config.latencyChart)

        # self.add_data(data, chart, color=Qt.red)
        latencyTab.setLayout(latencyLayout)

        compressionTab = QWidget()
        compressionLayout = QVBoxLayout()
        config.compressionChart  = PlotCanvas("Compression", "compression ratio", width=5, height=4)
        compressionLayout.addWidget(config.compressionChart)


        compressionTab.setLayout(compressionLayout)

        acucracyTab = QWidget()
        accuracyLayout = QVBoxLayout()
        config.accuracyChart  = PlotCanvas("Accuracy", "", width=5, height=4)
        accuracyLayout.addWidget(config.accuracyChart)
        # config.compressionChart = chart
        # data = [(0, 8), (1, 9), (2, 9), (3, 10), (4, 9)]
        # self.add_data(data, chart, color=Qt.red)
        acucracyTab.setLayout(accuracyLayout)

        tabs.addTab(latencyTab, "Latency")
        tabs.addTab(compressionTab, "Compression")
        tabs.addTab(acucracyTab, "Accuracy")

        qvbox.addWidget(tabs)
        horizontalGroupBox.setFixedSize(480, 400)
        return horizontalGroupBox


    def highlightGroup(self):
        horizontalGroupBox = QGroupBox("(d) Visualization")
        horizontalGroupBox.setMinimumWidth(100)
        qvbox = QVBoxLayout()
        hbox1 = QHBoxLayout()

        edgeIcon = QLabel()
        edgeIcon.setAlignment(Qt.AlignCenter)
        edgeIcon.setPixmap(QPixmap('icons/edge-icon.png'))
        h12 = QLabel("512KB transferred")
        config.transferedLabel = h12
        h12.setAlignment(Qt.AlignCenter)
        cloudIcon = QLabel()
        cloudIcon.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("icons/cloudIcon.png")
        pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio)
        cloudIcon.setPixmap(pixmap)
        hbox1.addWidget(edgeIcon)
        hbox1.addWidget(h12)
        hbox1.addWidget(cloudIcon)

        qvbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        t2 = QLabel("5 Layers on edge")
        config.edgeLayer = t2
        t2.setAlignment(Qt.AlignCenter)
        qvbox.addLayout(hbox2)

        hbox2.addWidget(t2)
        t2 = QLabel("")
        t2.setAlignment(Qt.AlignCenter)
        hbox2.addWidget(t2)
        t2 = QLabel("10 Layers on Cloud")
        config.cloudLayer = t2
        t2.setAlignment(Qt.AlignCenter)
        hbox2.addWidget(t2)
        horizontalGroupBox.setLayout(qvbox)

        horizontalGroupBox.setFixedSize(480, 200)
        return horizontalGroupBox

        # self.ncurves += 1

    def add_data(self, chart, color=None):
        curve = QLineSeries(chart)
        curve.setName("latency")
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        # for x in data:
        #   curve.append(x[0], x[1])
        # curve.append(series_to_polyline(xdata, ydata))
        curve.append(1, 10)
        curve.append(2, 10)
        #chart.addSeries(curve)
        #chart.createDefaultAxes()
        #chart.setAxisX(axisX, curve)
        #chart.setAxisY(axisY, curve)
        return curve



app = QApplication(sys.argv)
win = Window()
win2 = Window2()
# player.play()
sys.exit(app.exec_())
