import sys
import Pyro4
import Pyro4.util
import os
import threading
import time
import json

sys.excepthook = Pyro4.util.excepthook

class Client:
    def __init__(self, proxy_address):
        self.proxy = Pyro4.Proxy("PYRONAME:" + proxy_address)
        self.proxy_address = proxy_address


class Main(object):

    def __init__(self, proxy_list, path_to_input, path_to_output, pack_quantity):
        self.proxy_list = proxy_list
        self.path_to_input = path_to_input
        self.path_to_output = path_to_output
        self.pack_quantity = int(pack_quantity)
        self.file_list = os.listdir(self.path_to_input)
        self.node_list = []
        self.threads = []
        self.elapsed_time = 0

    def worker(self, node, file_list):
        for filename in file_list:
            print node.proxy_address + ": Processing " + filename
            file_format = filename[-4:]
            open_file = open(self.path_to_input + filename, 'rb')
            read_file = open_file.read()
            open_file.close()

            temp = {"READ_FILE":read_file.encode("base64"), "FILE_FORMAT":file_format.encode("base64")}
            serialized = json.dumps(temp)
            converted = json.loads(node.proxy.image_converter(serialized))

            deserialized = converted["RESULT"].decode("base64")

            write_file = open(self.path_to_output + filename, 'wb')
            write_file.write(deserialized)
            write_file.close()

    def run(self):
        if self.path_to_input[-1] != '/':
            self.path_to_input += '/'

        if self.path_to_output[-1] != '/':
            self.path_to_output += '/'

        # Connect to server
        for proxy in self.proxy_list:
            self.node_list.append(Client(proxy))

        i = 0
        j = self.pack_quantity
        server_selector = 0

        start_time = time.time()
        while True:
            if len(self.file_list) == 0:
                break

            if i == len(self.file_list):
                break

            if j > len(self.file_list):
                j = len(self.file_list)

            if server_selector == len(self.node_list):
                server_selector = 0

            t = threading.Thread(target=self.worker, args=(self.node_list[server_selector], self.file_list[i:j]))
            self.threads.append(t)
            t.start()
            for files in range(i, j):
                del self.file_list[0]

            server_selector += 1

        for thread in self.threads:
            thread.join()

        self.elapsed_time = time.time() - start_time

if __name__ == "__main__":
    path_to_input = None
    path_to_output = None

    print "How many servers do you want to use?"
    qty = raw_input()
    address_list = []
    for node in range(int(qty)):
        if node == 0:
            print "Usage: [nameserver.service]"
            print "Example: wololo.RGBService"

        address_list.append(raw_input())

    print "Enter input folder"
    print "Usage: /path/to/input"
    print "Example: /home/input"
    while True:
        path_to_input = raw_input()
        if not os.path.isdir(path_to_input):
            print "Invalid argument: Input path is incorrect. Make sure it is a directory, not a file."

        else:
            break

    print "Enter output folder"
    print "Usage: /path/to/output"
    print "Example: /home/output"
    while True:
        path_to_output = raw_input()
        if not os.path.isdir(path_to_output):
            print "Invalid argument: Output path is incorrect. Make sure it is a directory, not a file."

        else:
            break

    print "How many files to distribute?"
    pack_quantity = raw_input()

    main = Main(address_list, path_to_input, path_to_output, pack_quantity)
    main.run()

    print "Elapsed time " + str(main.elapsed_time)