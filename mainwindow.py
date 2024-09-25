import os
import tkinter as tk
from tkinter import PhotoImage, messagebox
from pages.presence import PresenceApp  # Import the logic from presence.py


def relative_to_assets(folder: str, filename: str) -> str:
    """Helper function to get the assets path."""
    return os.path.join( "assets", folder, filename)


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1194x834")
        self.root.configure(bg="#FFFFFF")
        self.root.title("CodeChrono - Presence Scanning")

        # Canvas and layout
        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", height=834, width=1194, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.canvas.create_text(20.0, 0.0, anchor="nw", text="Menu", fill="#000000", font=("Roboto", 28 * -1))
        self.canvas.create_text(140.0, 0.0, anchor="nw", text="Langue", fill="#000000", font=("Roboto", 28 * -1))
        self.canvas.create_text(1194/2, 112.0, anchor="center", text="CodeChrono - Barcode Scanner", fill="#000000", font=("Roboto", 57 * -1))

        # Load button images
        self.button_image_1 = PhotoImage(file=relative_to_assets("mainwindow", "button_1.png"))
        self.button_image_hover_1 = PhotoImage(file=relative_to_assets("mainwindow", "button_hover_1.png"))

        self.button_image_2 = PhotoImage(file=relative_to_assets("mainwindow", "button_2.png"))
        self.button_image_hover_2 = PhotoImage(file=relative_to_assets("mainwindow", "button_hover_2.png"))

        self.button_image_3 = PhotoImage(file=relative_to_assets("mainwindow", "button_3.png"))
        self.button_image_hover_3 = PhotoImage(file=relative_to_assets("mainwindow", "button_hover_3.png"))

        # Create buttons
        self.presenceButton = tk.Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, relief="flat", command=self.open_presence)
        self.presenceButton.place(x=422.0, y=303.0, width=350.0, height=110.0)

        self.quitButton = tk.Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, relief="flat", command=self.quit_app)
        self.quitButton.place(x=422.0, y=587.0, width=350.0, height=110.0)

        self.reservationButton = tk.Button(image=self.button_image_3, borderwidth=0, highlightthickness=0, relief="flat",
                                           command=self.open_reservation)
        self.reservationButton.place(x=422.0, y=445.0, width=350.0, height=110.0)

        # Bind hover events to buttons
        self.presenceButton.bind('<Enter>', self.button_1_hover)
        self.presenceButton.bind('<Leave>', self.button_1_leave)

        self.quitButton.bind('<Enter>', self.button_2_hover)
        self.quitButton.bind('<Leave>', self.button_2_leave)

        self.reservationButton.bind('<Enter>', self.button_3_hover)
        self.reservationButton.bind('<Leave>', self.button_3_leave)

    # Hover effects for buttons
    def button_1_hover(self, e):
        self.presenceButton.config(image=self.button_image_hover_1)

    def button_1_leave(self, e):
        self.presenceButton.config(image=self.button_image_1)

    def button_2_hover(self, e):
        self.quitButton.config(image=self.button_image_hover_2)

    def button_2_leave(self, e):
        self.quitButton.config(image=self.button_image_2)

    def button_3_hover(self, e):
        self.reservationButton.config(image=self.button_image_hover_3)

    def button_3_leave(self, e):
        self.reservationButton.config(image=self.button_image_3)

    # Function to open the PresenceApp (scan logic)
    def open_presence(self):
        #self.root.withdraw()  # Hide the main window
        presence_window = tk.Toplevel(self.root)
        PresenceApp(presence_window)

    # Function to open the ReservationApp
    def open_reservation(self):
        #self.root.withdraw()
        messagebox.showwarning("Avertissement", "En cours de développement")
        #reservation_window = tk.Toplevel(self.root)

    # Function to quit the application
    def quit_app(self):
        self.root.quit()

# Main function to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()