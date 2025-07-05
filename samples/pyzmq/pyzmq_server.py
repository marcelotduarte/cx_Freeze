from __future__ import annotations

import sys
import time

import zmq  # pyzmq >= 20.0

port = int(sys.argv[1]) if len(sys.argv) > 1 else 5556

url = f"tcp://*:{port}"
reply = "Pong"

context = zmq.Context()
socket = context.socket(zmq.REP)

print(f"Server listening at {url}")
try:
    with socket.bind(url):
        while True:
            message = socket.recv_string()
            print(f"Server received: {message}")
            if message == "Close":
                reply = "Closing"
            else:
                time.sleep(1)
            print(f"Server sending: {reply}")
            socket.send_string(reply)
            if message == "Close":
                break
except KeyboardInterrupt:
    sys.exit(0)
