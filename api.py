import cv2
import serial
import face_recognition as fr

# our libs importing
from backend.VideoThread import VideoThread

# Qt importing
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog


PORT = "COM6"
MIN_HORIZONTAL_BAND = 0
MAX_HORIZONTAL_BAND = 180
MIN_VERTICAL_BAND = 10
MAX_VERTICAL_BAND = 170
SIZE_OF_VIEW = (640, 480)

NO_AVALBLE_IMAGE = cv2.imread("icons/NO_AVAILABLE_IMAGE.jpg")
NO_AVALBLE_IMAGE = cv2.cvtColor(NO_AVALBLE_IMAGE, cv2.COLOR_BGR2RGB)
NO_AVALBLE_IMAGE = cv2.resize(NO_AVALBLE_IMAGE, (SIZE_OF_VIEW))


class api:
    def __init__(self, ui_obj):

        self.ui_obj = ui_obj
        self.camera = None
        self.selected_face_encoding = None
        # self.ser = serial.Serial(PORT, 115200, timeout=1000, parity=serial.PARITY_NONE)
        self.horizontal_position = 100
        self.vertical_position = 100
        str_ = (
            "m:"
            + str(self.horizontal_position)
            + ":"
            + str(self.vertical_position)
            + "-"
        ).encode("ASCII")
        # self.ser.write(str_)
        self.load_camera()
        self.widget_connector()
        self.set_image_label(self.ui_obj.LBL_live_camara, NO_AVALBLE_IMAGE)

    def load_camera(self):
        """loading camera for captureing video"""

        if self.camera == None:
            try:
                self.camera = cv2.VideoCapture(0)
            except:
                print("CONECTION WITH WEBCAM HAS PROBLEM")

    def start_live_on_another_thread(self):

        self.thread = QThread()
        self.Videoworker = VideoThread()
        self.Videoworker.set_param(
            camera=self.camera,
            encoded_wanted_face=self.selected_face_encoding,
            name_of_encoded_wanted_face="Amin",
        )
        self.Videoworker.moveToThread(self.thread)
        self.thread.started.connect(self.Videoworker.video_capture)
        self.Videoworker.finished.connect(self.thread.quit)
        self.Videoworker.finished.connect(self.Videoworker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.Videoworker.change_frame_signal.connect(self.show_live)
        self.Videoworker.x_and_y_pivots_signal.connect(
            self.guide_camera_to_face_location
        )
        self.Videoworker.finished.connect(self.set_no_image_label)
        self.thread.start()

    def show_live(self, frame):
        self.frame = frame
        self.set_image_label(self.ui_obj.LBL_live_camara, frame)

    def stop_live(self):
        self.Videoworker.set_live_flag(value=False)

    def set_no_image_label(self):
        self.set_image_label(self.ui_obj.LBL_live_camara, NO_AVALBLE_IMAGE)

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

    def upload_image(self):

        self.path_of_selected_img = QFileDialog.getOpenFileName(
            self.ui_obj, "Picture Location", "", "image Files (*.png *.jpg)"
        )
        if self.path_of_selected_img:
            try:
                selected_facce = fr.load_image_file(str(self.path_of_selected_img[0]))
                self.selected_face_encoding = fr.face_encodings(selected_facce)[0]
                self.Videoworker.set_encoded_wanted_face(
                    self.selected_face_encoding, "amin"
                )
                w = self.ui_obj.LBL_selected_image.width()
                h = self.ui_obj.LBL_selected_image.height()
                resized_img = cv2.resize(selected_facce, (w, h))
                self.set_image_label(self.ui_obj.LBL_selected_image, resized_img)
            except:
                pass
        else:
            pass

    def guide_camera_to_face_location(self, x_y):

        thresh = 15
        center_x = 640 // 2
        center_y = 480 // 2
        face_center_x, face_center_y = x_y

        x_distance = center_x - face_center_x
        y_distance = center_y - face_center_y

        if abs(x_distance) > thresh:
            if x_distance > 0:
                # print("left")
                self.horizontal_position += 5
            else:
                # print("right")
                self.horizontal_position -= 5

        if abs(y_distance) > thresh:
            if y_distance > 0:
                # print("up")
                self.vertical_position -= 5
            else:
                # print("down")
                self.vertical_position += 5

        str_ = (
            "m:"
            + str(self.horizontal_position)
            + ":"
            + str(self.vertical_position)
            + "-"
        ).encode("ASCII")
        # self.ser.write(str_)

    def widget_connector(self):
        """connect widget to function"""
        self.ui_obj.BTN_startLive.clicked.connect(self.start_live_on_another_thread)
        self.ui_obj.BTN_stopLive.clicked.connect(self.stop_live)
        self.ui_obj.BTN_upload_photo.clicked.connect(self.upload_image)
