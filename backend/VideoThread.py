import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread


class VideoThread(QThread):
    finished = pyqtSignal()
    change_frame_signal = pyqtSignal(np.ndarray)

    def set_param(
        self,
        camera=None,
    ):
        self.camera = camera
        self.live_flag = True

    def set_live_flag(self, value):
        self.live_flag = value

    def video_capture(self):

        while self.live_flag:
            ret, frame = self.camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if ret:
                self.change_frame_signal.emit(frame)
        self.finished.emit()
