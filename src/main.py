import usb.core
import usb.util
from usb.backend import libusb1
import sys
import os

os.environ['PYUSB_DEBUG'] = 'debug'

be = libusb1.get_backend(find_library=lambda x: "libusb\\libusb-1.0.dll")

def lire_code_barre():
    # Trouver le périphérique USB correspondant (scanner de code-barres)
    device = usb.core.find(backend=be, find_all=True)  # Remplacez avec l'ID du fabricant et du produit¸
    print(device)

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
                code_barre = ''.join([chr(x) for x in data if x > 0])
                print(f"Code-barres reçu : {code_barre}")
            except usb.core.USBError as e:
                if e.args == ('Operation timed out',):
                    continue
    except KeyboardInterrupt:
        print("\nArrêt de l'application.")
        sys.exit(0)

if __name__ == "__main__":
    lire_code_barre()
