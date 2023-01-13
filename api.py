import cv2
from backend.VideoThread import VideoThread
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread


class api:
    def __init__(self, ui_obj):

        self.ui_obj = ui_obj
        self.camera = None
        self.load_camera()
        self.widget_connector()

    def load_camera(self):
        """loading camera for captureing video"""

        if self.camera == None:
            try:
                self.camera = cv2.VideoCapture(0)
            except:
                print("CONECTION WITH WEBCAM HAS PROBLEM")

    def start_live_on_another_thread(self):

        self.thread = QThread()
        self.worker = VideoThread()
        self.worker.set_param(camera=self.camera)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.video_capture)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.change_frame_signal.connect(self.show_live)
        self.thread.start()

    def show_live(self, frame):
        self.set_image_label(self.ui_obj.LBL_live_camara, frame)

    def stop_live(self):
        self.worker.set_live_flag(value=False)

    def set_image_label(self, label_name, img):

        """set imnage in input label"""
        if len(img.shape) != 3:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        h, w, ch = img.shape

        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            img.data, w, h, bytes_per_line, QImage.Format_RGB888
        )
        label_name.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

    def widget_connector(self):
        """connect widget to function"""
        self.ui_obj.BTN_startLive.clicked.connect(self.start_live_on_another_thread)
        self.ui_obj.BTN_stopLive.clicked.connect(self.stop_live)
