import csv
import datetime
import usb.core
import usb.util
from usb.backend import libusb1
import sys
import os

from keyboardVal import decode_hid_keycode

# Construct the path to the libusb DLL
current_dir = os.path.dirname(os.path.abspath(__file__))
libusb_path = os.path.normpath(os.path.join(current_dir, os.pardir, 'DLLs', 'libusb-1.0.dll'))
be = libusb1.get_backend(find_library=lambda x: libusb_path)

# Stockage de la liste et de celui en cours
barcode_characters = []
list_barcodes = []

def save_to_csv(filename='Liste_code.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Barcode', 'Time'])  # Header
        for barcode, time in list_barcodes:
            writer.writerow([barcode, time])

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

    print("Scanner de code-barres prêt. Scannez un code-barres...")

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
                            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                            list_barcodes.append((complete_barcode, timestamp))
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
    lire_code_barre()