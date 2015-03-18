__author__ = 'reisuke'

import numpy as np
import rpyc
import cv2
from sys import argv, exit


class RGB2GrayscaleService(rpyc.Service):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def exposed_image_converter(self, bytes_string, file_format):
        """image_converter(string, string) => string

        Description:
        Convert RGB image bytes string to grayscale image bytes string.
        To use this function, argument must be an image bytes string
        and file format in string.

        Returns a converted image bytes string.
        """
        numpy_array = np.fromstring(bytes_string, np.uint8)
        image_numpy = cv2.imdecode(numpy_array, cv2.CV_LOAD_IMAGE_COLOR)
        convert = cv2.cvtColor(image_numpy, cv2.COLOR_BGR2GRAY)

        result = cv2.imencode(file_format, convert)[1].tostring()
        return result

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