__author__ = 'reisuke'

import xmlrpclib
import cv2
import pickle
import os
import sys
import time


def main(argv):
    # To record image processing execution time
    start_time = 0
    end_time = 0
    time_elapsed = 0

    # Command line argument
    host_address = argv[0]
    path_to_input = argv[1]
    path_to_output = argv[2]

    # Argument checking
    if host_address[0:7] is "http://" or host_address[0:8] is "https://":
        print "Invalid argument: The protocol you are going to use is unsupported by XML-RPC Protocol."
        sys.exit(1)

    if not os.path.isdir(path_to_input):
        print "Invalid argument: Input path is incorrect. Make sure it is a directory, not a file."
        sys.exit(1)

    if not os.path.isdir(path_to_output):
        print "Invalid argument: Output path is incorrect. Make sure it is a directory, not a file."
        sys.exit(1)

    if path_to_input[-1] != '/':
        path_to_input += '/'

    if path_to_output[-1] != '/':
        path_to_output += '/'

    # Contact server
    proxy = xmlrpclib.ServerProxy(host_address)

    # Read list of files inside path_to_input
    file_list = os.listdir(path_to_input)

    start_time = time.time()
    for file in file_list:
        print file
        read_image = pickle.dumps(cv2.imread(path_to_input + file))  # Transform file into numpy matrix and pickle it
        grayscale_matrix = proxy.RGB2Grayscale.image_converter(read_image)  # Call image_converter service
        grayscale_matrix = pickle.loads(grayscale_matrix)  # Unpickle grayscaled matrix
        cv2.imwrite(path_to_output + file, grayscale_matrix)  # Transform numpy matrix into file
    end_time = time.time()

    time_elapsed = end_time - start_time
    print "Time elapsed: %.5f" % time_elapsed

if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) != 3:
        print "Usage: python xmlrpc_client.py http://host:port /full/path/to/input /full/path/to/output"
        print "Example: python xmlrpc_client.py http://localhost:9000 /home/test/input /home/test/output"
        sys.exit(2)

    main(argv)