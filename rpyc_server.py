__author__ = 'reisuke'

import rpyc
import cv2
import os
from sys import argv, exit


class RGB2GrayscaleService(rpyc.Service):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def exposed_open(self, filename, mode):
        """open('path_to_file', 'mode') => file

        Description:
        Returns file
        """
        return open(filename, mode)

    def exposed_image_converter(self, rgb_image):
        """image_converter(string)

        Description:
        Convert RGB image file to grayscale image file.
        To use this function, argument must be an image file.

        Converted image will be saved in server.
        """
        image = cv2.imread(rgb_image)
        convert = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('grayscaled_' + rgb_image, convert)

    def exposed_clean(self, filename):
        """clean(filename)

        Description:
        Delete files
        """
        os.remove(filename)
        os.remove('grayscaled_' + filename)

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    argument = argv[1:]
    if len(argument) != 1:
        print "Usage: python rpyc_server.py [hostname]:[port]"
        print "Example: python rpyc_server.py localhost:9000"
        exit(2)

    hostname, port = argument[0].split(':')
    t = ThreadedServer(RGB2GrayscaleService, hostname=hostname, port=int(port), protocol_config={"allow_public_attrs": True})
    t.start()