import cv2
import numpy as np


class TrouDetector:
    def __init__(self, min_contour_area=100, threshold=60):
        """
        Initialise le détecteur de trous.

        :param min_contour_area: surface minimale pour considérer un contour comme trou.
        :param threshold: seuil binaire pour séparer fond et trous.
        """
        self.min_contour_area = min_contour_area
        self.threshold = threshold

    def detect_trous(self, frame):
        """
        Détecte les trous dans une image (frame).
        Retourne une liste de contours détectés et le masque binaire.

        :param frame: image BGR (numpy array)
        :return: (list_contours, mask)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        _, thresh = cv2.threshold(blurred, self.threshold, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        trous = [cnt for cnt in contours if cv2.contourArea(cnt) > self.min_contour_area]

        return trous, thresh

    def process_frame(self, frame, draw_trous=True):
        """
        Traite une seule frame et retourne :
        - une copie annotée (si draw_trous est True)
        - les contours détectés
        - le masque

        :param frame: image BGR
        :param draw_trous: dessine les trous détectés si True
        :return: frame_result, contours, mask
        """
        trous, mask = self.detect_trous(frame)

        frame_result = frame.copy()
        if draw_trous and trous:
            cv2.drawContours(frame_result, trous, -1, (0, 0, 255), 2)

        return frame_result, trous, mask