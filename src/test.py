import usb.core
from usb.backend import libusb1
import os
os.environ['PYUSB_DEBUG'] = 'debug'

# Determine the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the libusb DLL in your project folder
libusb_path = os.path.join(current_dir, '..', 'libusb', 'libusb-1.0.dll')

# Print the path to verify it's correct
print(f"Using libusb DLL from: {libusb_path}")

be = libusb1.get_backend(find_library=lambda x: libusb_path)

def test():

    #be = libusb1.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")
    #be = libusb1.get_backend(find_library=lambda x: ".\\libusb\\libusb-1.0.dll")
    dev = usb.core.find(backend=be, find_all=True)

if __name__ == "__main__":
    test()
