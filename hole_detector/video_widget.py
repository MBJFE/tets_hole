from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class VideoWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(620, 440)
        self.setStyleSheet("background-color: black;")
        self.setAlignment(Qt.AlignCenter)

    def update_frame(self, image):
        self.setPixmap(QPixmap.fromImage(image))
