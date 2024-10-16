import usb.core
import usb.util
import libusb_package

# Trouver le périphérique USB (le scanner de code-barres)
def detect_usb_device():
    # Recherche du périphérique USB correspondant
    device = libusb_package.find(find_all=True)

    if device is None:
        print("Aucun périphérique USB trouvé.")
        return None

    for dev in device:
        print(f"ID: {hex(dev.idVendor)}:{hex(dev.idProduct)}")
        print(f"Manufacturer: {usb.util.get_string(dev, dev.iManufacturer)}")
        print(f"Product: {usb.util.get_string(dev, dev.iProduct)}")

    return device

# Fonction principale
if __name__ == "__main__":
    detect_usb_device()
