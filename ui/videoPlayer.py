import cv2
import time
from multiprocessing import Process
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import imagedetector


class Background(QObject):
    data = pyqtSignal(int)

    def __init__(self, config):
        super().__init__()
        self.config = config
        print(self.config.playing)

    @pyqtSlot()
    def work(self):
        #vidcap = cv2.VideoCapture('../frame_extractor/highway.mp4')

        file = self.config.videoFile
        while file is None:
            file = self.config.videoFile
            time.sleep(2)

        vidcap = cv2.VideoCapture(file)
        count = 0
        success = True

        while success:
            print(self.config.playing)
            if self.config.playing == True:
                if file is not self.config.videoFile:
                    file = self.config.videoFile
                    vidcap = cv2.VideoCapture(file)
                    count = 0
                success,image = vidcap.read()
                cv2.imwrite("input.png", image)     # save frame as JPEG file
                #self.config.updateImage()

                # time.sleep(0.25)
                if count % 10 == 0:
                    self.config.count= count
                    imagedetector.detect(self.config)
                    self.data.emit(1)

                print("input")
                if cv2.waitKey(10) == 27:                     # exit if Escape is hit
                    break

                count += 1
            else:
                time.sleep(2)



class Player:
    currentFrame = 0
    config = None
    __threads = []
    def play(self):
        b = Background(self.config)
        thread = QThread()
        b.moveToThread(thread)
        b.data.connect(self.config.updateImage)
        self.__threads.append((thread, b))
        thread.started.connect(b.work)
        thread.start()
        #b.start()
        print("start")