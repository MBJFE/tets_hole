import cv2
import os
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime

class VideoSaverThread(QThread):
    finished = pyqtSignal(str)  # Signal avec le chemin du fichier vidéo

    def __init__(self, cap, frame_buffer, fps):
        super().__init__()
        self.cap = cap
        self.frame_buffer = frame_buffer
        self.fps = fps

    def run(self):
        frames_before = self.frame_buffer[-(self.fps * 5):]
        frames_after = []

        for _ in range(self.fps * 5):
            ret, frame = self.cap.read()
            if not ret:
                break
            frames_after.append(frame)
            cv2.waitKey(int(1000 / self.fps))

        all_frames = frames_before + frames_after
        if all_frames:
            height, width, _ = all_frames[0].shape
            filename = QDateTime.currentDateTime().toString("yyyyMMdd_HHmmss") + "_casse.avi"
            filepath = os.path.abspath(filename)

            out = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'XVID'), self.fps, (width, height))
            for frame in all_frames:
                out.write(frame)
            out.release()

            self.finished.emit(filepath)
