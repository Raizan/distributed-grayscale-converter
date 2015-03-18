import Pyro4
import cv2
import numpy as np
import json

class RGB2GrayscaleService(object):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def image_converter(self, serialized):
        """image_converter(string, string) => string

        Description:
        Convert RGB image bytes string to grayscale image bytes string.
        To use this function, argument must be an image bytes string
        and file format in string.

        Returns a converted image bytes string.
        """
        temp = json.loads(serialized.strip())
        bytes_string = temp["READ_FILE"].decode("base64")
        file_format = temp["FILE_FORMAT"].decode("base64")
        numpy_array = np.fromstring(bytes_string, np.uint8)
        image_numpy = cv2.imdecode(numpy_array, cv2.CV_LOAD_IMAGE_COLOR)
        convert = cv2.cvtColor(image_numpy, cv2.COLOR_BGR2GRAY)

        result = cv2.imencode(file_format, convert)[1].tostring()
        serialized = json.dumps({"RESULT" : result.encode("base64")})
        return serialized

def main(host, port):
    RGBService = RGB2GrayscaleService()
    Pyro4.Daemon.serveSimple(
        {
            RGBService: "wololo.RGBService"
        },
        host = host,
        port = int(port),
        ns = True)

if __name__=="__main__":
    host = raw_input("enter your host address : ")
    port = raw_input("enter your port : ")
    main(host, port)
