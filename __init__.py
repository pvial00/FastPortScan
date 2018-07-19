import sys
import socket
import time
from multiprocessing import Process

class FastPortScan:
    def __init__(self, mode=None, timeout=0.5, threads=32):
        self.mode = mode
        self.timeout = timeout
        if threads < 1:
            self.threads = 1
        else:
            self.threads = threads

    def scan(self, host, ports=[]):
        self.dividepools(host, ports, self.threads)

    def dividepools(self, host, ports, threads):
        start = 1
        if len(ports) < threads:
            threads = len(ports)
        chunks = len(ports) / threads
        extra = len(ports) % threads
        if extra > 0:
            chunks += 1
        for thread in range(threads):
            selected_ports = []
            if len(ports) < chunks:
                chunks = len(ports)
            for c in range(chunks):
                selected_ports.append(ports.pop(0))
            Process(target=self.scanpool, args=(host,selected_ports)).start()

    def scanpool(self, host, ports):
        openports = []
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            try:
               s.settimeout(0.5)
               s.connect((host, port))
               sys.stdout.write("Detected open TCP port: %i" % port)
               sys.stdout.write("\n")
               openports.append(port)
               s.close()
            except socket.error as er:
               #sys.stdout.write("Detected closed TCP port: %i" % port)
               #sys.stdout.write("\n")
               continue
    
    def slowscan(self, host, ports):
        openports = []
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            try:
               s.settimeout(self.timeout)
               s.connect((host, port))
               #sys.stdout.write("Detected open TCP port: %i" % port)
               #sys.stdout.write("\n")
               openports.append(port)
            except socket.error as er:
               s.close()
        return openports
