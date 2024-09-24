
from PyQt6.QtWidgets import QMessageBox, QFileDialog
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

        # Définir l'état initial (par exemple, français par défaut)
        self.change_language('fr')

    # Fonction pour capturer le code-barres et ajouter un timestamp
    def scan_code(self):
        scanned_code = self.entry.text()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if scanned_code and len(scanned_code) == 7:
            # Vérifier si le code-barres est déjà scanné (vérification des doublons)
            if any(scanned_code == code for code, _ in scanned_data):
                QMessageBox.warning(self, "Erreur", "Le code-barres est déjà scanné.")
            else:
                scanned_data.append((scanned_code, timestamp))
                self.entry.clear()
        else:
            QMessageBox.warning(self, "Erreur", "Le code-barres est invalide")

    # Fonction pour exporter les données en CSV
    def export_data(self):
        if not scanned_data:
            QMessageBox.warning(self, "Erreur", "Aucune donnée à exporter.")
            return

        # Ouvrir une boîte de dialogue pour sélectionner l'emplacement de sauvegarde
        file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer sous", "", "CSV Files (*.csv);;All Files (*)")

        # Vérifier si l'utilisateur a sélectionné un fichier
        if file_path:
            formatted_data = [(f"{code[:3]}-{code[3:]}", timestamp) for code, timestamp in scanned_data]
            # Exporter les données en CSV
            df = pd.DataFrame(formatted_data, columns=["Code étudiant", "Timestamp"])
            df.to_csv(file_path, index=False)
            QMessageBox.information(self, "Exportation réussie", f"Les données ont été exportées vers '{file_path}'.")

    # Fonction pour changer la langue
    def change_language(self, lang):
        if lang == 'fr':
            self.label.setText("Scannez le code-barres :")
            self.export_button.setText("Exporter en CSV")
            self.language_menu.actions()[0].setText("Anglais")
            self.language_menu.actions()[1].setText("Français")

            self.french_action.setDisabled(True)
            self.english_action.setDisabled(False)
        else:
            self.label.setText("Scan Barcode:")
            self.export_button.setText("Export to CSV")
            self.language_menu.actions()[0].setText("English")
            self.language_menu.actions()[1].setText("French")

            self.english_action.setDisabled(True)
            self.french_action.setDisabled(False)

