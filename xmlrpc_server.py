from SimpleXMLRPCServer import SimpleXMLRPCServer, list_public_methods
import inspect
import cv2
import pickle


def expose(func):
    func.exposed = True
    return func


def is_exposed(func):
    return getattr(func, 'exposed', False)


class RGB2GrayscaleService:

    def __init__(self):
        self.PREFIX = 'RGB2Grayscale'

    def _dispatch(self, method, params):
        if not method.startswith(self.PREFIX + '.'):
            raise Exception('method "%s" is not supported' % method)

        method_name = method.partition('.')[2]
        func = getattr(self, method_name)
        if not is_exposed(func):
            raise Exception('method "%s" is not supported' % method)

        return func(*params)

    @expose
    def list_methods(self):
        """Function: list_methods() => [<method_name>]

        Description:
        Returns a list containing the usage of public methods
        """
        return list_public_methods(self)

    @expose
    def method_help(self, method):
        """Function: method_help(string)

        Description:
        Returns method help
        """
        func = getattr(self, method)
        return inspect.getdoc(func)

    @expose
    def image_converter(self, rgb_image):
        """image_converter(numpy.ndarray) => pickled numpy.ndarray

        Description:
        Convert RGB image matrix to grayscale image matrix.
        To use this function, argument must be a pickled numpy.ndarray
        which is read from cv2.imread function.

        Returns pickled numpy.ndarray
        """
        rgb_image_matrix = pickle.loads(rgb_image)
        print type(rgb_image_matrix)
        grayscale_matrix = cv2.cvtColor(rgb_image_matrix, cv2.COLOR_RGB2GRAY)
        grayscale_matrix = pickle.dumps(grayscale_matrix)
        return grayscale_matrix


if __name__ == "__main__":
    server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True, allow_none=True)
    server.register_introspection_functions()
    server.register_instance(RGB2GrayscaleService())

    try:
        print 'Use Control-C to exit'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Exiting'