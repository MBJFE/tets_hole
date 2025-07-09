from PyQt5.QtWidgets import QApplication
import sys
import qdarkstyle
from interface_cam import InterfaceCam

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = InterfaceCam()
    window.show()
    sys.exit(app.exec_())
