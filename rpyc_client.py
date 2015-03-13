import rpyc
import os
import pickle
import cv2
import sys


def main(argv):
    # Command line argument
    host, port = argv[0].split(':')
    path_to_input = argv[1]
    path_to_output = argv[2]

    # Argument checking
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

    conn = rpyc.connect(host, int(port))
    file_list = os.listdir('./input')
    for file in file_list:
        print "Processing " + file
        read_image = pickle.dumps(cv2.imread(path_to_input + file))  # Transform file into numpy matrix and pickle it
        grayscale_matrix = conn.root.image_converter(read_image)  # Call image_converter service
        grayscale_matrix = pickle.loads(grayscale_matrix)  # Unpickle grayscaled matrix
        cv2.imwrite(path_to_output + file, grayscale_matrix)  # Transform numpy matrix into file

if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) != 3:
        print "Usage: python rpyc_client.py host:port /full/path/to/input /full/path/to/output"
        print "Example: python rpyc_client.py localhost:9000 /home/test/input /home/test/output"
        sys.exit(2)

    main(argv)