import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime


class PresenceApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("CodeChrono - Presence Scanning")

        # Create label and entry for barcode scanning
        self.label = tk.Label(self.root, text="Scan Barcode:", font=("Arial", 14))
        self.label.pack(pady=20)

        self.entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', self.scan_code)

        # Button to export data
        self.export_button = tk.Button(self.root, text="Export to CSV", command=self.export_data, font=("Arial", 12))
        self.export_button.pack(pady=20)

        # Button to return to the main menu
        self.back_button = tk.Button(self.root, text="Back to Main Menu", command=self.back_to_main, font=("Arial", 12))
        self.back_button.pack(pady=10)

        self.scanned_data = []

    # Function to scan code and add a timestamp
    def scan_code(self, event=None):
        scanned_code = self.entry.get()

        # Check if the scanned code has a length of 7 characters
        if len(scanned_code) == 7:
            # Check for duplicates
            if not any(scanned_code == code for code, _ in self.scanned_data):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.scanned_data.append((scanned_code, timestamp))
                self.entry.delete(0, tk.END)
                messagebox.showinfo("Scanned", f"Code-barres scanné : {scanned_code} à {timestamp}")
            else:
                messagebox.showwarning("Erreur", "Le code-barres est déjà scanné.")
        else:
            messagebox.showwarning("Erreur", "Le code-barres doit contenir exactement 7 caractères.")

    # Function to export the scanned data to CSV
    def export_data(self):
        if not self.scanned_data:
            messagebox.showwarning("Erreur", "Aucune donnée à exporter.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])

        if file_path:
            formatted_data = [(f"{code[:3]}-{code[3:]}", timestamp) for code, timestamp in self.scanned_data]
            df = pd.DataFrame(formatted_data, columns=["Code-barres", "Timestamp"])
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Exportation réussie", f"Les données ont été exportées vers '{file_path}'.")

    # Function to go back to the main window
    def back_to_main(self):
        self.root.destroy()  # Close the presence window
        main_window = tk.Toplevel(self.root)
        main_app = MainWindow(main_window)  # Reopen the main window

