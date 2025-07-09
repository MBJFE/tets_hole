from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class AdminLoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connexion Mode Process")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("Mot de passe :")
        layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Se connecter")
        self.login_button.clicked.connect(self.check_password)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.authenticated = False

    def check_password(self):
        if self.password_input.text() == "6760":  # À remplacer plus tard par une vraie gestion sécurisée
            self.authenticated = True
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", "Mot de passe incorrect")
