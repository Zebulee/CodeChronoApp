
from PyQt6.QtWidgets import QMessageBox
from ui.codechronoui import CodeChronoUI
from datetime import datetime
import pandas as pd

# Liste pour stocker les codes scannés et les timestamps
scanned_data = []

class CodeChronoApp(CodeChronoUI):
    def __init__(self):
        super().__init__()

        # Connecter les événements
        self.entry.returnPressed.connect(self.scan_code)
        self.export_button.clicked.connect(self.export_data)

        # Connecter les actions du menu pour changer de langue
        self.english_action.triggered.connect(lambda: self.change_language('en'))
        self.french_action.triggered.connect(lambda: self.change_language('fr'))

    # Fonction pour capturer le code-barres et ajouter un timestamp
    def scan_code(self):
        scanned_code = self.entry.text()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if scanned_code:
            scanned_data.append((scanned_code, timestamp))
            self.entry.clear()
            QMessageBox.information(self, "Scanned", f"Code-barres scanné : {scanned_code} à {timestamp}")
        else:
            QMessageBox.warning(self, "Erreur", "Le champ est vide, veuillez scanner un code-barres.")

    # Fonction pour exporter les données en CSV
    def export_data(self):
        if not scanned_data:
            QMessageBox.warning(self, "Erreur", "Aucune donnée à exporter.")
            return

        df = pd.DataFrame(scanned_data, columns=["Code-barres", "Timestamp"])
        df.to_csv('codes_scannes.csv', index=False)
        QMessageBox.information(self, "Exportation réussie", "Les données ont été exportées vers 'codes_scannes.csv'.")

    # Fonction pour changer la langue
    def change_language(self, lang):
        if lang == 'fr':
            self.label.setText("Scannez le code-barres :")
            self.export_button.setText("Exporter en CSV")
            self.language_menu.actions()[0].setText("Français")
            self.language_menu.actions()[1].setText("English")
        else:
            self.label.setText("Scan Barcode:")
            self.export_button.setText("Export to CSV")
            self.language_menu.actions()[0].setText("English")
            self.language_menu.actions()[1].setText("Français")

