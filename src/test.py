

import os
os.environ['PYUSB_DEBUG'] = 'debug'

def test():

    import usb.core
    from usb.backend import libusb1
    #be = libusb1.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")
    be = libusb1.get_backend(find_library=lambda x: ".\\libusb\\libusb-1.0.dll")
    dev = usb.core.find(backend=be, find_all=True)

if __name__ == "__main__":
    test()
