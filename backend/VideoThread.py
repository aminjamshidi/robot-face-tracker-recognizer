import cv2
import numpy as np
import face_recognition as fr
from PyQt5.QtCore import pyqtSignal, QThread

import time


class VideoThread(QThread):
    finished = pyqtSignal()
    change_frame_signal = pyqtSignal(np.ndarray)
    x_and_y_pivots_signal = pyqtSignal(tuple)

    def set_param(
        self, camera=None, encoded_wanted_face=None, name_of_encoded_wanted_face=None
    ):
        self.camera = camera
        self.live_flag = True
        self.frame = None
        self.encoded_wanted_face = encoded_wanted_face
        self.have_target = False
        self.name_of_encoded_wanted_face = name_of_encoded_wanted_face
        self.face_locations = None
        self.face_encodings = None

        self.t1 = time.time()
        self.t2 = 0
        self.num_frame_face_encoding = 0
        self.num_frame_fcae_location = 0

    def set_encoded_wanted_face(self, encoded_wanted_face, name_of_encoded_wanted_face):
        self.encoded_wanted_face = encoded_wanted_face
        self.name_of_encoded_wanted_face = name_of_encoded_wanted_face
        self.have_target = True

    def set_live_flag(self, value):
        self.live_flag = value

    def map_instand_for(self, face_encoding, face_location):

        if len(face_encoding) > 0:
            matches = fr.compare_faces(
                [self.encoded_wanted_face], face_encoding, tolerance=0.75
            )
            top, right, bottom, left = face_location
            cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(
                self.frame,
                (left, bottom - 35),
                (right, bottom),
                (0, 0, 255),
                cv2.FILLED,
            )

            if matches[0]:
                name = self.name_of_encoded_wanted_face
                face_center_x = (left + right) / 2
                face_center_y = (top + bottom) / 2
                self.x_and_y_pivots_signal.emit((face_center_x, face_center_y))
            else:
                name = "Unknown"

            cv2.putText(
                self.frame,
                name,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                1.0,
                (255, 255, 255),
                1,
            )
        return True

    def map_instand_for_simple_version(self, face_location):

        top, right, bottom, left = face_location
        cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 255, 0), 2)

        return True

    def video_capture(self):

        while self.live_flag:
            ret, frame = self.camera.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame = frame
            if ret:
                self.num_frame_face_encoding += 1
                self.num_frame_fcae_location += 1

                if (self.num_frame_fcae_location % 5) == 1:
                    self.face_locations = fr.face_locations(
                        frame, model="hog", number_of_times_to_upsample=1
                    )
                    self.num_frame_fcae_location = 0

                if (
                    ((self.num_frame_face_encoding % 15) == 1)
                    and self.have_target
                    and self.face_locations != None
                ):
                    self.num_frame_face_encoding = 0
                    self.face_encodings = fr.face_encodings(
                        frame, self.face_locations, num_jitters=1, model="small"
                    )
                if self.have_target and self.face_encodings != None:
                    _ = list(
                        map(
                            self.map_instand_for,
                            self.face_encodings,
                            self.face_locations,
                        )
                    )
                else:
                    _ = list(
                        map(
                            self.map_instand_for_simple_version,
                            self.face_locations,
                        )
                    )

                self.change_frame_signal.emit(self.frame)

        self.finished.emit()
