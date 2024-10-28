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
    device = usb.core.find(backend=be, find_all=True)
    print(device)

    if device is None:
        print("Aucun périphérique USB trouvé.")
        return None

    for dev in device:
        print(f"ID: {hex(dev.idVendor)}:{hex(dev.idProduct)}")

    return device

if __name__ == "__main__":
    detect_usb_device()
