import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QCalendarWidget, QTableWidget, QTableWidgetItem, QGridLayout,
    QSplitter, QToolBar, QAction, QMessageBox
)
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QImage, QIcon
from video_widget import VideoWidget
from admin_login import AdminLoginDialog
from interface_analyse_trou import VoirCasseWindow

class InterfaceCam(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface Caméras")
        self.setGeometry(100, 100, 1200, 700)
        self.mode_process = False

        # Layout principal
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Toolbar
        self.toolbar = QToolBar("Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("background: #2c2c2c; color: white;")
        settings_action = QAction(QIcon("icons/images.png"), "Mode Process", self)
        settings_action.triggered.connect(self.open_login_dialog)
        self.toolbar.addAction(settings_action)
        main_layout.addWidget(self.toolbar)

        # Layout de contenu
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        splitter = QSplitter(Qt.Horizontal)
        content_layout.addWidget(splitter)

        # Partie gauche (infos)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        left_layout.addWidget(self.time_label)

        self.date_label = QLabel()
        left_layout.addWidget(self.date_label)

        self.calendar = QCalendarWidget()
        self.calendar.setMaximumHeight(200)
        left_layout.addWidget(self.calendar)

        self.selected_date_label = QLabel("Date sélectionnée : ")
        left_layout.addWidget(self.selected_date_label)
        self.calendar.selectionChanged.connect(self.update_selected_date)

        self.table = QTableWidget(6, 6)
        self.table.setHorizontalHeaderLabels(["Heure", "Recette", "PO", "Longueur", "Largeur", "Taille"])
        left_layout.addWidget(self.table)

        self.btn_voir_casse = QPushButton("Voir casse")
        self.btn_voir_casse.clicked.connect(self.ouvrir_fenetre_casse)
        left_layout.addWidget(self.btn_voir_casse)

        splitter.addWidget(left_widget)

        # Partie droite (vidéos simulées)
        video_widget = QWidget()
        video_layout = QGridLayout(video_widget)

        self.est_label = QLabel("EST")
        self.est_label.setAlignment(Qt.AlignCenter)
        self.est_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        video_layout.addWidget(self.est_label, 0, 0, 1, 2)

        self.cam1 = VideoWidget()
        self.cam2 = VideoWidget()
        self.cam3 = VideoWidget()
        self.cam4 = VideoWidget()

        video_layout.addWidget(self.cam1, 1, 0)
        video_layout.addWidget(self.cam2, 1, 1)

        self.ouest_label = QLabel("OUEST")
        self.ouest_label.setAlignment(Qt.AlignCenter)
        self.ouest_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        video_layout.addWidget(self.ouest_label, 2, 0, 1, 2)

        video_layout.addWidget(self.cam3, 3, 0)
        video_layout.addWidget(self.cam4, 3, 1)

        splitter.addWidget(video_widget)
        splitter.setSizes([400, 800])

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.video_timer = QTimer()
        self.video_timer.timeout.connect(self.update_video)
        self.video_timer.start(30)

        self.update_time()
        self.update_selected_date()

    def update_time(self):
        current = QDateTime.currentDateTime()
        self.time_label.setText(current.toString("HH:mm:ss"))
        self.date_label.setText("Aujourd’hui : " + current.toString("dddd dd MMMM yyyy"))

    def update_selected_date(self):
        date = self.calendar.selectedDate()
        self.selected_date_label.setText("Date sélectionnée : " + date.toString("dddd dd MMMM yyyy"))

    def update_video(self):
        # Image verte simulant le flux caméra
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:] = (0, 255, 0)  # Vert

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        scaled = image.scaled(620, 440, Qt.KeepAspectRatio)

        self.cam1.update_frame(scaled)
        self.cam2.update_frame(scaled)
        self.cam3.update_frame(scaled)
        self.cam4.update_frame(scaled)

    def open_login_dialog(self):
        dialog = AdminLoginDialog(self)
        if dialog.exec_() == dialog.Accepted and dialog.authenticated:
            self.mode_process = True
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Information")
            msg_box.setText("✅ Mode Process activé")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()

    def closeEvent(self, event):
        # Rien à libérer puisque plus de webcam
        super().closeEvent(event)

    def ouvrir_fenetre_casse(self):
        self.fenetre_casse = VoirCasseWindow()
        self.fenetre_casse.show()

