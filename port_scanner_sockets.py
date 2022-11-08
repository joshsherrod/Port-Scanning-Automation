#!/usr/bin/env python3
# The socket module in Python
import socket
# We need to create regular expressions to ensure that the input is correctly formatted.
import re
# We need to import threading, queue, and time to handle multithreading which improves run time of the program
import threading
from queue import Queue
import time

# Make a print lock to keep multiple threads from outputting at once
print_lock = threading.Lock()

# Regular Expression Pattern to recognise IPv4 addresses.
ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
# Regular Expression Pattern to extract the number of ports you want to scan.
# You have to specify <lowest_port_number>-<highest_port_number> (ex 10-100)
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
# Initialising the port numbers, will be using the variables later on.
port_min = 0
port_max = 65535


# designating the queue variable and
q = Queue()
open_ports = []
# Input from the user to designate target IP
while True:
    host = input("\nPlease enter the ip address that you want to scan: ")
    if ip_add_pattern.search(host):
        print(f"{host} is a valid ip address")
        break

# Input from the user to designate port range and verify it
while True:
    # You can scan 0-65535 ports.
    print("Please enter the range of ports you want to scan (ex 60-120): ")
    ports = input("Port range: ")
    port_range_valid = port_range_pattern.search(ports.replace(" ", ""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        break

#define the port scanner to create the socket
def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        con =s.connect((host, port))
        with print_lock:
            print(f"Port {port} is open on {host}.")
        con.close()

    except:
        pass

# Next we make the threader
def threader():
    while True:
        worker = q.get()
        scan(worker)
        q.task_done()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# now we set the start time to see total elapse time
start = time.time()

for worker in range(port_min, port_max + 1):
    q.put(worker)
q.join()

print('Entire job took:',time.time()-start)
#