import socket
import os
import threading
from queue import Queue

# Color codes
BLUE = '\033[94m'
RESET = '\033[0m'

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# Big ASCII Art Header
ascii_heading = f"""{BLUE}
  ____   ___  ____ _____     ____                  _             
 |  _ \ / _ \|  _ \_   _|   / ___|  ___ _ ____   _(_) ___ ___ ___ 
 | |_) | | | | |_) || |____| |  _  / _ \ '__\ \ / / |/ __/ __/ _ \\
 |  __/| |_| |  _ < | |____| |_| |  __/ |   \ V /| | (_| (_|  __/
 |_|    \___/|_| \_\|_|     \____|\___|_|    \_/ |_|\___\___\___|{RESET}
"""

# Info box
info_box = f"""
{BLUE}+{'-'*60}+
| Author      : S Juthansan                                      |
| Description : Multithreaded port scanner to identify open      |
|               ports and common services like HTTP, DNS, etc.   |
|                                                                |
| How to Use:                                                    |
|  - Enter the target IP address or domain                       |
|  - Enter the start and end port numbers                        |
|  - Enjoy faster scanning with threading                        |
+{'-'*60}+{RESET}
"""

print(ascii_heading)
print(info_box)

# Input target and port range
target = input("Enter the IP address or hostname to scan: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

# Resolve host
try:
    ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Error: Unable to resolve hostname.")
    exit()

print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

# Queue for thread-safe task assignment
port_queue = Queue()

# Thread worker function
def scan_port():
    while not port_queue.empty():
        port = port_queue.get()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown"
                print(f"[+] Port {port:5} is OPEN\tService: {service}")
            sock.close()
        finally:
            port_queue.task_done()

# Fill the queue
for port in range(start_port, end_port + 1):
    port_queue.put(port)

# Create and start threads
num_threads = 100
threads = []

for _ in range(num_threads):
    t = threading.Thread(target=scan_port)
    t.start()
    threads.append(t)

# Wait for all threads to finish
port_queue.join()
