import sys
import socket
import time
from multiprocessing import Process

class FastPortScan:
    def __init__(self, mode=None):
        self.mode = mode

    def scan(self, host, ports=65536, threads=32):
        self.dividepools(host, ports, threads)

    def dividepools(self, host, ports, threads):
        a = 1
        chunk = ports / threads
        z = chunk * 2
        for thread in range(1,threads):
            Process(target=self.scanpool, args=(host,a,z)).start()
            a = z + 1
            z = z + chunk

    def scanpool(self, host, a, z):
        openports = []
        for port in range(a,z):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            try:
               s.settimeout(0.5)
               s.connect((host, port))
               sys.stdout.write("Detected open TCP port: %i" % port)
               sys.stdout.write("\n")
               openports.append(port)
            except socket.error as er:
               s.close()
               s = None
               continue

fps = FastPortScan()
fps.scan("localhost", 65536, 32)
