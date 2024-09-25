import os
import tkinter as tk
from tkinter import Canvas, Entry, Menu, filedialog, messagebox, PhotoImage
import pandas as pd
from datetime import datetime
from tktimepicker import SpinTimePickerModern, constants

# Global scanned data for barcode tracking
scanned_data = []


def relative_to_assets(folder: str, filename: str) -> str:
    """Helper function to get the assets path."""
    # Get the absolute path of the current directory (where presence.py is located)
    base_path = os.path.abspath(os.path.dirname(__file__))

    # Traverse up one directory to reach the project root, then access assets
    assets_path = os.path.join(base_path, "..", "assets", folder, filename)

    return os.path.normpath(assets_path)  # Normalize the path to handle ".."


def export_data():
    if not scanned_data:
        messagebox.showwarning("Erreur", "Aucune donnée à exporter.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    if file_path:
        formatted_data = [(f"{code[:3]}-{code[3:]}", timestamp) for code, timestamp in scanned_data]
        df = pd.DataFrame(formatted_data, columns=["Code-barres", "Timestamp"])
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Exportation réussie", f"Les données ont été exportées vers '{file_path}'.")


class PresenceApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1194x834")
        self.root.configure(bg="#FFFFFF")
        self.root.title("CodeChrono - Presence Scanning")

        #TDOO: change font menubar
        # Create a menu bar
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Create a "File" menu with a "Return to Menu" option
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Return to Main Menu", command=self.back_to_main)

        # Canvas and layout
        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=834,
            width=1194,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Add title and labels
        self.canvas.create_text(
            480.0, 85.0,
            anchor="nw",
            text="Présence",
            fill="#000000",
            font=("Roboto", 57 * -1)
        )

        self.canvas.create_text(
            67.0, 200.0,
            anchor="nw",
            text="Scanner le code-barres :",
            fill="#000000",
            font=("Roboto", 36 * -1)
        )

        # Entry for barcode input
        self.entry_barcode_Image = PhotoImage(
            file=relative_to_assets("presence", "entry_1.png"))
        self.canvas.create_image(
            813.0,
            222.0,
            image=self.entry_barcode_Image
        )
        self.entry_barcode = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_barcode.place(
            x=514.0,
            y=200.0,
            width=598.0,
            height=42.0
        )

        self.canvas.create_text(
            67.0,
            304.0,
            anchor="nw",
            text="Heure du début du cours : ",
            fill="#000000",
            font=("Roboto", 36 * -1)
        )

        time_picker = SpinTimePickerModern(self.root)
        time_picker.addAll(constants.HOURS24)  # adds hours clock, minutes and period
        time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Roboto", 36 * -1), hoverbg="#404040",
                                 hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
        time_picker.configure_separator(bg="#404040", fg="#ffffff", font=("Roboto", 36 * -1))

        time_picker.place(
            x=514.0,
            y=303.0,
            width=400.0,
            height=45.0
        )

        self.canvas.create_text(
            76.0,
            408.0,
            anchor="nw",
            text="Délai de grâce avant un retard :",
            fill="#000000",
            font=("Roboto", 36 * -1)
        )

        entry_image_3 = PhotoImage(
            file=relative_to_assets("presence", "entry_3.png"))
        self.canvas.create_image(
            714.0,
            430.0,
            image=entry_image_3
        )
        entry_3 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_3.place(
            x=605.0,
            y=395.0,
            width=218.0,
            height=68.0
        )

        self.canvas.create_text(
            67.0,
            551.0,
            anchor="nw",
            text="Nombre de code scanné :",
            fill="#000000",
            font=("Roboto", 36 * -1)
        )

        entry_image_4 = PhotoImage(
            file=relative_to_assets("presence", "entry_4.png"))
        self.canvas.create_image(
            631.0,
            578.5,
            image=entry_image_4
        )
        entry_4 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_4.place(
            x=524.0,
            y=548.0,
            width=214.0,
            height=59.0
        )

        self.canvas.create_text(
            859.0,
            407.0,
            anchor="nw",
            text="minutes",
            fill="#000000",
            font=("Roboto", 36 * -1)
        )

        # Load button images
        self.button_image_1 = PhotoImage(file=relative_to_assets("presence", "button_1.png"))
        self.button_image_hover_1 = PhotoImage(file=relative_to_assets("presence", "button_hover_1.png"))

        self.button_image_2 = PhotoImage(file=relative_to_assets("presence", "button_2.png"))
        self.button_image_hover_2 = PhotoImage(file=relative_to_assets("presence", "button_hover_2.png"))

        self.button_image_3 = PhotoImage(file=relative_to_assets("presence", "button_3.png"))
        self.button_image_hover_3 = PhotoImage(file=relative_to_assets("presence", "button_hover_3.png"))

        self.button_image_4 = PhotoImage(file=relative_to_assets("presence", "button_4.png"))
        self.button_image_hover_4 = PhotoImage(file=relative_to_assets("presence", "button_hover_4.png"))

        # Create buttons
        self.setTimeButton = tk.Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, relief="flat",
                                       command=self.set_Time)
        self.setTimeButton.place(x=956.0, y=271.0, width=190.0, height=110.0)

        self.omnivoxButton = tk.Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, relief="flat",
                                       command=self.export_omnivox)
        self.omnivoxButton.place(x=626.0, y=681.0, width=540.0, height=110.0)

        self.exportDataButton = tk.Button(image=self.button_image_3, borderwidth=0, highlightthickness=0, relief="flat",
                                          command=export_data)
        self.exportDataButton.place(x=43.0, y=681.0, width=540.0, height=110.0)

        self.viewDataButton = tk.Button(image=self.button_image_4, borderwidth=0, highlightthickness=0,
                                          relief="flat",
                                          command=self.view_data)
        self.viewDataButton.place( x=776.0, y=518.0, width=390.0, height=110.0)

        # Bind hover events to buttons
        self.setTimeButton.bind('<Enter>', self.button_1_hover)
        self.setTimeButton.bind('<Leave>', self.button_1_leave)

        self.omnivoxButton.bind('<Enter>', self.button_2_hover)
        self.omnivoxButton.bind('<Leave>', self.button_2_leave)

        self.exportDataButton.bind('<Enter>', self.button_3_hover)
        self.exportDataButton.bind('<Leave>', self.button_3_leave)

        self.viewDataButton.bind('<Enter>', self.button_4_hover)
        self.viewDataButton.bind('<Leave>', self.button_4_leave)

    # Hover effects for buttons

    def button_1_hover(self, e):
        self.setTimeButton.config(image=self.button_image_hover_1)

    def button_1_leave(self, e):
        self.setTimeButton.config(image=self.button_image_1)

    def button_2_hover(self, e):
        self.omnivoxButton.config(image=self.button_image_hover_2)

    def button_2_leave(self, e):
        self.omnivoxButton.config(image=self.button_image_2)

    def button_3_hover(self, e):
        self.exportDataButton.config(image=self.button_image_hover_3)

    def button_3_leave(self, e):
        self.exportDataButton.config(image=self.button_image_3)

    def button_4_hover(self, e):
        self.viewDataButton.config(image=self.button_image_hover_4)

    def button_4_leave(self, e):
        self.viewDataButton.config(image=self.button_image_4)

    # Logic for scanning the barcode
    def scan_code(self):
        scanned_code = self.entry_barcode.get()

        if len(scanned_code) == 7:  # Only accept 7-digit barcodes
            if not any(scanned_code == code for code, _ in scanned_data):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                scanned_data.append((scanned_code, timestamp))
                self.entry_barcode.delete(0, tk.END)
                messagebox.showinfo("Scanned", f"Code-barres scanné : {scanned_code} à {timestamp}")
            else:
                messagebox.showwarning("Erreur", "Le code-barres est déjà scanné.")
        else:
            messagebox.showwarning("Erreur", "Le code-barres doit contenir exactement 7 caractères.")

    # Logic for exporting scanned data to CSV

    def export_omnivox(self):
        return export_data()

    def set_Time(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def view_data(self):
        return 0

    # Function to go back to the main window
    def back_to_main(self):
        self.root.destroy()  # Close the presence window
        main_window = tk.Toplevel(self.root)
        #main_app = MainWindow(main_window)  # Reopen the main window

if __name__ == "__main__":
    root = tk.Tk()
    app = PresenceApp(root)
    root.mainloop()
