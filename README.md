# FastPortScan
Threaded TCP port scanner
6 minutes 28 seconds to scan all localhost TCP ports with default settings

# Usage:
fps = FastPortScan()
fps.scan("localhost", [80,443])

or 

fps.scan("localhost", range(65536))

or slow sequential scan which returns a list of ports

openports = fps.slowscan("localhost", range(65536))
