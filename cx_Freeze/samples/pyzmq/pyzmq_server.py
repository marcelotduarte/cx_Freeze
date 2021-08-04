import time
import sys
import zmq
from contextlib import AbstractContextManager


class ignore(AbstractContextManager):
    def __init__(self, call):
        self.call = call

    def __enter__(self):
        if hasattr(self.call, "__enter__"):
            return self.call
        return self

    def __exit__(self, *exc_info):
        if hasattr(self.call, "__exit__"):
            return self.call.__exit__
        return None


if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 5556

url = f"tcp://*:{port}"
reply = "Pong"

context = zmq.Context()
socket = context.socket(zmq.REP)

print(f"Server listening at {url}")
try:
    with ignore(socket.bind(url)):
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
