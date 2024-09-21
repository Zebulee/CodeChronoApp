from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMenuBar
from PyQt6.QtGui import QAction

class CodeChronoUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("CodeChrono - Barcode Scanner")
        self.setGeometry(100, 100, 400, 300)

        # Configuration du menu
        menu_bar = self.menuBar()
        self.language_menu = menu_bar.addMenu("Language")

        # Actions du menu
        self.english_action = QAction("English", self)
        self.french_action = QAction("Français", self)

        self.language_menu.addAction(self.english_action)
        self.language_menu.addAction(self.french_action)

        # Création du widget central
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # Layout vertical
        layout = QVBoxLayout()

        # Étiquette pour l'instruction
        self.label = QLabel("Scan Barcode:", self)
        layout.addWidget(self.label)

        # Zone de texte pour entrer les codes-barres
        self.entry = QLineEdit(self)
        layout.addWidget(self.entry)

        # Bouton pour exporter en CSV
        self.export_button = QPushButton("Export to CSV", self)
        layout.addWidget(self.export_button)

        # Appliquer le layout au widget central
        widget.setLayout(layout)
