__author__ = 'reisuke'

import rpyc
import cv2
import pickle
from sys import argv, exit


class RGB2GrayscaleService(rpyc.Service):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def exposed_image_converter(self, rgb_image):
        """image_converter(numpy.ndarray) => pickled numpy.ndarray

        Description:
        Convert RGB image matrix to grayscale image matrix.
        To use this function, argument must be a pickled numpy.ndarray
        which is read from cv2.imread function.

        Returns pickled numpy.ndarray
        """
        rgb_image_matrix = pickle.loads(rgb_image)
        grayscale_matrix = cv2.cvtColor(rgb_image_matrix, cv2.COLOR_RGB2GRAY)
        grayscale_matrix = pickle.dumps(grayscale_matrix)
        return grayscale_matrix


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    argument = argv[1:]
    if len(argument) != 1:
        print "Usage: python rpyc_server.py [hostname]:[port]"
        print "Example: python rpyc_server.py localhost:9000"
        exit(2)

    hostname, port = argument[0].split(':')
    t = ThreadedServer(RGB2GrayscaleService, hostname=hostname, port=int(port))
    t.start()