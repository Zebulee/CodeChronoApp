import time
import usb.core
import usb.util
import os
from usb.backend import libusb1

os.environ['PYUSB_DEBUG'] = 'debug'

# Determine the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the libusb DLL in your project folder
libusb_path = os.path.join(current_dir, '..', 'libusb', 'libusb-1.0.dll')

be = libusb1.get_backend(find_library=lambda x: libusb_path)

# Trouver le périphérique USB (le scanner de code-barres)
def detect_usb_device():
    # Recherche du périphérique USB correspondant
    device = usb.core.find(backend=be, idVendor=0xe851, idProduct=0x1000)

    if device is None:
        return False
    
    return True

def wait_reconnect():
    print("Veuillez connecter le scanner.")
    while not detect_usb_device():
        time.sleep(1)  # Attendre 1 seconde avant de vérifier à nouveau
    print("Scanner connecté.")
        
def install_driver():
    try:
        # Vérifiez la connexion du scanner au début du programme
        if not detect_usb_device():
            raise Exception("Le Scanner n'est pas connecté")

        #continue and install driver in InstallForge
        #PNPUTIL /add-driver <InstallPath>\scanner\tera\2D_Barcode_Scanner.inf /install

    except Exception as e:
        print(e)
        wait_reconnect()  # Attendre la connexion du scanner
        # Reprendre la logique principale après reconnexion
        print("Reprise de la logique principale après connexion.")

if __name__ == "__main__":
    install_driver()