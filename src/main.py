import csv
from datetime import datetime
import usb.core
import usb.util
from usb.backend import libusb1
import sys
import os
from tkinter import Tk, filedialog

from connection import create_course, create_group, create_session, send_scanned_code
from keyboardVal import decode_hid_keycode

# Construct the path to the libusb DLL
current_dir = os.path.dirname(os.path.abspath(__file__))
libusb_path = os.path.normpath(os.path.join(current_dir, 'libusb', 'libusb-1.0.dll'))
be = libusb1.get_backend(find_library=lambda x: libusb_path)

# Stockage de la liste et de celui en cours
barcode_characters = []
list_barcodes = []
session_date = datetime.now().date()
scan_mode = 0

def save_to_csv():
    root = Tk()
    root.withdraw()
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            match scan_mode:
                case "1":
                    writer.writerow(['Barcode', 'Time', 'Book Name'])  # Header
                    for barcode, time, book_name in list_barcodes:
                        writer.writerow([barcode, time, book_name])
                case "2":
                    writer.writerow(['Barcode', 'Time'])  # Header
                    for barcode, time in list_barcodes:
                        writer.writerow([barcode, time]) 
    root.destroy() 
    
def select_mode():
    scan_mode = input("Entrer le type de scan ([1] pour les emprunts ou [2] pour les absences): ")
    match scan_mode:
        case "1":
            print("Emprunt")
        case "2":
            class_code = input("Entrer le sigle du cours (ex: 420-ASU-OS): ")
            group_code = input("Entrer le numéro du groupe (ex: 01)): ")
            #create_course(class_code)
            #create_group(class_code, group_code)
            #create_session(class_code, group_code, session_date)
        case _:
            print("Type non valide. Veillez utiliser un type valide.")
            select_mode()

def lire_code_barre():
    # Trouver le périphérique USB correspondant (scanner de code-barres)
    device = usb.core.find(backend=be,idVendor=0xe851, idProduct=0x1000)  # ID Scanner

    if device is None:
        print("Scanner de code-barres non trouvé.")
        sys.exit(1)

    # Configurer l'appareil pour interagir
    device.set_configuration()

    # Obtenez l'interface et le point d'accès (endpoint)
    cfg = device.get_active_configuration()
    intf = cfg[(0, 0)]

    # Trouver le point d'accès (endpoint) de lecture
    endpoint = usb.util.find_descriptor(
        intf,
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
    )

    if endpoint is None:
        print("Point d'accès de lecture non trouvé.")
        sys.exit(1)

    print("Scanner de code-barres prêt. Utiliser CTRL + C pour quitter l'application...")

    try:
        while True:
            try:
                # Lire les données du scanner
                data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
                # Convertir les données reçues en code-barres
                keycode = data[2]
                if keycode > 0:
                    character = decode_hid_keycode(keycode)
                    if character == 'ENTER':
                        # Ajouter le code-barres scanné à la liste.
                        if barcode_characters:
                            complete_barcode = ''.join(barcode_characters)
                            timestamp = datetime.now().strftime('%H:%M:%S')
                            match scan_mode:
                                case "1":
                                    book_name = input("Entrer le nom du livre: ")
                                    list_barcodes.append((complete_barcode, timestamp, book_name))
                                case "2":
                                    list_barcodes.append((complete_barcode, timestamp))
                                    #send_scanned_code(session_date, complete_barcode)
                            print(f"Code Scanné: {complete_barcode} at {timestamp}")
                            barcode_characters.clear()  # Effacer le tampon pour le prochain code-barres.
                    else:
                        # Accumuler les caractères pour le code-barres en cours.
                        barcode_characters.append(character)
            except usb.core.USBError as e:
                if e.args == ('Operation timed out',):
                    continue
    except KeyboardInterrupt:
        print("\nArrêt de l'application.")
        save_to_csv()
        sys.exit(0)

if __name__ == "__main__":
    select_mode()
    lire_code_barre()
