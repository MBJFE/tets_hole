import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSlider
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap


class VoirCasseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Détail de la casse")
        self.setGeometry(150, 150, 1000, 600)

        # Simuler des vidéos de 5 secondes à 30 FPS
        self.frames_cam1 = []
        self.frames_cam2 = []
        self.selected_frames = []
        self.frame_index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

        self.init_ui()
        self.load_dummy_video()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # === Partie gauche : Miniatures caméras
        left_layout = QVBoxLayout()

        self.cam1_preview = QLabel("Caméra 1")
        self.cam1_preview.setFixedSize(300, 200)
        self.cam1_preview.setStyleSheet("background-color: black;")
        self.cam1_preview.mousePressEvent = lambda e: self.select_camera(1)
        left_layout.addWidget(self.cam1_preview)

        self.cam2_preview = QLabel("Caméra 2")
        self.cam2_preview.setFixedSize(300, 200)
        self.cam2_preview.setStyleSheet("background-color: black;")
        self.cam2_preview.mousePressEvent = lambda e: self.select_camera(2)
        left_layout.addWidget(self.cam2_preview)

        main_layout.addLayout(left_layout)

        # === Partie droite : Affichage principal + contrôles
        right_layout = QVBoxLayout()

        self.main_video_label = QLabel("Aperçu")
        self.main_video_label.setFixedSize(640, 480)
        self.main_video_label.setStyleSheet("background-color: gray;")
        right_layout.addWidget(self.main_video_label)

        # Slider (curseur)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 149)
        self.slider.setValue(0)
        self.slider.sliderMoved.connect(self.slider_moved)
        right_layout.addWidget(self.slider)

        # Contrôles de lecture
        controls = QHBoxLayout()

        self.btn_prev = QPushButton("⏮ Frame -1")
        self.btn_prev.clicked.connect(self.prev_frame)
        controls.addWidget(self.btn_prev)

        self.btn_play_pause = QPushButton("▶ Play")
        self.btn_play_pause.clicked.connect(self.toggle_play)
        controls.addWidget(self.btn_play_pause)

        self.btn_next = QPushButton("⏭ Frame +1")
        self.btn_next.clicked.connect(self.next_frame)
        controls.addWidget(self.btn_next)

        right_layout.addLayout(controls)

        main_layout.addLayout(right_layout)

    def load_dummy_video(self):
        for _ in range(150):  # 5 sec à 30 FPS
            frame1 = np.full((480, 640, 3), (0, 255, 0), dtype=np.uint8)  # vert
            frame2 = np.full((480, 640, 3), (0, 0, 255), dtype=np.uint8)  # rouge
            self.frames_cam1.append(frame1)
            self.frames_cam2.append(frame2)

        self.update_preview(self.cam1_preview, self.frames_cam1[0])
        self.update_preview(self.cam2_preview, self.frames_cam2[0])
        self.select_camera(1)

    def update_preview(self, label, frame):
        image = self.convert_to_qimage(frame)
        pixmap = QPixmap.fromImage(image).scaled(label.size(), Qt.KeepAspectRatio)
        label.setPixmap(pixmap)

    def convert_to_qimage(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        return QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

    def select_camera(self, cam_number):
        if cam_number == 1:
            self.selected_frames = self.frames_cam1
        else:
            self.selected_frames = self.frames_cam2
        self.frame_index = 0
        self.slider.setValue(0)
        self.show_current_frame()

    def show_current_frame(self):
        if 0 <= self.frame_index < len(self.selected_frames):
            frame = self.selected_frames[self.frame_index]
            image = self.convert_to_qimage(frame)
            pixmap = QPixmap.fromImage(image).scaled(self.main_video_label.size(), Qt.KeepAspectRatio)
            self.main_video_label.setPixmap(pixmap)
            self.slider.setValue(self.frame_index)

    def toggle_play(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn_play_pause.setText("▶ Play")
        else:
            self.timer.start(33)
            self.btn_play_pause.setText("⏸ Pause")

    def next_frame(self):
        if self.frame_index < len(self.selected_frames) - 1:
            self.frame_index += 1
            self.show_current_frame()
        else:
            self.timer.stop()
            self.btn_play_pause.setText("▶ Play")

    def prev_frame(self):
        if self.frame_index > 0:
            self.frame_index -= 1
            self.show_current_frame()

    def slider_moved(self, value):
        self.frame_index = value
        self.show_current_frame()
