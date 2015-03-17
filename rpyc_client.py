import rpyc
import os
import threading
from shutil import copyfileobj
import time


class Client:
    def __init__(self, host, port):
        self.conn = rpyc.connect(host, int(port))
        self.host = host
        self.port = port


class Main:

    def __init__(self, address_list, path_to_input, path_to_output, pack_quantity):
        self.address_list = address_list
        self.path_to_input = path_to_input
        self.path_to_output = path_to_output
        self.pack_quantity = int(pack_quantity)
        self.file_list = os.listdir(self.path_to_input)
        self.node_list = []
        self.threads = []
        self.elapsed_time = 0

    def worker(self, node, file_list):
        for filename in file_list:
            print node.host + ": Processing " + filename
            local = open(self.path_to_input + filename, 'rb')
            remote = node.conn.root.open(filename, 'wb')
            copyfileobj(local, remote)
            local.close()
            remote.close()

            node.conn.root.image_converter(filename)
            local = open(self.path_to_output + filename, 'wb')
            remote = node.conn.root.open('grayscaled_' + filename, 'rb')
            copyfileobj(remote, local)
            local.close()
            remote.close()

            node.conn.root.clean(filename)

    def run(self):
        if self.path_to_input[-1] != '/':
            self.path_to_input += '/'

        if self.path_to_output[-1] != '/':
            self.path_to_output += '/'

        # Connect to server
        for address in self.address_list:
            host, port = address.split(':')
            self.node_list.append(Client(host, port))

        i = 0
        j = self.pack_quantity
        server_selector = 0

        start_time = time.time()
        while True:
            if len(self.file_list) == 0:
                break

            if i == len(self.file_list):
                break

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
            print "Usage: [ip_addr:port]"
            print "Example: 127.0.0.1:9000"

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

    print "Elapsed time " + main.elapsed_time